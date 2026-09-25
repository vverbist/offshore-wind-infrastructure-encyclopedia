"""Radial strings, physical lengths and I-squared-R losses; owner: infield_ac_cables.qmd."""
from math import floor
import numpy as np
import pandas as pd
from model.records import Infeasible


def radial_routes(coordinates: pd.DataFrame, turbine_kw: float, sink_xy: tuple,
                  depth_m: float, inputs) -> pd.DataFrame:
    per_string = floor(inputs.positive("array-usable-string-rating", "MW") * 1000 / turbine_kw)
    if per_string < 1:
        raise Infeasible("One turbine exceeds the adopted cable string capacity")
    allowance = inputs.number("array-route-allowance", "fraction")
    if depth_m < 0 or allowance < 0:
        raise ValueError("Depth and route allowance must be non-negative")
    records = []
    # Coordinate-file order declares the string assignment; no route optimisation.
    for start in range(0, len(coordinates), per_string):
        group = coordinates.iloc[start:start + per_string]
        previous = sink_xy
        for offset, row in enumerate(group.itertuples()):
            horizontal = np.hypot(row.x_m - previous[0], row.y_m - previous[1]) / 1000
            records.append({"section": f"ac-{start}-{offset}", "horizontal_km": horizontal,
                            "physical_km": horizontal * (1 + allowance) + 2 * depth_m / 1000,
                            "upstream": group.turbine.iloc[offset:].tolist()})
            previous = row.x_m, row.y_m
    return pd.DataFrame(records)


def loss_kw(routes: pd.DataFrame, power_kw: np.ndarray, turbine_ids: list[str], inputs) -> np.ndarray:
    resistance = inputs.number("array-ac-resistance", "ohm/km")
    voltage = inputs.positive("array-voltage", "kV") * 1000
    pf = inputs.fraction("array-power-factor")
    if pf == 0 or resistance < 0:
        raise ValueError("Cable power factor must be positive and resistance non-negative")
    loss = np.zeros(power_kw.shape[0])
    for section in routes.itertuples():
        indices = [turbine_ids.index(t) for t in section.upstream]
        flow = power_kw[:, indices].sum(axis=1)
        current = flow * 1000 / (np.sqrt(3) * voltage * pf)
        loss += 3 * current**2 * resistance * section.physical_km / 1000
    if np.any(loss > power_kw.sum(axis=1)):
        raise Infeasible("Calculated AC collection losses exceed generated power")
    return loss


def supply_cost(routes: pd.DataFrame, inputs) -> float:
    return routes.physical_km.sum() * 1000 * inputs.number("array-supply-unit-cost", "EUR/m")
