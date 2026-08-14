# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 10:49:22 2026

@author: VictorVerbist
"""


#%%
import hub_optimisation.analysis_functions as af
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('stack_analysis.csv')

df['yield'] =  df[['yield_el_MWh_year','yield_h2_MWh_year']].max(axis=1)
df['yield_TWh'] = df['yield']/ 1e6 
df = df.rename(columns={'total_LCOE':'LCOE'})

D = 'export_pipeline_diameter_inch'
P = 'compressor_outlet_pressure_bar'
nt = 'num_turbines'
S = 'stack_overplant_factor'
nep = 'num_export_pipelines'


#%%

dfhd = df[ df['carrier']=='hydrogen_decentral']
af.plot_best_y_for_x( dfhd , nt , S , 'LCOE' , agg='min' )
af.plot_best_y_for_x( dfhd , nt , nep , 'LCOE' , agg='min' , new_fig=False )
plt.title('Stack Overplant Factor and # export pipelines as function of num_turbines')
plt.ylabel('')
plt.legend([S,nep])

#%%
x,y = af.plot_best_y_for_x( dfhd , 'num_turbines' , 'yield_h2_MWh_year' , 'LCOE' , agg='min' )
plt.plot( x , y[0] * x/x[0]  , 'k--')
af.plot_best_y_for_x( dfhd , 'num_turbines' , 'wake_loss_frac' , 'LCOE' , agg='min' )

#%%
df1 = df.copy()
df1 = df1.rename(columns={'total_LCOE':'LCOE'})
carriers = df['carrier'].unique()
plt.figure(figsize=(18,6))
for i,c in enumerate(carriers):
    plt.subplot(1,3,i+1)
    df2 = df1[ df1['carrier']==c].fillna(0)
    af.plot_stacked_costs(df2, 'num_turbines', value_key='LCOE', suffix='_LCOE',new_fig=False)
    plt.title(c)
    plt.ylim([0,100])
    plt.ylabel('EUR/MWh')
    
#%%
x_key =  'num_turbines' # 'farm_area_km2'
carriers = df['carrier'].unique()
df1['yield'] =  df[['yield_el_MWh_year','yield_h2_MWh_year']].max(axis=1)
df1['yield_TWh'] = df1['yield']/ 1e6 
plt.figure(figsize=(18,6))
for i,c in enumerate(carriers):
    plt.subplot(1,3,i+1)
    df2 = df1[ df1['carrier']==c].fillna(0)
    x,y = af.plot_best_y_for_x( df2 , x_key , 'yield_TWh' , 'LCOE' , agg='min',new_fig=False )
    plt.plot( x , y[0] * x/x[0]  , 'k--')
    plt.ylim([0,20])
    plt.title(c)
    #af.plot_best_y_for_x( df2 , 'num_turbines' , 'wake_loss_frac' , 'total_LCOE' , agg='min' )
plt.tight_layout()
#%%

carriers = df['carrier'].unique()
for c in carriers:
    df1 = df[ df['carrier']==c]
    af.plot_best_y_for_x(df1, 'farm_area_km2','total_LCOE','total_LCOE',agg='min',new_fig=False)
plt.legend(carriers,title='carrier')