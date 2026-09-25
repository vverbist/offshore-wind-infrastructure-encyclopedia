from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import sys

matplotlib.use("Agg")
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from model.inputs import load_inputs
from model.hydrogen_infra.hydrogen_pipelines import capacity_kg_h
from research_articles.turbine_level_hydrogen.analysis.reference_case import (
    absolute_pressure_bar, load_reference_case)

FIGURE_DIR = PROJECT_ROOT / "figures"


def build_pipeline_data():
    inputs = load_inputs({})
    # Inlet pressure and diameter are explicit figure cases, not model defaults.
    # Route length and delivery pressure come from the agreed reference case.
    case = load_reference_case()["hydrogen"]
    length_m = case["export_length_km"] * 1000
    delivery_bar = absolute_pressure_bar(case["delivery_pressure_bar_g"],
                                         inputs.number("standard-atmospheric-pressure", "bar"))
    pressures = np.arange(80, 155, 5)
    diameters = np.arange(4, 9, 1)
    rows = []
    for diameter in diameters:
        for pressure in pressures:
            capacity = capacity_kg_h(diameter * 0.0254, pressure, delivery_bar, length_m, inputs)
            rows.append({"P": pressure, "D": diameter, "capacity_kg_h": capacity,
                         "capacity_mw_hhv": capacity * inputs.number("hydrogen-hhv", "kWh/kg") / 1000})
    data = pd.DataFrame(rows)
    try:
        from pipeline_cost_curve import pipeline_cost_curve
    except ModuleNotFoundError:
        return data, None
    # Pressures on the figure axis are absolute; the fit is read in bar(g).
    atmospheric = inputs.number("standard-atmospheric-pressure", "bar")
    cost_grid = np.array([pipeline_cost_curve(row.P - atmospheric, row.D) for row in data.itertuples()]).reshape(-1)
    data["cost"] = cost_grid
    data["cost_per_capacity"] = data.cost / data.capacity_kg_h
    return data, cost_grid


def plot_capacity_curves(df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.4))

    for diameter in sorted(df["D"].unique()):
        dfd = df[df["D"] == diameter].sort_values("P")
        ax.plot(
            dfd["P"],
            dfd["capacity_mw_hhv"],
            marker="o",
            linewidth=2,
            label=f"{diameter:.0f} inch",
        )

    ax.set_title("Hydrogen Pipeline Capacity")
    ax.set_xlabel("Inlet pressure [bar(a)]")
    ax.set_ylabel("Capacity [MW HHV]")
    ax.set_ylim(bottom=0)
    ax.grid(True, color="#d1d5db", linewidth=0.8)
    ax.legend(title="Diameter")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_cost_curves(df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.4))

    for diameter in sorted(df["D"].unique()):
        dfd = df[df["D"] == diameter].sort_values("P")
        ax.plot(
            dfd["P"],
            dfd["cost"],
            marker="o",
            linewidth=2,
            label=f"{diameter:.0f} inch",
        )

    ax.set_title("Hydrogen Pipeline Material Cost")
    ax.set_xlabel("Inlet pressure [bar(a)]")
    ax.set_ylabel("Material cost per unit length")
    ax.set_ylim(bottom=0)
    ax.set_yticklabels([])
    ax.grid(True, color="#d1d5db", linewidth=0.8)
    ax.legend(title="Diameter")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_cost_per_capacity_curves(df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.4))

    for diameter in sorted(df["D"].unique()):
        dfd = df[df["D"] == diameter].sort_values("P")
        ax.plot(
            dfd["P"],
            dfd["cost_per_capacity"],
            marker="o",
            linewidth=2,
            label=f"{diameter:.0f} inch",
        )

    ax.set_title("Hydrogen Pipeline Cost per Unit Capacity")
    ax.set_xlabel("Inlet pressure [bar(a)]")
    ax.set_ylabel("Material cost per unit capacity")
    ax.set_ylim(bottom=0)
    ax.set_yticklabels([])
    ax.grid(True, color="#d1d5db", linewidth=0.8)
    ax.legend(title="Diameter")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    df, cost_grid = build_pipeline_data()

    capacity_path = FIGURE_DIR / "pipeline-capacity-vs-pressure.svg"
    plot_capacity_curves(df, capacity_path)
    print(f"Wrote {capacity_path.relative_to(PROJECT_ROOT)}")

    if cost_grid is None:
        print("Skipped cost figures: pipeline_cost_curve is not available.")
        return

    cost_path = FIGURE_DIR / "pipeline-cost-vs-pressure.svg"
    plot_cost_curves(df, cost_path)
    print(f"Wrote {cost_path.relative_to(PROJECT_ROOT)}")

    cost_per_capacity_path = FIGURE_DIR / "pipeline-cost-per-capacity-vs-pressure.svg"
    plot_cost_per_capacity_curves(df, cost_per_capacity_path)
    print(f"Wrote {cost_per_capacity_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

