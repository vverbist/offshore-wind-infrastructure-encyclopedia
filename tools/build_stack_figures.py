"""Build static figures used by the Quarto site.

Run manually when numerical inputs change:

    python tools/build_stack_figures.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "numerical_inputs" / "pem_polarisation_curve.xlsx"
DEFAULT_OUTPUT = PROJECT_ROOT / "figures" / "pem-polarisation.svg"
DEFAULT_SHEET = "polarisation_curve"
REVERSIBLE_CELL_VOLTAGE_HHV = 1.481
MIN_CURRENT_DENSITY_A_CM2 = 0.2


def build_pem_polarisation_figure(
    input_path: Path = DEFAULT_INPUT,
    output_path: Path = DEFAULT_OUTPUT,
    sheet_name: str = DEFAULT_SHEET,
) -> None:
    df = pd.read_excel(input_path, sheet_name=sheet_name)
    df = df[df["current_density_A_cm2"] >= MIN_CURRENT_DENSITY_A_CM2]

    current_density = df["current_density_A_cm2"]
    cell_voltage = df["cell_voltage_V"]
    efficiency = REVERSIBLE_CELL_VOLTAGE_HHV / cell_voltage * 100

    fig, (ax_voltage, ax_efficiency) = plt.subplots(1, 2, figsize=(10, 4))

    ax_voltage.plot(current_density, cell_voltage, linewidth=2.2)
    ax_voltage.set_xlabel("Current density [A/cm2]")
    ax_voltage.set_ylabel("Cell voltage [V]")
    ax_voltage.set_title("Polarisation curve")
    ax_voltage.set_xlim(left=MIN_CURRENT_DENSITY_A_CM2)
    ax_voltage.grid(True, color="#d1d5db", linewidth=0.8)

    ax_efficiency.plot(current_density, efficiency, linewidth=2.2)
    ax_efficiency.set_xlabel("Current density [A/cm2]")
    ax_efficiency.set_ylabel("Stack efficiency [% HHV]")
    ax_efficiency.set_title("Efficiency")
    ax_efficiency.set_xlim(left=MIN_CURRENT_DENSITY_A_CM2)
    ax_efficiency.grid(True, color="#d1d5db", linewidth=0.8)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, format=output_path.suffix.lstrip(".") or "svg")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build static figures for the Quarto site.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--sheet", default=DEFAULT_SHEET)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_pem_polarisation_figure(
        input_path=args.input,
        output_path=args.output,
        sheet_name=args.sheet,
    )
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
