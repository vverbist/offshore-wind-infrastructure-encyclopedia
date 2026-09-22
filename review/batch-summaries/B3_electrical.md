# Batch 3 review — Electrical infrastructure

## Scope

Reviewed and reconciled on 2026-08-21:

- `electrical_infra/overview.qmd`;
- `electrical_infra/infield_ac_cables.qmd` (existing pilot review integrated);
- `electrical_infra/hvdc_converter_stations.qmd`;
- `electrical_infra/hvdc_export_cables.qmd`; and
- `electrical_infra/onshore_grid_connection.qmd`.

No source `.qmd`, model code or source parameter file was changed. The review
artifacts remain the handoff to a separately approved correction stage.

## Outcome

| Result | Count |
|---|---:|
| Pages reviewed | 5 |
| Partially implementable overview pages | 1 |
| Blocked calculation pages | 4 |
| B3 issues including cable pilot | 28 |
| Blockers | 12 |
| Major issues | 14 |
| Moderate issues | 2 |
| New issues added in this completion pass | 14 |
| B3-specific decisions proposed | 4 |

The section has a strong physical and accounting structure. Its pages clearly
separate equipment supply from installation, distinguish reference costs from
booked costs, and repeatedly warn against double-counting loss or availability.
The integrated electrical model is nevertheless blocked because the written
pages, legacy executable, physical installation inventories and onshore endpoint
do not yet describe one closed system.

## Most important result

The adopted converter cost contains a confirmed transformation error. The
Danish Energy Agency catalogue gives 320 EUR/kW as the 2025 central value for
one 1.5–2 GW onshore DC converter station, with 250–420 EUR/kW as the 2025
range. The page escalates those 2025 values again by 1.22621 and reports 392
EUR2025/kW per terminal and 785 EUR2025/kW for the pair.

Before any separate offshore premium, direct application of the source gives:

| Item | Correct use of DEA 2025 values | Current page |
|---|---:|---:|
| One terminal, central | 320 EUR/kW | 392 EUR/kW |
| Two-terminal pair, central | 640 EUR/kW | 785 EUR/kW |
| Pair range | 500–840 EUR/kW | 613–1,030 EUR/kW |

The current central pair is therefore about 22.6% above the direct source value
because of double escalation (ISS-0061). This correction does not resolve the
separate uncertainty from applying an onshore coefficient offshore
(ISS-0062).

## Review by criterion

### Technical correctness

Verified relationships:

- the 2 GW, ±525 kV balanced-bipole current is 1.905 kA;
- two terminal efficiencies of 98.5% multiply to 97.0225%;
- the cable-loss equation $2I^2R'L$ and all four printed distance examples
  reproduce;
- 0.5% conductor loss occurs at about 191 km under the stated R20 assumptions;
- the onshore 2 GW/380 kV current is 3.039 kA at unity power factor; and
- at 0.95 power factor, the examples reproduce at 2.105 GVA and 657 MVAr.

Technical corrections/gaps:

- the converter cost is escalated twice (ISS-0061);
- the cable time-series equation calls for $R'(T)$ but provides no operating-
  temperature rule, and degraded pole/metallic-return loss is absent
  (ISS-0068);
- the onshore requirements are informative but no selected PCC or grid-
  acceptance constraint makes them executable (ISS-0072); and
- the documented component loss/availability chain is not the one implemented
  in the legacy yield model (ISS-0064).

### Model approach: accuracy versus complexity

The chosen screening approach is broadly appropriate:

- one standard 2 GW TenneT link;
- aggregate converter-terminal cost and loss;
- load-dependent cable $I^2R$ loss;
- discrete 2 GW link and pole-capacity states; and
- a qualification gate rather than a detailed power-flow study for every case.

More detailed valve, electromagnetic or grid-dynamic simulation is not needed
at this stage. The minimum additional fidelity is physical and discrete:

- complete 66 kV feeder/bay topology;
- full/partial 2 GW link utilisation and cost rules;
- converter block mass/lift records;
- one record per cable and route segment;
- healthy/half-capacity/common-outage states; and
- a declared onshore connection class or PCC scenario.

### Cost inputs and references

Strong practices to preserve:

- green booked costs versus grey comparators;
- route-km versus cable-km distinction;
- separate material and installation owners; and
- explicit non-additivity of programme/EPC comparators.

Unresolved cost inputs:

- correct converter basis and offshore electrical premium (ISS-0061/0062);
- converter equipment mass needed by the separate platform cost
  (ISS-0063);
- cable material price year and topology/accessory scope (ISS-0065/0066);
- underground cable material and route (ISS-0067);
- grid bay, site, land and project-assigned reinforcement (ISS-0071); and
- component OPEX scopes/evidence (ISS-0070 and pilot ISS-0009).

The legacy executable uses materially different values: 1,000,000 per MW for
the offshore converter, 150,000 per MW for the onshore substation, 5.5 million
per route-km for cable supply, and unsupported CAPEX-percentage OPEX. Those
values cannot be treated as implementation of the reviewed pages.

### Explanation and directness

The electrical overview and scope tables are excellent. The pages explain
physical versus accounting boundaries directly, and the technical background
on current, reactive power and grid requirements is proportionate.

The main clarity issue is calculation status. Several pages read as complete
models before revealing that core outputs are TBD. Corrections should put a
compact “adopted inputs / unresolved outputs” ledger near the beginning of each
calculation page. No page move or broad rewrite is needed.

### Independent model development

An implementer can reproduce:

- turbine/string count arithmetic for a chosen infield rating;
- the converter and AC-current equations;
- the printed cable losses; and
- the documented cost-conversion arithmetic, including identifying the DEA
  error.

They cannot independently produce the complete electricity-export result. The
minimum missing information is:

| Missing item | Consequence | Finding |
|---|---|---|
| deterministic radial topology/substation point | infield length and loss absent | ISS-0001 |
| pull-ins, conductor allocation and array loss | supply/installation/energy incomplete | ISS-0002/0003/0006 |
| bay-compatible collection design | reference 34 strings cannot terminate | ISS-0004 |
| partial final-link rule | capacity and CAPEX threshold ambiguous | ISS-0023 |
| corrected/offshore converter cost | converter CAPEX not adoptable | ISS-0061/0062 |
| converter equipment mass/blocks | platform/installation blocked | ISS-0063 |
| controlled cable cost and physical inventory | supply/installation blocked | ISS-0065/0066/0069 |
| land route and material coefficient | chain stops at shore | ISS-0067 |
| R(T) and degraded cable path | annual cable loss incomplete | ISS-0068 |
| dedicated PCC package and acceptance scenario | onshore endpoint infeasible/unpriced | ISS-0071/0072 |
| canonical executable parameter ledger | page results cannot be reproduced in code | ISS-0064 |

### General site and cross-page structure

The navigation order and page placement are logical. ELEC-001 is the right
place for the ownership matrix. No new page is strictly required.

Cross-page corrections are needed:

- central-hydrogen collection switchgear remains without an applicable owner
  despite the overview mapping (ISS-0012);
- immediate converter AC switchgear and the TSO/grid bay overlap in wording
  (ISS-0073);
- onshore terminal efficiency and availability are repeated on ELEC-003 and
  ELEC-005 even though ELEC-003 is the declared owner (ISS-0074);
- converter/cable states have no combined availability ledger (ISS-0024/0025);
  and
- installation pages need physical inventories that the component pages do
  not yet emit.

## Coverage

| Page ID | Readiness | Blockers | Major issues | Review note |
|---|---|---:|---:|---|
| ELEC-001 | Partially implementable | 1 | 0 | Strong overview; execution and one owner remain open |
| ELEC-002 | Blocked | 4 | 8 | Existing pilot: topology, pull-ins, losses and bay closure block result |
| ELEC-003 | Blocked | 3 | 3 | Cost error, offshore proxy, mass and code alignment |
| ELEC-004 | Blocked | 4 | 5 | Price year, land route, inventory and loss states |
| ELEC-005 | Blocked | 4 | 4 | PCC route, residual CAPEX and performance ownership |

Counts include material inherited/shared issues shown on each page and should
not be summed to reproduce the 28 unique B3 issues.

## Decisions required

| Decision ID | Question | Main consequence of delay |
|---|---|---|
| DEC-0001 | Which reference string, topology and platform/bay design applies? | array length and the 34-string platform incompatibility remain open |
| DEC-0002 | Should cable cost remain blended or follow segment conductor classes? | cable cost and installation mass remain physically inconsistent |
| DEC-0013 | How is offshore converter cost and physical equipment booked? | converter/platform CAPEX and installation remain open |
| DEC-0014 | What base onshore route/PCC connection scenario applies? | architecture stops at shore and grid feasibility/cost remain open |

Inherited decisions DEC-0005 (search and partial 2 GW link treatment) and
DEC-0006 (availability accounting) must be resolved during the same correction
sequence. DEC-0004 governs OPEX/replacement/decommissioning cash flows.

## Proposed correction sequence

| Correction batch | Scope | Issues | Decisions | Validation |
|---|---|---|---|---|
| C3.1 Electrical reference and executable ledger | correct DEA cost; select converter basis; define link utilisation; align page/code parameter owners | ISS-0061–0064; ISS-0023 | DEC-0013; DEC-0005 | source-cost reproduction; full/partial/multiple-link regression; code/page parity |
| C3.2 AC collection closure | topology, substation point, bay-compatible design, conductor sections, pull-ins and losses | ISS-0001–0008; ISS-0011/0012 | DEC-0001; DEC-0002 | worked array; feasibility thresholds; loss and installation interfaces |
| C3.3 HVDC cable system | price basis, matched topology, marine/land segments, inventory and loss states | ISS-0065–0069 | DEC-0014 | route/cable-km conservation; R20/Roperating tests; degraded pole-return case |
| C3.4 Onshore endpoint | PCC class, land route, bay/TSO boundary, dedicated cost and reinforcement/curtailment branch | ISS-0071–0074 | DEC-0014 | zero-route only when explicit; weak/strong node scenarios; ownership audit |
| C3.5 Lifecycle and availability | OPEX/repair scope and combined 100/50/0% capacity states | ISS-0009/0010; ISS-0024/0025; ISS-0070 | DEC-0004; DEC-0006 | no double derating; event/state limiting cases; lifecycle cash-flow test |

After correction, render all five electrical pages plus affected methodology,
architecture, platform and installation pages; then render the full site because
the ownership and navigation tables are shared conventions.

## Records created or updated

- New detailed reviews: `ELEC-001.md`, `ELEC-003.md`, `ELEC-004.md` and
  `ELEC-005.md`; existing `ELEC-002.md` retained and integrated.
- New issues: ISS-0061 to ISS-0074.
- New inputs: INP-0092 to INP-0124.
- New dependencies: DEP-0060 to DEP-0076.
- New decisions: DEC-0013 and DEC-0014; pilot decisions DEC-0001 and DEC-0002
  remain part of B3.
