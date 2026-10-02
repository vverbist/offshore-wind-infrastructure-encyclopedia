"""Technical-scope LCOH; unresolved included categories block the complete metric."""
from model.records import CostLine
from .financial_and_price_basis import annual_cost


EXCLUSIONS = ["development", "shared owner engineering", "insurance", "owner contingency",
              "construction finance and tax", "downstream storage, distribution and end use"]


def summarize(costs: list[CostLine], delivered_kg: float | None, inputs) -> dict:
    categories = ("supply", "installation", "epci", "annual_opex", "replacement", "decommissioning")
    for line in costs:
        if line.category not in categories or (line.amount_eur is not None and line.amount_eur < 0):
            raise ValueError("Invalid cost ledger entry")
    if len({(c.component, c.category) for c in costs}) != len(costs):
        raise ValueError("Duplicate component/category in cost ledger")
    epci_owners = {c.component for c in costs if c.category == "epci"}
    if any(c.component in epci_owners and c.category in {"supply", "installation"} for c in costs):
        raise ValueError("EPCI cannot be combined with separate supply or installation for the same component")
    output = {"cost_scope": "technical scope", "excluded_costs": EXCLUSIONS,
              "price_basis": "constant EUR2025", "lcoh_eur_kg": None}
    for category in categories:
        rows = [c for c in costs if c.category == category]
        output[f"known_{category}_subtotal_eur"] = sum(c.amount_eur for c in rows if c.amount_eur is not None)
    if not costs or any(c.amount_eur is None for c in costs) or delivered_kg is None or delivered_kg <= 0:
        return output
    initial = (output["known_supply_subtotal_eur"] + output["known_installation_subtotal_eur"]
               + output["known_epci_subtotal_eur"])
    output.update(annual_cost(initial, output["known_replacement_subtotal_eur"],
                              output["known_installation_subtotal_eur"], output["known_annual_opex_subtotal_eur"], inputs,
                              additional_decommissioning_eur=output["known_decommissioning_subtotal_eur"]))
    output["initial_capex_eur"] = initial
    output["lcoh_eur_kg"] = output["annual_cost_eur"] / delivered_kg
    output["lcoh_eur_mwh_hhv"] = output["lcoh_eur_kg"] * 1000 / inputs.positive("hydrogen-hhv", "kWh/kg")
    return output
