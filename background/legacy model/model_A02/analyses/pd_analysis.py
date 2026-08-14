# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 15:15:43 2026

@author: VictorVerbist
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 14:18:43 2026

@author: VictorVerbist
"""

#%%
import hub_optimisation.analysis_functions as af
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('pd_analysis.csv')


df['yield'] =  df[['yield_el_MWh_year','yield_h2_MWh_year']].max(axis=1)
df['yield_TWh'] = df['yield']/ 1e6 
df = df.rename(columns={'total_LCOE':'LCOE'})

D = 'export_pipeline_diameter_inch'
P = 'compressor_outlet_pressure_bar'
nt = 'num_turbines'

#%%

dfhd = df[ df['carrier']=='hydrogen_decentral']


#%%




epds = np.sort( dfhd[D].unique() )
plt.figure()
for epd in epds :
    df1 = af.fix_params(dfhd, {D:epd})
    af.plot_best_y_for_x(df1, nt, P, 'LCOE',new_fig=False)
plt.legend(epds,title=D)

#%%

plt.figure(figsize=(8,12))

plt.subplot(4,1,1)
af.plot_best_y_for_x(dfhd, nt, 'LCOE','LCOE',new_fig=False)
plt.title('LCOE [€/MWh]')
plt.subplot(4,1,2)
af.plot_best_y_for_x(dfhd, nt, P,'LCOE',new_fig=False)
plt.ylabel('Pressure [bar]')
plt.title('Pressure [bar]')
plt.subplot(4,1,3)
af.plot_best_y_for_x(dfhd, nt, D,'LCOE',new_fig=False)
plt.ylabel('Pipeline Diameter [inch]')
plt.title('Pipeline Diameter [inch]')
plt.subplot(4,1,4)
af.plot_best_y_for_x(dfhd, nt, 'num_export_pipelines','LCOE',new_fig=False)
plt.ylabel('# pipelines')
plt.title('# pipelines')

plt.tight_layout()

sys.exit()

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