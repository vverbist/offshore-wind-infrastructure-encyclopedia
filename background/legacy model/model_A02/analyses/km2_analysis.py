# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 15:21:49 2026

@author: VictorVerbist
"""

#%%
import hub_optimisation.analysis_functions as af
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('../results/km2_analysis.csv')

df['yield'] =  df[['yield_el_MWh_year','yield_h2_MWh_year']].max(axis=1)
df['yield_TWh'] = df['yield']/ 1e6 


df['infield_length_km'] =  df[['infield_horizontal_pipeline_length_m','infield_horizontal_cable_length_m']].max(axis=1) / 1e3

df['wake_loss_%'] = df['wake_loss_frac'] * 100

#df['MW/km2'] = df['']

df = df.rename(columns={'total_LCOE':'LCOE'})

D = 'export_pipeline_diameter_inch'
P = 'compressor_outlet_pressure_bar'
nt = 'num_turbines'
km2 = 'farm_area_km2'
S = 'stack_overplant_factor'
nep = 'num_export_pipelines'

mk = 'Areal Yield [GWh/km2/year]'
df[mk] = df['yield'] /1e3 / df[km2]

#%%
dfe  = df[ df['carrier']=='electricity']
dfhc = df[ df['carrier']=='hydrogen_central']
dfhd = df[ df['carrier']=='hydrogen_decentral']



x,y = af.plot_best_y_for_x( dfhd , km2 , 'yield' , 'LCOE' , agg='min' )
plt.plot( x , y[0] * x/x[0]  , 'k--')

#%%
plt.figure()

af.plot_best_y_for_x( dfhd , km2 , 'wake_loss_%' , 'LCOE' , agg='min' )
plt.ylabel('Wake Losses [%]')
plt.title('Wake Losses as function of # turbines')


#%%
df1 = df.copy()
carriers = df['carrier'].unique()
plt.figure(figsize=(24,8))
for i,c in enumerate(carriers):
    plt.subplot(1,3,i+1)
    df2 = df1[ df1['carrier']==c].fillna(0)
    df2 = af.fix_params(df2, {nt:134})
    af.plot_stacked_costs(df2, km2, value_key='LCOE', suffix='_cLCOE',new_fig=False)
    plt.title(c)
    plt.ylim([0,100])
    plt.ylabel('EUR/MWh')
    
#%%
x_key =  km2 # 'farm_area_km2'
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
    #af.plot_best_y_for_x( df2 , km2 , 'wake_loss_frac' , 'total_LCOE' , agg='min' )
plt.tight_layout()

#%%

carriers = df['carrier'].unique()
plt.figure()
for c in carriers:
    df1 = df[ df['carrier']==c]
    af.plot_best_y_for_x(df1, km2,'LCOE','LCOE',agg='min',new_fig=False)
plt.legend(carriers,title='carrier')
plt.ylim([0,100])

#%%


carriers = df['carrier'].unique()
plt.figure()
for c in carriers:
    if c == 'hydrogen_central' : continue
    df1 = df[ df['carrier']==c]
    af.plot_best_y_for_x(df1, km2,'infield_length_km','LCOE',agg='min',new_fig=False)
plt.legend(carriers,title='carrier')
#plt.ylim([0,100])

#%%

af.plot_best_y_for_x(dfe, nt, 'LCOE', 'LCOE')


#%%

nts = np.sort( df[nt].unique() )
GWs = np.round( nts * 15 / 1e3 )
 
plt.figure()
for nti in nts :
    dfgw = af.fix_params(dfhd, {nt:nti} )
    af.plot_best_y_for_x(dfgw, mk, 'LCOE', 'LCOE',new_fig=False)

plt.legend(GWs,title='Farm Capacity [GW]')
plt.xlim([0,200])

#%%

nts = np.sort( df[nt].unique() )
GWs = np.round( nts * 15 / 1e3 )
 
plt.figure()
for nti in nts :
    dfgw = af.fix_params(dfe, {nt:nti} )
    af.plot_best_y_for_x(dfgw, mk, 'LCOE', 'LCOE',new_fig=False)

plt.legend(GWs,title='Farm Capacity [GW]')
plt.xlim([0,200])