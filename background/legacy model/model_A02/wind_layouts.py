# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 13:59:49 2026

@author: VictorVerbist

farm_config_sweep.py

Sweep over wind farm configurations and calculate:
- turbine production
- farm production
- capacity factor
- wake losses
- layout spacing metrics

Uses helper functions from wind_calculations.py.

"""


from __future__ import annotations

import itertools
from dataclasses import asdict, replace
from typing import Iterable, Optional

import numpy as np
import pandas as pd

from py_wake.deficit_models import TurboNOJDeficit
from py_wake.deficit_models.no_wake import NoWakeDeficit
from py_wake.wind_farm_models.engineering_models import PropagateDownwind
from py_wake.superposition_models import SquaredSum
from py_wake.rotor_avg_models.area_overlap_model import AreaOverlapAvgModel

from wind_calculations import (
    build_site_from_weibull_csv,
    build_turbine_from_design,
)
from scenario_types import Assumptions, Design, Derived, Artifacts


def make_grid_layout_rectangular(
    num_turbines: int,
    rotor_diameter_m: float,
    farm_area_km2: float,
    orientation_deg_from_north: float,
    squareness: float,
) -> tuple[np.ndarray, np.ndarray, dict]:
    """
    Create a grid layout inside a rectangular area.

    squareness is defined as:
        squareness = Lx / Ly

    So:
        squareness = 1.0 -> square
        squareness = 2.0 -> wide rectangle
        squareness = 0.5 -> tall rectangle
    """
    N = int(num_turbines)
    D = float(rotor_diameter_m)
    area_m2 = float(farm_area_km2) * 1e6
    ar = float(squareness)

    if N <= 0:
        raise ValueError("num_turbines must be > 0")
    if D <= 0:
        raise ValueError("rotor_diameter_m must be > 0")
    if area_m2 <= 0:
        raise ValueError("farm_area_km2 must be > 0")
    if ar <= 0:
        raise ValueError("squareness must be > 0")

    # Rectangle dimensions from:
    # Lx * Ly = area_m2
    # Lx / Ly = ar
    Lx = np.sqrt(area_m2 * ar)
    Ly = np.sqrt(area_m2 / ar)

    # Choose grid counts roughly matching aspect ratio
    nx = int(np.ceil(np.sqrt(N * ar)))
    ny = int(np.ceil(N / nx))

    while nx * ny < N:
        ny += 1

    if nx < 1:
        nx = 1
    if ny < 1:
        ny = 1

    spacing_x = Lx / (nx - 1) if nx > 1 else Lx
    spacing_y = Ly / (ny - 1) if ny > 1 else Ly

    u = np.linspace(0.0, Lx, nx)
    v = np.linspace(-(Ly / 2.0), (Ly / 2.0), ny)

    uu, vv = np.meshgrid(u, v)
    u_flat = uu.ravel()[:N]
    v_flat = vv.ravel()[:N]

    theta = np.deg2rad(orientation_deg_from_north)

    # Keep the same rotation convention as your original script
    x = u_flat * np.sin(theta) + v_flat * np.cos(theta)
    y = u_flat * np.cos(theta) - v_flat * np.sin(theta)

    meta = {
        "Lx_m": Lx,
        "Ly_m": Ly,
        "nx": nx,
        "ny": ny,
        "spacing_x_m": spacing_x,
        "spacing_y_m": spacing_y,
        "spacing_x_D": spacing_x / D,
        "spacing_y_D": spacing_y / D,
        "min_spacing_D": min(spacing_x, spacing_y) / D,
        "squareness": ar,
    }

    return x, y, meta


def compute_wind_pywake_rectangular(
    design: Design,
    assumptions: Assumptions,
    orientation_deg_from_north: float,
    squareness: float,
) -> tuple[Derived, Artifacts, dict]:
    """
    Same idea as compute_wind_pywake(), but with a rectangular/squareness-controlled layout.
    """
    site, wd = build_site_from_weibull_csv(
        weibull_csv_path=assumptions.weibull_csv_path,
        ti_default=assumptions.ti_default,
    )

    wt = build_turbine_from_design(design)

    x, y, layout_meta = make_grid_layout_rectangular(
        num_turbines=design.num_turbines,
        rotor_diameter_m=design.rotor_diameter_m,
        farm_area_km2=design.farm_area_km2,
        orientation_deg_from_north=orientation_deg_from_north,
        squareness=squareness,
    )

    ws = np.arange(0.0, 30.5, 0.5)

    wfm = PropagateDownwind(
        site=site,
        windTurbines=wt,
        wake_deficitModel=TurboNOJDeficit(),
        rotorAvgModel=AreaOverlapAvgModel(),
        superpositionModel=SquaredSum(),
    )
    sim_res = wfm(x=x, y=y, wd=wd, ws=ws)

    wfm_single = PropagateDownwind(
        site=site,
        windTurbines=wt,
        wake_deficitModel=NoWakeDeficit(),
        superpositionModel=SquaredSum(),
    )
    sim_res_single = wfm_single(x=[0], y=[0], wd=wd, ws=ws)

    aep_GWh = float(sim_res.aep().sum())
    farm_AEP_MWh = aep_GWh * 1e3

    aep_single_GWh = float(sim_res_single.aep().sum())
    aep_single_MWh = aep_single_GWh * 1e3
    farm_AEP_no_wake_MWh = aep_single_MWh * design.num_turbines

    wake_loss_frac = 1.0 - farm_AEP_MWh / farm_AEP_no_wake_MWh
    farm_capacity_MW = design.num_turbines * design.turbine_capacity_MW
    farm_cf = farm_AEP_MWh / (farm_capacity_MW * 8760.0)

    # Per-turbine gross from your current convention
    turbine_gross_yield_MWh = farm_AEP_MWh / design.num_turbines

    P_wake_farm_kW = sim_res.Power.sum(dim="wt").values / 1e3
    P_nowake_1t_kW = sim_res_single.Power.sum(dim="wt").values / 1e3
    P_nowake_farm_kW = P_nowake_1t_kW * design.num_turbines

    wake_eff_wd_ws = np.divide(
        P_wake_farm_kW,
        P_nowake_farm_kW,
        out=np.ones_like(P_wake_farm_kW),
        where=P_nowake_farm_kW > 0,
    )
    wake_eff_wd_ws = np.clip(wake_eff_wd_ws, 0.0, 1.0)

    d = Derived(
        layout_x=x,
        layout_y=y,
        wind_wd=wd,
        wind_ws=ws,
        farm_AEP_MWh=farm_AEP_MWh,
        farm_AEP_no_wake_MWh=farm_AEP_no_wake_MWh,
        wake_loss_frac=wake_loss_frac,
        farm_cf=farm_cf,
        turbine_gross_yield_MWh=turbine_gross_yield_MWh,
    )

    art = Artifacts(
        layout_x=x,
        layout_y=y,
        wind_wd=wd,
        wind_ws=ws,
        pywake_farm_power_wake_kW=P_wake_farm_kW,
        pywake_farm_power_nowake_kW=P_nowake_farm_kW,
        pywake_wake_eff_wd_ws=wake_eff_wd_ws,
    )

    return d, art, layout_meta


def _safe_float(x: Optional[float]) -> float:
    return np.nan if x is None else float(x)


def build_summary_row(
    design: Design,
    assumptions: Assumptions,
    derived: Derived,
    layout_meta: dict,
    orientation_deg_from_north: float,
    squareness: float,
) -> dict:
    """
    Convert one evaluated configuration to a flat summary row.
    """
    farm_capacity_MW = design.num_turbines * design.turbine_capacity_MW

    farm_AEP_MWh = _safe_float(derived.farm_AEP_MWh)
    farm_AEP_no_wake_MWh = _safe_float(derived.farm_AEP_no_wake_MWh)
    wake_loss_frac = _safe_float(derived.wake_loss_frac)
    farm_cf = _safe_float(derived.farm_cf)
    turbine_net_yield_MWh = (
        farm_AEP_MWh / design.num_turbines if design.num_turbines > 0 else np.nan
    )
    turbine_no_wake_yield_MWh = (
        farm_AEP_no_wake_MWh / design.num_turbines if design.num_turbines > 0 else np.nan
    )

    row = {
        "scenario_id": design.scenario_id(),
        "carrier": design.carrier,
        "num_turbines": design.num_turbines,
        "turbine_capacity_MW": design.turbine_capacity_MW,
        "farm_capacity_MW": farm_capacity_MW,
        "farm_area_km2": design.farm_area_km2,
        "orientation_deg_from_north": orientation_deg_from_north,
        "assumptions_layout_orientation_deg_from_north": assumptions.layout_orientation_deg_from_north,
        "squareness": squareness,
        "farm_AEP_MWh": farm_AEP_MWh,
        "farm_AEP_GWh": farm_AEP_MWh / 1e3,
        "farm_AEP_no_wake_MWh": farm_AEP_no_wake_MWh,
        "farm_AEP_no_wake_GWh": farm_AEP_no_wake_MWh / 1e3,
        "wake_loss_frac": wake_loss_frac,
        "wake_loss_pct": 100.0 * wake_loss_frac,
        "farm_cf": farm_cf,
        "farm_cf_pct": 100.0 * farm_cf,
        "turbine_net_yield_MWh": turbine_net_yield_MWh,
        "turbine_no_wake_yield_MWh": turbine_no_wake_yield_MWh,
        "Lx_m": layout_meta["Lx_m"],
        "Ly_m": layout_meta["Ly_m"],
        "nx": layout_meta["nx"],
        "ny": layout_meta["ny"],
        "spacing_x_m": layout_meta["spacing_x_m"],
        "spacing_y_m": layout_meta["spacing_y_m"],
        "spacing_x_D": layout_meta["spacing_x_D"],
        "spacing_y_D": layout_meta["spacing_y_D"],
        "min_spacing_D": layout_meta["min_spacing_D"],
    }
    return row


def sweep_farm_configurations(
    base_design: Design,
    assumptions: Assumptions,
    num_turbines_list: Iterable[int],
    farm_area_km2_list: Iterable[float],
    orientation_list: Iterable[float],
    squareness_list: Iterable[float],
    keep_artifacts: bool = False,
) -> tuple[pd.DataFrame, list[dict]]:
    """
    Sweep over farm configurations.

    Returns
    -------
    df_summary : pd.DataFrame
        Flat table with performance metrics for each configuration.
    records : list[dict]
        Each entry contains:
            - design
            - assumptions
            - derived
            - artifacts (optional, if keep_artifacts=True)
            - layout_meta
    """
    rows = []
    records = []

    combinations = list(itertools.product(
        num_turbines_list,
        farm_area_km2_list,
        orientation_list,
        squareness_list,
    ))

    print(f"Running {len(combinations)} configurations...")

    for i, (num_turbines, farm_area_km2, orientation, squareness) in enumerate(combinations, start=1):
        print(
            f"[{i}/{len(combinations)}] "
            f"N={num_turbines}, A={farm_area_km2} km2, "
            f"orientation={orientation} deg, squareness={squareness}"
        )

        design_i = replace(
            base_design,
            num_turbines=int(num_turbines),
            farm_area_km2=float(farm_area_km2),
        )

        try:
            derived_i, artifacts_i, layout_meta_i = compute_wind_pywake_rectangular(
                design=design_i,
                assumptions=assumptions,
                orientation_deg_from_north=float(orientation),
                squareness=float(squareness),
            )

            row = build_summary_row(
                design=design_i,
                assumptions=assumptions,
                derived=derived_i,
                layout_meta=layout_meta_i,
                orientation_deg_from_north=float(orientation),
                squareness=float(squareness),
            )
            rows.append(row)

            rec = {
                "design": design_i,
                "assumptions": assumptions,
                "derived": derived_i,
                "layout_meta": layout_meta_i,
            }
            if keep_artifacts:
                rec["artifacts"] = artifacts_i
            records.append(rec)

        except Exception as e:
            rows.append({
                "scenario_id": design_i.scenario_id(),
                "carrier": design_i.carrier,
                "num_turbines": design_i.num_turbines,
                "farm_area_km2": design_i.farm_area_km2,
                "orientation_deg_from_north": float(orientation),
                "squareness": float(squareness),
                "error": str(e),
            })

    df = pd.DataFrame(rows)
    return df, records


def add_rankings(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    if "farm_AEP_MWh" in out.columns:
        out["rank_AEP"] = out["farm_AEP_MWh"].rank(ascending=False, method="min")

    if "farm_cf" in out.columns:
        out["rank_CF"] = out["farm_cf"].rank(ascending=False, method="min")

    if "wake_loss_frac" in out.columns:
        out["rank_wake_loss"] = out["wake_loss_frac"].rank(ascending=True, method="min")

    return out


if __name__ == "__main__":
    # ------------------------------------------------------------------
    # BASE INPUTS
    # ------------------------------------------------------------------

    assumptions = Assumptions(
        weibull_csv_path="weibull_per_sector.csv",
        ti_default=0.058,
        layout_orientation_deg_from_north=30.0,
    )

    base_design = Design(
        carrier="electricity",
        num_turbines=25,
        turbine_capacity_MW=15.0,
        farm_area_km2=25.0,
        v_in=3.0,
        v_rated=12.0,
        v_out=25.0,
        rotor_diameter_m=236.0,
        hub_height_m=150.0,
    )

    # ------------------------------------------------------------------
    # SWEEP DEFINITIONS
    # ------------------------------------------------------------------

    num_turbines_list = [16, 25, 36, 49]
    farm_area_km2_list = [15.0, 20.0, 25.0, 30.0]
    orientation_list = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0]
    squareness_list = [0.5, 0.75, 1.0, 1.5, 2.0]

    # ------------------------------------------------------------------
    # RUN
    # ------------------------------------------------------------------

    df_summary, records = sweep_farm_configurations(
        base_design=base_design,
        assumptions=assumptions,
        num_turbines_list=num_turbines_list,
        farm_area_km2_list=farm_area_km2_list,
        orientation_list=orientation_list,
        squareness_list=squareness_list,
        keep_artifacts=False,
    )

    df_summary = add_rankings(df_summary)

    if "farm_AEP_MWh" in df_summary.columns:
        df_summary = df_summary.sort_values("farm_AEP_MWh", ascending=False)

    df_summary.to_csv("farm_config_sweep_results.csv", index=False)

    cols_show = [
        "scenario_id",
        "num_turbines",
        "farm_area_km2",
        "orientation_deg_from_north",
        "squareness",
        "farm_capacity_MW",
        "farm_AEP_GWh",
        "farm_AEP_no_wake_GWh",
        "farm_cf_pct",
        "wake_loss_pct",
        "turbine_net_yield_MWh",
        "min_spacing_D",
        "spacing_x_D",
        "spacing_y_D",
        "rank_AEP",
        "rank_CF",
        "rank_wake_loss",
    ]
    cols_show = [c for c in cols_show if c in df_summary.columns]

    print("\nTop 20 configurations by AEP:")
    print(df_summary[cols_show].head(20).to_string(index=False))

    print("\nSaved results to farm_config_sweep_results.csv")
    
#%%

import hub_optimisation.analysis_functions as af
import matplotlib.pyplot as plt

df = df_summary.copy()

#%%

af.plot_best_y_for_x(df, 'orientation_deg_from_north', 'farm_cf', 'farm_AEP_MWh',agg='max')

af.plot_best_y_for_x(df, 'squareness', 'orientation_deg_from_north', 'farm_AEP_MWh',agg='max')

















