"""Probability-weighted operating states; owner: wind_resource_and_weibull.qmd."""
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd


@dataclass
class WindStates:
    state_ids: list[str]
    hours: np.ndarray
    turbine_ids: list[str]
    power_kw: np.ndarray

    @classmethod
    def read(cls, path: Path, turbine_ids: list[str], annual_hours: float):
        """Wide CSV: state,hours,<one generator-output kW column per turbine>."""
        data = pd.read_csv(path, dtype={"state": str})
        hours = data["hours"].to_numpy(float)
        power = data[turbine_ids].to_numpy(float)
        if (data["state"].duplicated().any() or len(data) == 0
                or not np.isfinite(hours).all() or not np.isfinite(power).all()
                or (hours < 0).any() or (power < 0).any()
                or not np.isclose(hours.sum(), annual_hours)):
            raise ValueError("Wind states need unique IDs, non-negative finite values and a complete year")
        return cls(data["state"].tolist(), hours, turbine_ids, power)


def weibull_weights(sectors: pd.DataFrame, speed_edges: np.ndarray) -> np.ndarray:
    """Preserve bin probabilities; tails are not silently renormalised."""
    probability = sectors["freq"].to_numpy(float)
    shape = sectors["k"].to_numpy(float)
    scale = sectors["c"].to_numpy(float)
    if (not np.isfinite(probability).all() or not np.isfinite(shape).all()
            or not np.isfinite(scale).all() or np.any(probability < 0)
            or np.any(shape <= 0) or np.any(scale <= 0)
            or not np.isclose(probability.sum(), 1)
            or speed_edges[0] != 0 or not np.isposinf(speed_edges[-1])
            or np.any(np.diff(speed_edges) <= 0)):
        raise ValueError("Weibull input must cover [0, infinity) with valid sector probabilities")
    cdf = 1 - np.exp(-(speed_edges[None, :] / scale[:, None]) ** shape[:, None])
    return probability[:, None] * np.diff(cdf, axis=1)
