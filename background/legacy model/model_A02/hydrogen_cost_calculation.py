# -*- coding: utf-8 -*-
"""

hydrogen_cost_calculation.py

Created on Tue Nov 11 17:13:47 2025

@author: VictorVerbist
"""

# hydrogen_cost_calculation.py
def h2_decentral_hydrogen_costs(scn: dict, params: dict) -> dict:
    
    
    stack_capex = params['stack_costs_per_MW'] * scn['turbine_capacity_MW'] * scn['stack_overplant_factor'] * scn['num_turbines']
    stack_opex  = params['stack_opex_rate'] * stack_capex

    bop_capex = params['bop_costs_per_MW'] * scn['turbine_capacity_MW'] * scn['num_turbines']
    bop_opex  = params['bop_opex_rate'] * bop_capex
    
    ebop_capex = params['decentral-electrical-bop_costs_per_MW'] * scn['turbine_capacity_MW'] * scn['num_turbines']
    ebop_opex  = params['electrical-bop_opex_rate'] * ebop_capex

    compressor_capex = (
        params['compressor_cost_factor_A']
        * (scn['compressor_turbine_power_kW_max'] ** params['compressor_cost_scaling_factor'])
        * scn['num_turbines']
    )
    compressor_opex  = params['compressor_opex_rate'] * compressor_capex

    res = {
        'stack_capex':      stack_capex,
        'stack_opex':       stack_opex,
        'bop_capex':        bop_capex,
        'bop_opex':         bop_opex,
        'electrical-bop_capex' : ebop_capex,
        'electrical-bop_opex'  : ebop_opex,
        'compressor_capex': compressor_capex,
        'compressor_opex':  compressor_opex,
    }
    return {f"hydrogen_{k}": v for k, v in res.items()}



def h2_central_hydrogen_costs(scn: dict, params: dict) -> dict:
    
    reference_MW = params['reference_rating_MW']
    scn_bop_rating_MW = scn['P_oss_max_MW']
    scn_stack_rating_MW = scn_bop_rating_MW * scn['stack_overplant_factor']
    
    
    stack_capex = params['stack_costs_per_MW'] * reference_MW * ( scn_stack_rating_MW / reference_MW )**params['stack_scaling_factor']
    stack_opex  = params['stack_opex_rate'] * stack_capex

    bop_capex = params['bop_costs_per_MW'] * reference_MW * ( scn_bop_rating_MW / reference_MW )**params['bop_scaling_factor']
    bop_opex  = params['bop_opex_rate'] * bop_capex
    
    ebop_capex = params['central-electrical-bop_costs_per_MW'] * reference_MW * ( scn_bop_rating_MW / reference_MW )**params['electrical-bop_scaling_factor']
    ebop_opex  = params['electrical-bop_opex_rate'] * ebop_capex
    
    # TO DO 
    compressor_capex = (
        params['compressor_cost_factor_A']
        * (scn['compressor_turbine_power_kW_max'] ** params['compressor_cost_scaling_factor'])
     #   * scn['num_turbines']
    ) 
    compressor_opex  = params['compressor_opex_rate'] * compressor_capex

    res = {
        'stack_capex':      stack_capex,
        'stack_opex':       stack_opex,
        'bop_capex':        bop_capex,
        'bop_opex':         bop_opex,
        'electrical-bop_capex' : ebop_capex,
        'electrical-bop_opex'  : ebop_opex,
        'compressor_capex': compressor_capex,
        'compressor_opex':  compressor_opex,
    }
    return {f"hydrogen_{k}": v for k, v in res.items()}