# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 13:47:58 2026

@author: VictorVerbist
"""

# visualise_turbine_grid_from_design.py

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import numpy as np

from wind_calculations import make_grid_layout
from scenario_types import Design


def get_rotated_farm_corners(
    num_turbines: int,
    farm_area_km2: float,
    orientation_deg_from_north: float,
):
    N = num_turbines

    nx = int(np.ceil(np.sqrt(N)))
    ny = int(np.ceil(N / nx))
    if nx < ny:
        nx, ny = ny, nx

    area_m2 = farm_area_km2 * 1e6
    Ly = np.sqrt(area_m2 * (ny / nx))
    Lx = area_m2 / Ly

    corners_uv = np.array([
        [0.0, -Ly / 2],
        [Lx, -Ly / 2],
        [Lx,  Ly / 2],
        [0.0,  Ly / 2],
    ])

    theta = np.deg2rad(orientation_deg_from_north)
    x = corners_uv[:, 0] * np.sin(theta) + corners_uv[:, 1] * np.cos(theta)
    y = corners_uv[:, 0] * np.cos(theta) - corners_uv[:, 1] * np.sin(theta)

    return np.column_stack([x, y]), Lx, Ly, nx, ny


def plot_layout_from_design(
    design: Design,
    orientation_deg_from_north: float,
    show_labels: bool = True,
    show_rotor: bool = True,
    save_path: str | None = None,
):
    x, y = make_grid_layout(
        num_turbines=design.num_turbines,
        rotor_diameter_m=design.rotor_diameter_m,
        farm_area_km2=design.farm_area_km2,
        orientation_deg_from_north=orientation_deg_from_north,
    )

    corners, Lx, Ly, nx, ny = get_rotated_farm_corners(
        num_turbines=design.num_turbines,
        farm_area_km2=design.farm_area_km2,
        orientation_deg_from_north=orientation_deg_from_north,
    )

    spacing_x = Lx / (nx - 1) if nx > 1 else Lx
    spacing_y = Ly / (ny - 1) if ny > 1 else Ly
    min_spacing_D = min(spacing_x, spacing_y) / design.rotor_diameter_m

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.add_patch(Polygon(corners, closed=True, fill=False, linewidth=2, linestyle="--"))
    ax.scatter(x, y, s=60, zorder=3)

    if show_rotor:
        r = design.rotor_diameter_m / 2
        for xi, yi in zip(x, y):
            ax.add_patch(Circle((xi, yi), r, fill=False, alpha=0.4))

    if show_labels:
        for i, (xi, yi) in enumerate(zip(x, y), start=1):
            ax.text(xi, yi, str(i), fontsize=8, ha="center", va="center")

    xmin, xmax = np.min(corners[:, 0]), np.max(corners[:, 0])
    ymin, ymax = np.min(corners[:, 1]), np.max(corners[:, 1])
    span = max(xmax - xmin, ymax - ymin)
    pad = 0.15 * span

    ax.set_title(
        f"Turbine Grid Layout\n"
        f"N={design.num_turbines}, D={design.rotor_diameter_m:.1f} m, "
        f"Area={design.farm_area_km2:.2f} km², Orientation={orientation_deg_from_north:.1f}°\n"
        f"Grid={nx} x {ny}, spacing≈({spacing_x:.0f} m, {spacing_y:.0f} m), min spacing={min_spacing_D:.2f}D"
    )
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(xmin - pad, xmax + pad)
    ax.set_ylim(ymin - pad, ymax + pad)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved figure to {save_path}")

    plt.show()
    
    
if __name__ == "__main__":
    # Example inputs
    num_turbines = 132
    rotor_diameter_m = 180.0
    farm_area_km2 = 200
    orientation_deg_from_north = 30.0

    d = Design(
        carrier='electricity',
        num_turbines=num_turbines,
        turbine_capacity_MW=15,
        farm_area_km2=farm_area_km2,
    )
    
    plot_layout_from_design(d, orientation_deg_from_north)