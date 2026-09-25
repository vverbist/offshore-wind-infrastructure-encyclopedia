"""Run explicit values of one named central parameter; no optimisation."""
import argparse
import copy
from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from model.inputs import read_scenario, load_inputs
from model.workflow import run_case
from model.reporting import write_result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", type=Path)
    parser.add_argument("parameter")
    parser.add_argument("values", nargs="+", type=float)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    baseline = read_scenario(args.scenario)
    rows = []
    for i, value in enumerate(args.values):
        scenario = copy.deepcopy(baseline)
        scenario.setdefault("overrides", {})[args.parameter] = value
        result = run_case(scenario, load_inputs(scenario), args.scenario.resolve().parent)
        write_result(result, args.output / str(i))
        rows.append({"parameter": args.parameter, "value": value, "status": result.status, **result.summary})
    pd.DataFrame(rows).to_csv(args.output / "comparison.csv", index=False)


if __name__ == "__main__":
    main()
