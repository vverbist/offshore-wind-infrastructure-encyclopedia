"""Preserved average-property/Fanning pipeline method; no qualification claim."""
from math import log10, pi, sqrt, ceil
from CoolProp.CoolProp import PropsSI
from model.inputs import Inputs


def capacity_kg_h(diameter_m: float, inlet_bar: float, outlet_bar: float,
                  length_m: float, inputs: Inputs) -> float:
    if min(diameter_m, inlet_bar, outlet_bar, length_m) <= 0 or inlet_bar <= outlet_bar:
        raise ValueError("Pipeline requires positive dimensions and absolute inlet > outlet pressure")
    pin, pout = inlet_bar * 1e5, outlet_bar * 1e5
    temperature = inputs.positive("pipeline-temperature", "K")
    roughness = inputs.number("pipeline-roughness", "m")
    if roughness < 0:
        raise ValueError("Pipeline roughness must not be negative")
    average = (2 / 3) * (pin**3 - pout**3) / (pin**2 - pout**2)
    rho = PropsSI("D", "T", temperature, "P", average, "Hydrogen")
    mu = PropsSI("V", "T", temperature, "P", average, "Hydrogen")
    re_sqrt_f = diameter_m**1.5 / mu * sqrt((pin - pout) * rho / (2 * length_m))
    inverse = -4 * log10(roughness / (inputs.positive("pipeline-colebrook-roughness-divisor") * diameter_m)
                         + inputs.positive("pipeline-colebrook-reynolds-coefficient") / re_sqrt_f)
    if inverse <= 0:
        raise ValueError("Pipeline state is outside the friction relation's usable domain")
    velocity = sqrt(diameter_m * (pin - pout) / (2 * rho * length_m)) * inverse
    return rho * pi * diameter_m**2 / 4 * velocity * 3600


def export_count(peak_kg_h: float, capacity: float) -> int:
    if peak_kg_h < 0 or capacity <= 0:
        raise ValueError("Invalid pipeline flow or capacity")
    return ceil(peak_kg_h / capacity)


def supply_cost(length_km: float, unit_cost_eur_m: float) -> float:
    if length_km < 0 or unit_cost_eur_m < 0:
        raise ValueError("Pipeline length and rate must be non-negative")
    return length_km * 1000 * unit_cost_eur_m
