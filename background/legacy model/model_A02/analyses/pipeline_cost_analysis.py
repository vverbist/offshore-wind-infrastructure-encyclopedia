# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 11:00:16 2026

@author: VictorVerbist
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import hub_optimisation.analysis_functions as af

from pipeline_cost_curve import pipeline_cost_curve
from infra_cost_calculation import h2_export_pipeline_capacity

Ps = np.arange(80, 155, 5)
Ds = np.arange(4,9,1) #np.linspace(4, 10, 20)

P_grid, D_grid = np.meshgrid(Ps, Ds)

cost_grid = pipeline_cost_curve(P_grid, D_grid)

vec_capacity = np.vectorize(h2_export_pipeline_capacity)
capacity_grid = vec_capacity(D_grid, P_grid)

df = pd.DataFrame({
    "P": P_grid.ravel(),
    "D": D_grid.ravel(),
    "cost": cost_grid.ravel(),
    "capacity": capacity_grid.ravel()
})

#%%

df['cost_per_capacity'] = df['cost'] / df['capacity']


#%%

plt.figure()
for d in Ds :
    dfd = af.fix_params( df , {"D":d})
    af.plot_best_y_for_x(dfd, 'P', 'capacity','capacity',agg='max',new_fig=False)
plt.legend(Ds,title='Pipeline Diameter [inch]')
plt.title('Pipeline Capacity as function of Diameter and Pressure')
plt.ylabel('Capacity [kg/h]')
plt.xlabel('Inlet Pressure [bar]')

plt.figure()
for d in Ds :
    dfd = af.fix_params( df , {"D":d})
    af.plot_best_y_for_x(dfd, 'P', 'cost','capacity',agg='max',new_fig=False)
plt.legend(Ds,title='Pipeline Diameter [inch]')
plt.title('Pipeline Cost [€/m] as function of Diameter and Pressure')
plt.ylabel('Cost [€/m]')
plt.xlabel('Inlet Pressure [bar]')

plt.figure()
for d in Ds :
    if d==4 : continue
    dfd = af.fix_params( df , {"D":d})
    af.plot_best_y_for_x(dfd, 'P', 'cost_per_capacity','capacity',agg='max',new_fig=False)
plt.legend(Ds,title='Pipeline Diameter [inch]')
plt.title('Pipeline Specific Cost [€/m/(kg/h)] as function of Diameter and Pressure')
plt.ylabel('Specific Cost [€/m/(kg/h)]')
plt.xlabel('Inlet Pressure [bar]')

#%%

def plot_cost_heatmap( ):
    plt.figure()
    im = plt.imshow(
        cost_grid,
        origin="lower",
        aspect="auto",
        extent=[Ps.min(), Ps.max(), Ds.min(), Ds.max()]
    )
    plt.xlabel("Pressure (bar)")
    plt.ylabel("Diameter (inch)")
    plt.title("Pipeline Cost – 2D Linear Regression")
    plt.colorbar(im, label="Cost (€)")
    plt.show()

def plot_capacity_heatmap():
    plt.figure()
    im = plt.imshow(
        capacity_grid,
        origin="lower",
        aspect="auto",
        extent=[Ps.min(), Ps.max(), Ds.min(), Ds.max()]
    )
    plt.xlabel("Pressure (bar)")
    plt.ylabel("Diameter (inch)")
    plt.title("Pipeline Capacity")
    plt.colorbar(im, label="Capacity [kg/h]")
    plt.show()

def plot_cpc_heatmap():
    
    x_col= 'D' 
    y_col = 'P'
    value_col = 'cost_per_capacity'
    # Pivot to grid
    pivot = df.pivot(index=y_col, columns=x_col, values=value_col)

    # Ensure sorted axes
    pivot = pivot.sort_index().sort_index(axis=1)

    x_vals = pivot.columns.values
    y_vals = pivot.index.values
    Z = pivot.values
    
    plt.figure()
    im = plt.imshow(
        Z,
        origin="lower",
        aspect="auto",
        extent=[x_vals.min(), x_vals.max(), y_vals.min(), y_vals.max()],
        cmap = 'viridis_r',
        vmin = 0.01 , vmax = 0.05,
    )
    plt.ylabel("Pressure (bar)")
    plt.xlabel("Diameter (inch)")
    plt.title("Pipeline Specific Cost [€/(kg/h)/m]")
    plt.colorbar(im, label="Specific Cost [€/(kg/h)/m]")
    plt.show()

plot_cpc_heatmap()

#%%





