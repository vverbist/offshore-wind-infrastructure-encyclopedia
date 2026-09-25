"""Central AC-to-DC package; owner: elx_power_electronics.qmd."""
from model.inputs import Inputs


def efficiency(inputs: Inputs) -> float:
    return inputs.fraction("central-conversion-efficiency")


def supply_cost(rating_kw: float, inputs: Inputs) -> float:
    return rating_kw * inputs.number("central-conversion-unit-cost", "EUR/kW")
