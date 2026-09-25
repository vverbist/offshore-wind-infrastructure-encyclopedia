"""Build compressor energy and cost figures used by the Quarto site.

Run manually when the compressor assumptions change:

    python tools/build_compressor_figures.py

The multistage compression-work relation and its constants (gamma, T, eta_comp,
eta_motor, r_max) are taken directly from hydrogen_infra/compressor.qmd. The
average hydrogen compressibility factor Z_avg is not pinned to a fixed value
on that page; it is computed here from real-gas hydrogen properties via
CoolProp, evaluated at the arithmetic mean of inlet and outlet pressure.

The cost curve is anchored to the single disclosed reference point on that
page (30 -> 150 bar gives approximately 56 EUR/kW of electrolyser capacity)
and extended using the 0.8335 cost-scaling exponent, so no additional
undisclosed cost constants are introduced.
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
from model.hydrogen_infra.compressor import specific_energy, reference_cost_curve

FIGURE_DIR = PROJECT_ROOT / "figures"


def compressor_energy_kwh_per_kg(p_in_bar, p_out_bar, inputs):
    return specific_energy(p_in_bar, p_out_bar, inputs)


def compressor_cost_eur_per_kw_ely(p_in_bar, p_out_bar, inputs):
    return reference_cost_curve(p_in_bar, p_out_bar, inputs)


def plot_energy_curves(output_path: Path, inputs) -> None:
    inlet_pressures = [1, 10, 20, 30]
    outlet_pressures = np.arange(80, 155, 5)

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for p_in in inlet_pressures:
        energy = [compressor_energy_kwh_per_kg(p_in, p_out, inputs) for p_out in outlet_pressures]
        ax.plot(outlet_pressures, energy, marker="o", linewidth=2, label=f"{p_in:.0f} bar")

    ax.set_title("Compressor Electricity Consumption")
    ax.set_xlabel("Outlet pressure [bar]")
    ax.set_ylabel("Compressor electricity [kWh/kg H₂]")
    ax.set_ylim(bottom=0)
    ax.grid(True, color="#d1d5db", linewidth=0.8)
    ax.legend(title="Inlet pressure")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_cost_curves(output_path: Path, inputs) -> None:
    inlet_pressures = [1, 10, 20, 30]
    outlet_pressures = np.arange(80, 155, 5)

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for p_in in inlet_pressures:
        cost = [compressor_cost_eur_per_kw_ely(p_in, p_out, inputs) for p_out in outlet_pressures]
        ax.plot(outlet_pressures, cost, marker="o", linewidth=2, label=f"{p_in:.0f} bar")

    ax.set_title("Compressor Cost")
    ax.set_xlabel("Outlet pressure [bar]")
    ax.set_ylabel("Compressor cost [EUR/kW electrolyser]")
    ax.set_ylim(bottom=0)
    ax.grid(True, color="#d1d5db", linewidth=0.8)
    ax.legend(title="Inlet pressure")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs({})

    energy_path = FIGURE_DIR / "compressor-energy-vs-pressure.svg"
    plot_energy_curves(energy_path, inputs)
    print(f"Wrote {energy_path.relative_to(PROJECT_ROOT)}")

    cost_path = FIGURE_DIR / "compressor-cost-vs-pressure.svg"
    plot_cost_curves(cost_path, inputs)
    print(f"Wrote {cost_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
