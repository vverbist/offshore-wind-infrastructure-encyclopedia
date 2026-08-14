# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 15:21:49 2026

@author: VictorVerbist
"""

#%%
import hub_optimisation.analysis_functions as af
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull

df = pd.read_csv('../results/results_big.csv')

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

mkr = mk + ' r'
round_to = 10
df[mkr] = (df[mk] / round_to).round() * round_to

mwkm = 'Areal Capacity [MW/km2]'
df[mwkm] = df['farm_capacity_MW'] / df['farm_area_km2']
mwkmr = mwkm + ' r'
round_to = 3
df[mwkmr] = ( df[mwkm] / round_to).round() * round_to 


spacing = 'Spacing [-]'
cf = 'Capacity Factor [-]'
df[cf] = df['farm_cf']

df[spacing] = np.sqrt( df['farm_area_km2'] / ( df['num_turbines'] * 0.236**2 ) )

gw ='Farm Capacity [GW]'
df[gw] = ( df[nt] * 15 / 1e3 ).round()

cpmw = 'Specific Capex [€/MW]'
df[cpmw] = df['total_capex_EUR'] / df[gw]

dfe  = df[ df['carrier']=='electricity']
dfhc = df[ df['carrier']=='hydrogen_central']
dfhd = df[ df['carrier']=='hydrogen_decentral']

#%%




#%%
df1 = df.copy()
carriers = df['carrier'].unique()
plt.figure(figsize=(24,8))
for i,c in enumerate(carriers):
    plt.subplot(1,3,i+1)
    df2 = df1[ df1['carrier']==c].fillna(0)
    df2 = af.fix_params(df2, {nt:133})
    af.plot_stacked_costs(df2, km2, value_key='LCOE', suffix='_cLCOE',new_fig=False)
    plt.title(c)
    plt.ylim([0,100])
    plt.ylabel('EUR/MWh')
    

#%% INFIELD LENGTH


nts = np.sort( df[nt].unique() )
GWs = np.round( nts * 15 / 1e3 )
 
plt.figure()
for i, nti in enumerate( nts ) :
    dfgw = af.fix_params(dfhd, {nt:nti} )
    af.plot_best_y_for_x(dfgw, spacing, 'infield_length_km', 'LCOE',new_fig=False, fmt=f'C{i}o-')

plt.legend(GWs,title='Farm Capacity [GW]')
plt.xlim([0,10])



nts = np.sort( df[nt].unique() )
GWs = np.round( nts * 15 / 1e3 )
 
#plt.figure()
for i, nti in enumerate( nts ) :
    dfgw = af.fix_params(dfe, {nt:nti} )
    af.plot_best_y_for_x(dfgw, spacing, 'infield_length_km', 'LCOE',new_fig=False,fmt=f'o--C{i}')

plt.legend(GWs,title='Farm Capacity [GW] \n'+'Bold=Hydrogen, Dashed=Electric')
plt.xlim([0,10])
plt.ylim(bottom=0)
plt.ylabel('Infield Length [km]')
plt.title('Infield Length as function of spacing, wind farm capacity and configuration')


#%%
ilpmw = 'Infield Length per MW [km/MW]'
df[ilpmw] = df['infield_length_km'] / df['farm_capacity_MW']
ehs = ['electricity','hydrogen_decentral']

spr = 'Spacing [-] rounded'
round_to = 0.75 
df[spr] = ( df[spacing] / round_to ).round() * round_to

for c in ehs :
    
    dfc = df[df['carrier']==c]
    
    x,y = af.plot_best_y_for_x(dfc, spr, ilpmw, ilpmw,new_fig=False,)# fmt=f'C{i}o-')


#%% LCOE vs YIELD, per capacity


nts = np.sort( df[nt].unique() )
GWs = np.round( nts * 15 / 1e3 )
 
plt.figure()
for i, nti in enumerate( nts ) :
    dfgw = af.fix_params(dfhd, {nt:nti} )
    af.plot_best_y_for_x(dfgw, mkr, 'LCOE', 'LCOE',new_fig=False, fmt=f'C{i}o-')

plt.legend(GWs,title='Farm Capacity [GW]')
plt.xlim([0,200])



nts = np.sort( df[nt].unique() )
GWs = np.round( nts * 15 / 1e3 )
 
#plt.figure()
for i, nti in enumerate( nts ) :
    dfgw = af.fix_params(dfe, {nt:nti} )
    af.plot_best_y_for_x(dfgw, mkr, 'LCOE', 'LCOE',new_fig=False,fmt=f'o--C{i}')

plt.legend(GWs,title='Farm Capacity [GW]')
plt.xlim([0,200])

plt.ylim(bottom=0)

#%%

areas = np.sort( df[km2].unique() )
area = 200
dfa = af.fix_params(df, {km2:area})

plt.figure()
for c in carriers: 
    dfc = dfa[ dfa['carrier']==c]
    
    af.plot_best_y_for_x(dfc, mkr, 'LCOE', 'LCOE',new_fig=False)
plt.legend(carriers)


#%%

nts = np.sort( df[nt].unique() )
GWs = np.round( nts * 15 / 1e3 )
 

plt.figure()
for nti in nts :
    dfgw = af.fix_params(dfhd, {nt:nti} )
    af.plot_best_y_for_x(dfgw, mwkm, S, 'LCOE',new_fig=False)

plt.legend(GWs,title='Farm Capacity [GW]')
plt.xlim([0,200])


#%%



round_to = 0.05
df[mwkmr] = ( df[mwkm] / round_to).round() * round_to 

round_to = 0.05
df[mkr] = (df[mk] / round_to).round() * round_to

dfw = df[ df[mwkm]<=30 ]
x,y = af.plot_best_y_for_x(dfw, mwkmr, mkr , mkr , agg='max', fmt='o-') ; plt.close()
plt.figure(figsize=(8,4))

p = np.poly1d(np.polyfit(x, y, 3))   # polynomial fit
plt.plot( x, p(x), '-')    # data + fitted curve
plt.plot( x, x*y[0]/x[0], 'k--')
plt.title('Areal Yield [MWh/km2] vs Areal Capacity [GWh/km2/year]')
plt.xlabel(mwkm)
plt.ylabel(mk)
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.legend(['Calculated','Linear Increase'])

#%%



dfw = df[ df[mwkm]<=30 ]
x,y = af.plot_best_y_for_x(dfw, spacing ,cf , cf , agg='max', fmt='o-') ; plt.close()
plt.figure(figsize=(8,4))
p = np.poly1d(np.polyfit(x, y, 3))   # polynomial fit
plt.plot( x, p(x), '-')    # data + fitted curve
plt.xlabel(spacing)
plt.ylabel(cf)
plt.title('Farm Capacity Factor, as function of turbine Spacing')

#%%

d = 'Spacing [-]'
wl = 'Wake Losses [-]'

df[wl] = df['wake_loss_frac']
df[d] = np.sqrt( df['farm_area_km2'] / ( df['num_turbines'] * 0.236**2 ) )

dfw = df[ df[mwkm]<=30 ]
x,y = af.plot_best_y_for_x(dfw, d ,wl , cf , agg='max', fmt='o-') ; plt.close()
plt.figure(figsize=(8,4))
p = np.poly1d(np.polyfit(x, y, 3))   # polynomial fit
plt.plot( x, p(x), '-')    # data + fitted curve
plt.xlabel(d)
plt.ylabel(wl)
plt.title('Farm Capacity Factor, as function of turbine Spacing')


#%%

dfw = dfe[ dfe[mwkm]<=30 ]
x,y = af.plot_best_y_for_x(dfw, mkr , cf , 'LCOE', agg='min', fmt='o-') #; plt.close()
plt.figure(figsize=(8,4))
p = np.poly1d(np.polyfit(x, y*100, 3))   # polynomial fit
plt.plot( x, p(x), '-')    # data + fitted curve
plt.xlabel(mkr)
plt.ylabel(cf[:-3]+' [%]')
plt.title('Farm Capacity Factor vs Areal Yield')

#%% cost per mw

# component or section?
sc_value = 's'

#%% spacing and GW

gws = np.sort( df[gw].unique() )
carriers = df['carrier'].unique()
plt.figure(figsize=(24,8))
for i,c in enumerate(carriers):
    plt.subplot(1,3,i+1)
    dfc = df[ df['carrier']==c].fillna(0)
    
    for p in gws : 
    
        df2 = af.fix_params(dfc, {gw:p})
        af.plot_best_y_for_x(df2, spacing, 'total_pMW',value_key='LCOE' ,new_fig=False)
    plt.title(c)
    plt.ylim([0,5e6])
    plt.ylabel('EUR/MW')
    plt.xlabel('Spacing [-]')
    plt.legend(GWs,title='Farm Capacity [GW]')

#%% fix capacity , vary area
nt0 = 133

carriers = df['carrier'].unique()
plt.figure(figsize=(24,8))
for i,c in enumerate(carriers):
    plt.subplot(1,3,i+1)
    df2 = df[ df['carrier']==c].fillna(0)
    df2 = af.fix_params(df2, {nt:nt0})
    af.plot_stacked_costs(df2, km2, value_key='LCOE', suffix=f'_{sc_value}pMW',new_fig=False)
    plt.title(c)
    plt.ylim([0,5e6])
    plt.ylabel('EUR/MW')
    plt.xlabel('Farm Area [km2]')

#%% fix area , vary capacity
A0 = 200
carriers = df['carrier'].unique()
plt.figure(figsize=(24,8))
for i,c in enumerate(carriers):
    plt.subplot(1,3,i+1)
    df2 = df[ df['carrier']==c].fillna(0)
    df2 = af.fix_params(df2, {km2:A0})
    af.plot_stacked_costs(df2, gw, value_key='LCOE', suffix=f'_{sc_value}pMW',new_fig=False)
    plt.title(c)
    plt.ylim([0,5e6])
    plt.ylabel('EUR/MW')
    plt.xlabel('Farm Capacity [GW]')


#%% cost per NWh

#%% spacing and GW

gws = np.sort( df[gw].unique() )
carriers = df['carrier'].unique()
plt.figure(figsize=(24,8))
for i,c in enumerate(carriers):
    plt.subplot(1,3,i+1)
    dfc = df[ df['carrier']==c].fillna(0)
    
    for p in gws : 
    
        df2 = af.fix_params(dfc, {gw:p})
        af.plot_best_y_for_x(df2, spacing, 'LCOE',value_key='LCOE' ,new_fig=False)
    plt.title(c)
    plt.ylim([0,120])
    plt.ylabel('EUR/MWh')
    plt.xlabel('Spacing [-]')
    plt.legend(GWs,title='Farm Capacity [GW]')

#%% fix capacity , vary area

nt0 = 133

carriers = df['carrier'].unique()
plt.figure(figsize=(24,8))
for i,c in enumerate(carriers):
    plt.subplot(1,3,i+1)
    df2 = df[ df['carrier']==c].fillna(0)
    df2 = af.fix_params(df2, {nt:nt0})
    af.plot_stacked_costs(df2, km2, value_key='LCOE', suffix=f'_{sc_value}LCOE',new_fig=False)
    plt.title(c)
    plt.ylim([0,120])
    plt.ylabel('EUR/MWh')
    plt.xlabel('Farm Area [km2]')

#%% fix area , vary capacity

A0 = 200

carriers = df['carrier'].unique()
plt.figure(figsize=(24,8))
for i,c in enumerate(carriers):
    plt.subplot(1,3,i+1)
    df2 = df[ df['carrier']==c].fillna(0)
    df2 = af.fix_params(df2, {km2:A0})
    af.plot_stacked_costs(df2, gw, value_key='LCOE', suffix=f'_{sc_value}LCOE',new_fig=False)
    plt.title(c)
    plt.ylim([0,120])
    plt.ylabel('EUR/MWh')
    plt.xlabel('Farm Capacity [GW]')


#%%


def lower_hull( x , y ):
    
    # sort by x, then by y
    
    points = np.column_stack((x, y))
    
    pts = np.array(sorted(points.tolist()))
    
    # remove exact duplicates
    pts = np.unique(pts, axis=0)

    if len(pts) <= 2:
        return pts

    lower = []
    for p in pts:
        while len(lower) >= 2:
            a = np.array(lower[-2])
            b = np.array(lower[-1])
            c = p
            cross = (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
            if cross <= 0:
                lower.pop()
            else:
                break
        lower.append(tuple(p))
    lower= np.array(lower)
    
    xh = lower[:, 0]
    yh = lower[:, 1]
    return xh, yh
    
    

mkr1 = mk + ' r1'
round_to =  10
df[mkr1] = (df[mk] / round_to).round() * round_to

plt.figure('hull',figsize=(10,6))
for i,c in enumerate(carriers): 
    
    dfc = df[ df['carrier']==c]
    
    x,y = af.plot_best_y_for_x(dfc, mkr1, 'LCOE', 'LCOE',agg='min',new_fig=True,fmt=f'C{i}o--') 
    plt.close()
    
    plt.figure('hull')
    xh,yh = lower_hull(x, y)
    plt.plot(xh, yh, f'C{i}-' )
    

plt.figure('hull')
plt.legend(carriers)
plt.ylabel('LCOE [€/MWh]')
plt.xlabel(mk)
plt.ylim(bottom=0)


#%% RELATIVES


dft = df[ df[nt]==133 ]

dfte = dft[ dft['carrier']=='electricity' ]

i0 = dfte['LCOE'].idxmin()
row0 = dfte.loc[i0,:]



x_key = km2 
x0 = row0[x_key]


y_keys = [cpmw,cf,'LCOE']
for y_key in y_keys :
    x,y = af.plot_best_y_for_x(dfte, x_key, y_key, 'LCOE') ; plt.close()
    plt.figure('rel')
    y0 = row0[y_key]
    plt.plot( x , y / y0)


plt.plot(x0,1,'kx',markersize=10)

#plt.ylim([0.5,1.5])
plt.xlabel('Wind Farm Area')
plt.ylabel('Relative Value [-]')
plt.legend([cpmw,'Yield','LCOE'])

#%% 



dft = df[ df[km2]==200 ]

dfte = dft[ dft['carrier']=='electricity' ]

i0 = dfte['LCOE'].idxmin()
row0 = dfte.loc[i0,:]

x_key = nt 
x0 = row0[x_key]

y_keys = [cpmw,cf,'LCOE']
for y_key in y_keys :
    x,y = af.plot_best_y_for_x(dfte, x_key, y_key, 'LCOE') ; plt.close()
    plt.figure('rel2')
    y0 = row0[y_key]
    plt.plot( x , y / y0)

plt.plot(x0,1,'kx',markersize=10)

#plt.ylim([0.5,1.5])
plt.xlabel(nt)
plt.ylabel('Relative Value [-]')
plt.legend([cpmw,'Capacity Factor','LCOE'])








