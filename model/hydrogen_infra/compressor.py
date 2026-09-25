"""Existing multistage compression method; owner: hydrogen_infra/compressor.qmd."""
from dataclasses import dataclass
from math import ceil, log
from CoolProp.CoolProp import PropsSI
from model.inputs import Inputs
from model.methodology.financial_and_price_basis import normalize_usd


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


def cost_coefficient_eur2025(inputs: Inputs) -> float:
    """Uninstalled cost [EUR2025] of the sourced power law at 1 kW motor input.

    The brief's 2019 CAD value is returned to 2019 USD at the brief's own exchange
    rate, escalated with the compressor producer price index and converted at the
    common 2025 USD/EUR rate. The brief's installation factor is excluded.
    """
    usd_2019 = (inputs.positive("compressor-source-cost-coefficient", "CAD")
                * inputs.positive("compressor-source-usd-per-cad-2019", "USD/CAD"))
    return normalize_usd(usd_2019, inputs.positive("compressor-usd-escalation-2019-2025", "factor"), inputs)


def reference_purchase_cost(inputs: Inputs) -> float:
    """EUR2025 purchase cost at the reference motor input; unrounded by construction."""
    return (cost_coefficient_eur2025(inputs)
            * inputs.positive("compressor-reference-motor-power", "kW") ** inputs.positive("compressor-cost-exponent", "factor"))


def supply_cost(packages: list[Compressor], inputs: Inputs) -> float:
    if not any(p.trains for p in packages):
        return 0.0  # Explicit no-compression duty.
    reference = inputs.positive("compressor-reference-motor-power", "kW")
    cost = reference_purchase_cost(inputs)
    exponent = inputs.positive("compressor-cost-exponent", "factor")
    return sum(p.trains * cost * (p.motor_kw_per_train / reference) ** exponent for p in packages)


def reference_cost_curve(inlet_bar: float, outlet_bar: float, inputs: Inputs) -> float:
    """Legacy figure anchor only; its unresolved price basis excludes it from case CAPEX."""
    reference = specific_energy(inputs.number("compressor-reference-inlet-pressure", "bar"),
                                inputs.number("compressor-reference-outlet-pressure", "bar"), inputs)
    # Deliberate reference-only display; never call this from the cost ledger.
    anchor = inputs.reference_number("compressor-legacy-cost-anchor", "EUR/kW")
    return anchor * (specific_energy(inlet_bar, outlet_bar, inputs) / reference) ** inputs.number("compressor-cost-exponent")
