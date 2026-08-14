# -*- coding: utf-8 -*-
"""

export_cost_calculation.py

Created on Tue Nov 11 17:13:47 2025

@author: VictorVerbist
"""
# infra_cost_calculation.py
from math import ceil, floor
import numpy as np
from CoolProp.CoolProp import PropsSI
from pipeline_cost_curve import pipeline_cost_curve

def el_infield_cable_length( scn , params ):
    """
    Estimate infield cable length (horizontal + vertical) for an offshore wind farm.

    Parameters
    ----------
    scn : dict
        Must contain at least:
        - 'num_turbines'           : int, N
        - 'area_km2'               : float, A (total farm area in km²)
        - 'turbine_capacity_mw'    : float, rated power of one turbine in MW

    params : dict
        Must contain at least:
        - 'cable_rated_power_mw'   : float, rating of the infield cable in MW
        - 'sea_depth_m'            : float, mean water depth (m)
        - 'burial_depth_m'         : float, burial depth below seabed (m)

    Returns
    -------
    scn : dict
        Same dict with three additional keys (all in meters):
        - 'infield_horizontal_cable_length_m'
        - 'infield_vertical_cable_length'
        - 'infield_total_cable_length'

    """
    
  

    # Unpack scenario
    N_turb          = scn["num_turbines"]
    A_km2           = scn["farm_area_km2"]

    P_turb_MW       = scn["turbine_capacity_MW"]

    # Unpack parameters
    P_cable_MW      = params["infield_cable_capacity_MW"]
    sea_depth_m     = params["sea_depth_m"]
    burial_depth_m  = params["burial_depth_m"]
   
    
    # Horizontal length
    max_turbines_per_string = floor( P_cable_MW / P_turb_MW )
    num_strings = ceil(N_turb / max_turbines_per_string)
    
    avg_string_length_m = 0.5 * np.sqrt(2) * A_km2**0.5 * 1000
    
    infield_horizontal_cable_length_m = num_strings * avg_string_length_m

    # Vertical length: for each turbine, down and up
    vertical_per_turbine_m = 2.0 * (sea_depth_m + burial_depth_m)
    infield_vertical_cable_length_m = N_turb * vertical_per_turbine_m
    
    # Total
    infield_total_cable_length_m = infield_horizontal_cable_length_m + infield_vertical_cable_length_m

    # 
    res = {
        "infield_horizontal_cable_length_m" :  infield_horizontal_cable_length_m,
        "infield_vertical_cable_length_m"   :  infield_vertical_cable_length_m,
        "infield_total_cable_length_m"      :  infield_total_cable_length_m,
        }

    return res

def h2_infield_pipeline_length( scn , params ):
    """
    Estimate infield cable length (horizontal + vertical) for an offshore wind farm.

    Parameters
    ----------
    scn : dict
        Must contain at least:
        - 'num_turbines'           : int, N
        - 'area_km2'               : float, A (total farm area in km²)

    params : dict
        Must contain at least:
        - 'sea_depth_m'            : float, mean water depth (m)
        - 'burial_depth_m'         : float, burial depth below seabed (m)

    Returns
    -------
    scn : dict
        Same dict with three additional keys (all in meters):
        - 'infield_horizontal_pipeline_length_m'
        - 'infield_vertical_pipeline_length'
        - 'infield_total_pipeline_length'

    """
  
    
    # Unpack scenario
    N_turb          = scn["num_turbines"]
    A_km2           = scn["farm_area_km2"]
    

    # Unpack parameters
    sea_depth_m     = params["sea_depth_m"]
    burial_depth_m  = params["burial_depth_m"]
    
    # Horizontal length: ladder structure
    num_strings = ceil( N_turb**0.5 ) + 2
    length_string_m = A_km2**0.5 * 1000
    
    infield_horizontal_pipeline_length_m = num_strings * length_string_m 
    
    # Vertical length: for each turbine, down and up
    vertical_per_turbine_m = 1.0 * (sea_depth_m + burial_depth_m)
    infield_vertical_pipeline_length_m = N_turb * vertical_per_turbine_m
    
    # Total
    infield_total_pipeline_length_m = infield_horizontal_pipeline_length_m + infield_vertical_pipeline_length_m


    # 
    res = {
        "infield_horizontal_pipeline_length_m" : infield_horizontal_pipeline_length_m,
        "infield_vertical_pipeline_length_m"   : infield_vertical_pipeline_length_m,
        "infield_total_pipeline_length_m"      : infield_total_pipeline_length_m,
        }
    
    return res

def h2_export_pipeline_capacity( 
    D_inch: float,
    P_in_bar: float,
    L_m : float = 80e3,
    eps_surface_roughness_m: float=1.5e-7,
    P_out_bar: float=66,
    T_K: float=293,
) -> float:
    """
    Returns hydrogen pipeline capacity in kg/h using Colebrook equation 
    
    [1] Transition Accelerator : https://transitionaccelerator.ca/wp-content/uploads/2023/06/The-Techno-Economics-of-Hydrogen-Pipelines-v2.pdf
    
    [2] Perry's Handbook: https://mathguy.us/BySubject/Chemistry/Perrys_Chemical_Engineers_Handbook.pdf
    Eqns: (6-38) with (6-32) and (6-33) [8th Edition]

    Note: [1] uses f as Darcy-Weisbach friction factor, [2] uses f as Fanning friction factor.
    Difference is factor 4. Here [2]'s Fanning fricion factor is used (eqn 6-32)

    Parameters
    ----------
    D_inch : inner diameter [inch]
    Pin_bar : inlet absolute pressure [bar]
    L_m : pipeline length [m]
    f_darcy : Darcy friction factor [-]
    Pout_Pa : outlet absolute pressure [bar]
    T_K : temperature [K]

    Returns
    -------
    Capacity [kg/h] as float
    """
    
    if P_in_bar <= P_out_bar:
        raise ValueError("Pin_Pa must be greater than Pout_Pa.")
    
    # unit conversions and renaming
    D_m = D_inch * 0.0254
    P_in_Pa  = P_in_bar  * 1e5
    P_out_Pa = P_out_bar * 1e5
    
    eps = eps_surface_roughness_m
    dP = P_in_Pa - P_out_Pa
    
    # from here on: everthing in SI units
    
    # Calculate average Pressure, using Transition Accelerator method, eqn (4)
    P_avg_Pa = (2/3) * ( ( P_in_Pa**3 - P_out_Pa**3) / ( P_in_Pa**2 - P_out_Pa**2)  )
    # get density and viscosity at this avg pressure
    rho_avg = PropsSI('D', "T", T_K, "P", P_avg_Pa , "Hydrogen" ) # density, kg/m3
    mu_avg  = PropsSI('V', "T", T_K, "P", P_avg_Pa , "Hydrogen" ) # viscosity, kg/(m.s)
    
    # Calc Re * sqrt(f), using (6-32) and (6-33) 
    Re_sqrt_f = D_m**(3/2) / mu_avg * np.sqrt( (dP*rho_avg)/(2*L_m) )
    
    # Calc 1/sqrt(f), eqn ( 6-38 )
    sqrt_f_inv = -4 * np.log10( eps/(3.7*D_m) + 1.256/Re_sqrt_f )
    
    # Calc v using eqn (6-32)
    v = np.sqrt( (D_m*dP)/(2*rho_avg*L_m) ) * sqrt_f_inv
    
    # Convert speed to mass flow
    A_m2 = np.pi/4 * D_m**2
    m_dot_kgs = rho_avg * A_m2 * v 
    m_dot_kgh = m_dot_kgs * 3600
    
    return m_dot_kgh
    

def el_infra_costs(scn: dict, params: dict) -> dict:
    
    
    development_capex = params['development_costs_farm'] + params['development_costs_per_turbine'] * scn['num_turbines']
    
    infield_capex = params['infield_cable_cost_per_meter'] * scn['infield_total_cable_length_m']
    infield_installation = params['infield_cable_installation_cost_per_meter'] * scn['infield_horizontal_cable_length_m']
    infield_decommissioning = infield_installation * params['infield_decommissioning_factor']
    infield_opex = infield_capex * params['infield_cable_opex_rate']
    
    
    offshore_platform_capex = scn['P_oss_max_MW'] * params['offshore-platform_cost_per_MW']
    offshore_platform_opex  = offshore_platform_capex * params['offshore-platform_opex_rate']
    
    offshore_substation_converter_capex = scn['P_oss_max_MW'] * params['offshore-substation-converter_cost_per_MW']
    offshore_substation_converter_opex  = offshore_substation_converter_capex * params['offshore-substation-converter_opex_rate']

    num_export_cables = ceil(scn['P_oss_max_MW'] / params['export_cable_capacity_MW'])

    export_length_m = params['export_length_km'] * 1000
    
    export_capex = params['export_cable_cost_per_m'] * export_length_m * num_export_cables
    export_installation = (
        params['export_cable_installation_cost_per_m'] * export_length_m * num_export_cables
  #      / params['export_cable_parallel_factor']
    )
    export_decommissioning = export_installation * params['export_decommissioning_factor']
    export_opex = export_capex * params['export_cable_opex_rate']

    onshore_substation_capex = scn['P_oss_max_MW'] * params['onshore-substation_costs_per_MW'] # TODO EFFICIENCIES
    onshore_substation_opex  = onshore_substation_capex * params['onshore-substation_opex_rate']

    res = {
        
        'development_capex' : development_capex,
        
        'infield_capex' : infield_capex,
        'infield_installation' : infield_installation,
        'infield_decommissioning' : infield_decommissioning,
        'infield_opex' : infield_opex,
        
        'offshore-platform_capex': offshore_platform_capex,
        'offshore-platform_opex':  offshore_platform_opex,
        
        'offshore-substation-converter_capex': offshore_substation_converter_capex,
        'offshore-substation-converter_opex':  offshore_substation_converter_opex,
        
        'export_capex':              export_capex,
        'export_installation':       export_installation,
        'export_decommissioning':    export_decommissioning,
        'export_opex':               export_opex,
        'onshore-substation_capex':  onshore_substation_capex,
        'onshore-substation_opex':   onshore_substation_opex,
    }
    return {f"infra_{k}": v for k, v in res.items()}

def h2_central_infra_costs(scn: dict, params: dict) -> dict:
    
    
    development_capex = params['development_costs_farm'] + params['development_costs_per_turbine'] * scn['num_turbines']
    
    infield_capex = params['infield_cable_cost_per_meter'] * scn['infield_total_cable_length_m']
    infield_installation = params['infield_cable_installation_cost_per_meter'] * scn['infield_horizontal_cable_length_m']
    infield_decommissioning = infield_installation * params['infield_decommissioning_factor']
    infield_opex = infield_capex * params['infield_cable_opex_rate']
    
    
    offshore_platform_capex = scn['P_oss_max_MW'] * params['offshore-platform_cost_per_MW']
    offshore_platform_opex  = offshore_platform_capex * params['offshore-platform_opex_rate']
    
    
    
    export_length_m = params['export_length_km'] * 1000
    
    export_pipeline_capacity_kgh = h2_export_pipeline_capacity( scn['export_pipeline_diameter_inch'], scn['compressor_outlet_pressure_bar'] , L_m=export_length_m )
    num_export_pipelines = ceil(scn['H2_export_capacity_kgph'] / export_pipeline_capacity_kgh )

    export_pipeline_cost_per_m = pipeline_cost_curve(scn['compressor_outlet_pressure_bar'] , scn['export_pipeline_diameter_inch'])
    export_capex = export_pipeline_cost_per_m * export_length_m * num_export_pipelines
    
    num_installation_runs = ceil( num_export_pipelines / params['export_pipeline_parallel_factor'] )
    
    export_installation = (
        params['export_pipeline_installation_cost_per_m'] * export_length_m * num_installation_runs
    )
    export_decommissioning = export_installation * params['export_decommissioning_factor']
    export_opex = export_capex * params['export_pipeline_opex_rate']

    res = {
        
        'development_capex' : development_capex,
        
        'infield_capex' : infield_capex,
        'infield_installation' : infield_installation,
        'infield_decommissioning' : infield_decommissioning,
        'infield_opex' : infield_opex,
        
        'offshore-platform_capex': offshore_platform_capex,
        'offshore-platform_opex':  offshore_platform_opex,
        
        'num_export_pipelines':     num_export_pipelines,
        
        'export_capex':            export_capex,
        'export_installation':     export_installation,
        'export_decommissioning':  export_decommissioning,
        'export_opex':             export_opex,
    }
    return {f"infra_{k}": v for k, v in res.items()}

def h2_decentral_infra_costs(scn: dict, params: dict) -> dict:
    
    
    development_capex = params['development_costs_farm'] + params['development_costs_per_turbine'] * scn['num_turbines']
    
    
    
    infield_capex = params['infield_pipeline_cost_per_m'] * scn['infield_total_pipeline_length_m']
    infield_installation = params['infield_pipeline_installation_cost_per_m'] * scn['infield_horizontal_pipeline_length_m']
    infield_decommissioning = infield_installation * params['infield_decommissioning_factor']
    infield_opex = infield_capex * params['infield_pipeline_opex_rate']
    
    export_length_m = params['export_length_km'] * 1000
    export_pipeline_capacity_kgh = h2_export_pipeline_capacity( scn['export_pipeline_diameter_inch'], scn['compressor_outlet_pressure_bar'] , L_m=export_length_m )
    num_export_pipelines = ceil(scn['H2_export_capacity_kgph'] / export_pipeline_capacity_kgh )

    export_pipeline_cost_per_m = pipeline_cost_curve(scn['compressor_outlet_pressure_bar'] , scn['export_pipeline_diameter_inch'])
    export_capex = export_pipeline_cost_per_m * export_length_m * num_export_pipelines
    
      
    num_installation_runs = ceil( num_export_pipelines / params['export_pipeline_parallel_factor'] )
    
    export_installation = (
        params['export_pipeline_installation_cost_per_m'] * export_length_m * num_installation_runs
    )
    
    export_decommissioning = export_installation * params['export_decommissioning_factor']
    export_opex = export_capex * params['export_pipeline_opex_rate']

    res = {
        
        'development_capex' : development_capex,
        
        'infield_capex' : infield_capex,
        'infield_installation' : infield_installation,
        'infield_decommissioning' : infield_decommissioning,
        'infield_opex' : infield_opex,
        
        'num_export_pipelines':     num_export_pipelines,
        
        'export_capex':            export_capex,
        'export_installation':     export_installation,
        'export_decommissioning':  export_decommissioning,
        'export_opex':             export_opex,
    }
    return {f"infra_{k}": v for k, v in res.items()}
