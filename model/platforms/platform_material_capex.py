"""One central platform: complete topside mass to structure and supply CAPEX.

Units: mass t, depth m, power GW and costs EUR2025. Equipment purchase is
booked by component owners. Missing costs remain None, never zero.
"""
from math import isfinite

from model.records import MissingInput, required


def estimate_topside_mass(rated_power_gw: float, inputs) -> float:
    """Optional upstream aggregate scaling; reference mass must cover all equipment."""
    if not isfinite(rated_power_gw) or rated_power_gw <= 0:
        raise ValueError("Platform rated power must be finite and positive")
    return (inputs.positive("platform-reference-topside-mass", "t")
            * (rated_power_gw / inputs.positive("platform-reference-power", "GW"))
            ** inputs.positive("platform-mass-scaling-exponent", "exponent"))


def inventory(case: dict, water_depth_m: float, inputs) -> dict:
    """Complete topside mass is the boundary input; lift design is independent."""
    if case.get("count", 1) != 1:
        raise ValueError("The central-platform model requires exactly one platform")
    topside_t = float(required(case, "topside_mass_t"))
    if not all(isfinite(v) and v > 0 for v in (topside_t, water_depth_m)):
        raise ValueError("Complete topside mass and water depth must be finite and positive")
    structure_t = inputs.fraction("platform-topside-structural-fraction") * topside_t
    jacket_t = (inputs.positive("platform-jacket-depth-coefficient", "t^(1-b)/m")
                * water_depth_m * topside_t ** inputs.positive("platform-jacket-mass-exponent", "exponent"))
    piles_t = (inputs.positive("platform-pile-load-coefficient", "t/t") * (topside_t + jacket_t)
               + inputs.positive("platform-pile-mass-intercept", "t"))
    return {"platform_count": 1, "topside_t": topside_t,
            "water_depth_m": water_depth_m, "topside_structure_t": structure_t,
            "equipment_t": topside_t - structure_t, "jacket_t": jacket_t, "piles_t": piles_t}


def supply_cost(platform: dict, inputs) -> dict:
    """Preserve known subtotals when a fabrication rate or integration quote is absent."""
    result = {}
    missing = []
    for name, mass, parameter, unit in (
        ("topside_structure_eur", platform["topside_structure_t"], "platform-topside-structure-unit-cost", "EUR/t"),
        ("jacket_eur", platform["jacket_t"], "platform-jacket-unit-cost", "EUR/t"),
        ("piles_eur", platform["piles_t"], "platform-pile-unit-cost", "EUR/t"),
        ("yard_integration_eur", 1, "platform-yard-integration-cost", "EUR"),
    ):
        try:
            rate = inputs.number(parameter, unit)
            if rate < 0:
                raise ValueError(f"{parameter} must be nonnegative")
            result[name] = mass * rate
        except MissingInput as exc:
            result[name] = None
            missing.append(str(exc))
    structural = [result[name] for name in ("topside_structure_eur", "jacket_eur", "piles_eur")]
    result["structure_eur"] = None if any(v is None for v in structural) else sum(structural)
    components = [result[name] for name in ("topside_structure_eur", "jacket_eur", "piles_eur", "yard_integration_eur")]
    result["known_subtotal_eur"] = sum(v for v in components if v is not None)
    result["total_eur"] = None if missing else sum(components)
    result["missing_inputs"] = missing
    return result


def specific_cost_eur_per_kw(total_eur: float, rated_power_kw: float) -> float:
    """Reporting metric, not a capacity-based cost input."""
    if rated_power_kw <= 0:
        raise ValueError("Rated power must be positive")
    return total_eur / rated_power_kw
