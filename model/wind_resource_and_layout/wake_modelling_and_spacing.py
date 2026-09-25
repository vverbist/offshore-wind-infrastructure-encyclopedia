"""Coordinate layouts and a version-recorded optional PyWake calculation."""
from importlib.metadata import version
from math import ceil
from pathlib import Path
import numpy as np
import pandas as pd
from model.records import MissingInput, Infeasible, required
from .wind_resource_and_weibull import WindStates


def layout(case: dict, base: Path) -> pd.DataFrame:
    if "coordinates_file" in case:
        frame = pd.read_csv(base / case["coordinates_file"], dtype={"turbine": str})
        frame = frame[["turbine", "x_m", "y_m"]]
    else:
        n, columns = int(required(case, "turbine_count")), int(required(case, "columns"))
        dx, dy = float(required(case, "spacing_x_m")), float(required(case, "spacing_y_m"))
        if n <= 0 or columns <= 0 or min(dx, dy) <= 0:
            raise ValueError("Layout counts and spacings must be positive")
        points = []
        for row in range(ceil(n / columns)):
            count = min(columns, n - row * columns)
            for column in range(count):
                points.append((str(len(points) + 1), (column - (count - 1) / 2) * dx, row * dy))
        frame = pd.DataFrame(points, columns=["turbine", "x_m", "y_m"])
        angle = np.deg2rad(float(required(case, "orientation_deg")))
        x, y = frame.x_m.copy(), frame.y_m.copy()
        frame["x_m"], frame["y_m"] = x * np.cos(angle) - y * np.sin(angle), x * np.sin(angle) + y * np.cos(angle)
    if frame.empty or frame.turbine.duplicated().any() or not np.isfinite(frame[["x_m", "y_m"]]).all().all():
        raise ValueError("Coordinates need unique turbine IDs and finite positions")
    minimum = float(required(case, "minimum_spacing_m"))
    if minimum <= 0:
        raise ValueError("Minimum spacing must be positive")
    xy = frame[["x_m", "y_m"]].to_numpy()
    distances = np.linalg.norm(xy[:, None] - xy[None, :], axis=2)
    np.fill_diagonal(distances, np.inf)
    if distances.min() < minimum:
        raise Infeasible("Turbine coordinates violate scenario minimum spacing")
    # Farm area is a reporting boundary, never a multiplier on route lengths.
    area = float(required(case, "farm_area_km2"))
    if area <= 0:
        raise ValueError("Farm area must be positive")
    return frame


def calculate_wakes(coordinates: pd.DataFrame, wind: dict, turbine: dict, base: Path, inputs):
    """Use explicit state weights and supplied curves; never build a synthetic turbine curve."""
    try:
        from py_wake.site import UniformSite
        from py_wake.wind_turbines import WindTurbine
        from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
        from py_wake.deficit_models import TurboNOJDeficit
        from py_wake.wind_farm_models.engineering_models import PropagateDownwind
        from py_wake.superposition_models import SquaredSum
        from py_wake.rotor_avg_models.area_overlap_model import AreaOverlapAvgModel
    except ImportError as exc:
        raise MissingInput("PyWake is not installed; supply a saved turbine-state power CSV or install the wind extra") from exc
    states = pd.read_csv(base / required(wind, "wind_states_file"))
    curve = pd.read_csv(base / required(wind, "turbine_curve_file"))
    ti = inputs.positive("wind-turbulence-intensity", "fraction")
    machine = WindTurbine("case", diameter=required(turbine, "rotor_diameter_m"),
                          hub_height=required(turbine, "hub_height_m"),
                          powerCtFunction=PowerCtTabular(curve.speed_m_s, curve.power_kw, "kW", curve.ct))
    wake = PropagateDownwind(UniformSite(p_wd=[1], ti=ti), machine,
                            wake_deficitModel=TurboNOJDeficit(),
                            rotorAvgModel=AreaOverlapAvgModel(), superpositionModel=SquaredSum())
    x, y = coordinates.x_m.to_numpy(), coordinates.y_m.to_numpy()
    power = np.zeros((len(states), len(coordinates)))
    # One PyWake call per direction; every state keeps its own speed and weight.
    for direction, group in states.groupby("direction_deg", sort=False):
        speeds, index = np.unique(group.speed_m_s.to_numpy(float), return_inverse=True)
        result = wake(x, y, wd=[direction], ws=speeds)
        # PyWake returns W with dimensions (turbine, direction, speed).
        power[group.index.to_numpy()] = result.Power.values[:, 0, :].T[index] / 1000
    hours = states.hours.to_numpy(float)
    if (not np.isclose(hours.sum(), inputs.number("annual-hours", "h/year"))
            or np.any(hours < 0) or not np.isfinite(hours).all()):
        raise ValueError("Wind-state hours must cover a full year")
    return WindStates(states.state.astype(str).tolist(), hours, coordinates.turbine.tolist(), power), version("py-wake")
