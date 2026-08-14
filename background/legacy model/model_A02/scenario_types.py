# -*- coding: utf-8 -*-
"""
scenario_types.py

Created on Mon Feb 16 15:58:03 2026

@author: VictorVerbist
"""
# scenario_types.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import hashlib, json

@dataclass(frozen=True)
class Assumptions:
    weibull_csv_path: str = "weibull_per_sector.csv"
    yield_params_path: str = "yield_params.yaml"
    finance_params_path: str = "finance_params.yaml"
    infra_params_path: str = "infra_params.yaml"
    turbine_params_path: str = "turbine_params.yaml"
    hydrogen_params_path: str = "hydrogen_params.yaml"

    ti_default: float = 0.058
    layout_orientation_deg_from_north: float = 30.0
    HHV_kWh_per_kg: float = 39.44

@dataclass(frozen=True)
class Design:
    carrier: str  # "electricity" | "hydrogen_central" | "hydrogen_decentral"
    num_turbines: int
    turbine_capacity_MW: float
    farm_area_km2: float

    stack_overplant_factor: Optional[float] = None
    compressor_outlet_pressure_bar: Optional[float] = None
    export_pipeline_diameter_inch: Optional[float] = None

    v_in: float = 3.0
    v_rated: float = 12.0
    v_out: float = 25.0

    rotor_diameter_m: float = 236.0
    hub_height_m: float = 150.0

    def scenario_id(self) -> str:
        payload = asdict(self)
        s = json.dumps(payload, sort_keys=True)
        h = hashlib.md5(s.encode("utf-8")).hexdigest()[:8]
        return f"{self.carrier}_nt{self.num_turbines}_tc{self.turbine_capacity_MW:g}_A{self.farm_area_km2:g}_{h}"


@dataclass
class Artifacts:
    # heavy objects (store to disk; don't try to JSON-serialize)
    h2_states: Optional[Any] = None       # pandas df
    h2_summary: Optional[Any] = None      # pandas df
    layout_x: Optional[Any] = None        # np array
    layout_y: Optional[Any] = None        # np array
    wind_wd: Optional[Any] = None         # np array
    wind_ws: Optional[Any] = None         # np array
    
    pywake_farm_power_wake_kW: Optional[Any] = None     # np.ndarray (n_wd, n_ws)
    pywake_farm_power_nowake_kW: Optional[Any] = None   # np.ndarray (n_wd, n_ws) (farm-level)
    pywake_wake_eff_wd_ws: Optional[Any] = None         # np.ndarray (n_wd, n_ws)
    
    costs_breakdown : Optional[Any] = None


@dataclass
class Derived:
    # wind
    layout_x: Optional[Any] = None
    layout_y: Optional[Any] = None
    wind_wd: Optional[Any] = None
    wind_ws: Optional[Any] = None
    farm_AEP_MWh: Optional[float] = None
    farm_AEP_no_wake_MWh: Optional[float] = None
    wake_loss_frac: Optional[float] = None
    farm_cf: Optional[float] = None
    turbine_gross_yield_MWh: Optional[float] = None

    # yields
    electric_yield_farm_MWh: Optional[float] = None
    h2_states: Optional[Any] = None
    h2_summary: Optional[Any] = None
    h2_elx_yield_kg_year: Optional[float] = None
    h2_export_kg_year: Optional[float] = None
    h2_export_MWh: Optional[float] = None
    H2_export_capacity_kgph: Optional[float] = None
    elx_export_capacity_MW: Optional[float] = None
    compressor_turbine_power_kW_max: Optional[float] = None

    # infrastructure
    infield_horizontal_cable_length_m: Optional[float] = None
    infield_vertical_cable_length_m: Optional[float] = None
    infield_total_cable_length_m: Optional[float] = None

    infield_horizontal_pipeline_length_m: Optional[float] = None
    infield_vertical_pipeline_length_m: Optional[float] = None
    infield_total_pipeline_length_m: Optional[float] = None

    export_capacity_MW: Optional[float] = None
    P_oss_max_MW : Optional[float] = None
    num_export_pipelines: Optional[int] = None

    # nice-to-have hydrogen metrics
    stack_sp_expected: Optional[float] = None
    stack_eff1: Optional[float] = None
    stack_eff2: Optional[float] = None
    
    stack_flh_per_year: Optional[float] = None
    stack_deg_eol_frac: Optional[float] = None
    stack_deg_mult_avg: Optional[float] = None
    stack_deg_mult_eol: Optional[float] = None
    h2_elx_lifetime_lost_kg: Optional[float] = None

@dataclass
class Results:
    costs_flat: Optional[Dict[str, float]] = None
    costs_breakdown_flat :  Optional[Dict[str, float]] = None
    total_LCOE: Optional[float] = None
    total_capex_EUR: Optional[float] = None
    total_annual_capex_EUR_per_year: Optional[float] = None
    total_annual_opex_EUR_per_year: Optional[float] = None
    total_annual_cost_EUR_per_year: Optional[float] = None
