# -*- coding: utf-8 -*-
"""

turbine_cost_calculation.py

Created on Tue Nov 11 16:46:20 2025

@author: VictorVerbist
"""

# turbine_cost_calculation.py

def turbine_costs(scn: dict, params: dict) -> dict:
    
    turbine_capex = scn['num_turbines'] * scn['turbine_capacity_MW'] * params['turbine_cost_per_MW']
    turbine_opex  = scn['num_turbines'] * params['opex_per_turbine']
    
    
    foundation_capex = params['foundation_capex_per_turbine'] * scn['num_turbines']
    foundation_installation = params['foundation_installation_cost_per_turbine'] * scn['num_turbines']
    foundation_decommissioning = foundation_installation * params['foundation_decommissioning_factor']
    foundation_opex = params['foundation_opex_rate'] * foundation_capex
    
    
    return {
        'turbine_turbine_capex': turbine_capex,
        'turbine_turbine_opex':  turbine_opex,
        
        'turbine_foundation_capex' : foundation_capex,
        'turbine_foundation_installation' : foundation_installation,
        'turbine_foundation_decommissioning' : foundation_decommissioning,
        'turbine_foundation_opex' : foundation_opex,
        
    }

#%%

"""

def el_turbine_costs(scn: dict, params: dict) -> dict:
    
    turbine_capex = scn['num_turbines'] * scn['turbine_capacity_MW'] * params['turbine_cost_per_MW']
    turbine_opex  = scn['num_turbines'] * params['opex_per_turbine']
    
    foundation_capex = params['foundation_capex_per_turbine'] * scn['num_turbines']
    foundation_installation = params['foundation_installation_cost_per_turbine'] * scn['num_turbines']
    foundation_decommissioning = foundation_installation * params['foundation_decommissioning_factor']
    foundation_opex = params['foundation_opex_rate'] * foundation_capex
    
    
    return {
        'turbine_turbine_capex': turbine_capex,
        'turbine_turbine_opex':  turbine_opex,
        
        'turbine_foundation_capex' : foundation_capex,
        'turbine_foundation_installation' : foundation_installation,
        'turbine_foundation_decommissioning' : foundation_decommissioning,
        'turbine_foundation_opex' : foundation_opex,
        
    }

def h2_turbine_costs(scn: dict, params: dict) -> dict:
    turbine_capex = scn['num_turbines'] * scn['turbine_capacity_MW'] * (
        params['turbine_cost_per_MW'] - params['hydrogen_electronics_savings_per_MW']
    )
    turbine_opex  = scn['num_turbines'] * params['opex_per_turbine']
    
    foundation_capex = params['foundation_capex_per_turbine'] * scn['num_turbines']
    foundation_installation = params['foundation_installation_cost_per_turbine'] * scn['num_turbines']
    foundation_decommissioning = foundation_installation * params['foundation_decommissioning_factor']
    foundation_opex = params['foundation_opex_rate'] * foundation_capex
    
    
    return {
        'turbine_turbine_capex': turbine_capex,
        'turbine_turbine_opex':  turbine_opex,
        
        'turbine_foundation_capex' : foundation_capex,
        'turbine_foundation_installation' : foundation_installation,
        'turbine_foundation_decommissioning' : foundation_decommissioning,
        'turbine_foundation_opex' : foundation_opex,
        
    }

"""