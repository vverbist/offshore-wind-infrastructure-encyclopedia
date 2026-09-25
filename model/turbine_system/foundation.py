"""Mass/depth monopile screening law; owner: turbine_system/foundation.qmd."""
from model.methodology.financial_and_price_basis import normalize_usd


def calculate(supported_mass_t: float, depth_m: float, inputs) -> dict:
    if min(supported_mass_t, depth_m) <= 0:
        raise ValueError("Foundation needs positive supported mass and depth")
    mass = (inputs.positive("foundation-reference-monopile-mass", "t")
            * supported_mass_t / (inputs.positive("foundation-reference-rna-mass", "t")
                                  + inputs.positive("foundation-reference-tower-mass", "t"))
            * depth_m / inputs.positive("foundation-reference-depth", "m"))
    usd = mass * inputs.number("foundation-fabrication-unit-cost", "USD/t") * (1 + inputs.number("foundation-transition-piece-cost-ratio", "fraction"))
    return {"monopile_t": mass, "supply_usd2022": usd}


def supply_eur(result: dict, count: int, inputs) -> float:
    return count * normalize_usd(result["supply_usd2022"], inputs.positive("financial-usd-escalation-2022-2025", "factor"), inputs)
