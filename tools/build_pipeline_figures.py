from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from CoolProp.CoolProp import PropsSI

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def h2_export_pipeline_capacity( 
    D_inch: float,
    P_in_bar: float,
    L_m : float = 80e3,
    eps_surface_roughness_m: float=1.5e-7,
    P_out_bar: float=66,
    T_K: float=293,
) -> float:
    """
    Returns hydrogen pipeline capacity in kg/h using Colebrook equation 
    
    [1] Transition Accelerator : https://transitionaccelerator.ca/wp-content/uploads/2023/06/The-Techno-Economics-of-Hydrogen-Pipelines-v2.pdf
    
    [2] Perry's Handbook: https://mathguy.us/BySubject/Chemistry/Perrys_Chemical_Engineers_Handbook.pdf
    Eqns: (6-38) with (6-32) and (6-33) [8th Edition]

    Note: [1] uses f as Darcy-Weisbach friction factor, [2] uses f as Fanning friction factor.
    Difference is factor 4. Here [2]'s Fanning fricion factor is used (eqn 6-32)

    Parameters
    ----------
    D_inch : inner diameter [inch]
    Pin_bar : inlet absolute pressure [bar]
    L_m : pipeline length [m]
    f_darcy : Darcy friction factor [-]
    Pout_Pa : outlet absolute pressure [bar]
    T_K : temperature [K]

    Returns
    -------
    Capacity [kg/h] as float
    """
    
    if P_in_bar <= P_out_bar:
        raise ValueError("Pin_Pa must be greater than Pout_Pa.")
    
    # unit conversions and renaming
    D_m = D_inch * 0.0254
    P_in_Pa  = P_in_bar  * 1e5
    P_out_Pa = P_out_bar * 1e5
    
    eps = eps_surface_roughness_m
    dP = P_in_Pa - P_out_Pa
    
    # from here on: everthing in SI units
    
    # Calculate average Pressure, using Transition Accelerator method, eqn (4)
    P_avg_Pa = (2/3) * ( ( P_in_Pa**3 - P_out_Pa**3) / ( P_in_Pa**2 - P_out_Pa**2)  )
    # get density and viscosity at this avg pressure
    rho_avg = PropsSI('D', "T", T_K, "P", P_avg_Pa , "Hydrogen" ) # density, kg/m3
    mu_avg  = PropsSI('V', "T", T_K, "P", P_avg_Pa , "Hydrogen" ) # viscosity, kg/(m.s)
    
    # Calc Re * sqrt(f), using (6-32) and (6-33) 
    Re_sqrt_f = D_m**(3/2) / mu_avg * np.sqrt( (dP*rho_avg)/(2*L_m) )
    
    # Calc 1/sqrt(f), eqn ( 6-38 )
    sqrt_f_inv = -4 * np.log10( eps/(3.7*D_m) + 1.256/Re_sqrt_f )
    
    # Calc v using eqn (6-32)
    v = np.sqrt( (D_m*dP)/(2*rho_avg*L_m) ) * sqrt_f_inv
    
    # Convert speed to mass flow
    A_m2 = np.pi/4 * D_m**2
    m_dot_kgs = rho_avg * A_m2 * v 
    m_dot_kgh = m_dot_kgs * 3600
    
    return m_dot_kgh


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = PROJECT_ROOT / "figures"
HHV_H2_KWH_PER_KG = 39.4

if "pipeline_cost_curve" not in globals():
    try:
        from pipeline_cost_curve import pipeline_cost_curve
    except ModuleNotFoundError:
        pipeline_cost_curve = None


def build_pipeline_data():
    Ps = np.arange(80, 155, 5)
    Ds = np.arange(4, 9, 1)
    P_grid, D_grid = np.meshgrid(Ps, Ds)

    vec_capacity = np.vectorize(h2_export_pipeline_capacity)
    capacity_grid = vec_capacity(D_grid, P_grid)

    df = pd.DataFrame({
        "P": P_grid.ravel(),
        "D": D_grid.ravel(),
        "capacity_kg_h": capacity_grid.ravel(),
    })
    df["capacity_mw_hhv"] = df["capacity_kg_h"] * HHV_H2_KWH_PER_KG / 1000

    cost_grid = None
    if pipeline_cost_curve is not None:
        cost_grid = pipeline_cost_curve(P_grid, D_grid)
        df["cost"] = cost_grid.ravel()
        df["cost_per_capacity"] = df["cost"] / df["capacity_kg_h"]

    return df, cost_grid


def plot_capacity_curves(df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.4))

    for diameter in sorted(df["D"].unique()):
        dfd = df[df["D"] == diameter].sort_values("P")
        ax.plot(
            dfd["P"],
            dfd["capacity_mw_hhv"],
            marker="o",
            linewidth=2,
            label=f"{diameter:.0f} inch",
        )

    ax.set_title("Hydrogen Pipeline Capacity")
    ax.set_xlabel("Inlet pressure [bar]")
    ax.set_ylabel("Capacity [MW HHV]")
    ax.grid(True, color="#d1d5db", linewidth=0.8)
    ax.legend(title="Diameter")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_redacted_specific_cost(df: pd.DataFrame, output_path: Path) -> None:
    pivot = df.pivot(index="P", columns="D", values="cost_per_capacity")
    pivot = pivot.sort_index().sort_index(axis=1)

    values = pivot.values.astype(float)
    values = values / np.nanmin(values)

    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    ax.imshow(values, origin="lower", aspect="auto", cmap="viridis_r")
    ax.set_axis_off()
    ax.set_title("Relative Material Cost per Transport Capacity", pad=12)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    df, cost_grid = build_pipeline_data()

    capacity_path = FIGURE_DIR / "pipeline-capacity-vs-pressure.svg"
    plot_capacity_curves(df, capacity_path)
    print(f"Wrote {capacity_path.relative_to(PROJECT_ROOT)}")

    if cost_grid is None:
        print("Skipped cost figure: pipeline_cost_curve is not available.")
        return

    cost_path = FIGURE_DIR / "pipeline-specific-cost-redacted.svg"
    plot_redacted_specific_cost(df, cost_path)
    print(f"Wrote {cost_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

