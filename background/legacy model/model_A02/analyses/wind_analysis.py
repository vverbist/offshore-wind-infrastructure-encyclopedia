# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 14:02:50 2025

@author: VictorVerbist
"""

import yaml
import pandas as pd
import numpy as np
from math import ceil, floor
from scipy.interpolate import interp1d
from scipy.stats import weibull_min
from scipy.special import gamma
import matplotlib.pyplot as plt
#%%

excel_file = "WRA+H2-E_victor.xlsx"
df = pd.read_excel(excel_file,sheet_name='WRA',usecols='A:S')

#%%

# df['v'] contains wind speeds in m/s
wind = df['v'].dropna()

# Fit Weibull distribution
# floc=0 forces the distribution to start at 0 (physically correct for wind)
shape_k, loc, scale_c = weibull_min.fit(wind, floc=0)

print("Shape k:", shape_k)
print("Scale c:", scale_c)

#%%

# Histogram
counts, bins, _ = plt.hist(wind, bins=60, density=True, alpha=0.8)

# Weibull PDF
x = np.linspace(0, max(wind), 500)
pdf = weibull_min.pdf(x, shape_k, 0, scale_c)

plt.plot(x, pdf, linewidth=2)
plt.xlabel("Wind speed [m/s]")
plt.ylabel("Probability density")
plt.title("Weibull Fit")
plt.grid(True)

#%%

df['sector'] = (df['Direction'] // 30) * 30

sector_fits = {}

for sector, sub in df.groupby('sector'):
    wind = sub['v'].dropna()
    k, _, c = weibull_min.fit(wind, floc=0)
    sector_fits[sector] = {'k': k, 'c': c}

sector_fits

#%%



def fit_weibull_by_sector(df, n_dir=12):
    """
    Fit Weibull(k, c) per direction sector and return a DataFrame
    with one row per sector.
    """
    sector_width = 360 / n_dir

    df = df.copy()
    df['Direction'] = df['Direction'] % 360
    df['sector_deg'] = np.floor(df['Direction'] / sector_width) * sector_width

    sector_centers_deg = np.sort(df['sector_deg'].unique())

    records = []
    total_count = len(df)

    for sector in sector_centers_deg:
        sub = df[df['sector_deg'] == sector]['v'].dropna()
        n = len(sub)

        if n < 10:     # too few data points → mark as empty sector
            records.append({
                "sector_deg": sector,
                "freq": 0.0,
                "k": np.nan,
                "c": np.nan,
                "mean_speed": np.nan,
                "n_samples": n
            })
            continue

        # Fit Weibull with loc=0
        k, loc, c = weibull_min.fit(sub, floc=0)

        # Relative frequency
        freq = n / total_count

        # Mean wind speed from Weibull
        mean_speed = c * gamma(1.0 + 1.0 / k)

        records.append({
            "sector_deg": sector,
            "freq": freq,
            "k": k,
            "c": c,
            "mean_speed": mean_speed,
            "n_samples": n
        })

    params_df = pd.DataFrame.from_records(records)

    # Optional: ensure frequencies sum to 1 (small numerical corrections)
    total_freq = params_df['freq'].sum()
    if total_freq > 0:
        params_df['freq'] /= total_freq

    return params_df


def save_weibull_params(params_df, path="weibull_per_sector.csv"):
    """
    Save the Weibull-per-sector parameters to CSV.
    """
    params_df.to_csv(path, index=False)
    print(f"Weibull parameters saved to: {path}")



params_df = fit_weibull_by_sector(df, n_dir=12)
save_weibull_params(params_df, "weibull_per_sector.csv")



#%%
# 1. Parameters for the wind rose
N_DIR = 12                     # number of direction sectors (e.g. 12 → 30° each)
sector_width = 360 / N_DIR

# Make sure directions are between 0 and 360
df = df.copy()
df['Direction'] = df['Direction'] % 360

# 2. Assign each sample to a direction sector (0, 30, 60, ..., 330)
df['sector_deg'] = (np.floor(df['Direction'] / sector_width) * sector_width)

# For plotting, use sector *centers* in radians
sector_centers_deg = df['sector_deg'].unique()
sector_centers_deg = np.sort(sector_centers_deg)
sector_centers_rad = np.deg2rad(sector_centers_deg + sector_width / 2)

# Prepare containers
freq = []        # relative frequency per sector
mean_speed = []  # Weibull mean wind speed per sector
k_list = []      # shape parameters
c_list = []      # scale parameters

total_count = len(df)

for sector in sector_centers_deg:
    sub = df[df['sector_deg'] == sector]['v'].dropna()
    n = len(sub)
    if n < 10:   # skip sectors with too few points (tweak threshold if you like)
        freq.append(0)
        mean_speed.append(0)
        k_list.append(np.nan)
        c_list.append(np.nan)
        continue

    # 3. Fit Weibull to wind speeds in this sector
    k, loc, c = weibull_min.fit(sub, floc=0)   # loc fixed at 0
    k_list.append(k)
    c_list.append(c)

    # Relative frequency for this sector
    freq.append(n / total_count)

    # Mean wind speed of a Weibull: E[v] = c * Γ(1 + 1/k)
    m = c * gamma(1.0 + 1.0 / k)
    mean_speed.append(m)

freq = np.array(freq)
mean_speed = np.array(mean_speed)

# 4. Plot polar bar chart (wind rose)
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, polar=True)

# Start from North (π/2) and go clockwise (typical for met wind roses)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)

# Bar plot: angle = sector center, height = frequency
bars = ax.bar(
    sector_centers_rad,
    freq,
    width=np.deg2rad(sector_width * 0.9),   # small gap between bars
    bottom=0.0,
)

# 5. Color bars by Weibull mean speed
# Avoid division by zero in case some sectors have no data
mean_speed_safe = np.where(mean_speed > 0, mean_speed, np.nan)

# Use a colormap – higher mean speed → darker color
cmap = plt.cm.viridis
norm = plt.Normalize(np.nanmin(mean_speed_safe), np.nanmax(mean_speed_safe))

for bar, m in zip(bars, mean_speed):
    if m == 0 or np.isnan(m):
        bar.set_alpha(0.1)
        bar.set_facecolor('lightgray')
    else:
        bar.set_facecolor(cmap(norm(m)))

# Colorbar for mean speed
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, pad=0.1)
cbar.set_label("Weibull mean wind speed [m/s]")

# Some cosmetics
ax.set_title("Weibull Wind Rose (frequency by direction, color = mean speed)", pad=20)
ax.set_rlabel_position(225)   # move radial labels away from N
ax.grid(True)

plt.tight_layout()


















