"""Canonical simple-CRF convention, with undiscounted replacement/decommissioning."""
from decimal import Decimal
from model_data.parameters import capital_recovery_factor


def annual_cost(initial_eur: float, replacement_eur: float, installation_eur: float,
                opex_eur_year: float, inputs, additional_decommissioning_eur: float = 0) -> dict:
    """Explicit package decommissioning supplements the separate-installation proxy."""
    if min(initial_eur, replacement_eur, installation_eur, opex_eur_year, additional_decommissioning_eur) < 0:
        raise ValueError("Cost categories must be non-negative")
    years = inputs.positive("financial-project-life", "year")
    if not years.is_integer():
        raise ValueError("Project life must be an integer number of years")
    crf = float(capital_recovery_factor(Decimal(str(inputs.number("financial-real-wacc", "fraction/year"))), int(years)))
    decommissioning = (installation_eur * inputs.number("financial-decommissioning-fraction", "fraction")
                       + additional_decommissioning_eur)
    lifecycle = initial_eur + replacement_eur + decommissioning
    return {"crf": crf, "decommissioning_eur": decommissioning,
            "lifecycle_capital_eur": lifecycle, "annual_cost_eur": crf * lifecycle + opex_eur_year}


def normalize_usd(cost: float, escalation: float, inputs) -> float:
    if escalation <= 0:
        raise ValueError("Source-price escalation factor must be positive")
    return cost * escalation / inputs.positive("financial-usd-per-eur-2025", "USD/EUR")
