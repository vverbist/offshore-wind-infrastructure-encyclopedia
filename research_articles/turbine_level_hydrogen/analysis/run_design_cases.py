"""Run explicit design cases, such as pressure/diameter combinations; no optimisation.

Design variables are scenario inputs, not central parameters. Each row of the
cases CSV is one user-supplied case: column ``case`` names it and every other
column is a dotted scenario field, for example ``hydrogen.injection_bar`` or
``hydrogen.export_diameter_m``, with the scenario's own units (bar(a), m).
A field that the scenario or its included common case already defines is
rejected, so a case can only fill design inputs the template leaves open.

    uv run python research_articles/turbine_level_hydrogen/analysis/run_design_cases.py \\
        research_articles/turbine_level_hydrogen/scenarios/centralised.toml cases.csv \\
        --output model_runs/pressure-diameter

Each case is written as a normal result folder; ``comparison.csv`` lists the
supplied design values beside status, summary and export results. The runner
reports every case and does not select one.
"""
import argparse
import copy
from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from model.inputs import read_scenario, load_inputs
from model.workflow import run_case
from model.reporting import write_result


def apply_design_values(scenario: dict, values: dict) -> dict:
    """Return a copy with each dotted field set; existing fields are an error."""
    case = copy.deepcopy(scenario)
    for dotted, value in values.items():
        *sections, key = dotted.split(".")
        if not sections:
            raise ValueError(f"Design field {dotted} must name its scenario section")
        record = case
        for section in sections:
            record = record.setdefault(section, {})
            if not isinstance(record, dict):
                raise ValueError(f"Design field {dotted} does not address a scenario table")
        if key in record:
            raise ValueError(f"Design field {dotted} is already defined by the scenario")
        record[key] = value
    return case


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("scenario", type=Path)
    parser.add_argument("cases", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cases = pd.read_csv(args.cases, dtype={"case": str})
    if "case" not in cases or cases.case.duplicated().any():
        raise ValueError("The cases CSV needs a unique 'case' column")
    args.output.mkdir(parents=True, exist_ok=False)
    baseline = read_scenario(args.scenario)
    rows = []
    for row in cases.to_dict("records"):
        name = row.pop("case")
        scenario = apply_design_values(baseline, {k: v.item() if hasattr(v, "item") else v for k, v in row.items()})
        scenario.setdefault("case", {})["name"] = f"{baseline.get('case', {}).get('name', 'case')}:{name}"
        result = run_case(scenario, load_inputs(scenario), args.scenario.resolve().parent)
        write_result(result, args.output / name)
        export = {f"export_{k}": v for k, v in result.physical.get("export", {}).items()
                  if isinstance(v, (int, float, str))}
        rows.append({"case": name, **row, "status": result.status,
                     "reasons": len(result.reasons), **result.summary, **export})
    pd.DataFrame(rows).to_csv(args.output / "comparison.csv", index=False)


if __name__ == "__main__":
    main()
