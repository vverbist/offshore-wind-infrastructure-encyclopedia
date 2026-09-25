"""Deterministic capacity checks at supplied pressures; no optimiser."""
from .hydrogen_pipelines import capacity_kg_h, export_count
from model.records import Infeasible


def check_sections(sections, inputs):
    result = sections.copy()
    capacities = [capacity_kg_h(row.diameter_m, row.inlet_bar, row.outlet_bar,
                                row.physical_km * 1000, inputs) for row in sections.itertuples()]
    result["capacity_kg_h"] = capacities
    result["capacity_margin_kg_h"] = result.capacity_kg_h - result.peak_kg_h
    if (result.capacity_margin_kg_h < 0).any():
        failed = result.loc[result.capacity_margin_kg_h < 0, "section"].tolist()
        raise Infeasible(f"Pipeline section capacity exceeded: {failed}")
    # Junction pressure must support every active downstream segment.
    active = result[result.flow_share > 0]
    for _, incoming in active.iterrows():
        outgoing = active[active["from"] == incoming["to"]]
        if (outgoing.inlet_bar > incoming.outlet_bar).any():
            raise Infeasible(f"Pressure increases at junction {incoming['to']} without a compressor")
    return result
