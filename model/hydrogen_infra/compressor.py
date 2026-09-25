"""Existing multistage compression method; owner: hydrogen_infra/compressor.qmd."""
from dataclasses import dataclass
from math import ceil, log
from CoolProp.CoolProp import PropsSI
from model.inputs import Inputs


def stages(inlet_bar: float, outlet_bar: float, inputs: Inputs) -> int:
    if inlet_bar <= 0 or outlet_bar < inlet_bar:
        raise ValueError("Absolute compressor pressures require outlet >= inlet > zero")
    if inlet_bar == outlet_bar:
        return 0
    ratio = inputs.positive("compressor-max-stage-ratio", "factor")
    if ratio <= 1:
        raise ValueError("Maximum stage ratio must exceed one")
    return ceil(log(outlet_bar / inlet_bar) / log(ratio))


def specific_energy(inlet_bar: float, outlet_bar: float, inputs: Inputs) -> float:
    n = stages(inlet_bar, outlet_bar, inputs)
    if n == 0:
        return 0.0
    temperature = inputs.positive("compressor-temperature", "K")
    gamma = inputs.positive("hydrogen-heat-capacity-ratio", "factor")
    if gamma <= 1:
        raise ValueError("Heat-capacity ratio must exceed one")
    eta = inputs.fraction("compressor-efficiency") * inputs.fraction("compressor-motor-efficiency")
    if eta == 0:
        raise ValueError("Compressor and motor efficiencies must be positive")
    z = PropsSI("Z", "T", temperature, "P", (inlet_bar + outlet_bar) / 2 * 1e5, "Hydrogen")
    gas_constant = inputs.positive("universal-gas-constant", "J/mol/K")
    molar_mass = inputs.positive("hydrogen-molar-mass", "kg/mol")
    ratio = (outlet_bar / inlet_bar) ** (1 / n)
    return (n * gamma * z * gas_constant * temperature / ((gamma - 1) * molar_mass * eta)
            * (ratio ** ((gamma - 1) / gamma) - 1) / 3.6e6)


@dataclass
class Compressor:
    trains: int
    motor_kw_per_train: float
    total_motor_kw: float


def size(peak_power_per_location_kw: list[float], inputs: Inputs) -> list[Compressor]:
    limit = inputs.positive("compressor-train-limit", "kW")
    result = []
    for peak in peak_power_per_location_kw:
        if peak < 0:
            raise ValueError("Compressor peak duty must not be negative")
        n = ceil(peak / limit)
        result.append(Compressor(n, peak / n if n else 0, peak))
    return result


def supply_cost(packages: list[Compressor], inputs: Inputs) -> float:
    if not any(p.trains for p in packages):
        return 0.0  # Explicit no-compression duty.
    reference = inputs.positive("compressor-reference-motor-power", "kW")
    cost = inputs.number("compressor-reference-purchase-cost", "EUR")
    exponent = inputs.positive("compressor-cost-exponent", "factor")
    return sum(p.trains * cost * (p.motor_kw_per_train / reference) ** exponent for p in packages)


def reference_cost_curve(inlet_bar: float, outlet_bar: float, inputs: Inputs) -> float:
    """Legacy figure anchor only; its unresolved price basis excludes it from case CAPEX."""
    reference = specific_energy(inputs.number("compressor-reference-inlet-pressure", "bar"),
                                inputs.number("compressor-reference-outlet-pressure", "bar"), inputs)
    # Deliberate reference-only display; never call this from the cost ledger.
    anchor = inputs.reference_number("compressor-legacy-cost-anchor", "EUR/kW")
    return anchor * (specific_energy(inlet_bar, outlet_bar, inputs) / reference) ** inputs.number("compressor-cost-exponent")
