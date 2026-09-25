"""Explicit turbine-level interface cases; detailed electrical matching is deferred."""
from model.inputs import Inputs


def efficiency(interface: str, inputs: Inputs) -> float:
    if interface not in {"conservative", "converter_reduced"}:
        raise ValueError("Interface must be conservative or converter_reduced")
    return inputs.fraction(f"{interface.replace('_', '-')}-conversion-efficiency")


def supply_cost(interface: str, rating_kw: float, inputs: Inputs) -> float:
    return rating_kw * inputs.number(f"{interface.replace('_', '-')}-conversion-unit-cost", "EUR/kW")
