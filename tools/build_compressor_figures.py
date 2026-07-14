"""Build compressor energy and cost figures used by the Quarto site.

Run manually when the compressor assumptions change:

    python tools/build_compressor_figures.py

The multistage compression-work relation and its constants (gamma, T, eta_comp,
eta_motor, r_max) are taken directly from hydrogen_infra/compressor.qmd. The
average hydrogen compressibility factor Z_avg is not pinned to a fixed value
on that page; it is computed here from real-gas hydrogen properties via
CoolProp, evaluated at the arithmetic mean of inlet and outlet pressure, the
same way the pipeline capacity model in build_pipeline_figures.py evaluates
density and viscosity at an average pipeline pressure.

The cost curve is anchored to the single disclosed reference point on that
page (30 -> 150 bar gives approximately 56 EUR/kW of electrolyser capacity)
and extended using the 0.8335 cost-scaling exponent, so no additional
undisclosed cost constants are introduced.
"""

from pathlib import Path

import matplotlib
import numpy as np
from CoolProp.CoolProp import PropsSI

matplotlib.use("Agg")
import matplotlib.pyplot as plt

GAMMA = 1.41
T_K = 298.0
ETA_COMP = 0.80
ETA_MOTOR = 0.95
R_MAX = 3.3
R_GAS = 8.314
M_H2 = 2.016e-3

C_COMP_REF_EUR_PER_KW = 56.0
P_IN_REF_BAR = 30.0
P_OUT_REF_BAR = 150.0
COST_EXPONENT = 0.8335

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = PROJECT_ROOT / "figures"


def num_stages(p_in_bar: float, p_out_bar: float) -> int:
    return max(1, int(np.ceil(np.log(p_out_bar / p_in_bar) / np.log(R_MAX))))


def average_compressibility_factor(p_in_bar: float, p_out_bar: float) -> float:
    p_avg_pa = 0.5 * (p_in_bar + p_out_bar) * 1e5
    return PropsSI("Z", "T", T_K, "P", p_avg_pa, "Hydrogen")


def compressor_energy_kwh_per_kg(p_in_bar: float, p_out_bar: float) -> float:
    n = num_stages(p_in_bar, p_out_bar)
    r_s = (p_out_bar / p_in_bar) ** (1 / n)
    z_avg = average_compressibility_factor(p_in_bar, p_out_bar)
    w_shaft = (
        n * GAMMA * z_avg * R_GAS * T_K
        / ((GAMMA - 1) * M_H2 * ETA_COMP)
        * (r_s ** ((GAMMA - 1) / GAMMA) - 1)
    )
    return w_shaft / (ETA_MOTOR * 3.6e6)


def compressor_cost_eur_per_kw_ely(p_in_bar: float, p_out_bar: float) -> float:
    e_ref = compressor_energy_kwh_per_kg(P_IN_REF_BAR, P_OUT_REF_BAR)
    e = compressor_energy_kwh_per_kg(p_in_bar, p_out_bar)
    return C_COMP_REF_EUR_PER_KW * (e / e_ref) ** COST_EXPONENT


def plot_energy_curves(output_path: Path) -> None:
    inlet_pressures = [1, 10, 20, 30]
    outlet_pressures = np.arange(80, 155, 5)

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for p_in in inlet_pressures:
        energy = [compressor_energy_kwh_per_kg(p_in, p_out) for p_out in outlet_pressures]
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


def plot_cost_curves(output_path: Path) -> None:
    inlet_pressures = [1, 10, 20, 30]
    outlet_pressures = np.arange(80, 155, 5)

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for p_in in inlet_pressures:
        cost = [compressor_cost_eur_per_kw_ely(p_in, p_out) for p_out in outlet_pressures]
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

    energy_path = FIGURE_DIR / "compressor-energy-vs-pressure.svg"
    plot_energy_curves(energy_path)
    print(f"Wrote {energy_path.relative_to(PROJECT_ROOT)}")

    cost_path = FIGURE_DIR / "compressor-cost-vs-pressure.svg"
    plot_cost_curves(cost_path)
    print(f"Wrote {cost_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
