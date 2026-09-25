"""Read the article assumptions and derive the quantities shown in reference_case.qmd.

This prepares documentation variables only; it does not run an architecture case.
"""
import csv
from math import ceil, sqrt
from pathlib import Path
import tomllib


CASE_PATH = Path(__file__).resolve().parents[1] / "scenarios/reference_case.toml"


def load_reference_case():
    with CASE_PATH.open("rb") as stream:
        return tomllib.load(stream)


def derive_reference_case(case):
    """Lengths in km, spacing in m, power in MW, bearings clockwise from north."""
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
    }


def quarto_variables():
    case = load_reference_case()
    values = {key: value for section in case.values() for key, value in section.items()
              if isinstance(value, (int, float))}
    values.update(derive_reference_case(case))
    precision = {"breadth_km": 2, "length_km": 2,
                 "spacing_crosswind_m": 1, "spacing_alongwind_m": 1}
    return {"ijv-" + key.replace("_", "-"):
            (f"{value:.{precision[key]}f}" if key in precision else f"{value:g}")
            for key, value in values.items()}
