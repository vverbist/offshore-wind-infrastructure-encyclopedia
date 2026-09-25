"""Physical section inventory with explicitly selected healthy-state flow paths.

The existing ladder requires a declared flow allocation. No redundancy benefit
or equal split between headers is inferred. Inactive physical edges are retained
for supply and installation, while the active directed network must be acyclic.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from model.records import Infeasible


def section_inventory(path: Path, coordinates: pd.DataFrame, nodes: pd.DataFrame,
                      hydrogen_kg_h: np.ndarray, sink: str) -> tuple[pd.DataFrame, np.ndarray]:
    sections = pd.read_csv(path, dtype={"section": str, "from": str, "to": str})
    required = {"section", "from", "to", "vertical_m", "route_allowance", "flow_share", "diameter_m", "inlet_bar", "outlet_bar"}
    if not required.issubset(sections) or sections.section.duplicated().any():
        raise ValueError("Hydrogen sections need unique IDs and the documented section columns")
    if nodes.node.duplicated().any() or not np.isfinite(nodes[["x_m", "y_m"]]).all().all():
        raise ValueError("Network nodes need unique IDs and finite positions")
    positions = {str(r.node): (r.x_m, r.y_m) for r in nodes.itertuples()}
    for row in coordinates.itertuples():
        if row.turbine in positions:
            raise ValueError("Turbine and manifold node IDs overlap")
        positions[row.turbine] = (row.x_m, row.y_m)
    if sink not in positions:
        raise ValueError("Delivery node missing from node inventory")
    shares = sections.flow_share.to_numpy(float)
    if not np.isfinite(shares).all() or (shares < 0).any() or (shares > 1).any():
        raise ValueError("Flow shares must lie between zero and one")
    sources = {r.turbine: hydrogen_kg_h[:, i] for i, r in enumerate(coordinates.itertuples())}
    outgoing = {node: sections.index[(sections["from"] == node) & (sections.flow_share > 0)].tolist() for node in positions}
    incoming = {node: 0 for node in positions}
    lengths = []
    for index, row in sections.iterrows():
        start, end = row["from"], row["to"]
        if start not in positions or end not in positions:
            raise ValueError("A pipeline endpoint is absent from the coordinate inventory")
        if min(row.vertical_m, row.route_allowance) < 0:
            raise ValueError("Pipeline lengths and allowances must be non-negative")
        horizontal = np.linalg.norm(np.array(positions[start]) - np.array(positions[end])) / 1000
        lengths.append(horizontal * (1 + row.route_allowance) + row.vertical_m / 1000)
        if row.flow_share > 0:
            incoming[end] += 1
    balance = {node: np.array(sources.get(node, np.zeros(hydrogen_kg_h.shape[0])), dtype=float) for node in positions}
    queue = [node for node, degree in incoming.items() if degree == 0]
    flows = np.zeros((hydrogen_kg_h.shape[0], len(sections)))
    visited = []
    while queue:
        node = queue.pop(0)
        visited.append(node)
        edges = outgoing[node]
        if node != sink and (node in sources or np.any(balance[node])):
            if not np.isclose(sum(shares[i] for i in edges), 1):
                raise Infeasible(f"Hydrogen flow at {node} is not fully routed to the delivery node")
        if node == sink and edges:
            raise ValueError("The delivery node must not have outgoing active sections")
        for i in edges:
            end = sections.loc[i, "to"]
            flows[:, i] = balance[node] * shares[i]
            balance[end] += flows[:, i]
            incoming[end] -= 1
            if incoming[end] == 0:
                queue.append(end)
    if len(visited) != len(positions):
        raise Infeasible("Active hydrogen routes contain a cycle; supply a directed operating arrangement")
    if not np.allclose(balance[sink], hydrogen_kg_h.sum(axis=1)):
        raise Infeasible("Hydrogen network does not conserve delivery flow")
    sections["physical_km"] = lengths
    sections["peak_kg_h"] = flows.max(axis=0)
    return sections, flows
