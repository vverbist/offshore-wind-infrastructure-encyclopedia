# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 13:49:28 2025

@author: VictorVerbist
"""
import yaml
import pandas as pd
import numpy as np
from math import ceil, floor
from scipy.interpolate import interp1d
from scipy.stats import weibull_min
from CoolProp.CoolProp import PropsSI


def wind_production_timeseries(  ):
    excel_file = "WRA+H2-E_victor.xlsx"
    df = pd.read_excel(excel_file,sheet_name='WRA',usecols='A:S')
    turbine_production = df['P1']
    
    return turbine_production


    

def compute_hydrogen_from_weibull(
   
    wind_farm_power,
    scn,
    v_max=40.0,
    dv=0.25,
    hours_per_year=8760,
    save_states_path="hydrogen_states.parquet",
    save_summary_path="hydrogen_summary.csv",
):
    """
    Integrate wind -> power -> hydrogen chain over Weibull-per-sector distribution.

    params_df : DataFrame
        Columns: sector_deg, freq, k, c (from Weibull fitting).
    wind_farm_power : function(speed_mps, direction_deg) -> power_MW
        Should accept numpy arrays for speed and scalar direction, return MW (farm total).
    turbine_power_MW : float
        Rated power per turbine [MW].
    num_turbines : int
        Number of turbines in the farm.
    stack_size_MW : float
        Rated electrolyzer capacity per turbine [MW] or per “arrangement”
        (consistent with how you used it in hydrogen_production_elx).
    comp_eff : float
        Compression efficiency factor (0–1).
    electric_gain : float
        Electric gain factor (>0).
    v_max : float
        Max wind speed considered [m/s].
    dv : float
        Bin width for integration [m/s].
    hours_per_year : float
        Typically 8760.
    save_states_path : str or None
        If not None, save detailed per-(sector,speed) states as parquet.
    save_summary_path : str or None
        If not None, save summary metrics as CSV.

    Returns
    -------
    states_df : DataFrame
        Detailed states over (sector, speed bin) with probabilities and chain values.
    summary_df : DataFrame
        Summary of expected, annual and max values for key variables.
    """
    # 0. Unpack scn
    
    num_turbines        = scn['num_turbines']
    turbine_capacity_MW = scn['turbine_capcity_MW']
    
    stack_size_MW       = scn['stack_size_MW']
    
    compression_energy_kWhpkg  = scn['compression_energy_kWhpkg']

    with open('yield_params.yaml', 'r') as f : 
        yield_params = yaml.load(f,Loader=yaml.SafeLoader)
    hydrogen_electric_gain = yield_params['hydrogen_electric_gain']


    # 1. Speed bins
    v_bins = np.arange(0, v_max + dv, dv)
    v_mid = 0.5 * (v_bins[:-1] + v_bins[1:])  # midpoints
    n_bins = len(v_mid)

    # 2. Precompute stack efficiency curve (same for all sectors)
    stack_eff_curve = generate_total_stack_efficiency_curve(stack_size_MW)

    # 3. Collect all states for later inspection & aggregation
    state_records = []

    weibull_params_df = pd.read_csv("weibull_per_sector.csv")
    for _, row in weibull_params_df.iterrows():
        sector_deg = row["sector_deg"]
        p_dir = row["freq"]
        k = row["k"]
        c = row["c"]

        # Skip invalid / empty sectors
        if p_dir == 0 or np.isnan(k) or np.isnan(c):
            continue

        # 3a. Probabilities over speed for this sector (conditional on direction)
        F_edges = weibull_min.cdf(v_bins, k, loc=0, scale=c)
        p_speed_bins = np.diff(F_edges)  # length n_bins

        # 3b. Joint probability of (sector, speed)
        p_joint = p_dir * p_speed_bins   # length n_bins

        # If there is zero probability mass (shouldn't happen but be safe)
        if np.all(p_joint == 0):
            continue

        # 3c. Farm power at these speeds for this direction (MW)
        farm_power_MW = wind_farm_power(v_mid, sector_deg)  # array length n_bins

        # 3d. Turbine production in kW (total farm)
        farm_power_kW = farm_power_MW * 1e3  # MW -> kW
        
        turbine_production_kW = farm_power_kW / num_turbines
        
        turbine_production_kW *= hydrogen_electric_gain

        # 3e. BOP chain (vectorized, lifted from your hydrogen_production_elx)
        #     - BOP setpoint (fraction of rated)
        bop_sp = turbine_production_kW / (turbine_capacity_MW * 1e3)
        bop_loss = bop_loss_curve(bop_sp).clip(None, 1.0)   # fraction loss
        #     - Power to stack(s) after BOP [kW]
        stack_power_kW = turbine_production_kW * (1.0 - bop_loss)

        # 3f. Stack setpoint and efficiency
        stack_sp = stack_power_kW / (stack_size_MW * 1e3 )
        stack_eff = stack_eff_curve(stack_sp)  # 0–1 fraction

        # 3g. Hydrogen production rate [kg/h]
        #     From your formula: stack_power*1000 * 3600 / 142e6 * stack_eff
        #     stack_power in kW -> *1000 = W; *3600 = J/h; 142e6 J/kg -> kg/h
        H2_turbine_kgph = stack_power_kW * 1000 * 3600 / 142e6 * stack_eff
        # some of that energy had to be used for compression
        comp_power_kW = H2_turbine_kgph * compression_energy_kWhpkg # kg/h * kWh/kg = kW
        comp_loss = comp_power_kW / turbine_production_kW
        H2_turbine_kgph *= ( 1 - comp_loss )

        H2_farm_kgph = H2_turbine_kgph * num_turbines

        # 3h. Store state records
        for i in range(n_bins):
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
          #      "stack_power_kW": stack_power_kW[i],
                "stack_sp": stack_sp[i],
                "stack_eff": stack_eff[i],
          #     "compression_power_kW": comp_power_kW,
                "H2_turbine_kgph": H2_turbine_kgph[i],
                "H2_farm_kgph": H2_farm_kgph[i],
            })

    # 4. Build DataFrame of all states
    states_df = pd.DataFrame.from_records(state_records)

    # Safety check: normalize probabilities if needed
    total_prob = states_df["prob"].sum()
    if total_prob > 0:
        states_df["prob"] /= total_prob

    # 5. Compute expectation, annual, max for key variables
    def expectation(col):
        return (states_df[col] * states_df["prob"]).sum()

    summary_rows = []

    # "Flow-like" variables: annual = expectation * hours_per_year
    flow_vars = ["farm_power_MW", "H2_kgph"]
    for var in flow_vars:
        exp_val = expectation(var)
        annual = exp_val * hours_per_year
        max_val = states_df[var].max()
        summary_rows.append({
            "variable": var,
            "expected": exp_val,
            "annual": annual,
            "max": max_val,
        })

    # Dimensionless / fractional variables: annual not really meaningful,
    # so we store NaN or leave as None.
    frac_vars = ["bop_sp", "bop_loss", "stack_sp", "stack_eff"]
    for var in frac_vars:
        exp_val = expectation(var)
        max_val = states_df[var].max()
        summary_rows.append({
            "variable": var,
            "expected": exp_val,
            "annual": np.nan,  # or exp_val if you prefer
            "max": max_val,
        })

    summary_df = pd.DataFrame(summary_rows).set_index("variable")

    # 6. Save to disk if requested
    if save_states_path is not None:
        states_df.to_parquet(save_states_path, index=False)
        print(f"[INFO] Saved hydrogen chain states to {save_states_path}")

    if save_summary_path is not None:
        summary_df.to_csv(save_summary_path)
        print(f"[INFO] Saved hydrogen chain summary to {save_summary_path}")

    return states_df, summary_df




def bop_loss_curve( load ):
    """
    Computes the Balance-of-Plant (BOP) efficiency curve for input(s) `load`
    using a polynomial model plus a water treatment and TSA loss.

    The polynomial is valid for setpoints approximately in [0.095, 1.01].
    Values outside this range will be forced to zero.

    TODO: source of data/method

    Parameters
    ----------
    load : float or array-like
        Turbine setpoint (or array of setpoints), in [0,1] range typically.

    Returns
    -------
    float or ndarray
        BOP loss values. If `load` is a single scalar, a single float is returned;
        if `load` is an array-like, an ndarray of floats is returned.
    """
    a5, a4, a3, a2, a1, a0 = -1.135, 3.603, -4.440, 2.686, -0.818, 0.116
    water_treatment_loss = 0.002
    tsa_loss = 0.01
    
    # Convert input to a NumPy array (at least 1D):
    load_array = np.array(load, ndmin=1, dtype=float)
    
    y_array = a5*load_array**5 + a4*load_array**4 + a3*load_array**3 + a2*load_array**2 + a1*load_array + a0
    y_array += water_treatment_loss + tsa_loss
    
    # Create a boolean mask for where 0.1 <= load <= 1.0
    valid_mask = (load_array >= 0.095) & (load_array <= 1.01)
    
    # Vectorized computation
    result = np.where(valid_mask, y_array, 0)
    
    # If the original input was a single scalar, return a scalar
    if result.size == 1:
        return float(result[0])  # or result.item()
    return result


def single_stack_efficiency_curve( load ):
    """
    Computes the single-stack efficiency curve for input(s) `load` using a 
    cubic polynomial model. Values outside [0.095, 1.01] are set to 0.

    Parameters
    ----------
    load : float or array-like
        The fraction of rated power (setpoint) for a single electrolyzer stack,
        typically in [0,1].

    Returns
    -------
    efficiency : float or ndarray
        Stack efficiency values in fraction (0-1). If `load` is a single scalar, 
        a single float is returned; if `load` is array-like, an ndarray is returned.
    """
    a3, a2, a1, a0 = -0.1445, 0.3548, -0.4289, 0.9907
    
    # Convert input to a NumPy array (at least 1D):
    load_array = np.array(load, ndmin=1, dtype=float)
    
    # Create a boolean mask for where 0.1 <= load <= 1.0
    valid_mask = (load_array >= 0.095) & (load_array <= 1.01)
    
    # Vectorized computation
    efficiency = np.where(valid_mask, a3*load_array**3 + a2*load_array**2 + a1*load_array + a0, 0)
    
    # If the original input was a single scalar, return a scalar
    if efficiency.size == 1:
        return float(efficiency[0])  # or result.item()
    return efficiency


def generate_total_stack_efficiency_curve( MW , stack_size=2.5 ):
    """
    Generates a combined efficiency curve for a system using multiple stacks.
    Each stack has a maximum capacity of 2.5 MW, and the function uses
    `single_stack_efficiency_curve` to compute the maximum efficiency among
    the needed stacks at a given setpoint.

    Parameters
    ----------
    MW : float
        The total rated stack capacity in MW to be achieved by stacking
        multiple units.
    stack_size : float
        Capacity in MW of a single stack unit

    Returns
    -------
    efficiency_curve : function : [0,1]->[0,1]
        An interpolating function that, given a setpoint in [0,1], returns
        the maximum achievable efficiency considering multiple stacks.
    """
    MW_stack = stack_size
    num_stacks = ceil( MW / MW_stack )

    # BERNARD :
    #sp_stack  = np.array([0.000, 0.111, 0.125, 0.250, 0.375, 0.500, 0.625, 0.750, 0.875, 1.000])
    #eff_stack = np.array([0    , 0    , 73   , 73   , 71.5 , 70   , 68   , 67   , 65   , 64   ])/100 * 142/120 
    #stack_interp_func = interp1d( sp_stack , eff_stack , kind='linear', fill_value=(0,eff_stack[-1]), bounds_error=False )   

    sp_elx = np.arange( 101 ) / 100 
    sp_elx_stack = sp_elx[:,np.newaxis] * MW / ( np.arange(1,1+num_stacks)[np.newaxis,:] ) / MW_stack
    eff_elx_stack =  single_stack_efficiency_curve( sp_elx_stack) # stack_interp_func( sp_elx_stack ) 
    eff_elx = np.max( eff_elx_stack , axis=1 )
    
    return interp1d( 
        sp_elx , 
        eff_elx , 
        kind='linear', 
        fill_value=(0,0), 
        bounds_error=False  ) #fill_value=(0,eff_stack[-1])

def hydrogen_production_elx( turbine_production , turbine_power , num_turbines , stack_size, comp_eff, electric_gain ):
    """
    Computes hydrogen production for a given turbine production profile,
    accounting for BOP losses, stack efficiencies, compression, and
    an electrical gain factor.

    Parameters
    ----------
    turbine_production : array-like
        Time-series (or set of values) of wind turbine output power [kW].
    turbine_power : float
        Rated power per turbine [MW].
    num_turbines : int
        Number of turbines in this scenario.
    stack_size : float
        Rated electrolyzer capacity [MW] for each stack arrangement.
    comp_eff : float
        Overall compression efficiency factor (0 < comp_eff <= 1).
    electric_gain : float
        Additional electric gain factor (from removing power electronics in a H-turbine).

    Returns
    -------
    H2_production : ndarray
        Hydrogen production [kg/h] for each time step.
    stack_eff : ndarray
        The stack efficiency values (0-1) for each time step.
    stack_sp : ndarray
        The stack setpoint fraction [-] for each time step, i.e., 
        actual power / (stack_size * num_turbines * 1e3).
    avg_bop_loss : float
        The average BOP loss factor over the entire time-series.
    """
    # calculate  BOP losses
    bop_sp = turbine_production / ( turbine_power * num_turbines * 1e3 )
    bop_loss = bop_loss_curve(bop_sp).clip(None,1)
    avg_bop_loss = np.sum( bop_sp*bop_loss ) / np.sum( bop_sp)
    
    # Calculate stack efficiency
    stack_eff_curve = generate_total_stack_efficiency_curve( stack_size )
    stack_power = turbine_production * (1-bop_loss) 
    stack_sp = stack_power / ( stack_size * 1e3 * num_turbines ) 
    stack_eff = stack_eff_curve(stack_sp) 
    
    # Calculate H2 production
    H2_production = stack_power*1000 * 3600 / 142e6 * stack_eff
    H2_production *= comp_eff * electric_gain
    
    return H2_production , stack_eff , stack_sp , avg_bop_loss


def electric_yield( scn ) :
    
    with open('yield_params.yaml', 'r') as f : 
        params = yaml.load(f,Loader=yaml.SafeLoader)
        
    turbine_production = wind_production_timeseries() / 1000
    turbine_yield = turbine_production.sum()
    
    electric_yield_onshore = turbine_yield * ( 
        params['electric_turbine_availability'] *
        params['electric_infield_efficiency'  ] *
        params['electric_infield_availability'] *
        params['electric_export_efficiency'   ] *
        params['electric_export_availability' ] )
        
    return electric_yield_onshore
    
    
def hydrogen_yield( scn ) : 
    
    with open('yield_params.yaml', 'r') as f : 
        params = yaml.load(f,Loader=yaml.SafeLoader)
        
    turbine_production = wind_production_timeseries()
    h2_production, stack_eff, stack_sp, avg_bop_loss = hydrogen_production_elx(turbine_production, 
                                            scn['turbine_capacity_MW'], 
                                            scn['num_turbines'], 
                                            stack_size=scn['turbine_capacity_MW']*2, # TODO
                                            comp_eff=0.99,                              # TODO
                                            electric_gain=params['hydrogen_electric_gain'])
    
    h2_yield_elx = h2_production.sum()
    hydrogen_yield_onshore = h2_yield_elx * ( 
        params['hydrogen_turbine_availability'] *
        params['hydrogen_infield_efficiency'  ] *
        params['hydrogen_infield_availability'] *
        params['hydrogen_export_efficiency'   ] *
        params['hydrogen_export_availability' ] )
    
    # todo : stack degradation
    
    return hydrogen_yield_onshore
    
    