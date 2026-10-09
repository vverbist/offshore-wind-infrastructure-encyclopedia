"""Self-shuttling campaigns; owner: turbine_and_foundation_installation.qmd."""
from math import ceil, floor
from model.records import Infeasible


def campaign(kind: str, count: int, set_mass_t: float, lift_mass_t: float,
             port_distance_km: float, intersite_distance_km: float, inputs) -> dict:
    p = lambda key: inputs.number(f"install-{kind}-{key}")
    if count < 1 or min(set_mass_t, lift_mass_t) <= 0 or min(port_distance_km, intersite_distance_km) < 0:
        raise ValueError("Invalid installation inventory")
    sets = min(floor(p("sets-per-load")), floor(p("usable-payload") / set_mass_t))
    if sets < 1 or lift_mass_t > p("crane-capacity"):
        raise Infeasible(f"{kind} campaign exceeds the supplied vessel payload or crane limit")
    speed = p("speed")
    if speed <= 0:
        raise ValueError("Vessel speed must be positive")
    loads = ceil(count / sets)
    travel = (2 * loads * port_distance_km + (count - 1) * intersite_distance_km) / speed
    port = count * p("port-time")
    site = count * p("site-time")
    days = p("mobilisation-time") + port + site + travel
    return {"sets_per_load": sets, "loads": loads, "travel_days": travel,
            "port_days": port, "site_days": site, "chargeable_days": days,
            "installation_eur": days * p("spread-rate")}


def reference_installation(count: int, turbine_mw: float, inputs) -> dict:
    """Fixed BVG turbine benchmark; no mass or distance adjustment. Units: MW, EUR2025."""
    reference_mw = inputs.positive("install-turbine-reference-rating", "MW")
    if count < 1 or turbine_mw != reference_mw:
        raise ValueError("Fixed installation benchmark requires the reference turbine rating and a positive count")
    source_per_mw = inputs.positive("install-turbine-reference-unit-cost", "GBP/MW")
    inflation = inputs.positive("financial-gbp-cpi-2025", "index") / inputs.positive("financial-gbp-cpi-2024", "index")
    gbp_per_eur = inputs.positive("financial-gbp-per-eur-2025", "GBP/EUR")
    source_per_turbine = source_per_mw * reference_mw
    per_turbine = source_per_turbine * inflation / gbp_per_eur
    return {"method": "reference", "reference_rating_mw": reference_mw,
            "source_gbp2024_per_mw": source_per_mw,
            "source_gbp2024_per_turbine": source_per_turbine,
            "inflation_factor": inflation, "gbp_per_eur_2025": gbp_per_eur,
            "eur2025_per_turbine": per_turbine, "installation_eur": count * per_turbine,
            "mass_adjustment": "none", "installation_feasibility": "not_assessed"}
