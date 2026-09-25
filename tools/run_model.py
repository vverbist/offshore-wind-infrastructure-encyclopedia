"""Run one article scenario. Existing output directories are never overwritten."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model.inputs import read_scenario, load_inputs
from model.workflow import run_case
from model.reporting import write_result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    scenario = read_scenario(args.scenario)
    result = run_case(scenario, load_inputs(scenario), args.scenario.resolve().parent)
    write_result(result, args.output)
    print(f"{result.name}: {result.status}")
    print(f"{len(result.reasons)} unresolved inputs or failed checks; see {args.output / 'result.json'}")


if __name__ == "__main__":
    main()
