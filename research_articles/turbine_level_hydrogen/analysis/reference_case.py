"""Read the article assumptions and derive the quantities shown in reference_case.qmd.

This prepares documentation variables and the absolute pressures that the
architecture scenarios must use; it does not run an architecture case.
"""
import csv
import json
from math import ceil, sqrt
from pathlib import Path
import tomllib

from model_data.parameters import load_parameters


CASE_PATH = Path(__file__).resolve().parents[1] / "scenarios/reference_case.toml"
# Written by prepare_common_case.py; wake results need the optional PyWake extra.
SUMMARY_PATH = CASE_PATH.parent / "common/summary.json"


def load_reference_case():
    with CASE_PATH.open("rb") as stream:
        return tomllib.load(stream)


def absolute_pressure_bar(gauge_bar, atmospheric_bar):
    """Convert gauge to absolute pressure; all pressures in bar."""
    return gauge_bar + atmospheric_bar


def derive_reference_case(case, atmospheric_bar):
    """Lengths in km, spacing in m, power in MW, pressures in bar(a), bearings clockwise from north."""
    site = case["site"]
    count, area = site["turbine_count"], site["farm_area_km2"]
    ratio = site["crosswind_to_alongwind_ratio"]
    columns = ceil(sqrt(count * ratio))
    rows = ceil(count / columns)
    breadth, length = sqrt(area * ratio), sqrt(area / ratio)
    with (CASE_PATH.parent / case["wind"]["sector_file"]).open(newline="") as stream:
        sectors = list(csv.DictReader(stream))
    dominant = max(sectors, key=lambda row: float(row["freq"]))
    sector_width = float(sectors[1]["sector_deg"]) - float(sectors[0]["sector_deg"])
    return {
        "installed_mw": count * case["turbine"]["rated_power_mw"],
        "breadth_km": breadth, "length_km": length,
        "columns": columns, "rows": rows, "full_rows": rows - 1,
        "last_row": count - (rows - 1) * columns,
        "spacing_crosswind_m": breadth * 1000 / (columns - 1),
        "spacing_alongwind_m": length * 1000 / (rows - 1),
        "dominant_from_deg": float(dominant["sector_deg"]) + sector_width / 2,
        "minimum_spacing_m": case["layout"]["minimum_spacing_rotor_diameters"] * case["turbine"]["rotor_diameter_m"],
        "stack_outlet_pressure_bar_a": absolute_pressure_bar(
            case["electrolysis"]["stack_outlet_pressure_bar_g"], atmospheric_bar),
        "delivery_pressure_bar_a": absolute_pressure_bar(
            case["hydrogen"]["delivery_pressure_bar_g"], atmospheric_bar),
    }


def quarto_variables():
    case = load_reference_case()
    values = {key: value for section in case.values() for key, value in section.items()
              if isinstance(value, (int, float))}
    atmospheric_bar = float(load_parameters().number("standard-atmospheric-pressure", "bar"))
    values.update(derive_reference_case(case, atmospheric_bar))
    precision = {"breadth_km": 2, "length_km": 2,
                 "spacing_crosswind_m": 1, "spacing_alongwind_m": 1,
                 "stack_outlet_pressure_bar_a": 2, "delivery_pressure_bar_a": 2}
    variables = {"ijv-" + key.replace("_", "-"):
                 (f"{value:.{precision[key]}f}" if key in precision else f"{value:g}")
                 for key, value in values.items()}
    summary = json.loads(SUMMARY_PATH.read_text())
    for key, places in (("wake_loss", 1), ("gross_capacity_factor", 1),
                        ("weibull_vs_hourly_difference", 1), ("direction_step_difference", 2)):
        variables["ijv-" + key.replace("_", "-")] = f"{summary[key] * 100:.{places}f}%"
    for key in ("no_wake_aep_gwh", "wake_aep_gwh", "no_power_hours", "hourly_record_count"):
        variables["ijv-" + key.replace("_", "-")] = f"{summary[key]:,.0f}"
    variables["ijv-state-count"] = f"{summary['state_count']:,}"
    variables["ijv-pywake-version"] = summary["pywake_version"]
    return variables
