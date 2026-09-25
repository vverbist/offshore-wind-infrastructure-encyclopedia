"""One non-overlapping availability factor per owned production/transport boundary."""
import numpy as np


def annual_energy(power_kw: np.ndarray, hours: np.ndarray) -> float:
    return float(np.dot(power_kw, hours) / 1000)


def delivered_mass(production_kg_h: np.ndarray, hours: np.ndarray,
                   production_factors: np.ndarray, transport_factor: float) -> float:
    """Each location loses its own expected production, not the whole farm's output.

    Aggregate factors do not simulate failure-state redispatch or redundancy.
    """
    if (np.any(production_factors < 0) or np.any(production_factors > 1)
            or not 0 <= transport_factor <= 1):
        raise ValueError("Availability must lie between zero and one")
    return float(np.dot(production_kg_h @ production_factors, hours) * transport_factor)
