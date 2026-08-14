# -*- coding: utf-8 -*-
"""
scenario_workflow.py

High-level workflow for electricity / hydrogen scenarios using a Scenario class.

Created on Fri Nov 14 2025

@author: Victor
"""

# scenario_workflow.py
from __future__ import annotations

import json
from pathlib import Path
from dataclasses import asdict
from typing import Dict, Any, Optional, Protocol, Tuple
from collections import defaultdict

import yaml
import numpy as np
import pandas as pd

from scenario_types import Assumptions, Design, Derived, Results, Artifacts

from wind_calculations import compute_wind_pywake
from energy_calculations import (
    compute_electric_yields,
    compute_hydrogen_decentral_yields,
    compute_hydrogen_central_yields,
)


from turbine_cost_calculation import turbine_costs #el_turbine_costs, h2_turbine_costs
from hydrogen_cost_calculation import h2_central_hydrogen_costs, h2_decentral_hydrogen_costs
from infra_cost_calculation import (
    el_infield_cable_length, h2_infield_pipeline_length,
    el_infra_costs, 
    h2_central_infra_costs, h2_decentral_infra_costs
)
 


# -----------------------
# Param loading (once)
# -----------------------

def _load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return yaml.load(f, Loader=yaml.SafeLoader)

def load_all_params(assumptions: Assumptions) -> Dict[str, Dict[str, Any]]:
    return {
        "finance":   _load_yaml(assumptions.finance_params_path),
        "yield":     _load_yaml(assumptions.yield_params_path),
        "infra":    _load_yaml(assumptions.infra_params_path),
        "turbine":   _load_yaml(assumptions.turbine_params_path),
        "hydrogen":  _load_yaml(assumptions.hydrogen_params_path),
    }


# -----------------------
# Finance + flattener
# -----------------------

def _calc_crf(fin_params: Dict[str, Any]) -> float:
    wacc = fin_params["wacc"]
    lt = fin_params["lifetime_years"]
    return (wacc * (1 + wacc) ** lt) / ((1 + wacc) ** lt - 1)

#def _normalize_cost_keys(costs: Dict[str, float]) -> Dict[str, float]:
#    return {k.replace("-", "_"): v for k, v in costs.items()}

def analyze_costs_flat(
    data: Dict[str, float],
    yield_mwh: float,
    total_capacity_MW : float,
    fin_params: Dict[str, Any],
    include_decom: bool = True,
    allowed_costs: Optional[set] = None,
) -> Dict[str, float]:
    from collections import defaultdict

    BASE_COSTS = allowed_costs or {"capex", "installation", "decommissioning", "opex"}
    crf = _calc_crf(fin_params)
    
    
    # --- cheap validation to catch typos early (opes, platfrom, etc.)
    
    #bad_keys = []
    #for k in data.keys():
    #    if "_" not in k:
    #        bad_keys.append((k, "missing '_' delimiters"))
    #        continue
    #    section, rest = k.split("_", 1)
    #    if "_" not in rest:
    #        bad_keys.append((k, "missing trailing '_<costtype>'"))
    #        continue
    #    _, costtype = rest.rsplit("_", 1)
    #    if costtype not in BASE_COSTS:
    #        bad_keys.append((k, f"unknown costtype '{costtype}'"))
    #if bad_keys:
    #    msg = "Invalid cost keys detected:\n" + "\n".join([f"  - {k}: {why}" for k, why in bad_keys[:30]])
    #    raise ValueError(msg)

    def parse_key(key: str):
        """
        Robust parse: <section>_<component>_<costtype>
        - split on first "_" to get section
        - split on last "_" to get costtype
        Component may contain "_" or "-" safely.
        """
        if "_" not in key:
            return None
        section, rest = key.split("_", 1)
        if "_" not in rest:
            return None
        component, costtype = rest.rsplit("_", 1)
        if not section or not component or not costtype:
            return None
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

            flat[f"{section}_{component}_capex"] = capex_total
            flat[f"{section}_{component}_annual_capex"] = annual_capex
            flat[f"{section}_{component}_annual_opex"] = annual_opex
            flat[f"{section}_{component}_annual_total"] = annual_total
            flat[f"{section}_{component}_LCOE"] = LCOE

            flat[f"{section}_{component}_installation"] = installation
            flat[f"{section}_{component}_decommissioning"] = decommissioning
            flat[f"{section}_{component}_opex"] = opex

            for k in BASE_COSTS:
                section_totals[section][k] += ct.get(k, 0.0)

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

        flat[f"{section}_capex"] = capex_total
        flat[f"{section}_annual_capex"] = annual_capex
        flat[f"{section}_annual_opex"] = annual_opex
        flat[f"{section}_annual_total"] = annual_total
        flat[f"{section}_LCOE"] = LCOE

        flat[f"{section}_installation"] = installation
        flat[f"{section}_decommissioning"] = decommissioning
        flat[f"{section}_opex"] = opex

        for k in BASE_COSTS:
            grand_totals[k] += agg[k]

    capex = grand_totals["capex"]
    installation = grand_totals["installation"]
    decommissioning = grand_totals["decommissioning"]
    opex = grand_totals["opex"]

    capex_total = capex + installation + (decommissioning if include_decom else 0.0)
    annual_capex = capex_total * crf
    annual_opex = opex
    annual_total = annual_capex + annual_opex
    LCOE = (annual_total / yield_mwh) if yield_mwh > 0 else float("nan")

    flat["total_capex"] = capex_total
    flat["total_annual_capex"] = annual_capex
    flat["total_annual_opex"] = annual_opex
    flat["total_annual_total"] = annual_total
    flat["total_LCOE"] = LCOE

    flat["total_installation"] = installation
    flat["total_decommissioning"] = decommissioning
    flat["total_opex"] = opex
    
    flat["total_capex_per_MW"] = capex_total / float(total_capacity_MW)

    return flat

def analyze_costs_breakdown(
    data: Dict[str, float],
    yield_mwh: float,
    total_capacity_MW : float,
    fin_params: Dict[str, Any],
    include_decom: bool = True,
    allowed_costs: Optional[set[str]] = None,
    add_totals: bool = True,
) -> tuple[pd.DataFrame, Dict[str, float]]:
    """
    Returns:
      - df: tidy breakdown with columns:
            [level, section, component, costtype, cost_eur, annual_eur_per_year, lcoe, share_of_group, share_of_total]
      - flat: optional flattened dict for easy JSON export (same info but key-value)

    Notes:
      * cost_eur = raw input cost (capex/installation/decom are one-off; opex is annual)
      * annual_eur_per_year:
          - capex/installation/decommissioning are annualized via CRF
          - opex is assumed already annual
      * lcoe = annual_eur_per_year / yield_mwh
    """
    BASE_COSTS = allowed_costs or {"capex", "installation", "decommissioning", "opex"}
    crf = _calc_crf(fin_params)

    def parse_key(key: str) -> Optional[Tuple[str, str, str]]:
        if "_" not in key:
            return None
        section, rest = key.split("_", 1)
        if "_" not in rest:
            return None
        component, costtype = rest.rsplit("_", 1)
        if not section or not component or not costtype:
            return None
        if costtype not in BASE_COSTS:
            return None
        return section, component, costtype

    # costs[section][component][costtype] = eur
    costs = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for k, v in data.items():
        parsed = parse_key(k)
        if parsed is None:
            continue
        section, component, costtype = parsed
        costs[section][component][costtype] += float(v)

    # Helper: annualize one-off vs annual
    def annualize(costtype: str, eur: float) -> float:
        if costtype == "opex":
            return eur
        if costtype == "decommissioning" and (not include_decom):
            return 0.0
        return eur * crf

    rows = []

    # Component-level rows
    for section, comps in costs.items():
        for component, ct in comps.items():
            for costtype in BASE_COSTS:
                eur = float(ct.get(costtype, 0.0))
                ann = annualize(costtype, eur)
                lcoe = (ann / yield_mwh) if yield_mwh > 0 else float("nan")
                rows.append(
                    {
                        "level": "component",
                        "section": section,
                        "component": component,
                        "costtype": costtype,
                        "cost_eur": eur,
                        "annual_eur_per_year": ann,
                        "lcoe": lcoe,
                    }
                )

    

    df = pd.DataFrame(rows)
    if df.empty:
        return df, {}

    

    # --- add totals (section + total) by summing component rows
    if add_totals:
        section_df = (
            df.groupby(["section", "costtype"], as_index=False)[["cost_eur", "annual_eur_per_year"]]
            .sum()
            .assign(level="section", component="__total__")
        )
        section_df["lcoe"] = np.where(
            yield_mwh > 0, section_df["annual_eur_per_year"] / yield_mwh, np.nan
        )

        total_df = (
            df.groupby(["costtype"], as_index=False)[["cost_eur", "annual_eur_per_year"]]
            .sum()
            .assign(level="total", section="__total__", component="__total__")
        )
        total_df["lcoe"] = np.where(
            yield_mwh > 0, total_df["annual_eur_per_year"] / yield_mwh, np.nan
        )

        df = pd.concat([df, section_df[df.columns], total_df[df.columns]], ignore_index=True)

    # --- shares
    # share within group (group = (level, section, component))
    group_totals = df.groupby(["level", "section", "component"])["annual_eur_per_year"].transform("sum")
    df["share_of_group"] = np.where(group_totals > 0, df["annual_eur_per_year"] / group_totals, np.nan)

    # share of grand total annual cost (using the TOTAL row)
    grand_total = float(
        df.loc[(df["level"] == "total") & (df["costtype"].isin(list(BASE_COSTS))), "annual_eur_per_year"].sum()
    )
    df["share_of_total"] = np.where(grand_total > 0, df["annual_eur_per_year"] / grand_total, np.nan)
    
    # --- capex per MW (one-off costs only)
    if total_capacity_MW is not None and total_capacity_MW > 0:
        df["eur_per_MW"] = np.where(
            df["costtype"].isin(["capex", "installation", "decommissioning"]),
            df["cost_eur"] / float(total_capacity_MW),
            np.nan,
        )
    else:
        df["eur_per_MW"] = np.nan
    
    # --- also provide a flattened dict for JSON / your existing Results storage
    flat: Dict[str, float] = {}
    for r in df.itertuples(index=False):
        # prefix: component rows use section_component, section totals use section, total uses total
        if r.level == "component":
            prefix = f"{r.section}_{r.component}"
        elif r.level == "section":
            prefix = f"{r.section}"
        else:
            prefix = "total"

        # store annual contribution + lcoe contribution + shares
        flat[f"{prefix}_annual_{r.costtype}"] = float(r.annual_eur_per_year)
        flat[f"{prefix}_LCOE_{r.costtype}"] = float(r.lcoe)
        # shares as fraction (0-1)
        flat[f"{prefix}_share_group_{r.costtype}"] = float(r.share_of_group) if pd.notna(r.share_of_group) else float("nan")
        flat[f"{prefix}_share_total_{r.costtype}"] = float(r.share_of_total) if pd.notna(r.share_of_total) else float("nan")

        # optional: raw eur (one-off/annual as provided)
        flat[f"{prefix}_raw_{r.costtype}"] = float(r.cost_eur)
        
        # capex-like eur/MW (only if the column exists and is not nan)
        if hasattr(r, "eur_per_MW"):
            flat[f"{prefix}_eur_per_MW_{r.costtype}"] = float(r.eur_per_MW) if pd.notna(r.eur_per_MW) else float("nan")

    return df, flat

# -----------------------
# Cost input dict builder
# -----------------------

def build_cost_input_dict(design: Design, derived: Derived) -> Dict[str, Any]:
    d = asdict(design)
    d.update({
        "P_oss_max_MW": derived.P_oss_max_MW,
       # "P_elx_max_MW": derived.P_elx_max_MW,
      #  "export_capacity_MW": derived.export_capacity_MW,
        "H2_export_capacity_kgph": derived.H2_export_capacity_kgph,
        "elx_export_capacity_MW": derived.elx_export_capacity_MW,
        "compressor_turbine_power_kW_max": derived.compressor_turbine_power_kW_max,

        "infield_total_cable_length_m": derived.infield_total_cable_length_m,
        "infield_vertical_cable_length_m": derived.infield_vertical_cable_length_m,
        "infield_horizontal_cable_length_m": derived.infield_horizontal_cable_length_m,

        "infield_total_pipeline_length_m": derived.infield_total_pipeline_length_m,
        "infield_vertical_pipeline_length_m": derived.infield_vertical_pipeline_length_m,
        "infield_horizontal_pipeline_length_m": derived.infield_horizontal_pipeline_length_m,
    })
    return d


# -----------------------
# Carrier models
# -----------------------


class CarrierModel(Protocol):
    def compute_yields(self, design: Design, assumptions: Assumptions, derived: Derived, artifacts: Artifacts, params: Dict[str, Dict[str, Any]]) -> None: ...
    def compute_infrastructure(self, design: Design, assumptions: Assumptions, derived: Derived, params: Dict[str, Dict[str, Any]]) -> None: ...
    def compute_costs(self, design: Design, derived: Derived, params: Dict[str, Dict[str, Any]]) -> Dict[str, float]: ...
    def yield_mwh(self, derived: Derived) -> float: ...

class ElectricityModel:
    def compute_yields(self, design: Design, assumptions: Assumptions, derived: Derived, artifacts: Artifacts, params: Dict[str, Dict[str, Any]]) -> None:
        compute_electric_yields(design, derived, params["yield"])


    def compute_infrastructure(self, design: Design, assumptions: Assumptions, derived: Derived, params: Dict[str, Dict[str, Any]]) -> None:
        scn = build_cost_input_dict(design, derived)
        lens = el_infield_cable_length(scn, params["infra"])
        derived.infield_horizontal_cable_length_m = lens["infield_horizontal_cable_length_m"]
        derived.infield_vertical_cable_length_m = lens["infield_vertical_cable_length_m"]
        derived.infield_total_cable_length_m = lens["infield_total_cable_length_m"]

    def compute_costs(self, design: Design, derived: Derived, params: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        scn = build_cost_input_dict(design, derived)
        costs = {}
        costs |= turbine_costs(scn, params["turbine"])
        costs |= el_infra_costs(scn, params["infra"])
        return costs

    def yield_mwh(self, derived: Derived) -> float:
        return float(derived.electric_yield_farm_MWh or 0.0)

class HydrogenDecentralModel:
    def compute_yields(self, design: Design, assumptions: Assumptions, derived: Derived, artifacts: Artifacts, params: Dict[str, Dict[str, Any]]) -> None:
        compute_hydrogen_decentral_yields(design, assumptions, derived, artifacts, params["yield"])

    def compute_infrastructure(self, design: Design, assumptions: Assumptions, derived: Derived, params: Dict[str, Dict[str, Any]]) -> None:
        scn = build_cost_input_dict(design, derived)
        lens = h2_infield_pipeline_length(scn, params["infra"])
        derived.infield_horizontal_pipeline_length_m = lens["infield_horizontal_pipeline_length_m"]
        derived.infield_vertical_pipeline_length_m = lens["infield_vertical_pipeline_length_m"]
        derived.infield_total_pipeline_length_m = lens["infield_total_pipeline_length_m"]

    def compute_costs(self, design: Design, derived: Derived, params: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        scn = build_cost_input_dict(design, derived)
        costs: Dict[str, float] = {}
        costs |= turbine_costs(scn, params["turbine"])
        costs |= h2_decentral_hydrogen_costs(scn, params["hydrogen"])
        costs |= h2_decentral_infra_costs(scn, params["infra"])

        nep = costs.get("infra_num_export_pipelines")
        if nep is not None:
            derived.num_export_pipelines = int(nep)
        return costs

    def yield_mwh(self, derived: Derived) -> float:
        return float(derived.h2_export_MWh or 0.0)
    
class HydrogenCentralModel:
    def compute_yields(self, design: Design, assumptions: Assumptions, derived: Derived, artifacts: Artifacts, params: Dict[str, Dict[str, Any]]) -> None:
        compute_hydrogen_central_yields(design, assumptions, derived, artifacts, params["yield"])

        if design.stack_overplant_factor is None:
            raise ValueError("hydrogen_central requires design.stack_overplant_factor")

    def compute_infrastructure(self, design: Design, assumptions: Assumptions, derived: Derived, params: Dict[str, Dict[str, Any]]) -> None:
        # Central uses electric-style infield cables (not H2 infield pipelines)
        scn = build_cost_input_dict(design, derived)
        lens = el_infield_cable_length(scn, params["infra"])
        derived.infield_horizontal_cable_length_m = lens["infield_horizontal_cable_length_m"]
        derived.infield_vertical_cable_length_m = lens["infield_vertical_cable_length_m"]
        derived.infield_total_cable_length_m = lens["infield_total_cable_length_m"]

    def compute_costs(self, design: Design, derived: Derived, params: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        scn = build_cost_input_dict(design, derived)
        costs: Dict[str, float] = {}
        costs |= turbine_costs(scn, params["turbine"])
        costs |= h2_central_hydrogen_costs(scn, params["hydrogen"])
        costs |= h2_central_infra_costs(scn, params["infra"])

        nep = costs.get("infra_num_export_pipelines")
        if nep is not None:
            derived.num_export_pipelines = int(nep)
        return costs

    def yield_mwh(self, derived: Derived) -> float:
        return float(derived.h2_export_MWh or 0.0)

CARRIER_MODELS: Dict[str, CarrierModel] = {
    "electricity": ElectricityModel(),
    "hydrogen_decentral": HydrogenDecentralModel(),
    "hydrogen_central": HydrogenCentralModel(),
}


# -----------------------
# Scenario
# -----------------------

class Scenario:
    def __init__(self, design: Design, assumptions: Optional[Assumptions] = None):
        self.design = design
        self.assumptions = assumptions or Assumptions()
        self.derived = Derived()
        self.results = Results()
        self.artifacts = Artifacts()

        # load all YAML once for this run (or share across scenarios by passing in)
        self.params = load_all_params(self.assumptions)

    @property
    def scenario_id(self) -> str:
        return self.design.scenario_id()

    def run(
        self,
        save_artifacts: bool = True,
    ) -> None:
        sid = self.scenario_id

        total_capacity_MW = float(self.design.num_turbines * self.design.turbine_capacity_MW)

        wind_d, wind_art = compute_wind_pywake(self.design, self.assumptions)
        self.derived.__dict__.update(wind_d.__dict__)

        # store wind artifacts
        self.artifacts.layout_x = wind_art["layout_x"]
        self.artifacts.layout_y = wind_art["layout_y"]
        self.artifacts.wind_wd = wind_art["wind_wd"]
        self.artifacts.wind_ws = wind_art["wind_ws"]

        self.artifacts.pywake_farm_power_wake_kW = wind_art["pywake_farm_power_wake_kW"]

        model = CARRIER_MODELS.get(self.design.carrier)
        if model is None:
            raise ValueError(f"Unknown carrier: {self.design.carrier}")

        # --- yields + infra
        model.compute_yields(self.design, self.assumptions, self.derived, self.artifacts, self.params)
        model.compute_infrastructure(self.design, self.assumptions, self.derived, self.params)

        # --- costs
        base_costs = model.compute_costs(self.design, self.derived, self.params)
        #base_costs = _normalize_cost_keys(base_costs)

        y = model.yield_mwh(self.derived)

        cf = analyze_costs_flat(base_costs, yield_mwh=y, total_capacity_MW = total_capacity_MW, fin_params=self.params["finance"])
        self.results.costs_flat = cf
        self.results.total_LCOE = float(cf.get("total_LCOE")) if cf else None
        self.results.total_capex_EUR = float(cf.get("total_capex")) if cf else None
        self.results.total_annual_capex_EUR_per_year = float(cf.get("total_annual_capex")) if cf else None
        self.results.total_annual_opex_EUR_per_year = float(cf.get("total_annual_opex")) if cf else None
        self.results.total_annual_cost_EUR_per_year = float(cf.get("total_annual_total")) if cf else None
        
        df_break, cf2 = analyze_costs_breakdown(
            base_costs,
            yield_mwh=y,
            total_capacity_MW = total_capacity_MW,
            fin_params=self.params["finance"],
            include_decom=True,
        )

        # store the flattened dict (JSON-friendly) + optional parquet artifact
        self.results.costs_breakdown_flat = cf2

        # if you want the tidy table for analysis/plotting later:
        self.artifacts.costs_breakdown = df_break  # (if Artifacts allows)
