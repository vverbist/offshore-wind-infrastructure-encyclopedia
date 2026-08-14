# -*- coding: utf-8 -*-
"""
Scenario workflow for electricity / hydrogen cases

Created on Fri Nov 14 2025

@author: VictorVerbist (+ ChatGPT)
"""

import yaml
import numpy as np
import pandas as pd
from collections import defaultdict
from typing import Dict, Optional, Tuple

from scipy.stats import weibull_min
from math import ceil
from scipy.interpolate import interp1d

# === YOUR EXISTING COST / YIELD MODULES ===============================
from turbine_cost_calculation import el_turbine_costs, h2_turbine_costs
from hydrogen_cost_calculation import h2_hydrogen_costs
from farm_cost_calculation import el_farm_costs, h2_farm_costs
from export_cost_calculation import el_export_costs, h2_export_costs
from yield_calculation import electric_yield  # you can keep/replace this
from energy_calculations import compute_wind_production_from_weibull, hydrogen_chain_from_weibull
# If you already have a wind_production_calculation module you prefer, you can
# swap the Weibull-based functions below with imports from there.


# ---------------------------------------------------------------------
# 1. COST FLATTENER (your existing code, unchanged)
# ---------------------------------------------------------------------
def analyze_costs_flat(
    data: Dict[str, float],
    yield_mwh: float,
    include_decom: bool = True,
    allowed_costs: Optional[set] = None,
):
    BASE_COSTS = allowed_costs or {"capex", "installation", "decommissioning", "opex"}
    DERIVED_COSTS = ["capex", "annual_capex", "annual_opex", "annual_total", "LCOE"]
    
    with open("finance_params.yaml", "r") as f:
        fin_params = yaml.load(f, Loader=yaml.SafeLoader)
    wacc = fin_params["wacc"]
    lt = fin_params["lifetime_years"]
    crf = (wacc * (1 + wacc) ** lt) / ((1 + wacc) ** lt - 1)
    
    
    def parse_key(key: str):
        parts = key.split("_")
        if len(parts) != 3:
            return None
        section, component, costtype = parts
        if costtype not in BASE_COSTS:
            return None
        return section, component, costtype

    costs = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for k, v in data.items():
        parsed = parse_key(k)
        if parsed:
            section, component, costtype = parsed
            costs[section][component][costtype] += float(v)

    flat: Dict[str, float] = {}
    section_totals = defaultdict(lambda: defaultdict(float))
    grand_totals = defaultdict(float)

    # per-component
    for section, comps in costs.items():
        for component, ct in comps.items():
            capex = ct.get("capex", 0.0)
            installation = ct.get("installation", 0.0)
            decommissioning = ct.get("decommissioning", 0.0)
            opex = ct.get("opex", 0.0)

            capex_total = capex + installation + (decommissioning if include_decom else 0.0)
            annual_capex = capex_total * crf
            annual_opex = opex
            annual_total = annual_capex + annual_opex
            LCOE = (annual_total / yield_mwh) if yield_mwh > 0 else float("nan")

            per_comp = {
                "capex": capex_total,
                "annual_capex": annual_capex,
                "annual_opex": annual_opex,
                "annual_total": annual_total,
                "LCOE": LCOE,
                "installation": installation,
                "decommissioning": decommissioning,
                "opex": opex,
            }

            for kname, val in per_comp.items():
                flat[f"{section}_{component}_{kname}"] = val

            for k in BASE_COSTS:
                section_totals[section][k] += ct.get(k, 0.0)

    # per-section
    for section, agg in section_totals.items():
        capex = agg["capex"]
        installation = agg["installation"]
        decommissioning = agg["decommissioning"]
        opex = agg["opex"]

        capex_total = capex + installation + (decommissioning if include_decom else 0.0)
        annual_capex = capex_total * crf
        annual_opex = opex
        annual_total = annual_capex + annual_opex
        LCOE = (annual_total / yield_mwh) if yield_mwh > 0 else float("nan")

        per_sec = {
            "capex": capex_total,
            "annual_capex": annual_capex,
            "annual_opex": annual_opex,
            "annual_total": annual_total,
            "LCOE": LCOE,
            "installation": installation,
            "decommissioning": decommissioning,
            "opex": opex,
        }

        for kname, val in per_sec.items():
            flat[f"{section}_{kname}"] = val

        for k in BASE_COSTS:
            grand_totals[k] += agg[k]

    # totals
    capex = grand_totals["capex"]
    installation = grand_totals["installation"]
    decommissioning = grand_totals["decommissioning"]
    opex = grand_totals["opex"]

    capex_total = capex + installation + (decommissioning if include_decom else 0.0)
    annual_capex = capex_total * crf
    annual_opex = opex
    annual_total = annual_capex + annual_opex
    LCOE = (annual_total / yield_mwh) if yield_mwh > 0 else float("nan")

    totals = {
        "capex": capex_total,
        "annual_capex": annual_capex,
        "annual_opex": annual_opex,
        "annual_total": annual_total,
        "LCOE": LCOE,
        "installation": installation,
        "decommissioning": decommissioning,
        "opex": opex,
    }

    for kname, val in totals.items():
        flat[f"total_{kname}"] = val

    return flat







# ---------------------------------------------------------------------
# 6. (c)+(d) HIGH-LEVEL SCENARIO RUNNER
# ---------------------------------------------------------------------
def run_scenario(
    scn: Dict,
) -> Dict:
    """
    Run a full scenario:
      a) wind production
      b) onshore yield (electric or H2)
      c) infrastructure costs
      d) levelized cost

    Returns a dict with:
      - "wind_results"
      - "yield_results"
      - "costs_flat"
      - optional "h2_states", "h2_summary" if carrier == hydrogen
    """

    carrier = scn.get("carrier", "electricity")
    turbine_power_MW = scn["turbine_capacity_MW"]
    num_turbines = scn["num_turbines"]

    # (a) Gross wind production from Weibull
    wind_results = compute_wind_production_from_weibull( scn )

    # (b) Yield onshore
    yield_results = {}
    h2_states = None
    h2_summary = None

    if carrier == "electricity":
        # keep your current logic: electric_yield(scn) already includes
        # availability, wake, etc. Adjust scaling if needed.
        net_el_yield_MWh = electric_yield(scn)  # you had /10; keep that if needed
        yield_results["energy_carrier"] = "electricity"
        yield_results["net_yield_MWh"] = net_el_yield_MWh

        # design value for export sizing (HVAC/HVDC)
        scn["export_capacity_MW"] = scn["farm_capacity_MW"]

        # Assemble costs
        costs_dict = (
            el_turbine_costs(scn)
            | el_farm_costs(scn)
            | el_export_costs(scn)
        )
        costs_flat = analyze_costs_flat(
            costs_dict, net_el_yield_MWh
        )

    elif carrier == "hydrogen":
        stack_size_MW = scn["stack_size_MW"]

        # Hydrogen chain from Weibull, including intermediates
        h2_states, h2_summary = hydrogen_chain_from_weibull(scn)

        # Expected H2 production [kg/h] and annual [kg/year]
        H2_kgph_expected = h2_summary.loc["H2_kgph", "expected"]
        H2_kg_year = H2_kgph_expected * 8760.0

        # Convert to MWh-equivalent for LCOH denominator
        H2_yield_MWh = H2_kg_year * 39.44 / 1000.0

        yield_results["energy_carrier"] = "hydrogen"
        yield_results["H2_kg_year"] = H2_kg_year
        yield_results["H2_yield_MWh"] = H2_yield_MWh

        # Design values feeding into cost modules
        scn["H2_export_capacity_kgph"] = h2_summary.loc["H2_kgph", "max"]
        scn["elx_export_capacity_MW"] = h2_summary.loc["stack_power_kW", "max"] / 1e3

        # Turbine + farm + hydrogen plant + export
        h2_costs_dict = (
            h2_turbine_costs(scn)
            | h2_hydrogen_costs(scn)
            | h2_farm_costs(scn)
            | h2_export_costs(scn)
        )
        costs_flat = analyze_costs_flat(
            h2_costs_dict, H2_yield_MWh
        )

    else:
        raise ValueError(f"Unknown carrier type: {carrier}")

    return {
        "carrier": carrier,
        "scenario": scn,
        "wind_results": wind_results,
        "yield_results": yield_results,
        "costs_flat": costs_flat,
        "h2_states": h2_states,
        "h2_summary": h2_summary,
    }


# ---------------------------------------------------------------------
# 7. EXAMPLE USAGE
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Example Weibull-per-sector params (fit separately and save to CSV)
    

    

    # Scenario definition
    scn_h2 = {
        "num_turbines": 134,
        "turbine_capacity_MW": 15.0,
        "farm_capacity_MW": 15.0 * 134,
        "carrier": "hydrogen",
        "stack_size_MW": 30.0,
        # add whatever your cost modules expect (distance, water depth, etc.)
    }

    scn_el = {
        "num_turbines": 134,
        "turbine_capacity_MW": 15.0,
        "farm_capacity_MW": 15.0 * 134,
        "carrier": "electricity",
        # any extra inputs for el_* cost functions
    }

    res_h2 = run_scenario(scn_h2)
    res_el = run_scenario(scn_el)

    print("\n=== ELECTRICITY LCOE ===")
    for key in ["turbine_LCOE", "farm_LCOE", "export_LCOE", "total_LCOE"]:
        if key in res_el["costs_flat"]:
            print(f"{key}: {res_el['costs_flat'][key]:.2f} €/MWh")

    print("\n=== HYDROGEN LCOH (in €/MWh_H2_eq) ===")
    for key in ["turbine_LCOE", "farm_LCOE", "export_LCOE", "total_LCOE"]:
        if key in res_h2["costs_flat"]:
            print(f"{key}: {res_h2['costs_flat'][key]:.2f} €/MWh_H2_eq")
