# -*- coding: utf-8 -*-
"""

energy_calculations.py

Energy-related calculations for wind, electricity and hydrogen.

Created on Fri Nov 14 15:45:14 2025

@author: Victor
"""

# energy_calculations.py
from __future__ import annotations
import yaml
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Any
from math import ceil
from scipy.stats import weibull_min
from scipy.interpolate import interp1d
from CoolProp.CoolProp import PropsSI

from scipy.interpolate import RegularGridInterpolator


from scenario_types import Assumptions, Design, Derived

def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return yaml.load(f, Loader=yaml.SafeLoader)

def make_wind_farm_power(design: Design, artifacts: Any):
    """
    Returns a callable wind_farm_power(speed_mps, direction_deg) -> farm_power_MW.

    Uses PyWake farm-level power table (wd, ws) stored in artifacts.
    Raises if wake data is missing.
    """

    # --- enforce presence of wake-aware table
    Ptab = getattr(artifacts, "pywake_farm_power_wake_kW", None)
    wd = getattr(artifacts, "wind_wd", None)
    ws = getattr(artifacts, "wind_ws", None)

    if Ptab is None or wd is None or ws is None:
        raise ValueError(
            "PyWake farm power table missing in artifacts. "
            "Wind must be computed before hydrogen/electric yields."
        )

    wd_arr = np.asarray(wd, dtype=float)
    ws_arr = np.asarray(ws, dtype=float)
    P_arr = np.asarray(Ptab, dtype=float)  # farm-level kW, shape (n_wd, n_ws)

    # Ensure axes are sorted (required for RegularGridInterpolator)
    wd_idx = np.argsort(wd_arr)
    ws_idx = np.argsort(ws_arr)

    wd_arr = wd_arr[wd_idx]
    ws_arr = ws_arr[ws_idx]
    P_arr = P_arr[np.ix_(wd_idx, ws_idx)]

    wake_power_interp = RegularGridInterpolator(
        (wd_arr, ws_arr),
        P_arr,
        bounds_error=False,
        fill_value=0.0,
    )

    def wind_farm_power(speed_mps, direction_deg):
        v = np.asarray(speed_mps, dtype=float)

        wd_val = np.asarray(direction_deg, dtype=float)
        if wd_val.ndim == 0:
            wd_val = np.full_like(v, float(wd_val))
        else:
            wd_val = np.broadcast_to(wd_val, v.shape).astype(float)

        pts = np.column_stack([wd_val.ravel(), v.ravel()])
        farm_kW = wake_power_interp(pts).reshape(v.shape)

        return farm_kW / 1e3  # return MW

    return wind_farm_power


def compression_power_kWh_per_kg(outlet_pressure_bar: float, yield_params: Dict[str, Any]) -> float:
    inlet_pressure_bar = 30
    M = 2 * 1.008
    R = 8.314
    R_s = R / M * 1000
    k = 1.41
    T_K = 298.0
    max_compression_ratio = 3.3

    isothermal_efficiency = yield_params["compressor_isothermal_efficiency"]
    electric_efficiency = yield_params["compressor_electric_efficiency"]

    P_in = inlet_pressure_bar * 1e5
    P_out = outlet_pressure_bar * 1e5

    Z_in  = PropsSI('Z', "T", T_K, "P", float(P_in),  "Hydrogen")
    Z_out = PropsSI('Z', "T", T_K, "P", float(P_out), "Hydrogen")
    Z_avg = (Z_in + Z_out) / 2

    num_stages = ceil(np.log(P_out / P_in) / np.log(max_compression_ratio))

    E_thermo_Jpkg = (
        num_stages
        * k / (k - 1)
        * (Z_avg / isothermal_efficiency)
        * T_K * R_s
        * ((P_out / P_in) ** ((k - 1) / (num_stages * k)) - 1)
    )
    E_thermo_kWhpkg = E_thermo_Jpkg / 3.6e6
    return E_thermo_kWhpkg / electric_efficiency

def bop_loss_curve(load):
    a5, a4, a3, a2, a1, a0 = -1.135, 3.603, -4.440, 2.686, -0.818, 0.116
    water_treatment_loss = 0.002
    tsa_loss = 0.01
    load_array = np.array(load, ndmin=1, dtype=float)
    y_array = a5*load_array**5 + a4*load_array**4 + a3*load_array**3 + a2*load_array**2 + a1*load_array + a0
    y_array += water_treatment_loss + tsa_loss
    valid_mask = (load_array >= 0.095) & (load_array <= 1.01)
    result = np.where(valid_mask, y_array, 0)
    return float(result[0]) if result.size == 1 else result

def single_stack_efficiency_curve(load):
    a3, a2, a1, a0 = -0.1445, 0.3548, -0.4289, 0.9907
    load_array = np.array(load, ndmin=1, dtype=float)
    valid_mask = (load_array >= 0.095) & (load_array <= 1.01)
    efficiency = np.where(valid_mask, a3*load_array**3 + a2*load_array**2 + a1*load_array + a0, 0)
    return float(efficiency[0]) if efficiency.size == 1 else efficiency

def generate_total_stack_efficiency_curve(MW, stack_module_size=2.5):
    MW_module = stack_module_size
    num_stacks = ceil(MW / MW_module)
    sp_elx = np.arange(101) / 100.0
    sp_elx_stack = sp_elx[:, None] * MW / (np.arange(1, 1 + num_stacks)[None, :]) / MW_module
    eff_elx_stack = single_stack_efficiency_curve(sp_elx_stack)
    eff_elx = np.max(eff_elx_stack, axis=1)
    return interp1d(sp_elx, eff_elx, kind="linear", fill_value=(0, 0), bounds_error=False)

# --- add near other helpers (e.g., after generate_total_stack_efficiency_curve) ---

def stack_degradation_linear_multiplier(
    flh_per_year: float,
    d_per_1000: float,
    lifetime_years: float = 25.0,
) -> Dict[str, float]:
    """
    Linear degradation approximation.

    d_per_1000: fractional degradation after 1000 full-load hours (e.g., 0.01 for 1%).
    flh_per_year: full-load hours per year (based on expected loading).

    Returns dict with:
      - deg_eol_frac: degradation fraction at end of life
      - mult_avg: average production multiplier over lifetime (1 - deg_eol/2)
      - mult_eol: end-of-life production multiplier (1 - deg_eol)
      - flh_life: lifetime full-load hours
    """
    flh_life = float(flh_per_year) * float(lifetime_years)
    deg_eol = float(d_per_1000) * (flh_life / 1000.0)
    deg_eol = float(np.clip(deg_eol, 0.0, 1.0))

    mult_eol = 1.0 - deg_eol
    mult_avg = 1.0 - 0.5 * deg_eol  # linear ramp 0 -> deg_eol

    return {
        "flh_life": flh_life,
        "deg_eol_frac": deg_eol,
        "mult_eol": mult_eol,
        "mult_avg": mult_avg,
    }


def hydrogen_chain_decentral_from_weibull(
    design: Design,
    assumptions: Assumptions,
    artifacts: Any,
    yield_params: Dict[str, Any],
    v_max: float = 40.0,
    dv: float = 0.25,
    hours_per_year: float = 8760.0,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    v_bins = np.arange(0, v_max + dv, dv)
    v_mid = 0.5 * (v_bins[:-1] + v_bins[1:])

    if design.stack_overplant_factor is None or design.compressor_outlet_pressure_bar is None:
        raise ValueError("Hydrogen scenarios require stack_overplant_factor and compressor_outlet_pressure_bar")

    num_turbines = design.num_turbines
    turbine_capacity_MW = design.turbine_capacity_MW
    stack_size_MW = design.turbine_capacity_MW *  design.stack_overplant_factor

    stack_eff_curve = generate_total_stack_efficiency_curve(stack_size_MW)

    hydrogen_decentral_electric_gain = yield_params["hydrogen_decentral_electric_gain"]
    comp_kWh_per_kg = compression_power_kWh_per_kg(design.compressor_outlet_pressure_bar, yield_params)

    weibull_df = pd.read_csv(assumptions.weibull_csv_path)
    wind_farm_power = make_wind_farm_power(design, artifacts)
    
    state_records = []
    for _, row in weibull_df.iterrows():
        sector_deg = row["sector_deg"]
        p_dir = row["freq"]
        k = row["k"]
        c = row["c"]
        if p_dir == 0 or np.isnan(k) or np.isnan(c):
            continue

        F_edges = weibull_min.cdf(v_bins, k, loc=0, scale=c)
        p_speed_bins = np.diff(F_edges)
        p_joint = p_dir * p_speed_bins
        if np.all(p_joint == 0):
            continue

        
        farm_power_MW = wind_farm_power(v_mid, sector_deg)
        farm_power_kW = farm_power_MW * 1e3

        turbine_production_kW = (farm_power_kW / num_turbines) * hydrogen_decentral_electric_gain

        bop_sp = turbine_production_kW / (turbine_capacity_MW * 1e3)
        bop_loss = bop_loss_curve(bop_sp).clip(None, 1.0)
        stack_power_kW = turbine_production_kW * (1.0 - bop_loss)

        stack_sp = np.clip(stack_power_kW / (stack_size_MW * 1e3), 0, 1)
        stack_eff = stack_eff_curve(stack_sp)

        H2_turbine_kgph = stack_power_kW * 1000 * 3600 / 142e6 * stack_eff

        comp_power_kW = H2_turbine_kgph * comp_kWh_per_kg
        comp_loss = np.divide( comp_power_kW, stack_power_kW, out=np.zeros_like(comp_power_kW, dtype=float), where=stack_power_kW > 0)
        comp_loss = np.clip(comp_loss, 0.0, 1.0)

        H2_turbine_kgph *= (1 - comp_loss)
        H2_farm_kgph = H2_turbine_kgph * num_turbines

        for i in range(len(v_mid)):
            if p_joint[i] == 0:
                continue
            state_records.append({
                "sector_deg": sector_deg,
                "speed_mps": v_mid[i],
                "prob": p_joint[i],
                "farm_power_MW": farm_power_MW[i],
                "turbine_prod_kW": turbine_production_kW[i],
                "bop_sp": bop_sp[i],
                "bop_loss": bop_loss[i],
                "stack_power_kW": stack_power_kW[i],
                "stack_sp": stack_sp[i],
                "stack_eff": stack_eff[i],
                "compressor_turbine_power_kW": comp_power_kW[i],
                "H2_turbine_kgph": H2_turbine_kgph[i],
                "H2_farm_kgph": H2_farm_kgph[i],
            })

    states_df = pd.DataFrame.from_records(state_records)
    total_prob = states_df["prob"].sum()
    if total_prob > 0:
        states_df["prob"] /= total_prob

    def expectation(col):
        return (states_df[col] * states_df["prob"]).sum()

    summary_rows = []
    flow_vars = ["farm_power_MW", "stack_power_kW", "H2_farm_kgph", "compressor_turbine_power_kW"]
    frac_vars = ["bop_sp", "bop_loss", "stack_sp", "stack_eff"]

    for var in flow_vars:
        exp_val = expectation(var)
        annual = exp_val * hours_per_year
        max_val = states_df[var].max()
        summary_rows.append({"variable": var, "expected": exp_val, "annual": annual, "max": max_val})

    for var in frac_vars:
        exp_val = expectation(var)
        max_val = states_df[var].max()
        summary_rows.append({"variable": var, "expected": exp_val, "annual": np.nan, "max": max_val})

    summary_df = pd.DataFrame(summary_rows).set_index("variable")
    return states_df, summary_df

def hydrogen_chain_central_from_weibull(
    design: Design,
    assumptions: Assumptions,
    artifacts: Any,
    yield_params: Dict[str, Any],
    v_max: float = 40.0,
    dv: float = 0.25,
    hours_per_year: float = 8760.0,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Central hydrogen: electric chain to OSS, then central electrolysis.

    - Apply electric multipliers up to OSS to farm power
    - Size stack by stack_overplant_factor * P_oss_max
    - Do BOP/stack/compression at farm level
    """
    if design.stack_overplant_factor is None or design.compressor_outlet_pressure_bar is None:
        raise ValueError("hydrogen_central requires stack_overplant_factor and compressor_outlet_pressure_bar")

    v_bins = np.arange(0, v_max + dv, dv)
    v_mid = 0.5 * (v_bins[:-1] + v_bins[1:])

    num_turbines = design.num_turbines
    
    # power arriving at OSS (MW)
    el_infield_eff = yield_params["electric_infield_efficiency"]
    h2_central_electric_efficiency = yield_params["hydrogen_central_electric_efficiency"]

    # compression
    comp_kWh_per_kg = compression_power_kWh_per_kg(design.compressor_outlet_pressure_bar, yield_params)

    weibull_df = pd.read_csv(assumptions.weibull_csv_path)
    wind_farm_power = make_wind_farm_power(design, artifacts)

    state_records = []
    for _, row in weibull_df.iterrows():
        sector_deg = row["sector_deg"]
        p_dir = row["freq"]
        k = row["k"]
        c = row["c"]
        if p_dir == 0 or np.isnan(k) or np.isnan(c):
            continue

        F_edges = weibull_min.cdf(v_bins, k, loc=0, scale=c)
        p_speed_bins = np.diff(F_edges)
        p_joint = p_dir * p_speed_bins
        if np.all(p_joint == 0):
            continue

        # farm gross power (before el multipliers)
        farm_power_MW_gross = wind_farm_power(v_mid, sector_deg)

        # power arriving at elx (MW), efficiency only
        P_oss_MW = farm_power_MW_gross * el_infield_eff 
        P_oss_kW = P_oss_MW * 1e3


        # --- size stack based on global P_oss_max (we need it, but do it per-sector binning)
        # We'll store P_oss_kW now; stack_rating computed later after we collect states.
        # For now we compute conversion assuming stack_rating will be set in a second pass.
        for i in range(len(v_mid)):
            if p_joint[i] == 0:
                continue
            state_records.append({
                "sector_deg": sector_deg,
                "speed_mps": v_mid[i],
                "prob": p_joint[i],
                "farm_power_MW_gross": farm_power_MW_gross[i],
                "P_oss_MW": P_oss_MW[i],
                "P_oss_kW": P_oss_kW[i],
            })

    df0 = pd.DataFrame.from_records(state_records)
    if df0.empty:
        return df0, pd.DataFrame()

    # normalize probs
    total_prob = df0["prob"].sum()
    if total_prob > 0:
        df0["prob"] /= total_prob

    # stack sizing
    
    P_elx_kW = df0['P_oss_kW'] * h2_central_electric_efficiency
    
    P_elx_max_MW = P_elx_kW.max() / 1e3
    stack_rating_MW = P_elx_max_MW * float(design.stack_overplant_factor)

    # curves
    stack_eff_curve = generate_total_stack_efficiency_curve(stack_rating_MW)

    # BOP + stack + compression at farm level
    # BOP setpoint relative to OSS power vs rating (for curve usage)
    bop_sp = P_elx_kW.to_numpy() / (stack_rating_MW * 1e3)
    bop_loss = bop_loss_curve(bop_sp).clip(None, 1.0)
    stack_power_kW = P_elx_kW.to_numpy() * (1.0 - bop_loss)

    stack_sp = np.clip(stack_power_kW / (stack_rating_MW * 1e3), 0, 1)
    stack_eff = stack_eff_curve(stack_sp)

    H2_farm_kgph = stack_power_kW * 1000 * 3600 / 142e6 * stack_eff

    comp_power_kW = H2_farm_kgph * comp_kWh_per_kg
    comp_loss = np.divide( comp_power_kW, stack_power_kW, out=np.zeros_like(comp_power_kW, dtype=float), where=stack_power_kW > 0)
    comp_loss = np.clip(comp_loss, 0.0, 1.0)
    H2_farm_kgph = H2_farm_kgph * (1 - comp_loss)

    out = df0.copy()
    out["stack_rating_MW"] = stack_rating_MW
    out["bop_sp"] = bop_sp
    out["bop_loss"] = bop_loss
    out["stack_power_kW"] = stack_power_kW
    out["stack_sp"] = stack_sp
    out["stack_eff"] = stack_eff
    out["compressor_power_kW"] = comp_power_kW
    out["H2_farm_kgph"] = H2_farm_kgph

    def expectation(col):
        return float((out[col] * out["prob"]).sum())

    summary_rows = []
    flow_vars = ["P_oss_MW", "stack_power_kW", "H2_farm_kgph", "compressor_power_kW"]
    frac_vars = ["bop_sp", "bop_loss", "stack_sp", "stack_eff"]

    for var in flow_vars:
        exp_val = expectation(var)
        annual = exp_val * hours_per_year
        max_val = float(out[var].max())
        summary_rows.append({"variable": var, "expected": exp_val, "annual": annual, "max": max_val})

    for var in frac_vars:
        exp_val = expectation(var)
        max_val = float(out[var].max())
        summary_rows.append({"variable": var, "expected": exp_val, "annual": np.nan, "max": max_val})

    summary_df = pd.DataFrame(summary_rows).set_index("variable")
    summary_df.loc["P_oss_max_MW", "max"] = df0['P_oss_kW'].max() / 1e3
    summary_df.loc["stack_rating_MW", "max"] = stack_rating_MW

    return out, summary_df





def compute_electric_yields(
    design: Design,
    derived: Derived,
    yield_params: Dict[str, Any],
) -> None:
    """
    Sets:
      - derived.electric_yield_farm_MWh  (annual yield: eff * avail)
      - derived.P_oss_max_MW             (peak at OSS: efficiency only, no availability)
    """
    if derived.turbine_gross_yield_MWh is None:
        raise ValueError("derived.turbine_gross_yield_MWh missing (run wind first)")

    gross_per_turb_MWh = float(derived.turbine_gross_yield_MWh)
    N = int(design.num_turbines)

    # --- annual yield: efficiencies + availabilities (explicit)
    eff = (
        yield_params["electric_infield_efficiency"]
        * yield_params["electric_export_efficiency"]
    )
    avail = (
        yield_params["electric_turbine_availability"]
        * yield_params["electric_infield_availability"]
        * yield_params["electric_export_availability"]
    )

    per_turb_net_MWh = gross_per_turb_MWh * eff * avail
    derived.electric_yield_farm_MWh = per_turb_net_MWh * N

    # --- peak at OSS: efficiency only (no availability)
    # "electric chain to OSS" => apply infield efficiency only (export is after OSS)
    nameplate_farm_MW = float(design.num_turbines * design.turbine_capacity_MW)
    derived.P_oss_max_MW = nameplate_farm_MW * float(yield_params["electric_infield_efficiency"])


def compute_hydrogen_decentral_yields(
    design: Design,
    assumptions: Assumptions,
    derived: Derived,
    artifacts: Any,
    yield_params: Dict[str, Any],
) -> None:
    """
    Decentral hydrogen:
      - The chain computes physical power/flows and peak values (NO availability).
      - Annual export yield applies export/infield efficiencies + availabilities explicitly.
    """
    states_df, summary_df = hydrogen_chain_decentral_from_weibull(design, assumptions, artifacts, yield_params)

    artifacts.h2_states = states_df
    artifacts.h2_summary = summary_df

    # physical (no availability) expected H2 at turbine-level chain output, aggregated at farm
    H2_kgph_expected = float(summary_df.loc["H2_farm_kgph", "expected"])
    derived.h2_elx_yield_kg_year = H2_kgph_expected * 8760.0
    
    # --- STACK DEGRADATION (linear approximation) ---
    d_1000 = float(yield_params.get("stack_degradation_per_1000hrs", 0.0) or 0.0)
    if d_1000 > 0:
        # expected stack power at farm
        P_stack_kW_exp_farm = float(summary_df.loc["stack_power_kW", "expected"])
        # per turbine expected stack power
        P_stack_kW_exp_turb = P_stack_kW_exp_farm / float(design.num_turbines)

        # stack rating per turbine (MW -> kW)
        stack_size_MW = float(design.turbine_capacity_MW * design.stack_overplant_factor)
        stack_rating_kW_turb = stack_size_MW * 1e3

        flh_per_year = 0.0
        if stack_rating_kW_turb > 0:
            flh_per_year = (P_stack_kW_exp_turb / stack_rating_kW_turb) * 8760.0

        deg = stack_degradation_linear_multiplier(flh_per_year, d_1000, lifetime_years=25.0)

        # apply avg multiplier to annual physical yield
        h2_elx_bol = derived.h2_elx_yield_kg_year
        derived.h2_elx_yield_kg_year = h2_elx_bol * deg["mult_avg"]

        # diagnostics (optional but useful)
        derived.stack_flh_per_year = float(flh_per_year)
        derived.stack_deg_eol_frac = float(deg["deg_eol_frac"])
        derived.stack_deg_mult_avg = float(deg["mult_avg"])
        derived.stack_deg_mult_eol = float(deg["mult_eol"])
        derived.h2_elx_lifetime_lost_kg = float(h2_elx_bol * 25.0 * (1.0 - deg["mult_avg"]))
    
    # annual export yield: efficiency + availability (explicit)
    h2_eff = (
        yield_params["hydrogen_infield_efficiency"]
        * yield_params["hydrogen_export_efficiency"]
    )
    h2_avail = (
        yield_params["hydrogen_turbine_availability"]
        * yield_params["hydrogen_infield_availability"]
        * yield_params["hydrogen_export_availability"]
    )

    derived.h2_export_kg_year = derived.h2_elx_yield_kg_year * h2_eff * h2_avail
    derived.h2_export_MWh = derived.h2_export_kg_year * assumptions.HHV_kWh_per_kg / 1000.0

    # peaks: from chain only (no availability)
    derived.H2_export_capacity_kgph = float(summary_df.loc["H2_farm_kgph", "max"])
    derived.elx_export_capacity_MW = float(summary_df.loc["stack_power_kW", "max"]) / 1e3
    derived.compressor_turbine_power_kW_max = float(summary_df.loc["compressor_turbine_power_kW", "max"])

    # diagnostics
    derived.stack_sp_expected = float(summary_df.loc["stack_sp", "expected"])

    # weighted efficiencies
    df = states_df
    den = float((df["stack_power_kW"] * df["prob"]).sum())
    if den > 0:
        derived.stack_eff1 = float((df["stack_eff"] * df["stack_power_kW"] * df["prob"]).sum() / den)
        mask_on = df["stack_sp"] >= 0.095
        den_on = float((df.loc[mask_on, "stack_power_kW"] * df.loc[mask_on, "prob"]).sum())
        if den_on > 0:
            derived.stack_eff2 = float((df.loc[mask_on, "stack_eff"] * df.loc[mask_on, "stack_power_kW"] * df.loc[mask_on, "prob"]).sum() / den_on)


def compute_hydrogen_central_yields(
    design: Design,
    assumptions: Assumptions,
    derived: Derived,
    artifacts: Any,
    yield_params: Dict[str, Any],
) -> None:
    """
    Central hydrogen:
      - Chain computes P_oss with electric infield efficiency only (NO availability) and then central electrolysis.
      - Annual export yield applies:
          electric availabilities up to OSS (annual only)
          hydrogen export efficiency + availability (annual only)
      - Peak sizing uses efficiency-only chain maxima.
    """
    states_df, summary_df = hydrogen_chain_central_from_weibull(design, assumptions, artifacts, yield_params)
    artifacts.h2_states = states_df
    artifacts.h2_summary = summary_df

    # physical (no availability) expected H2 at chain output
    H2_kgph_expected = float(summary_df.loc["H2_farm_kgph", "expected"])
    derived.h2_elx_yield_kg_year = H2_kgph_expected * 8760.0
    
    # --- STACK DEGRADATION (linear approximation) ---
    d_1000 = float(yield_params.get("stack_degradation_per_1000hrs", 0.0) or 0.0)
    if d_1000 > 0:
        # expected stack power at farm
        P_stack_kW_exp = float(summary_df.loc["stack_power_kW", "expected"])

        # stack rating at farm level (MW -> kW)
        stack_rating_MW = float(states_df["stack_rating_MW"].iloc[0]) if "stack_rating_MW" in states_df.columns else float(summary_df.loc["stack_rating_MW", "max"])
        stack_rating_kW = stack_rating_MW * 1e3

        flh_per_year = 0.0
        if stack_rating_kW > 0:
            flh_per_year = (P_stack_kW_exp / stack_rating_kW) * 8760.0

        deg = stack_degradation_linear_multiplier(flh_per_year, d_1000, lifetime_years=25.0)

        h2_elx_bol = derived.h2_elx_yield_kg_year
        derived.h2_elx_yield_kg_year = h2_elx_bol * deg["mult_avg"]

        derived.stack_flh_per_year = float(flh_per_year)
        derived.stack_deg_eol_frac = float(deg["deg_eol_frac"])
        derived.stack_deg_mult_avg = float(deg["mult_avg"])
        derived.stack_deg_mult_eol = float(deg["mult_eol"])
        derived.h2_elx_lifetime_lost_kg = float(h2_elx_bol * 25.0 * (1.0 - deg["mult_avg"]))
    
    # annual: apply availability to the electric part up to OSS (annual only)
    el_avail_to_oss = (
        yield_params["electric_turbine_availability"]
        * yield_params["electric_infield_availability"]
    )

    # annual: export pipeline efficiency + availability (annual only)
    h2_export_eff = float(yield_params["hydrogen_export_efficiency"])
    h2_export_avail = float(yield_params["hydrogen_export_availability"])

    derived.h2_export_kg_year = derived.h2_elx_yield_kg_year * el_avail_to_oss * h2_export_eff * h2_export_avail
    derived.h2_export_MWh = derived.h2_export_kg_year * assumptions.HHV_kWh_per_kg / 1000.0

    # peaks: from chain only (no availability)
    derived.P_oss_max_MW = float(summary_df.loc["P_oss_MW", "max"])
    derived.elx_export_capacity_MW = float(summary_df.loc["stack_power_kW", "max"]) / 1e3
    derived.compressor_turbine_power_kW_max = float(summary_df.loc["compressor_power_kW", "max"])
    derived.H2_export_capacity_kgph = float(summary_df.loc["H2_farm_kgph", "max"])

    # diagnostics
    derived.stack_sp_expected = float(summary_df.loc["stack_sp", "expected"]) if "stack_sp" in summary_df.index else None

