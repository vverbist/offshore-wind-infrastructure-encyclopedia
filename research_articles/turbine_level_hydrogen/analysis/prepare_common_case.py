"""Generate the common operating case shared by both article architectures.

Reads the agreed record (scenarios/reference_case.toml) and the central inputs,
then writes scenarios/common_case.toml and the data files in scenarios/common/.
Both architecture templates include common_case.toml, so they receive the same
coordinates, turbine definition, wind states and turbine-level power.

Run from the repository root with the optional wind dependency:

    uv run --extra wind python research_articles/turbine_level_hydrogen/analysis/prepare_common_case.py

To rebuild the turbine curve from its pinned source, add
``--turbine-source <downloaded IEA-15-240-RWT_tabular.xlsx>``; the file's
SHA-256 must match the record.

Units: m, m/s, degrees clockwise from north (direction wind comes FROM),
kW, hours per year. Coordinates: x east, y north, origin at the farm centre.
"""
import argparse
import hashlib
import json
from math import ceil, sqrt
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from model.inputs import load_inputs
from model.wind_resource_and_layout.wake_modelling_and_spacing import calculate_wakes
from research_articles.turbine_level_hydrogen.analysis.reference_case import (
    CASE_PATH, absolute_pressure_bar, derive_reference_case, load_reference_case)

SCENARIOS = CASE_PATH.parent
COMMON = SCENARIOS / "common"
CURVE_FILE, COORDINATE_FILE = "common/turbine_power_ct.csv", "common/coordinates.csv"
WIND_FILE, POWER_FILE = "common/wind_states.csv", "common/power_states.csv"
SUMMARY_FILE = "common/summary.json"
NODE_FILE, SECTION_GEOMETRY_FILE = "common/collection_nodes.csv", "common/collection_sections_geometry.csv"
MANIFOLD = "manifold"
DESIGN_STATE = "design-all-rated"
NO_POWER_STATE = "below-cut-in-or-above-cut-out"
# Explicit idle rows: PyWake holds the first tabulated value below the table, so
# zero power and thrust are declared 1 mm/s outside the tabulated operating range.
IDLE_OFFSET_M_S = 0.001


def turbine_curve_from_source(xlsx: Path, case: dict) -> pd.DataFrame:
    """Tabulated electrical power and thrust coefficient; noise above rating is capped.

    Idle rotor thrust outside the operating range is neglected (zero power and thrust).
    """
    digest = hashlib.sha256(xlsx.read_bytes()).hexdigest()
    if digest != case["turbine"]["curve_source_sha256"]:
        raise ValueError("Turbine source file does not match the recorded SHA-256")
    table = pd.read_excel(xlsx, sheet_name="Rotor Performance").dropna(subset=["Power [MW]"])
    rated_kw = case["turbine"]["rated_power_mw"] * 1000
    curve = pd.DataFrame({
        "speed_m_s": table["Wind [m/s]"].astype(float).round(6),
        "power_kw": np.minimum(table["Power [MW]"].astype(float) * 1000, rated_kw).round(3),
        "ct": table["Thrust Coefficient [-]"].astype(float).round(6)})
    low, high = curve.speed_m_s.min(), curve.speed_m_s.max()
    idle = pd.DataFrame({"speed_m_s": [0.0, low - IDLE_OFFSET_M_S, high + IDLE_OFFSET_M_S],
                         "power_kw": 0.0, "ct": 0.0})
    return pd.concat([idle.iloc[:2], curve, idle.iloc[2:]], ignore_index=True)


def coordinates(case: dict, derived: dict) -> pd.DataFrame:
    """Rows run crosswind and are numbered from the upwind edge; the last row is centred.

    With the dominant direction theta (wind FROM, clockwise from north), the
    downwind unit vector is (-sin theta, -cos theta) and the crosswind unit vector
    is (cos theta, -sin theta). Row order also sets the provisional AC string order.
    """
    theta = np.deg2rad(derived["dominant_from_deg"])
    downwind = np.array([-np.sin(theta), -np.cos(theta)])
    crosswind = np.array([np.cos(theta), -np.sin(theta)])
    count, columns, rows = case["site"]["turbine_count"], derived["columns"], derived["rows"]
    records = []
    for row in range(rows):
        in_row = min(columns, count - row * columns)
        for column in range(in_row):
            u = (column - (in_row - 1) / 2) * derived["spacing_crosswind_m"]
            v = (row - (rows - 1) / 2) * derived["spacing_alongwind_m"]
            x, y = u * crosswind + v * downwind
            records.append({"turbine": f"T{len(records) + 1:03d}", "x_m": round(x, 2), "y_m": round(y, 2)})
    return pd.DataFrame(records)


def collection_network(case: dict, derived: dict, coords: pd.DataFrame):
    """Ladder nodes and section geometry with the healthy-state flow shares.

    Rungs follow the rows; end turbines of full rows lie on the headers and the
    shorter final row reaches them through one extension per side. Each rung
    splits at its centre (the middle turbine of an odd row sends half each way).
    Headers drain to their midpoints, and tie-ins run along the crosswind
    centreline to the manifold at the farm centre. Vertical length is one water
    depth per turbine end (riser); header nodes and the manifold are on the seabed.
    No route allowance is applied (hydrogen base case). Diameters and pressures
    are design inputs of each case and are not part of this geometry.
    """
    theta = np.deg2rad(derived["dominant_from_deg"])
    downwind = np.array([-np.sin(theta), -np.cos(theta)])
    crosswind = np.array([np.cos(theta), -np.sin(theta)])
    half_breadth = derived["breadth_km"] * 500
    depth = case["site"]["water_depth_m"]
    columns, rows = derived["columns"], derived["rows"]
    ids = coords.turbine.tolist()
    row_ids, start = [], 0
    for row in range(rows):
        size = min(columns, len(ids) - start)
        row_ids.append(ids[start:start + size])
        start += size
    nodes, sections = [], []

    def node(name, u, v):
        x, y = u * crosswind + v * downwind
        nodes.append({"node": name, "x_m": round(x, 2), "y_m": round(y, 2)})
        return name

    def section(kind, a, b, share):
        risers = sum(end in ids for end in (a, b))
        sections.append({"section": f"{kind}-{len(sections) + 1:03d}", "class": kind, "from": a, "to": b,
                         "vertical_m": risers * depth, "route_allowance": 0.0, "flow_share": share})

    along = lambda row: (row - (rows - 1) / 2) * derived["spacing_alongwind_m"]
    header = {}
    for row, members in enumerate(row_ids):
        for side, end in (("a", members[0]), ("b", members[-1])):
            if len(members) == columns:
                header[side, row] = end
            else:
                header[side, row] = node(f"header-{side}-{row + 1}", -half_breadth if side == "a" else half_breadth, along(row))
        middle = (len(members) - 1) / 2
        for index, turbine in enumerate(members):
            if index < middle:
                target = [members[index - 1] if index else header["a", row]]
            elif index > middle:
                target = [members[index + 1] if index < len(members) - 1 else header["b", row]]
            else:
                target = [members[index - 1], members[index + 1]]
            for end in target:
                if end != turbine:
                    section("rung", turbine, end, 1.0 / len(target))
    manifold = node(MANIFOLD, 0.0, 0.0)
    for side in ("a", "b"):
        midpoint = node(f"header-{side}-mid", -half_breadth if side == "a" else half_breadth, 0.0)
        for row in range(rows):
            downstream = header[side, row + 1] if row < rows // 2 - 1 else (
                midpoint if row in (rows // 2 - 1, rows // 2) else header[side, row - 1])
            section("header", header[side, row], downstream, 1.0)
        section("tie-in", midpoint, manifold, 1.0)
    return pd.DataFrame(nodes), pd.DataFrame(sections)


def wind_states(case: dict, curve: pd.DataFrame, annual_hours: float,
                direction_step_deg: float, speed_bin_m_s: float) -> pd.DataFrame:
    """Joint direction-speed states from the fitted sector Weibull table.

    Direction is spread uniformly within each 30-degree sector, whose stored label
    is its lower edge. Each speed bin is represented by its midpoint. All speeds
    outside the tabulated operating range form one zero-power state.
    """
    sectors = pd.read_csv(SCENARIOS / case["wind"]["sector_file"])
    width = float(sectors.sector_deg.iloc[1] - sectors.sector_deg.iloc[0])
    per_sector = round(width / direction_step_deg)
    if not np.isclose(per_sector * direction_step_deg, width):
        raise ValueError("Direction step must divide the sector width")
    operating = curve[curve.power_kw > 0].speed_m_s
    cut_in, cut_out = operating.min(), operating.max()
    edges = np.arange(cut_in, cut_out + speed_bin_m_s / 2, speed_bin_m_s)
    if not np.isclose(edges[-1], cut_out):
        raise ValueError("Speed bins must end at cut-out")
    records, operating_probability = [], 0.0
    for sector in sectors.itertuples():
        cdf = 1 - np.exp(-(edges / sector.c) ** sector.k)
        probability = sector.freq * np.diff(cdf) / per_sector
        for step in range(per_sector):
            direction = (sector.sector_deg + (step + 0.5) * direction_step_deg) % 360
            for low, p in zip(edges[:-1], probability):
                records.append({"state": f"d{direction:05.1f}-v{low + speed_bin_m_s / 2:05.2f}",
                                "speed_m_s": round(low + speed_bin_m_s / 2, 4),
                                "direction_deg": direction, "hours": p * annual_hours})
        operating_probability += probability.sum() * per_sector
    states = pd.DataFrame(records)
    remainder = annual_hours - states.hours.sum()
    if not np.isclose(1 - operating_probability, remainder / annual_hours):
        raise ValueError("State probabilities do not close")
    return states, remainder


def power_states(coords, states, remainder_hours, case, inputs):
    machine = {"rotor_diameter_m": case["turbine"]["rotor_diameter_m"],
               "hub_height_m": case["turbine"]["hub_height_m"]}
    wind_case = {"wind_states_file": WIND_FILE, "turbine_curve_file": CURVE_FILE}
    # The wake adapter checks a complete year, so the zero-power hours ride on a
    # dummy calm state that is replaced by an explicit all-zero row afterwards.
    calm = pd.DataFrame([{"state": NO_POWER_STATE, "speed_m_s": 0.0, "direction_deg": 0.0,
                          "hours": remainder_hours}])
    (SCENARIOS / WIND_FILE).write_text(pd.concat([states, calm]).to_csv(index=False, lineterminator="\n"))
    wind, version = calculate_wakes(coords, wind_case, machine, SCENARIOS, inputs)
    table = pd.DataFrame(wind.power_kw, columns=wind.turbine_ids).round(1)
    table.insert(0, "hours", wind.hours)
    table.insert(0, "state", wind.state_ids)
    table.loc[table.state == NO_POWER_STATE, wind.turbine_ids] = 0.0
    rated = case["turbine"]["rated_power_mw"] * 1000
    design = {"state": DESIGN_STATE, "hours": 0.0, **{t: rated for t in wind.turbine_ids}}
    return pd.concat([table, pd.DataFrame([design])], ignore_index=True), version


def empirical_no_wake_check(case, curve, annual_hours):
    """Single-turbine AEP from the hourly record versus the fitted Weibull states."""
    hourly = pd.read_excel(SCENARIOS / case["wind"]["hourly_workbook"], sheet_name="WRA", usecols="B")
    speeds = hourly.iloc[:, 0].dropna().to_numpy(float)
    power = np.interp(speeds, curve.speed_m_s, curve.power_kw, left=0, right=0)
    return float(power.mean() * annual_hours / 1000), len(speeds)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--turbine-source", type=Path)
    args = parser.parse_args()
    case = load_reference_case()
    inputs = load_inputs({})
    atmospheric = inputs.number("standard-atmospheric-pressure", "bar")
    annual_hours = inputs.number("annual-hours", "h/year")
    derived = derive_reference_case(case, atmospheric)
    COMMON.mkdir(exist_ok=True)
    if args.turbine_source:
        (SCENARIOS / CURVE_FILE).write_text(
            turbine_curve_from_source(args.turbine_source, case).to_csv(index=False, lineterminator="\n"))
    curve = pd.read_csv(SCENARIOS / CURVE_FILE)
    coords = coordinates(case, derived)
    (SCENARIOS / COORDINATE_FILE).write_text(coords.to_csv(index=False, lineterminator="\n"))
    network_nodes, network_sections = collection_network(case, derived, coords)
    (SCENARIOS / NODE_FILE).write_text(network_nodes.to_csv(index=False, lineterminator="\n"))
    (SCENARIOS / SECTION_GEOMETRY_FILE).write_text(network_sections.to_csv(index=False, lineterminator="\n"))
    wind = case["wind"]
    states, remainder = wind_states(case, curve, annual_hours, wind["direction_step_deg"], wind["speed_bin_m_s"])
    table, version = power_states(coords, states, remainder, case, inputs)
    (SCENARIOS / POWER_FILE).write_text(table.to_csv(index=False, lineterminator="\n"))

    ids = coords.turbine.tolist()
    annual = table[table.state != DESIGN_STATE]
    wake_mwh = float((annual[ids].sum(axis=1) * annual.hours).sum() / 1000)
    single = np.interp(states.speed_m_s, curve.speed_m_s, curve.power_kw)
    no_wake_mwh = float((single * states.hours).sum() * len(ids) / 1000)
    empirical_mwh, hourly_count = empirical_no_wake_check(case, curve, annual_hours)
    # Discretisation check: repeat the wake calculation with 1-degree directions.
    fine, fine_remainder = wind_states(case, curve, annual_hours, 1, wind["speed_bin_m_s"])
    fine_table, _ = power_states(coords, fine, fine_remainder, case, inputs)
    fine_mwh = float((fine_table[ids].sum(axis=1) * fine_table.hours).sum() / 1000)
    # Leave the adopted states, not the check states, in the wind-state file.
    power_states(coords, states, remainder, case, inputs)
    installed_kw = len(ids) * case["turbine"]["rated_power_mw"] * 1000
    summary = {
        "pywake_version": version, "state_count": len(annual), "design_state": DESIGN_STATE,
        "no_power_hours": float(remainder),
        "no_wake_aep_gwh": no_wake_mwh / 1000, "wake_aep_gwh": wake_mwh / 1000,
        "wake_loss": 1 - wake_mwh / no_wake_mwh,
        "gross_capacity_factor": wake_mwh * 1000 / (installed_kw * annual_hours),
        "max_annual_farm_fraction": float(annual[ids].sum(axis=1).max() / installed_kw),
        "single_turbine_weibull_aep_mwh": no_wake_mwh / len(ids),
        "single_turbine_hourly_aep_mwh": empirical_mwh, "hourly_record_count": hourly_count,
        "weibull_vs_hourly_difference": no_wake_mwh / len(ids) / empirical_mwh - 1,
        "wake_aep_1deg_gwh": fine_mwh / 1000,
        "direction_step_difference": wake_mwh / fine_mwh - 1,
    }
    (SCENARIOS / SUMMARY_FILE).write_text(json.dumps(summary, indent=2) + "\n")
    (SCENARIOS / "common_case.toml").write_text(common_case_toml(case, derived, atmospheric))
    print(json.dumps(summary, indent=2))


def common_case_toml(case: dict, derived: dict, atmospheric_bar: float) -> str:
    site, turbine = case["site"], case["turbine"]
    minimum = derived["minimum_spacing_m"]
    return f"""# GENERATED by analysis/prepare_common_case.py from reference_case.toml and the
# central inputs. Do not edit: change the record and rerun the script.
# Both architecture templates include this file; they may not redefine its keys.
# Evidence and reasoning: ../reference_case.qmd.

[site]
coordinates_file = "{COORDINATE_FILE}"
minimum_spacing_m = {minimum:.2f}
farm_area_km2 = {site["farm_area_km2"]!r}
water_depth_m = {site["water_depth_m"]!r}

[turbine]
rotor_diameter_m = {turbine["rotor_diameter_m"]!r}
hub_height_m = {turbine["hub_height_m"]!r}
rated_power_kw = {turbine["rated_power_mw"] * 1000!r}

[wind]
# Wake-affected power at the generator electrical output; built from
# {WIND_FILE} and {CURVE_FILE}.
power_states_file = "{POWER_FILE}"
design_state_ids = ["{DESIGN_STATE}"]

[electrolysis]
overplant_factor = {case["electrolysis"]["overplant_factor"]!r}

[hydrogen]
# Absolute pressures in bar(a), converted from the recorded gauge values.
stack_outlet_bar = {absolute_pressure_bar(case["electrolysis"]["stack_outlet_pressure_bar_g"], atmospheric_bar)!r}
delivery_bar = {absolute_pressure_bar(case["hydrogen"]["delivery_pressure_bar_g"], atmospheric_bar)!r}
export_length_km = {case["hydrogen"]["export_length_km"]!r}

[installation]
turbine_method = "{case['installation']['turbine_method']}"
"""


if __name__ == "__main__":
    main()
