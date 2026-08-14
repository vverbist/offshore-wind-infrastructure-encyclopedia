import numpy as np
import matplotlib.pyplot as plt



# -----------------------
# Cost function
# -----------------------
def pipeline_cost_curve(P_bar, D_inch):
    """
    

    Parameters 
    ---------- 
    P_bar : float 
        Rated pressure [bar] 
    
    D_inch : float 
        Pipeline diameter [inch]
    
    Returns 
    ------- 
        Price Pipeline material price [€/m]

    """
    a = -64.2348
    b =  29.5775
    c = - 1.8456
    d =   0.4771
    return a + b*D_inch + c*P_bar + d*D_inch*P_bar


# -----------------------
# Heatmap
# -----------------------
if __name__ == "__main__":
    # -----------------------
    # Data
    # -----------------------
    DATA = np.array([
        (4,  21,  57.50),
        (4,  52,  87.50),
        (4, 156, 130.00),
        (5,  17,  67.50),
        (5,  42, 102.50),
        (5, 156, 150.00),
        (5, 286, 252.50),
        (6,  36, 125.00),
        (6, 134, 165.00),
        (6, 244, 292.50),
        (7,  24, 200.00),
        (7,  95, 270.00),
        (7, 166, 445.00),
        (8,  82, 320.00),
        (8, 143, 520.00),
    ], dtype=float)

    D = DATA[:, 0]
    P = DATA[:, 1]
    C = DATA[:, 2]

    # -----------------------
    # Build regression matrix
    # Model: C = a + bD + cP + d(D·P)
    # -----------------------
    X = np.column_stack([
        np.ones_like(D),  # intercept
        D,
        P,
        D * P
    ])

    # Least squares solution
    beta, *_ = np.linalg.lstsq(X, C, rcond=None)

    a, b, c, d = beta

    print("Regression coefficients:")
    print(f"a = {a:.4f}")
    print(f"b = {b:.4f}")
    print(f"c = {c:.4f}")
    print(f"d = {d:.6f}")
    Ps = np.arange(20, 200, 5)
    Ds = np.linspace(4, 10, 50)

    P_grid, D_grid = np.meshgrid(Ps, Ds)

    C_grid = pipeline_cost_curve(P_grid, D_grid)

    plt.figure()
    im = plt.imshow(
        C_grid,
        origin="lower",
        aspect="auto",
        extent=[Ps.min(), Ps.max(), Ds.min(), Ds.max()]
    )
    plt.xlabel("Pressure (bar)")
    plt.ylabel("Diameter (inch)")
    plt.title("Pipeline Cost – 2D Linear Regression")
    plt.colorbar(im, label="Cost (€)")
    plt.show()
