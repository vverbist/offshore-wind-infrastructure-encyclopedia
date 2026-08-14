# -*- coding: utf-8 -*-
"""
test_single_scenario.py 

Created on Fri Feb 27 11:29:36 2026

@author: VictorVerbist


"""

# create_scenarios.py
from __future__ import annotations

from typing import List, Dict, Any
import numpy as np
import pandas as pd

from itertools import product

from scenario_types import Design, Assumptions
from scenario_workflow import Scenario

#out_path = 'results/km2_analysis.csv'


def get_designs() -> List[Design]:
    # --- define ranges ONCE (your preferred style) ---
    carriers = [
        "electricity", 
    #    "hydrogen_central", 
        "hydrogen_decentral"
        ]

    num_turbines = [67, 134, 200, 267, 334, 400] # np.arange(50, 275, 25).astype(int).tolist()
    turbine_capacity_MW = [15.0] 
    farm_area_km2 = [200] # np.arange( 50, 325, 25 )*1.0 # [200] # [50, 100, 150, 200, 250, 300]

    # hydrogen-only ranges (still defined here, in the same place)
    stack_overplant_factor = np.arange(10,21)/10 # [1.0]#, 1.2, 1.4, 1.6, 1.8, 2.0]
    compressor_outlet_pressure_bar = [150] # np.arange(80,160,10)*1.0 #[150]#, 75, 100.0, 125, 150]
    export_pipeline_diameter_inch = [8.0]# np.arange(4,9,1)*1.0

    designs: List[Design] = []

    # --- Cartesian product for shared params + carrier ---
    for carrier, nt, cap, area in product(
        carriers, num_turbines, turbine_capacity_MW, farm_area_km2
    ):
        if carrier == "electricity":
            designs.append(
                Design(
                    carrier=carrier,
                    num_turbines=nt,
                    turbine_capacity_MW=cap,
                    farm_area_km2=area,
                )
            )
        else:
            # add cartesian product over hydrogen-only params
            for sof, pbar, epd in product(stack_overplant_factor, compressor_outlet_pressure_bar, export_pipeline_diameter_inch):
                designs.append(
                    Design(
                        carrier=carrier,
                        num_turbines=nt,
                        turbine_capacity_MW=cap,
                        farm_area_km2=area,
                        stack_overplant_factor=sof,
                        compressor_outlet_pressure_bar=pbar,
                        export_pipeline_diameter_inch=epd,
                    )
                )

    return designs



def add_component_lcoe_columns(row: Dict[str, Any], costs_flat: Dict[str, float], suffix: str = "cLCOE") -> None:
    """
    Adds per-component LCOE columns from analyze_costs_flat() output.

    Example input key:  "turbine_monopile_LCOE"
    Output column:      "LCOE_turbine_monopile"
    """
    for k, v in (costs_flat or {}).items():
        if not k.endswith("_LCOE"):
            continue

        base = k[:-len("_LCOE")]  # strip suffix

        # skip overall total and section totals (keep if you want, but you already have them separately)
        if base == "total" or "_" not in base:
            continue

        col = f"{base}_{suffix}"
        row[col] = v
        
def add_component_capex_per_mw_columns(
    row: Dict[str, Any],
    costs_flat: Dict[str, float],
    capacity_mw: float,
    suffix: str = "cCAPEXpMW",
) -> None:
    """
    Adds per-component CAPEX per MW columns from analyze_costs_flat() output.

    Example input key:  "turbine_monopile_capex"
    Output column:      "turbine_monopile_cCAPEXpMW"   (EUR/MW)
    """
    if not capacity_mw or capacity_mw <= 0:
        return

    for k, v in (costs_flat or {}).items():
        # pick only the "capex" totals (not annual_capex etc.)
        if not k.endswith("_capex"):
            continue
        if k.endswith("_annual_capex"):
            continue  # safety; usually not needed because it endswith _capex not _annual_capex

        base = k[:-len("_capex")]  # strip suffix

        # skip overall total and section totals (we’ll do section totals separately)
        if base == "total" or "_" not in base:
            continue

        row[f"{base}_{suffix}"] = float(v) / float(capacity_mw)

def scenario_to_row(s: Scenario) -> Dict[str, Any]:
    d = s.design
    dv = s.derived
    r = s.results
    cf = r.costs_flat or {}

    row: Dict[str, Any] = {}
    row["scenario_id"] = s.scenario_id

    # design vars
    row["carrier"] = d.carrier
    row["num_turbines"] = d.num_turbines
    row["turbine_capacity_MW"] = d.turbine_capacity_MW
    row["farm_area_km2"] = d.farm_area_km2
    row["farm_capacity_MW"] = d.num_turbines * d.turbine_capacity_MW

    row["stack_overplant_factor"] = d.stack_overplant_factor
    row["compressor_outlet_pressure_bar"] = d.compressor_outlet_pressure_bar 
    row["export_pipeline_diameter_inch"] =  d.export_pipeline_diameter_inch

    # derived
    row["wake_loss_frac"] = dv.wake_loss_frac
    row["farm_cf"] = dv.farm_cf

    row["infield_horizontal_cable_length_m"] = dv.infield_horizontal_cable_length_m
    row["infield_horizontal_pipeline_length_m"] = dv.infield_horizontal_pipeline_length_m
    row["num_export_pipelines"] = dv.num_export_pipelines

    row["yield_el_MWh_year"] = dv.electric_yield_farm_MWh
    row["yield_h2_MWh_year"] = dv.h2_export_MWh
    row["yield_h2_kg_year"] = dv.h2_export_kg_year

    row["stack_sp_expected"] = dv.stack_sp_expected
    row["stack_eff1"] = dv.stack_eff1
    row["stack_eff2"] = dv.stack_eff2

    # KPIs
    row["total_LCOE"] = r.total_LCOE
    row["total_capex_EUR"] = r.total_capex_EUR
    row["total_annual_capex_EUR_per_year"] = r.total_annual_capex_EUR_per_year
    row["total_annual_opex_EUR_per_year"] = r.total_annual_opex_EUR_per_year
    row["total_annual_cost_EUR_per_year"] = r.total_annual_cost_EUR_per_year

    # optional breakdown
    row["turbine_sLCOE"] = cf.get("turbine_LCOE")
    row["hydrogen_sLCOE"] = cf.get("hydrogen_LCOE")
    row["infra_sLCOE"] = cf.get("infra_LCOE")
    
    # ✅ per-component LCOE columns
    add_component_lcoe_columns(row, cf, suffix="cLCOE")
    
    cap_mw = row["farm_capacity_MW"]

    row["turbine_spMW"]  = (cf.get("turbine_capex")  / cap_mw) #if cf.get("turbine_capex")  is not None and cap_mw > 0 else None
    row["hydrogen_spMW"] = (cf.get("hydrogen_capex") / cap_mw) if cf.get("hydrogen_capex") is not None and cap_mw > 0 else None
    row["infra_spMW"]    = (cf.get("infra_capex")    / cap_mw) #if cf.get("infra_capex")    is not None and cap_mw > 0 else None
    
    row["total_pMW"] = (cf.get("total_capex") / cap_mw) #if cf.get("total_capex") is not None and cap_mw > 0 else None
    
    add_component_capex_per_mw_columns(row, cf, capacity_mw=row["farm_capacity_MW"], suffix="cpMW")
    
    return row

def run_all() -> pd.DataFrame:
    assumptions = Assumptions()
    designs = get_designs()
    rows: List[Dict[str, Any]] = []

    s_ls = []
    for design in designs:
        s = Scenario(design=design, assumptions=assumptions)
        s.run( save_artifacts=True)
        rows.append(scenario_to_row(s))
        s_ls.append(s)
        print(f"{s.scenario_id} | {design.carrier} | nt={design.num_turbines} | LCO={s.results.total_LCOE:.2f}")

    return pd.DataFrame(rows),s_ls

def plot_results_quick( df ):
    
    import hub_optimisation.analysis_functions as af
    import matplotlib.pyplot as plt
    
    carriers = df['carrier'].unique()
    for c in carriers:
        df1 = df[ df['carrier']==c]
        af.plot_best_y_for_x(df1, 'num_turbines','total_LCOE','total_LCOE',agg='min',new_fig=False)
    plt.legend(carriers,title='carrier')


if __name__ == "__main__":
    df , s_ls = run_all()
#    df.to_csv(out_path, index=False)
#    print(f"Wrote: {out_path}")
    plot_results_quick(df)
    
import sys
sys.exit()

#%%

scn = s_ls[-1]
bd = scn.artifacts.costs_breakdown
#bd.to_excel('bd.xlsx')

#%%

import hub_optimisation.analysis_functions as af
import matplotlib.pyplot as plt

dfh = df[ df['carrier']=='hydrogen_decentral']
dfe = df[ df['carrier']=='electricity']

#%%

af.plot_stacked_costs(dfh.fillna(0), 'num_turbines', 'total_LCOE', suffix='_cpMW')
#plt.ylim([0,4e6])
plt.ylabel('€/MW')

af.plot_stacked_costs(dfh.fillna(0), 'num_turbines', 'total_LCOE', suffix='_cLCOE')
#plt.ylim([0,4e6])
plt.ylabel('€/MWh')


#%%
af.plot_best_y_for_x(dfh.fillna(0), 'num_turbines', 'total_LCOE','total_LCOE',new_fig=True)



dfh['lcoe_gv'] = dfh['total_LCOE'] + 20e6/dfh['yield_h2_MWh_year']
af.plot_best_y_for_x(dfh.fillna(0), 'num_turbines', 'lcoe_gv','total_LCOE',new_fig=False)

#%%

af.plot_best_y_for_x(dfh.fillna(0), 'num_turbines', 'stack_overplant_factor','total_LCOE',new_fig=False)

#%%


af.plot_best_y_for_x(dfh.fillna(0), 'num_turbines', 'stack_eff1','total_LCOE',new_fig=False)

dfhs = dfh[ dfh['stack_overplant_factor']==1]
af.plot_best_y_for_x(dfhs.fillna(0), 'num_turbines', 'stack_eff1','total_LCOE',new_fig=False)


#%%
af.plot_best_y_for_x(dfh.fillna(0), 'num_turbines', 'wake_loss_frac','total_LCOE',new_fig=False)

#%%


#%%

af.plot_best_y_for_x(dfh, 'num_turbines', 'wake_loss_frac', 'total_LCOE')

#%%
x,y = af.plot_best_y_for_x(dfh, 'num_turbines', 'yield_h2_MWh_year', 'total_LCOE')
plt.plot( x , y[0]/x[0]*x , 'k--')
#%%
plt.figure()
af.plot_best_y_for_x(dfh, 'num_turbines', 'infra_export_cpMW', 'total_LCOE')
plt.ylim(bottom=0,top=2e5)
#%%
plt.figure()
af.plot_best_y_for_x(dfh, 'num_turbines', 'infra_export_cLCOE', 'total_LCOE')

