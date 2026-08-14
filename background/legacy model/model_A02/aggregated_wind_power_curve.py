# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 09:41:23 2026

@author: VictorVerbist
"""
# aggregated_wind_power_curve.py

# plot_spacing_sensitivity_curves.py
from __future__ import annotations

from dataclasses import replace
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import weibull_min
from scipy.interpolate import RegularGridInterpolator

from scenario_types import Design, Assumptions
from wind_calculations import compute_wind_pywake
from energy_calculations import (
    load_yaml,
    compression_power_kWh_per_kg,
    bop_loss_curve,
    generate_total_stack_efficiency_curve,
)


# =============================================================================
# Helpers
# =============================================================================

def get_directional_weibull_df(weibull_csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(weibull_csv_path).copy()
    df["freq"] = df["freq"].fillna(0.0)

    s = df["freq"].sum()
    if s <= 0:
        raise ValueError("Weibull CSV has zero total frequency.")
    df["freq"] = df["freq"] / s
    return df


def aggregated_weibull_distribution(
    assumptions: Assumptions,
    ws_plot: np.ndarray,
) -> pd.DataFrame:
    weibull_df = get_directional_weibull_df(assumptions.weibull_csv_path)

    pdf = np.zeros_like(ws_plot, dtype=float)
    for _, row in weibull_df.iterrows():
        p_dir = float(row["freq"])
        k = float(row["k"])
        c = float(row["c"])

        if p_dir <= 0 or np.isnan(k) or np.isnan(c):
            continue

        pdf += p_dir * weibull_min.pdf(ws_plot, k, loc=0, scale=c)

    return pd.DataFrame(
        {
            "ws_mps": ws_plot,
            "pdf": pdf,
            "hours_per_year_per_mps": pdf * 8760.0,
        }
    )


def aggregated_farm_power_curve(
    p_wd: np.ndarray,
    P_farm_kW_wd_ws: np.ndarray,
) -> np.ndarray:
    return (p_wd[:, None] * P_farm_kW_wd_ws).sum(axis=0)


def make_farm_power_function_from_table(
    wd: np.ndarray,
    ws: np.ndarray,
    Ptab_kW: np.ndarray,
):
    wd_arr = np.asarray(wd, dtype=float)
    ws_arr = np.asarray(ws, dtype=float)
    P_arr = np.asarray(Ptab_kW, dtype=float)

    wd_idx = np.argsort(wd_arr)
    ws_idx = np.argsort(ws_arr)

    wd_arr = wd_arr[wd_idx]
    ws_arr = ws_arr[ws_idx]
    P_arr = P_arr[np.ix_(wd_idx, ws_idx)]

    interp = RegularGridInterpolator(
        (wd_arr, ws_arr),
        P_arr,
        bounds_error=False,
        fill_value=0.0,
    )

    def farm_power(speed_mps, direction_deg):
        v = np.asarray(speed_mps, dtype=float)

        wd_val = np.asarray(direction_deg, dtype=float)
        if wd_val.ndim == 0:
            wd_val = np.full_like(v, float(wd_val))
        else:
            wd_val = np.broadcast_to(wd_val, v.shape).astype(float)

        pts = np.column_stack([wd_val.ravel(), v.ravel()])
        farm_kW = interp(pts).reshape(v.shape)
        return farm_kW / 1e3  # MW

    return farm_power


def spacingD_to_area_km2(num_turbines: int, spacing_D: float, rotor_diameter_km: float = 0.236) -> float:
    """
    Inverse of:
        spacing_D = sqrt(farm_area_km2 / (num_turbines * rotor_diameter_km^2))

    So:
        farm_area_km2 = num_turbines * spacing_D^2 * rotor_diameter_km^2
    """
    return float(num_turbines) * float(spacing_D) ** 2 * float(rotor_diameter_km) ** 2


def design_with_spacing(
    design: Design,
    spacing_D: float,
    rotor_diameter_km: float = 0.236,
) -> Design:
    farm_area_km2 = spacingD_to_area_km2(
        num_turbines=design.num_turbines,
        spacing_D=spacing_D,
        rotor_diameter_km=rotor_diameter_km,
    )

    return replace(design, farm_area_km2=farm_area_km2)


# =============================================================================
# Hydrogen curves
# =============================================================================

def hydrogen_curve_decentral(
    design: Design,
    yield_params: dict,
    farm_power_MW_vs_ws: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns:
        H2_farm_kgph vs ws
        stack_eff vs ws
    """
    if design.stack_overplant_factor is None or design.compressor_outlet_pressure_bar is None:
        raise ValueError("Decentral hydrogen requires stack_overplant_factor and compressor_outlet_pressure_bar")

    num_turbines = design.num_turbines
    turbine_capacity_MW = design.turbine_capacity_MW
    stack_size_MW = turbine_capacity_MW * design.stack_overplant_factor

    stack_eff_curve = generate_total_stack_efficiency_curve(stack_size_MW)

    hydrogen_decentral_electric_gain = yield_params["hydrogen_decentral_electric_gain"]
    comp_kWh_per_kg = compression_power_kWh_per_kg(
        design.compressor_outlet_pressure_bar,
        yield_params,
    )

    farm_power_kW = np.asarray(farm_power_MW_vs_ws, dtype=float) * 1e3
    turbine_production_kW = (farm_power_kW / num_turbines) * hydrogen_decentral_electric_gain

    bop_sp = turbine_production_kW / (turbine_capacity_MW * 1e3)
    bop_loss = np.clip(bop_loss_curve(bop_sp), 0.0, 1.0)

    stack_power_kW = turbine_production_kW * (1.0 - bop_loss)
    stack_sp = np.clip(stack_power_kW / (stack_size_MW * 1e3), 0.0, 1.0)
    stack_eff = stack_eff_curve(stack_sp)

    H2_turbine_kgph = stack_power_kW * 1000.0 * 3600.0 / 142e6 * stack_eff

    comp_power_kW = H2_turbine_kgph * comp_kWh_per_kg
    comp_loss = np.divide(
        comp_power_kW,
        stack_power_kW,
        out=np.zeros_like(comp_power_kW, dtype=float),
        where=stack_power_kW > 0,
    )
    comp_loss = np.clip(comp_loss, 0.0, 1.0)

    H2_turbine_kgph = H2_turbine_kgph * (1.0 - comp_loss)
    H2_farm_kgph = H2_turbine_kgph * num_turbines

    return H2_farm_kgph, stack_eff


def hydrogen_curve_central(
    design: Design,
    yield_params: dict,
    farm_power_MW_vs_ws: np.ndarray,
    stack_rating_MW: float,
) -> np.ndarray:
    if design.stack_overplant_factor is None or design.compressor_outlet_pressure_bar is None:
        raise ValueError("Central hydrogen requires stack_overplant_factor and compressor_outlet_pressure_bar")

    el_infield_eff = yield_params["electric_infield_efficiency"]
    h2_central_electric_efficiency = yield_params["hydrogen_central_electric_efficiency"]

    comp_kWh_per_kg = compression_power_kWh_per_kg(
        design.compressor_outlet_pressure_bar,
        yield_params,
    )

    stack_eff_curve = generate_total_stack_efficiency_curve(stack_rating_MW)

    farm_power_MW_gross = np.asarray(farm_power_MW_vs_ws, dtype=float)
    P_oss_MW = farm_power_MW_gross * el_infield_eff
    P_elx_kW = P_oss_MW * h2_central_electric_efficiency * 1e3

    bop_sp = P_elx_kW / (stack_rating_MW * 1e3)
    bop_loss = np.clip(bop_loss_curve(bop_sp), 0.0, 1.0)

    stack_power_kW = P_elx_kW * (1.0 - bop_loss)
    stack_sp = np.clip(stack_power_kW / (stack_rating_MW * 1e3), 0.0, 1.0)
    stack_eff = stack_eff_curve(stack_sp)

    H2_farm_kgph = stack_power_kW * 1000.0 * 3600.0 / 142e6 * stack_eff

    comp_power_kW = H2_farm_kgph * comp_kWh_per_kg
    comp_loss = np.divide(
        comp_power_kW,
        stack_power_kW,
        out=np.zeros_like(comp_power_kW, dtype=float),
        where=stack_power_kW > 0,
    )
    comp_loss = np.clip(comp_loss, 0.0, 1.0)

    H2_farm_kgph = H2_farm_kgph * (1.0 - comp_loss)
    return H2_farm_kgph


def determine_central_stack_rating_MW(
    design: Design,
    yield_params: dict,
    P_nowake_farm_MW_vs_ws: np.ndarray,
) -> float:
    el_infield_eff = yield_params["electric_infield_efficiency"]
    h2_central_electric_efficiency = yield_params["hydrogen_central_electric_efficiency"]

    P_elx_max_MW = np.max(
        P_nowake_farm_MW_vs_ws * el_infield_eff * h2_central_electric_efficiency
    )
    return P_elx_max_MW * float(design.stack_overplant_factor)


# =============================================================================
# Single run for one spacing
# =============================================================================

def run_one_spacing(
    design: Design,
    assumptions: Assumptions,
    yield_params: dict,
):
    weibull_df = get_directional_weibull_df(assumptions.weibull_csv_path)
    wd = weibull_df["sector_deg"].to_numpy(dtype=float)
    p_wd = weibull_df["freq"].to_numpy(dtype=float)

    _, art = compute_wind_pywake(design=design, assumptions=assumptions)

    ws = np.asarray(art["wind_ws"], dtype=float)
    wd_model = np.asarray(art["wind_wd"], dtype=float)

    if len(wd) != len(wd_model) or not np.allclose(wd, wd_model):
        raise ValueError("Weibull CSV sectors and PyWake sectors do not match.")

    P_wake_kW_wd_ws = np.asarray(art["pywake_farm_power_wake_kW"], dtype=float)
    P_nowake_kW_wd_ws = np.asarray(art["pywake_farm_power_nowake_kW"], dtype=float)

    P_wake_MW_vs_ws = aggregated_farm_power_curve(p_wd, P_wake_kW_wd_ws) / 1e3
    P_nowake_MW_vs_ws = aggregated_farm_power_curve(p_wd, P_nowake_kW_wd_ws) / 1e3

    if design.carrier == "hydrogen_decentral":
        H2_wake_kgph, stack_eff_wake = hydrogen_curve_decentral(
            design=design,
            yield_params=yield_params,
            farm_power_MW_vs_ws=P_wake_MW_vs_ws,
        )
        H2_nowake_kgph, stack_eff_nowake = hydrogen_curve_decentral(
            design=design,
            yield_params=yield_params,
            farm_power_MW_vs_ws=P_nowake_MW_vs_ws,
        )

    elif design.carrier == "hydrogen_central":
        stack_rating_MW = determine_central_stack_rating_MW(
            design=design,
            yield_params=yield_params,
            P_nowake_farm_MW_vs_ws=P_nowake_MW_vs_ws,
        )

        H2_wake_kgph, stack_eff_wake = hydrogen_curve_central(
            design=design,
            yield_params=yield_params,
            farm_power_MW_vs_ws=P_wake_MW_vs_ws,
            stack_rating_MW=stack_rating_MW,
        )
        H2_nowake_kgph, stack_eff_nowake = hydrogen_curve_central(
            design=design,
            yield_params=yield_params,
            farm_power_MW_vs_ws=P_nowake_MW_vs_ws,
            stack_rating_MW=stack_rating_MW,
        )

    else:
        raise ValueError("Use hydrogen_central or hydrogen_decentral for hydrogen plot.")

    out = pd.DataFrame(
        {
            "ws_mps": ws,
            "farm_power_wake_MW": P_wake_MW_vs_ws,
            "farm_power_nowake_MW": P_nowake_MW_vs_ws,
            "stack_eff_wake": stack_eff_wake,
            "stack_eff_nowake": stack_eff_nowake,
            "h2_wake_kgph": H2_wake_kgph,
            "h2_nowake_kgph": H2_nowake_kgph,
        }
    )
    return out


# =============================================================================
# Multi-spacing driver
# =============================================================================

def build_spacing_sensitivity(
    design: Design,
    assumptions: Assumptions,
    yield_params_path: str,
    spacings_D: list[float] = [3.0, 5.0, 7.0, 9.0],
    rotor_diameter_km: float = 0.236,
):
    yield_params = load_yaml(yield_params_path)

    results = {}

    for spacing_D in spacings_D:
        d_i = design_with_spacing(
            design=design,
            spacing_D=spacing_D,
            rotor_diameter_km=rotor_diameter_km,
        )
        results[spacing_D] = run_one_spacing(
            design=d_i,
            assumptions=assumptions,
            yield_params=yield_params,
        )

    ws_ref = results[spacings_D[0]]["ws_mps"].to_numpy()
    df_weibull = aggregated_weibull_distribution(assumptions, ws_ref)

    # stand-alone = no-wake line, same for all spacings in this setup
    df_standalone = results[spacings_D[0]][
        ["ws_mps", "farm_power_nowake_MW", "stack_eff_nowake", "h2_nowake_kgph"]
        ].copy()

    return df_weibull, results, df_standalone


# =============================================================================
# Plotting
# =============================================================================

def plot_spacing_sensitivity(
    df_weibull: pd.DataFrame,
    spacing_results: dict[float, pd.DataFrame],
    df_standalone: pd.DataFrame,
    title_prefix: str = "",
):
    fig, axes = plt.subplots(4, 1, figsize=(10, 18), sharex=True)

    # 1) Weibull distribution
    ax = axes[0]
    ax.plot(df_weibull["ws_mps"], df_weibull["hours_per_year_per_mps"], label="Weibull")
    ax.set_ylabel("Hours/year per m/s")
    ax.set_title(f"{title_prefix}Wind-speed distribution")
    ax.grid(True, alpha=0.3)
    ax.legend()

    # 2) Aggregated wind power curve
    ax = axes[1]
    for spacing_D, df in spacing_results.items():
        ax.plot(df["ws_mps"], df["farm_power_wake_MW"], label=f"{spacing_D:.0f}D")
    ax.plot(
        df_standalone["ws_mps"],
        df_standalone["farm_power_nowake_MW"],
        "--",
        linewidth=2.0,
        label="Stand-alone",
    )
    ax.set_ylabel("Farm power [MW]")
    ax.set_title(f"{title_prefix}Aggregated wind power curve")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Spacing")

    # 3) Stack efficiency curve
    ax = axes[2]
    for spacing_D, df in spacing_results.items():
        ax.plot(df["ws_mps"], df["stack_eff_wake"], label=f"{spacing_D:.0f}D")
    ax.plot(
        df_standalone["ws_mps"],
        df_standalone["stack_eff_nowake"],
        "--",
        linewidth=2.0,
        label="Stand-alone",
    )
    ax.set_ylabel("Stack efficiency [-]")
    ax.set_title(f"{title_prefix}Stack efficiency curve")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Spacing")

    # 4) Hydrogen production curve
    ax = axes[3]
    for spacing_D, df in spacing_results.items():
        ax.plot(df["ws_mps"], df["h2_wake_kgph"], label=f"{spacing_D:.0f}D")
    ax.plot(
        df_standalone["ws_mps"],
        df_standalone["h2_nowake_kgph"],
        "--",
        linewidth=2.0,
        label="Stand-alone",
    )
    ax.set_xlabel("Wind speed [m/s]")
    ax.set_ylabel("Hydrogen production [kg/h]")
    ax.set_title(f"{title_prefix}Hydrogen production curve")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Spacing")

    plt.tight_layout()
    plt.show()


# =============================================================================
# Example
# =============================================================================

if __name__ == "__main__":
    assumptions = Assumptions()

    design = Design(
        carrier="hydrogen_decentral",   # or "hydrogen_decentral"
        num_turbines=133,
        turbine_capacity_MW=15.0,
        farm_area_km2=200.0,          # overwritten by spacing loop
        stack_overplant_factor=1,
        compressor_outlet_pressure_bar=120.0,
    )

    yield_params_path = "yield_params.yaml"
    spacings_D = [3.0, 5.0, 7.0, 9.0]

    df_weibull, spacing_results, df_standalone = build_spacing_sensitivity(
        design=design,
        assumptions=assumptions,
        yield_params_path=yield_params_path,
        spacings_D=spacings_D,
        rotor_diameter_km=0.236,   # matches your formula
    )

    plot_spacing_sensitivity(
        df_weibull=df_weibull,
        spacing_results=spacing_results,
        df_standalone=df_standalone,
        title_prefix=f"{design.carrier} | {design.num_turbines} x {design.turbine_capacity_MW:.1f} MW | ",
    )