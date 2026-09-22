# ARCH-004 — Decentralised Hydrogen

## Review metadata

- **Source page:** [architectures/decentralised_hydrogen.qmd](../../architectures/decentralised_hydrogen.qmd)
- **Batch:** B1_frame
- **Reviewer:** Codex
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Model role and boundary

The page clearly defines turbine-integrated electrolysis, local compression,
hydrogen infield collection and pipeline export. It explicitly removes the
grid-side inverter, step-up transformer, AC array network, central platform and
HVDC chain. That component-led comparison is clear and well placed.

The direct stack-to-turbine-DC-link assumption is stated rather than hidden,
and the compressor remains separately accounted even though it is physically
associated with the turbine. This is good scope control.

## Implementation gaps

The physical chain is not completely closed at the junction between the two
infield headers and the export pipeline. H2I-002 explicitly excludes the export
manifold and header-to-export connections, while neither this page nor the
component mapping assigns an owner. Connection count, sizing, pressure loss,
material, installation, cost and availability are therefore missing
(ISS-0029).

The onshore hydrogen-backbone connection has the same unowned interface gap as
the centralised architecture (ISS-0028). In addition, turbine-level equipment
masses must pass into turbine structure, foundation and installation models;
those downstream pages already expose several missing electrical and hydrogen
equipment masses. These are legitimate downstream blockers and should remain
with their component owners.

## Findings

| Issue | Severity | Finding |
|---|---|---|
| ISS-0029 | Blocker | Export manifold/header connections have no owner |
| ISS-0028 | Major | Onshore hydrogen connection has no component model |

## Conclusion

- **Readiness:** blocked
- **Open blockers:** 1
- **Open major issues:** inherited ISS-0028
- **Recommended correction order:** assign and define the export manifold;
  define the onshore connection; then validate all turbine-level mass handoffs.
