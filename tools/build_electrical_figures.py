"""Build the electrical-infrastructure figures used by the Quarto site.

Run manually when the reference cable assumptions change:

    python tools/build_electrical_figures.py

The array-string figure uses the documented 15 MW turbine and 70 MW usable
string assumptions. The HVDC figure uses the Prysmian indicative resistance
of 0.0072 ohm/km for a 2,500 mm2 copper 525 kV submarine pole cable. It shows
conductor I^2R loss only; converter, transformer, accessory, land-cable and
temperature effects are deliberately excluded and are discussed on the page.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = PROJECT_ROOT / "figures"

TURBINE_RATING_MW = 15.0
USABLE_STRING_RATING_MW = 70.0
TURBINES_PER_STRING = int(USABLE_STRING_RATING_MW // TURBINE_RATING_MW)

HVDC_RATING_MW = 2_000.0
HVDC_POLE_VOLTAGE_KV = 525.0
HVDC_RESISTANCE_OHM_PER_KM = 0.0072


def plot_array_string_count(output_path: Path) -> None:
    turbine_count = np.arange(1, 201)
    plant_capacity_mw = turbine_count * TURBINE_RATING_MW
    string_count = np.ceil(turbine_count / TURBINES_PER_STRING)

    reference_turbines = int(np.ceil(2_000 / TURBINE_RATING_MW))
    reference_capacity = reference_turbines * TURBINE_RATING_MW
    reference_strings = int(np.ceil(reference_turbines / TURBINES_PER_STRING))

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.step(
        plant_capacity_mw,
        string_count,
        where="post",
        color="#2563eb",
        linewidth=2,
    )
    ax.scatter(
        [reference_capacity],
        [reference_strings],
        color="#dc2626",
        zorder=3,
        label=f"Nominal 2 GW target: {reference_turbines} turbines, {reference_strings} strings",
    )
    ax.set_title("Discrete 66 kV Array-String Requirement")
    ax.set_xlabel("Installed turbine capacity [MW]")
    ax.set_ylabel("Required radial strings [-]")
    ax.set_xlim(0, 3_000)
    ax.set_ylim(bottom=0)
    ax.grid(True, color="#d1d5db", linewidth=0.8)
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def hvdc_conductor_loss_fraction(distance_km: np.ndarray, load_fraction: float) -> np.ndarray:
    transferred_power_w = load_fraction * HVDC_RATING_MW * 1e6
    pole_voltage_v = HVDC_POLE_VOLTAGE_KV * 1e3
    pole_current_a = transferred_power_w / (2 * pole_voltage_v)
    loss_w = (
        2
        * pole_current_a**2
        * HVDC_RESISTANCE_OHM_PER_KM
        * distance_km
    )
    return 100 * loss_w / transferred_power_w


def plot_hvdc_cable_loss(output_path: Path) -> None:
    distances_km = np.linspace(0, 300, 301)

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for load_fraction in (0.50, 0.75, 1.00):
        ax.plot(
            distances_km,
            hvdc_conductor_loss_fraction(distances_km, load_fraction),
            linewidth=2,
            label=f"{load_fraction:.0%} of 2 GW",
        )

    reference_loss = float(hvdc_conductor_loss_fraction(np.array([80.0]), 1.0)[0])
    ax.axvline(80, color="#6b7280", linestyle="--", linewidth=1)
    ax.scatter([80], [reference_loss], color="#dc2626", zorder=3)
    ax.annotate(
        f"80 km base case: {reference_loss:.2f}%",
        xy=(80, reference_loss),
        xytext=(105, reference_loss + 0.08),
        arrowprops={"arrowstyle": "->", "color": "#6b7280"},
    )
    ax.set_title("525 kV Bipole Conductor Loss")
    ax.set_xlabel("Submarine route length [km]")
    ax.set_ylabel("Conductor loss [% of transferred power]")
    ax.set_xlim(0, 300)
    ax.set_ylim(bottom=0)
    ax.grid(True, color="#d1d5db", linewidth=0.8)
    ax.legend(title="Link loading")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    array_path = FIGURE_DIR / "array-string-count.svg"
    plot_array_string_count(array_path)
    print(f"Wrote {array_path.relative_to(PROJECT_ROOT)}")

    hvdc_path = FIGURE_DIR / "hvdc-cable-loss-vs-distance.svg"
    plot_hvdc_cable_loss(hvdc_path)
    print(f"Wrote {hvdc_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
