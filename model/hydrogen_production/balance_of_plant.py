"""Aggregate BOP scaling; owner: hydrogen_production/balance_of_plant.qmd."""
from dataclasses import dataclass
from math import ceil
from model.inputs import Inputs
from model.methodology.financial_and_price_basis import normalize_usd


@dataclass
class BOP:
    blocks: int
    block_rating_kw: float
    reference_cost_multiplier: float


def size(served_power_kw: float, locations: int, inputs: Inputs) -> BOP:
    """Equal duty blocks at each location; stack overplanting is deliberately absent."""
    if served_power_kw <= 0 or locations < 1:
        raise ValueError("BOP needs positive power and at least one location")
    cap = inputs.positive("bop-block-limit", "kW")
    reference = inputs.positive("bop-reference-rating", "kW")
    exponent = inputs.positive("bop-scaling-exponent", "factor")
    blocks = locations * ceil(served_power_kw / locations / cap)
    rating = served_power_kw / blocks
    return BOP(blocks, rating, blocks * (rating / reference) ** exponent)


def supply_cost(bop: BOP, inputs: Inputs) -> float:
    # Water remains within the aggregate package, without inventing its missing cost.
    subtotal = sum(inputs.number(f"bop-{part}-manufactured-unit-cost", "USD/kW")
                   for part in ("thermal", "processing", "hydrogen-side", "piping-housing"))
    manufactured = subtotal * inputs.number("bop-reference-rating", "kW")
    nonwater = normalize_usd(manufactured * inputs.number("hydrogen-manufactured-cost-markup", "factor"),
                            inputs.positive("financial-usd-escalation-2020-2025", "factor"), inputs)
    water = inputs.number("bop-water-reference-purchase-cost", "EUR")
    return bop.reference_cost_multiplier * (nonwater + water)
