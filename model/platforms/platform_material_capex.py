"""One central platform: hosted equipment mass to commercial EPCI CAPEX.

Units: mass t, depth m, power GW and costs EUR2025. Equipment purchase is
booked by component owners. DNV inventory/supply helpers are legacy comparisons;
epci_inventory and epci_cost own the adopted aggregate calculation.
"""
from math import isfinite

from model.records import MissingInput, required


def epci_inventory(case: dict, inputs, water_depth_m: float | None = None) -> dict:
    """Accept exactly one direct mass; depth is metadata, not a cost dependency."""
    if case.get("count", 1) != 1:
        raise ValueError("The central-platform model requires exactly one platform")
    fields = [key for key in ("equipment_mass_t", "topside_mass_t") if key in case]
    if not fields:
        raise MissingInput("Platform equipment_mass_t or complete topside_mass_t is required")
    if len(fields) != 1:
        raise ValueError("Supply equipment mass or complete topside mass, not both")
    mass = float(case[fields[0]])
    if not isfinite(mass) or mass <= 0:
        raise ValueError("Platform mass must be finite and positive in tonnes")
    if water_depth_m is not None and (not isfinite(water_depth_m) or water_depth_m <= 0):
        raise ValueError("Provided platform depth must be finite and positive")
    fraction = inputs.fraction("platform-topside-structural-fraction")
    if fraction >= 1:
        raise ValueError("Topside structural fraction must be less than one")
    direct_equipment = fields[0] == "equipment_mass_t"
    equipment = mass if direct_equipment else (1 - fraction) * mass
    top = mass / (1 - fraction) if direct_equipment else mass
    return {"platform_count": 1, "equipment_t": equipment, "topside_t": top,
            "topside_structure_t": top - equipment, "water_depth_m": water_depth_m,
            "mass_basis": "direct_equipment" if direct_equipment else "inferred_from_topside",
            "installation_feasibility": "not_assessed"}


def epci_cost(platform: dict, inputs) -> dict:
    """Delivered offshore package, excluding hosted equipment purchase and OPEX.

    Reference mass is the Alpha topside converted using the same DNV assumption.
    Changing beta preserves cost at this reference. No jacket, fabrication or
    installation cost is added; water depth has no unsupported cost multiplier.
    """
    equipment = platform["equipment_t"]
    if platform["platform_count"] != 1 or not isfinite(equipment) or equipment <= 0:
        raise ValueError("EPCI requires one platform with positive finite equipment mass")
    coefficient = benchmark_cost_eur2025(
        inputs.positive("platform-epci-unit-cost-source", "EUR/t"), 1,
        inputs.parameters.get("platform-epci-unit-cost-source").price_year, inputs)
    reference_mass = ((1 - inputs.fraction("platform-topside-structural-fraction"))
                      * inputs.reference_number("platform-mhb-topside", "t"))
    if reference_mass <= 0:
        raise ValueError("Reference equipment mass must be positive")
    exponent = inputs.positive("platform-epci-cost-scaling-exponent", "exponent")
    reference_cost = coefficient * reference_mass
    total = reference_cost * (equipment / reference_mass) ** exponent
    if not isfinite(total):
        raise ValueError("Platform EPCI cost must be finite")
    return {"total_eur": total, "equipment_t": equipment,
            "reference_equipment_t": reference_mass, "reference_cost_eur": reference_cost,
            "coefficient_eur_per_t": coefficient, "cost_scaling_exponent": exponent,
            "price_basis": "EUR2025", "scope": "offshore_epci_excluding_hosted_equipment",
            "calibration": "commercial_screening_judgement_not_fitted"}


def benchmark_cost_eur2025(cost, currency_per_eur, source_year, inputs):
    """Platform price normalisation: source-year FX, then euro-area annual HICP.

    Consumer inflation is an explicit proxy, not an offshore construction index.
    The year is the assumed price basis of the award/estimate, not delivery year.
    """
    if cost <= 0 or currency_per_eur <= 0 or not 2019 <= source_year <= 2025:
        raise ValueError("Benchmark needs positive cost/FX and a price year from 2019 to 2025")
    result = cost / currency_per_eur
    for year in range(source_year + 1, 2026):
        result *= 1 + inputs.number(f"platform-benchmark-hicp-{year}", "fraction")
    return result


def commercial_benchmarks(inputs):
    """Six reference observations, never an adopted cost or workflow ledger item.

    Returned masses are tonnes, capacity GW, costs EUR2025. HKZ is one combined
    award displayed as a per-platform average. Framework and fabrication points
    overlap project scopes and must not be treated as independent EPCI samples.
    """
    ref = inputs.reference_number
    offshore = inputs.fraction("platform-benchmark-offshore-share")
    fraction = inputs.fraction("platform-topside-structural-fraction")
    if fraction >= 1:
        raise ValueError("Equipment mass must be positive for cost normalisation")
    hkz_count = ref("platform-hkz-count", "count")
    records = [
        ("hkz", "HKZ Alpha + Beta (average)",
         (ref("platform-hkz-alpha-topside", "t") + ref("platform-hkz-beta-topside", "t")) / hkz_count,
         ref("platform-hkz-power", "GW"), ref("platform-hkz-contract", "USD") / hkz_count,
         inputs.number("platform-benchmark-usd-eur-2019", "USD/EUR"), 2019, "award"),
        ("nederwiek", "Nederwiek 1 (offshore allocation)", ref("platform-nederwiek-topside", "t"),
         ref("platform-mhb-power", "GW"), ref("platform-nederwiek-petrofac", "USD") * offshore,
         inputs.number("platform-benchmark-usd-eur-2023", "USD/EUR"), 2023, "allocated"),
        ("framework", "Petrofac framework (allocated average)", ref("platform-mhb-topside", "t"),
         ref("platform-mhb-power", "GW"), ref("platform-petrofac-framework", "EUR")
         / ref("platform-petrofac-systems", "count")
         * inputs.fraction("platform-benchmark-petrofac-share") * offshore, 1, 2023, "framework"),
        ("nse", "North Sea Energy / Iv concept", ref("platform-nse-topside", "t"),
         ref("platform-nse-power", "GW"), ref("platform-nse-structure-cost", "EUR"), 1, 2022, "study"),
        ("offsh2ore", "OffsH2ore concept", ref("platform-offsh2ore-topside", "t"),
         ref("platform-offsh2ore-power", "GW"), ref("platform-offsh2ore-cost", "EUR"), 1, 2023, "study"),
        ("mhb", "MHB Alpha fabrication subcontract", ref("platform-mhb-topside", "t"),
         ref("platform-mhb-power", "GW"), ref("platform-mhb-contract", "MYR"),
         inputs.number("platform-benchmark-myr-eur-2023", "MYR/EUR"), 2023, "fabrication"),
    ]
    results = []
    for key, name, top, power, cost, fx, year, kind in records:
        equipment = (1 - fraction) * top
        normalised = benchmark_cost_eur2025(cost, fx, year, inputs)
        results.append(dict(key=key, name=name, topside_t=top, equipment_t=equipment,
                            power_gw=power, cost_eur2025=normalised, source_year=year,
                            equipment_t_per_kw=equipment / (power * 1e6),
                            eur_per_equipment_t=normalised / equipment,
                            eur_per_topside_t=normalised / top,
                            eur_per_kw=normalised / (power * 1e6), kind=kind))
    return results


def estimate_topside_mass(rated_power_gw: float, inputs) -> float:
    """Optional upstream aggregate scaling; reference mass must cover all equipment."""
    if not isfinite(rated_power_gw) or rated_power_gw <= 0:
        raise ValueError("Platform rated power must be finite and positive")
    return (inputs.positive("platform-reference-topside-mass", "t")
            * (rated_power_gw / inputs.positive("platform-reference-power", "GW"))
            ** inputs.positive("platform-mass-scaling-exponent", "exponent"))


def inventory(case: dict, water_depth_m: float, inputs) -> dict:
    """Legacy DNV inventory for comparisons only; not used to price active EPCI."""
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
    """Legacy additive comparison only; never combine with the active EPCI cost."""
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
