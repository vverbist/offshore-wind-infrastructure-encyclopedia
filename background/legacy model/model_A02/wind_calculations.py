# -*- coding: utf-8 -*-
"""
wind_calculations.py

Created on Mon Nov 17 15:15:22 2025

@author: VictorVerbist
"""
# wind_calculations.py
import numpy as np
import pandas as pd
from py_wake.site import UniformWeibullSite
from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
from py_wake.deficit_models import TurboNOJDeficit
from py_wake.deficit_models.no_wake import NoWakeDeficit
from py_wake.wind_farm_models.engineering_models import PropagateDownwind
from py_wake.superposition_models import SquaredSum
from py_wake.rotor_avg_models.area_overlap_model import AreaOverlapAvgModel

from scenario_types import Assumptions, Design, Derived

def build_site_from_weibull_csv(
    weibull_csv_path: str,
    ti_default: float,
) -> tuple[UniformWeibullSite, np.ndarray]:
    df = pd.read_csv(weibull_csv_path)

    k = df["k"].fillna(2.0).to_numpy()
    a = df["c"].fillna(1.0).to_numpy()
    p_wd = df["freq"].fillna(0.0).to_numpy()

    s = p_wd.sum()
    if s > 0:
        p_wd = p_wd / s

    site = UniformWeibullSite(p_wd=p_wd, a=a, k=k, ti=ti_default)
    wd = df["sector_deg"].to_numpy()
    return site, wd

def build_turbine_from_design(design: Design) -> WindTurbine:
    ws = np.arange(0.0, 35.1, 0.5)
    power_kw = np.zeros_like(ws)
    ct = np.zeros_like(ws)

    v_in = design.v_in
    v_r = design.v_rated
    v_out = design.v_out
    p_rated_kw = design.turbine_capacity_MW * 1e3

    ramp_mask = (ws >= v_in) & (ws < v_r)
    if ramp_mask.any():
        power_kw[ramp_mask] = np.linspace(0.0, p_rated_kw, ramp_mask.sum())
    power_kw[ws >= v_r] = p_rated_kw
    power_kw[ws >= v_out] = 0.0

    ct[(ws >= v_in) & (ws < v_out)] = 0.8
    ct[ws >= v_out] = 0.0

    return WindTurbine(
        name="ScenarioWT",
        diameter=design.rotor_diameter_m,
        hub_height=design.hub_height_m,
        powerCtFunction=PowerCtTabular(ws, power_kw, "kW", ct),
    )

def make_grid_layout(
    num_turbines: int,
    rotor_diameter_m: float,
    farm_area_km2: float,
    orientation_deg_from_north: float,
) -> tuple[np.ndarray, np.ndarray]:
    N = num_turbines
    D = rotor_diameter_m

    nx = int(np.ceil(np.sqrt(N)))
    ny = int(np.ceil(N / nx))
    if nx < ny:
        nx, ny = ny, nx

    area_m2 = farm_area_km2 * 1e6
    Ly = np.sqrt(area_m2 * (ny / nx))
    Lx = area_m2 / Ly

    spacing_x = Lx / (nx - 1) if nx > 1 else Lx
    spacing_y = Ly / (ny - 1) if ny > 1 else Ly

    min_spacing_D = min(spacing_x, spacing_y) / D
    if min_spacing_D < 3.0:
        print(f"WARNING: Turbine spacing = {min_spacing_D:.2f}D < 3D minimum threshold.")

    u = np.linspace(0, Lx, nx)
    v = np.linspace(-(Ly / 2), (Ly / 2), ny)

    uu, vv = np.meshgrid(u, v)
    u_flat = uu.ravel()[:N]
    v_flat = vv.ravel()[:N]

    theta = np.deg2rad(orientation_deg_from_north)
    x = u_flat * np.sin(theta) + v_flat * np.cos(theta)
    y = u_flat * np.cos(theta) - v_flat * np.sin(theta)
    return x, y

def compute_wind_pywake(design: Design, assumptions: Assumptions) -> tuple[Derived, dict]:

    site, wd = build_site_from_weibull_csv(
        weibull_csv_path=assumptions.weibull_csv_path,
        ti_default=assumptions.ti_default,
    )

    wt = build_turbine_from_design(design)
    x, y = make_grid_layout(
        num_turbines=design.num_turbines,
        rotor_diameter_m=design.rotor_diameter_m,
        farm_area_km2=design.farm_area_km2,
        orientation_deg_from_north=assumptions.layout_orientation_deg_from_north,
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
    aep_GWh = float(sim_res.aep().sum())
    farm_AEP_MWh = aep_GWh * 1e3

    wfm_single = PropagateDownwind(
        site=site,
        windTurbines=wt,
        wake_deficitModel=NoWakeDeficit(),
        superpositionModel=SquaredSum(),
    )
    sim_res_single = wfm_single(x=[0], y=[0], wd=wd, ws=ws)
    aep_single_GWh = float(sim_res_single.aep().sum())
    farm_AEP_no_wake_MWh = aep_single_GWh * 1e3 * design.num_turbines

    wake_loss_frac = 1.0 - farm_AEP_MWh / farm_AEP_no_wake_MWh
    
    

    
    d = Derived()
    d.layout_x = x
    d.layout_y = y
    d.wind_wd = wd
    d.wind_ws = ws
    d.farm_AEP_MWh = farm_AEP_MWh
    d.farm_AEP_no_wake_MWh = farm_AEP_no_wake_MWh
    d.wake_loss_frac = wake_loss_frac

    farm_capacity_MW = design.num_turbines * design.turbine_capacity_MW
    d.farm_cf = farm_AEP_MWh / (farm_capacity_MW * 8760.0)
    d.turbine_gross_yield_MWh = farm_AEP_MWh / design.num_turbines
    
    
    # Farm power tables from pywake. sim_res.Power is in [W] 
    P_wake_farm_kW = sim_res.Power.sum(dim="wt").values / 1e3 # (n_wd, n_ws)

    # No-wake farm power: single turbine sim, multiply by N
    P_nowake_1t_kW = sim_res_single.Power.sum(dim="wt").values / 1e3  # often (n_wd, n_ws) even for one turbine
    P_nowake_farm_kW = P_nowake_1t_kW * design.num_turbines

    wake_eff_wd_ws = np.divide(
        P_wake_farm_kW,
        P_nowake_farm_kW,
        out=np.ones_like(P_wake_farm_kW),
        where=P_nowake_farm_kW > 0,
    )
    wake_eff_wd_ws = np.clip(wake_eff_wd_ws, 0.0, 1.0)

    art = {
        "pywake_farm_power_wake_kW": P_wake_farm_kW,
        "pywake_farm_power_nowake_kW": P_nowake_farm_kW,
        "pywake_wake_eff_wd_ws": wake_eff_wd_ws,
        "wind_wd": wd,
        "wind_ws": ws,
        "layout_x": x,
        "layout_y": y,
    }
    
    return d, art
