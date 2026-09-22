"""Build the electrical-infrastructure figures used by the Quarto site.

Run manually when the reference cable assumptions change:

    python tools/build_electrical_figures.py

The figure inputs come from model_data/inputs.csv. The HVDC figure shows
conductor I^2R loss only; converter, transformer, accessory, land-cable and
temperature effects are deliberately excluded and are discussed on the page.
"""

from decimal import Decimal
from pathlib import Path
import sys

import matplotlib
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from model_data import hvdc_conductor_loss, load_parameters

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "offshore-wind-infrastructure-model"
import matplotlib.pyplot as plt


FIGURE_DIR = PROJECT_ROOT / "figures"
PARAMETERS = load_parameters()

TURBINE_RATING_MW = float(
    PARAMETERS.number("wind-turbine-rated-power", "MW")
)
USABLE_STRING_RATING_MW = float(
    PARAMETERS.number("array-usable-string-rating", "MW")
)
TURBINES_PER_STRING = int(USABLE_STRING_RATING_MW // TURBINE_RATING_MW)

HVDC_RATING_GW = float(PARAMETERS.number("hvdc-link-rated-power", "GW"))
HVDC_RATING_MW = HVDC_RATING_GW * 1_000
HVDC_POLE_VOLTAGE_KV = float(PARAMETERS.number("hvdc-pole-voltage", "kV"))
HVDC_REFERENCE_ROUTE_KM = float(
    PARAMETERS.number("hvdc-reference-route-length", "km")
)
ARRAY_REFERENCE_TARGET_GW = float(
    PARAMETERS.number("array-reference-target-power", "GW")
)


def save_svg(fig: plt.Figure, output_path: Path) -> None:
    """Write deterministic SVG without generator-added trailing whitespace."""

    fig.savefig(output_path, metadata={"Date": None})
    svg = output_path.read_text(encoding="utf-8")
    output_path.write_text(
        "\n".join(line.rstrip() for line in svg.splitlines()) + "\n",
        encoding="utf-8",
    )


def plot_array_string_count(output_path: Path) -> None:
    turbine_count = np.arange(1, 201)
    plant_capacity_mw = turbine_count * TURBINE_RATING_MW
    string_count = np.ceil(turbine_count / TURBINES_PER_STRING)

    reference_turbines = int(
        np.ceil(ARRAY_REFERENCE_TARGET_GW * 1_000 / TURBINE_RATING_MW)
    )
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
        label=(
            f"Nominal {ARRAY_REFERENCE_TARGET_GW:g} GW target: "
            f"{reference_turbines} turbines, {reference_strings} strings"
        ),
    )
    ax.set_title("Discrete 66 kV Array-String Requirement")
    ax.set_xlabel("Installed turbine capacity [MW]")
    ax.set_ylabel("Required radial strings [-]")
    ax.set_xlim(0, 3_000)
    ax.set_ylim(bottom=0)
    ax.grid(True, color="#d1d5db", linewidth=0.8)
    ax.legend(loc="upper left")
    fig.tight_layout()
    save_svg(fig, output_path)
    plt.close(fig)


def hvdc_conductor_loss_fraction(
    distance_km: np.ndarray, load_fraction: float
) -> np.ndarray:
    return np.array(
        [
            float(
                hvdc_conductor_loss(
                    PARAMETERS,
                    Decimal(str(distance)),
                    Decimal(str(load_fraction)),
                )[1]
                * 100
            )
            for distance in distance_km
        ]
    )


def plot_hvdc_cable_loss(output_path: Path) -> None:
    distances_km = np.linspace(0, 300, 301)

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for load_fraction in (0.50, 0.75, 1.00):
        ax.plot(
            distances_km,
            hvdc_conductor_loss_fraction(distances_km, load_fraction),
            linewidth=2,
            label=f"{load_fraction:.0%} of {HVDC_RATING_GW:g} GW",
        )

    reference_loss = float(
        hvdc_conductor_loss_fraction(np.array([HVDC_REFERENCE_ROUTE_KM]), 1.0)[0]
    )
    ax.axvline(
        HVDC_REFERENCE_ROUTE_KM,
        color="#6b7280",
        linestyle="--",
        linewidth=1,
    )
    ax.scatter(
        [HVDC_REFERENCE_ROUTE_KM], [reference_loss], color="#dc2626", zorder=3
    )
    ax.annotate(
        f"{HVDC_REFERENCE_ROUTE_KM:g} km base case: {reference_loss:.2f}%",
        xy=(HVDC_REFERENCE_ROUTE_KM, reference_loss),
        xytext=(HVDC_REFERENCE_ROUTE_KM + 25, reference_loss + 0.08),
        arrowprops={"arrowstyle": "->", "color": "#6b7280"},
    )
    ax.set_title(f"{HVDC_POLE_VOLTAGE_KV:g} kV Bipole Conductor Loss")
    ax.set_xlabel("Submarine route length [km]")
    ax.set_ylabel("Conductor loss [% of transferred power]")
    ax.set_xlim(0, 300)
    ax.set_ylim(bottom=0)
    ax.grid(True, color="#d1d5db", linewidth=0.8)
    ax.legend(title="Link loading")
    fig.tight_layout()
    save_svg(fig, output_path)
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
