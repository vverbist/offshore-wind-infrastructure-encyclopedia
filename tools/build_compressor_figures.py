"""Build compressor energy and cost figures used by the Quarto site.

Run manually when the compressor assumptions change:

    python tools/build_compressor_figures.py

The multistage compression-work relation and its constants (gamma, T, eta_comp,
eta_motor, r_max) are taken directly from hydrogen_infra/compressor.qmd. The
average hydrogen compressibility factor Z_avg is not pinned to a fixed value
on that page; it is computed here from real-gas hydrogen properties via
CoolProp, evaluated at the arithmetic mean of inlet and outlet pressure.

The purchase-cost curves call the shared stack/BOP/compression balance and
bounded-train cost model. They report EUR2025 per turbine kW at full turbine
power, with 1x stack capacity and no conversion losses or installation costs.
"""

from pathlib import Path

import matplotlib
import numpy as np
import sys

matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from model.inputs import load_inputs
from model.hydrogen_infra.compressor import specific_energy, turbine_reference
from model.hydrogen_production.stack import StackCurve

FIGURE_DIR = PROJECT_ROOT / "figures"


def compressor_energy_kwh_per_kg(p_in_bar, p_out_bar, inputs):
    return specific_energy(p_in_bar, p_out_bar, inputs)


def compressor_cost_eur_per_kw_turbine(p_in_bar, p_out_bar, inputs, curve):
    return turbine_reference(inputs.number("wind-turbine-rated-power", "MW") * 1000,
                             p_in_bar, p_out_bar, curve, inputs)["eur_per_turbine_kw"]


def plot_energy_curves(output_path: Path, inputs) -> None:
    inlet_pressures = [1, 10, 20, 30]
    outlet_pressures = np.arange(80, 155, 5)

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for p_in in inlet_pressures:
        energy = [compressor_energy_kwh_per_kg(p_in, p_out, inputs) for p_out in outlet_pressures]
        ax.plot(outlet_pressures, energy, marker="o", linewidth=2, label=f"{p_in:.0f} bar")

    ax.set_title("Compressor Electricity Consumption")
    ax.set_xlabel("Outlet pressure [bar(a)]")
    ax.set_ylabel("Compressor electricity [kWh/kg H₂]")
    ax.set_ylim(bottom=0)
    ax.grid(True, color="#d1d5db", linewidth=0.8)
    ax.legend(title="Inlet pressure [bar(a)]")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_cost_curves(output_path: Path, inputs, curve: StackCurve) -> None:
    inlet_pressures = [1, 10, 20, 30]
    outlet_pressures = np.arange(80, 155, 5)

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for p_in in inlet_pressures:
        cost = [compressor_cost_eur_per_kw_turbine(p_in, p_out, inputs, curve) for p_out in outlet_pressures]
        ax.plot(outlet_pressures, cost, marker="o", linewidth=2, label=f"{p_in:.0f} bar")

    rating = inputs.number("wind-turbine-rated-power", "MW")
    ax.set_title(f"Compressor Purchase Cost — {rating:g} MW Turbine\nFull power; 1× stack capacity; no conversion losses", fontsize=11)
    ax.set_xlabel("Outlet pressure [bar(a)]")
    ax.set_ylabel("Purchase cost [EUR2025/kW turbine]")
    ax.set_ylim(bottom=0)
    ax.grid(True, color="#d1d5db", linewidth=0.8)
    ax.legend(title="Inlet pressure [bar(a)]", loc="upper left", bbox_to_anchor=(1.01, 1))
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs({})
    curve = StackCurve.read(PROJECT_ROOT / "numerical_inputs/pem_polarisation_curve.xlsx")

    energy_path = FIGURE_DIR / "compressor-energy-vs-pressure.svg"
    plot_energy_curves(energy_path, inputs)
    print(f"Wrote {energy_path.relative_to(PROJECT_ROOT)}")

    cost_path = FIGURE_DIR / "compressor-cost-vs-pressure.svg"
    plot_cost_curves(cost_path, inputs, curve)
    print(f"Wrote {cost_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
