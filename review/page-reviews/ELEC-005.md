# ELEC-005 — Onshore Grid Connection

## Review metadata

- **Source page:** [electrical_infra/onshore_grid_connection.qmd](../../electrical_infra/onshore_grid_connection.qmd)
- **Batch:** B3_electrical
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The physical chain, PCC concept, AC-current/reactive-power examples and
distinction between dedicated connection assets and wider reinforcement are
technically sound and clearly explained. The page intentionally leaves the
actual grid bay, site, land route and reinforcement costs unresolved, so the
architecture cannot yet reach its stated onshore-grid endpoint with a closed
CAPEX or feasibility result. Switchgear ownership and repeated converter
efficiency/availability also remain ambiguous across pages.

## 1. Model role and boundary

- **Purpose:** define the landfall-to-PCC chain, grid-code qualification and
  onshore costs not owned by converter/cable pages.
- **Included economically:** 380 kV bay/extension, project-assigned wider
  reinforcement, land/site and planning mitigation.
- **Referenced but owned elsewhere:** landfall/land cable and onshore converter.
- **Endpoint:** electricity delivered at the agreed PCC.

## 2. Upstream inputs

| Input | Unit | Classification | Status |
|---|---:|---|---|
| Export capacity/link count | MW; count | design result | discrete rule partly defined |
| Land cable route | km | site input | missing in base case |
| PCC and grid voltage | node; kV | scenario input | generic 380 kV only |
| Connection bay/reinforcement scope | asset list | grid-study result | missing |
| Converter efficiency/availability | dimensionless | repeated input | owned on ELEC-003 but repeated here |
| Site footprint | ha | sourced comparator | about 5.5 ha; not a design |

## 3. Calculation reconstruction

At 2 GW and 380 kV unity power factor,
$I=P/(\sqrt3V)=3.039$ kA. At power factor 0.95, $S=2.105$ GVA and
$Q=657$ MVAr; both reproduce. Link count is
$\lceil P_\mathrm{export}/2000\,\mathrm{MW}\rceil$. A future onshore cost sum
is shown, but four of its terms are TBD and the land route is absent.

### Boundary and limiting-case checks

- The selected PCC must accept the maximum credible loss of infeed and reactive
  capability; otherwise the scenario is infeasible or reinforcement is added.
- A zero land route is valid only if explicitly defined by co-location, not by
  omission.
- Switchgear must belong either to the converter package or grid-interface
  package, never both.
- Grid curtailment is a dispatch state, not asset unavailability.
- Multiple links may trigger non-linear bay, circuit and reinforcement steps.

## 4. Outputs and downstream consumers

| Output | Unit | Downstream consumer | Interface status |
|---|---:|---|---|
| Dedicated onshore CAPEX | EUR2025 | METH-002 | missing |
| Wider reinforcement CAPEX | EUR2025 | scenario/LCOE | excluded or TBD without rule |
| Land route inventory | km; sections | ELEC-004/INST-003 | missing |
| PCC feasibility/curtailment | state; MW-hours | METH-005/METH-006 | missing |
| Onshore loss/availability | MWh/year | METH-006 | duplicated from ELEC-003 |

## 5. Technical correctness

The AC arithmetic, terminology and EU grid-code qualification list are sound.
The page appropriately warns that one power factor cannot size the station.
Published reactive ratios are context, not a selected operating point. The
page does not yet convert the requirements into a scenario-specific converter
MVA/compensation or feasibility result.

## 6. Model fidelity

A full power-flow model is not necessary for every screening case, but each
scenario needs an explicit PCC class: accepted existing connection, bounded
connection package, or site-specific study/reinforcement. Treating all residual
costs as zero without such a scenario would bias electricity export.

## 7. Cost and evidence audit

The page correctly does not add the NREL onshore comparator to the DEA
converter pair. However, all project-owned residual costs are TBD. The legacy
code applies 150,000 per MW plus 2% OPEX as an onshore substation, while the page
has no adopted corresponding input or scope. The 80 km legacy sea route ends at
shore, leaving underground cable supply/installation at zero unless separately
entered.

## 8. Independent-implementer test

The electrical examples can be implemented; the project connection cannot.
Missing items are land route/site/PCC, bay and reinforcement asset counts/costs,
converter-package switchgear boundary, grid acceptance/curtailment rule and
canonical loss/availability ownership.

## 9. Explanation and site placement

The page is clear and correctly placed after export cables. Technical background
is proportionate. The main improvement is an adopted scenario/decision table,
not additional explanation of electrical terms.

## 10. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0064 | cross-page consistency | blocker | page and executable onshore ledgers differ | no |
| ISS-0067 | implementation readiness | blocker | underground route and cable material input missing | yes, DEC-0014 |
| ISS-0071 | cost completeness | blocker | project-owned onshore interface costs are all unresolved | yes, DEC-0014 |
| ISS-0072 | implementation readiness | blocker | PCC/grid scenario and acceptance rule are missing | yes, DEC-0014 |
| ISS-0073 | cost boundary | major | 380 kV switchgear may overlap converter scope | yes, DEC-0014 |
| ISS-0074 | cross-page consistency | major | onshore loss/availability has duplicate owners | no |
| ISS-0023 | implementation readiness | major | multi-link/partial-use treatment unresolved | yes, DEC-0005 |
| ISS-0025 | reference evidence | major | flat availability is unsupported | yes, DEC-0006 |

## 11. Page conclusion

- **Readiness:** blocked
- **Reason:** the stated PCC endpoint has no closed route, cost or acceptance
  scenario.
- **Open blockers:** 4 page-specific/shared
- **Open major issues:** 4 page-specific/inherited
- **Downstream consequences:** delivered electricity CAPEX, grid feasibility,
  curtailment and LCOE.
- **Recommended correction order:** decide base PCC/onshore scenario; define
  route and asset owners; cost dedicated interface; align code/performance;
  then add site-specific reinforcement branches.
