"""PEM polarisation and modular operation; owner: hydrogen_production/stack.qmd.

The workbook is used as supplied. Current density is not treated as power:
normalised module power is j*V(j)/(j_ref*V_ref). Switching penalties and
chronological degradation are deferred; returned operation is beginning-of-life.
"""
from dataclasses import dataclass
from math import ceil
from pathlib import Path

import numpy as np
import pandas as pd

from model.inputs import Inputs


@dataclass
class StackCurve:
    current_density: np.ndarray
    voltage: np.ndarray

    @classmethod
    def read(cls, path: Path, sheet_name=0):
        data = pd.read_excel(path, sheet_name=sheet_name) if path.suffix == ".xlsx" else pd.read_csv(path)
        curve = cls(data["current_density_A_cm2"].to_numpy(float), data["cell_voltage_V"].to_numpy(float))
        if (len(curve.voltage) < 2 or not np.isfinite(curve.current_density).all()
                or not np.isfinite(curve.voltage).all()
                or np.any(curve.current_density <= 0) or np.any(curve.voltage <= 0)
                or np.any(np.diff(curve.current_density) <= 0)
                or np.any(np.diff(curve.current_density * curve.voltage) <= 0)):
            raise ValueError("Stack curve needs positive, increasing current and power points")
        return curve

    def voltage_at(self, current_density: float) -> float:
        if not self.current_density[0] <= current_density <= self.current_density[-1]:
            raise ValueError("Stack current density lies outside the supplied curve")
        return float(np.interp(current_density, self.current_density, self.voltage))

    def efficiency(self, inputs: Inputs) -> np.ndarray:
        return inputs.positive("stack-hhv-voltage", "V") / self.voltage


@dataclass
class StackOperation:
    installed_modules: int
    active_modules: int
    installed_kw: float
    stack_kw: float
    hydrogen_kg_h: float
    bop_kw: float
    compressor_kw: float
    curtailed_kw: float
    current_density_a_cm2: float


def operate(available_kw: float, requested_stack_kw: float, curve: StackCurve,
            compression_kwh_kg: float, inputs: Inputs) -> StackOperation:
    """Maximise production over integer active-module counts with a closed bus balance."""
    if available_kw < 0 or requested_stack_kw <= 0 or compression_kwh_kg < 0:
        raise ValueError("Invalid stack duty")
    module_kw = inputs.positive("stack-module-rating", "kW")
    j_ref = inputs.positive("stack-reference-current-density", "A/cm2")
    v_ref = curve.voltage_at(j_ref)
    minimum = inputs.fraction("stack-min-load") * j_ref * v_ref
    if minimum < curve.current_density[0] * curve.voltage[0]:
        raise ValueError("Minimum module load falls below the supplied polarisation curve")
    lo, hi = float(curve.current_density[0]), j_ref
    for _ in range(60):
        mid = (lo + hi) / 2
        if mid * curve.voltage_at(mid) < minimum:
            lo = mid
        else:
            hi = mid
    j_min = hi
    hhv_voltage = inputs.positive("stack-hhv-voltage", "V")
    hhv = inputs.positive("hydrogen-hhv", "kWh/kg")
    bop = inputs.number("bop-specific-electricity", "kWh/kg")
    if bop < 0:
        raise ValueError("BOP electricity must be non-negative")
    modules = ceil(requested_stack_kw / module_kw)
    best = StackOperation(modules, 0, modules * module_kw, 0, 0, 0, 0, available_kw, 0)
    # The highest permissible current is the reference rating, not the workbook maximum.
    for active in range(1, modules + 1):
        scale = active * module_kw / (j_ref * v_ref)

        def duty(j):
            power = scale * j * curve.voltage_at(j)
            mass = scale * j * hhv_voltage / hhv
            return power + mass * (bop + compression_kwh_kg), power, mass

        if duty(j_min)[0] > available_kw:
            break
        if duty(j_ref)[0] <= available_kw:
            j = j_ref
        else:
            lo, hi = j_min, j_ref
            # Numerical precision only; no physical assumption is embedded here.
            for _ in range(60):
                mid = (lo + hi) / 2
                if duty(mid)[0] > available_kw:
                    hi = mid
                else:
                    lo = mid
            j = lo
        bus, power, mass = duty(j)
        if mass > best.hydrogen_kg_h:
            best = StackOperation(modules, active, modules * module_kw, power, mass,
                                  mass * bop, mass * compression_kwh_kg,
                                  max(0, available_kw - bus), j)
    return best
