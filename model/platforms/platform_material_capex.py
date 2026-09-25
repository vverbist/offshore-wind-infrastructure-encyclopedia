"""Central-platform mass chain and material CAPEX; owner: platforms/platform_material_capex.qmd.

Units: masses in t, costs in EUR2025 unless the key names another basis, power in kW.
"""
from model.methodology.financial_and_price_basis import normalize_usd
from model.records import required


def inventory(case: dict, inputs) -> dict:
    """Per-platform masses (steps 1-3 on the page) and the installation handoff."""
    count = int(required(case, "count"))
    modules = int(required(case, "topside_modules_per_platform"))
    if min(count, modules) < 1:
        raise ValueError("A central platform requires positive platform and lift counts")
    equipment = {name: float(mass) for name, mass in required(case, "hosted_equipment_mass_t").items()}
    if not equipment or min(equipment.values()) <= 0:
        raise ValueError("Hosted equipment masses must be listed and positive")

    equipment_t = sum(equipment.values())
    structure_t = inputs.number("platform-structural-mass-ratio", "t/t") * equipment_t
    topside_t = equipment_t + structure_t
    jacket_t = inputs.positive("platform-jacket-topside-mass-ratio", "t/t") * topside_t
    piles_t = (inputs.positive("platform-pile-mass-coefficient", "coefficient")
               * jacket_t ** inputs.positive("platform-pile-mass-exponent", "coefficient"))
    return {"platform_count": count, "topside_lifts": count * modules,
            "hosted_equipment_t": equipment, "equipment_t": equipment_t,
            "topside_structure_t": structure_t, "topside_t": topside_t,
            "jacket_t": jacket_t, "piles_t": piles_t,
            # Installation-page interface; equal module split is a stated assumption.
            "jacket_lift_t": jacket_t, "largest_topside_lift_t": topside_t / modules}


def supply_cost(platform: dict, inputs) -> dict:
    """Material and fabrication CAPEX (step 4). Equipment CAPEX is booked by its component owners."""
    per_platform = {
        "topside_structure_eur": platform["topside_structure_t"] * inputs.number("platform-topside-structure-unit-cost", "EUR/t"),
        "yard_integration_eur": platform["equipment_t"] * inputs.number("platform-yard-integration-unit-cost", "EUR/t"),
        "jacket_eur": platform["jacket_t"] * inputs.number("platform-jacket-unit-cost", "EUR/t"),
        # Piles reuse the fabricated tubular-steel rate of the monopile page, without its transition-piece allowance.
        "piles_eur": normalize_usd(platform["piles_t"] * inputs.number("foundation-fabrication-unit-cost", "USD/t"),
                                   inputs.positive("financial-usd-escalation-2022-2025", "factor"), inputs),
    }
    count = platform["platform_count"]
    result = {key: count * value for key, value in per_platform.items()}
    result["total_eur"] = sum(result.values())
    return result


def specific_cost_eur_per_kw(total_eur: float, rated_power_kw: float) -> float:
    """Averaged platform cost per kW of the rated power it serves (reporting metric only)."""
    if rated_power_kw <= 0:
        raise ValueError("Rated power must be positive")
    return total_eur / rated_power_kw
