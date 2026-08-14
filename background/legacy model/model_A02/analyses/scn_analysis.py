# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 10:46:41 2025

@author: VictorVerbist
"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import hub_optimisation.analysis_functions as af

df = pd.read_csv('nt_optimisation.csv').sort_values('num_turbines')

df['LCOE'] = df['total_LCOE']
df.pop('total_LCOE')

df['carrier_id'] = np.where( df['carrier']=='electricity' , 0 , 1 )
df.loc[ df['carrier']=='electricity' , 'hydrogen_LCOE' ] = 0

wfpd = 'Wind Farm Power Density [MW/km2]'
df[wfpd] = df['farm_capacity_MW'] / 200

dfe = df[ df['carrier']=='electricity']
dfh = df[ df['carrier']=='hydrogen']


#%%

plt.figure()
plt.plot( dfh[wfpd] , dfh['wake_loss']*100 )
#plt.plot( dfe['num_turbines'] , dfe['wake_loss']*100 )

plt.xlabel(wfpd)
plt.ylabel('Wake Losses [%]')
plt.title('Wake loss as function of number of turbines')
#plt.legend(['Hydrogen','Electricity'],title='Carrier')


#%%    
    
plt.figure()
plt.plot( dfh['num_turbines'] , dfh['LCOE'] )
plt.plot( dfe['num_turbines'] , dfe['LCOE'] )

plt.xlabel('# turbines')
plt.ylabel('LCOE [EUR/MWh]')
plt.title('LCOE as function of number of turbines')
plt.legend(['Hydrogen','Electricity'],title='Carrier')

#%%
    
plt.figure()
plt.plot( dfh['yield_MWh_year'] /1e6 , dfh['LCOE'] )
plt.plot( dfe['yield_MWh_year'] /1e6 , dfe['LCOE'] )

plt.xlabel('Yield [TWh/year]')
plt.ylabel('LCOE [EUR/MWh]')
plt.title('LCOE as function of yield')
plt.legend(['Hydrogen','Electricity'],title='Carrier')
#plt.ylim([0,80])

#%%

af.plot_stacked_costs(dfe, 'num_turbines',value_key='LCOE',suffix='_LCOE')
plt.ylabel('EUR/MWh')
af.plot_stacked_costs(dfh, 'num_turbines',value_key='LCOE',suffix='_LCOE')
plt.ylabel('EUR/MWh')


#%%

df100 = df[ df['num_turbines']==100 ]
plt.figure(figsize=(5,8))
af.plot_stacked_costs(df100, 'carrier_id',value_key='LCOE',suffix='_LCOE',new_fig=False)
plt.ylabel('EUR/MWh')
plt.xlabel('Electricity                              Hydrogen')


#%%

plt.figure()
x,y = af.plot_best_y_for_x(dfe, 'num_turbines', 'yield_MWh_year',value_key='LCOE')
y1 = y[0] * x / x[0]
plt.plot(x,y1,'k--')
plt.xlabel('Num Turbines')
plt.ylabel('Yield [MWh/year]')
plt.title('Yield as function of # turbines')
plt.legend(['Yield','Linear'])

#%%




#%%

plt.figure()
plt.plot( dfh[wfpd]  , dfh['LCOE'] )
plt.plot( dfe[wfpd]  , dfe['LCOE'] )

plt.xlabel(wfpd)
plt.ylabel('LCOE [EUR/MWh]')
plt.title('LCOE as function of Wind Farm Power Density')
plt.legend(['Hydrogen','Electricity'],title='Carrier')

