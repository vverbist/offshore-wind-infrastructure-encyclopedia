# Batch 5 review — Hydrogen infrastructure and platform material CAPEX

## Scope

Reviewed and reconciled on 2026-08-21:

- `hydrogen_infra/overview.qmd`;
- `hydrogen_infra/infield_infrastructure.qmd`;
- `hydrogen_infra/compressor.qmd`;
- `hydrogen_infra/hydrogen_pipelines.qmd`;
- `hydrogen_infra/pipeline_pressure_and_capacity.qmd`; and
- `platforms/platform_material_capex.qmd`.

No source `.qmd`, model code, confidential input or generated site file was
changed. The review artifacts remain the handoff to a separately approved
correction stage.

## Outcome

| Result | Count |
|---|---:|
| Pages reviewed | 6 |
| Partially implementable overview pages | 1 |
| Blocked pages | 5 |
| Unique material B5 issues including inherited findings | 27 |
| Blockers | 18 |
| Major issues | 9 |
| New issues added in B5 | 15 |
| New B5-specific decisions proposed | 3 |

The section has a strong conceptual structure. It correctly couples compressor
pressure, pipeline capacity, discrete pipeline count and installation cost,
and its component pages generally state their scope and limitations directly.
The model is not yet a closed physical or economic chain. The current
calculation can generate smooth compressor and pipeline curves, but those
curves do not yet map to qualified train packages, manufactured pipe classes,
complete installation inventories or an auditable platform structure.

## Most important results

### 1. Pipeline capacity method is not the cited gas-flow method

The cited [Transition Accelerator General Flow Equation](https://transitionaccelerator.ca/wp-content/uploads/2023/06/The-Techno-Economics-of-Hydrogen-Pipelines-v2.pdf) makes gas flow
proportional to the square root of the difference in squared **absolute**
pressures. The current page/code instead applies a linear pressure difference
to gas density evaluated at one average pressure and then uses a rearranged
Fanning-friction relation. No derivation or benchmark establishes that
alternative over the candidate range, and no maximum/erosional-velocity gate
is applied (ISS-0084).

The current executable gives approximately 437 MW HHV for the stated 6 inch,
150-to-66 bar, 80 km case. The page's approximate 500 MW assumption is close
enough as historical context but cannot qualify infield rungs or headers,
whose lengths, outlet pressures and accumulated flows differ by section.

### 2. Pipeline material cost is neither interpolation nor publicly auditable

The page calls the confidential cost relation a two-dimensional interpolation.
The controlled local implementation is a global bilinear least-squares
regression. Against its confidential quote points, the fit has approximately
19% mean absolute percentage error and approximately 51% maximum error. The
coefficients are intentionally excluded from version control, and the page
does not state price year, quote boundary or fit diagnostics (ISS-0087).

Confidential evidence can be used in a governed internal model, but it cannot
support the site's stated independent-reproduction purpose without a public
validation/fallback basis and controlled version metadata. The model also
smoothly prices operating pressure instead of selecting a discrete rated pipe
class, erasing a material product threshold (ISS-0088).

### 3. Compressor cost extrapolation can predetermine centralisation

The compression-energy structure is broadly appropriate. The 30-to-150 bar
case uses two stages and the figure-builder implementation gives approximately
0.86 kWh/kg H2. The page does not state perfect intercooling and uses a
different `Z` averaging rule from legacy code, so exact reproduction still
requires one controlled property method (ISS-0079).

The larger issue is cost and modularity. The cited [Transition Accelerator compression brief](https://transitionaccelerator.ca/wp-content/uploads/2023/04/TA-Technical-Brief-1.1_TEEA-Hydrogen-Compression_PUBLISHED.pdf) gives an HDSAM
high-flow pipeline-compressor correlation based on motor power, an installation
factor and a maximum 16,000 kW unit rating, with multiple compressors above
that duty. The page omits the numerical coefficient and price transformation,
then applies one smooth economy-of-scale curve to a complete farm compressor
and the same general relation to turbine units. This can create an unsupported
centralisation advantage (ISS-0080/0081).

### 4. The infield ladder is geometry only

The 192.0 km continuous and 198.0 km integer reference calculations reproduce,
but neither is the adopted physical network required by the rest of the model.
The page replaces WIND-003's actual rectangular, rotated coordinates with a
separate square farm and recommends a fractional-rung result for optimisation.
It does not return segment flows, qualified products, valves, fault states,
manifold, risers, tie-ins, slack or installation sections
(ISS-0029/0076–0078).

### 5. The platform boundary is good; the calculation is absent

PLAT-001 is an excellent statement of ownership. Hosted-equipment CAPEX stays
with components, hosted mass is passed to the platform, and structure supply
is separated from installation. No platform result can be calculated because
platform multiplicity, every hosted-equipment mass ledger, structural and
outfitting mass, jacket/foundation quantities, material/fabrication cost and
lift modules are unresolved.

## Review by criterion

### Technical correctness

Verified relationships:

- the infield reference length arithmetic;
- compressor stage count and equal pressure ratio for the worked case;
- dimensional conversion from compressor work to kWh/kg and power;
- pipeline area, HHV conversion and ceiling-based pipeline count; and
- the leading `D^2.5` capacity dependence before friction/property effects.

Material corrections and qualifications:

- validate or replace the gas capacity equation (ISS-0084);
- distinguish gauge, absolute, operating, receipt, design and rated-class
  pressures (ISS-0085/0088);
- distinguish nominal product size from internal hydraulic diameter and add
  velocity/product qualification gates (ISS-0086);
- state the compressor's isentropic/perfect-intercooling basis and use one
  property function (ISS-0079); and
- remove the three-pipelines-per-pass installation assumption (ISS-0075).

### Model approach: accuracy versus complexity

The intended fidelity is close to the right level. No transient network,
detailed compressor map, CFD, or structural finite-element model is required.
The missing fidelity is physical and discrete rather than computationally
complex:

- a coordinate-derived ladder section table;
- steady segment flows in normal and selected isolation states;
- bounded compressor trains and spare states;
- discrete qualified TCP diameter/pressure classes;
- one physical inventory shared by supply and installation; and
- reference platform cases or a bounded mass/structure relationship.

These additions expose the quantities that drive cost without inventing
unsupported detailed engineering.

### Cost inputs and references

| Cost area | Status | Main finding |
|---|---|---|
| Compressor CAPEX | Blocked | numerical coefficient, normalization, offshore scope and train limits absent |
| Compressor OPEX | Major gap | page 3%, code 2%, cited source uses a different itemized scope |
| TCP material CAPEX | Blocked | confidential global regression, weak fit, no public audit or price basis |
| TCP OPEX | Major gap | unsupported 0.5% of material CAPEX |
| TCP installation | Blocked downstream | no qualified product, vessel/task/rate or complete physical inventory |
| Platform material/fabrication | Blocked | no mass-to-structure/cost method or price basis |

### Explanation and directness

The pages are generally concise and calculation-led. Scope tables and explicit
limitations are strong. No broad rewrite or page move is required.

Corrections should make calculation status visible earlier. Several figures
look like model outputs before the reader learns that product qualification,
cost constants or downstream pressure are unresolved. H2I-005 should remain as
a synthesis page, but be labelled as trade-off/search logic rather than another
calculation owner.

### Independent model development

An implementer can reproduce:

- the square-farm length proxy;
- compressor stage count and approximate energy curves;
- the written pipeline capacity algorithm; and
- pipeline-count ceiling logic once a peak flow is supplied.

They cannot independently produce the adopted hydrogen infrastructure or
platform result. The minimum missing information is:

| Missing item | Consequence | Finding |
|---|---|---|
| coordinate-based ladder and manifold | infield network/installation not closed | ISS-0029, ISS-0076–0078 |
| compressor train/type/cost package | architecture cost and mass biased | ISS-0080/0081/0083 |
| controlled compression property method | energy curves not exactly reproducible | ISS-0079 |
| qualified TCP class and physical data | capacity and installation infeasible | ISS-0086 |
| validated compressible-flow method | pipeline capacity/count uncertain | ISS-0084 |
| operating receipt pressure convention | export/backbone interface ambiguous | ISS-0028/0085 |
| auditable material cost method | pipeline CAPEX not reproducible | ISS-0087/0088 |
| lifecycle/availability ledgers | annual cost and delivery incomplete | ISS-0024/0025/0082/0089 |
| hosted equipment and structural model | platform CAPEX/installation absent | ISS-0027/0052/0053/0063/0083 |
| complete search sets and constraints | joint optimum not reproducible | ISS-0020/0022 |

### General site and cross-page structure

The navigation and page placement are logical. H2I-001 links all four
subpages, H2I-005 is useful after the component calculations, and the common
Platforms section correctly follows architecture-specific equipment. No new
page is strictly required.

Cross-page corrections are required:

- H2I-001 and H2I-005/INST-003 disagree on simultaneous pipeline laying;
- H2I-002 ignores the layout coordinates it is instructed to consume;
- the infield/export manifold is excluded everywhere;
- operating injection pressure is conflated with rated pipe pressure;
- the onshore backbone endpoint has no canonical component owner; and
- no common mass/lift data contract links hosted equipment to platform and
  installation pages.

## Coverage

| Page ID | Readiness | Blockers | Major issues | Review note |
|---|---|---:|---:|---|
| H2I-001 | Partially implementable | 1 | 2 | Clear overview; pass-count and endpoint claims need alignment |
| H2I-002 | Blocked | 7 | 1 | Proxy length only; topology, hydraulics and inventory absent |
| H2I-003 | Blocked | 4 | 4 | Energy conditional; cost, trains and physical package absent |
| H2I-004 | Blocked | 4 | 6 | Capacity unvalidated; product and cost basis unresolved |
| H2I-005 | Blocked | 2 | 2 | Good synthesis; search not executable |
| PLAT-001 | Blocked | 5 | 0 | Correct boundary; all physical/cost drivers unresolved |

Counts include inherited/shared issues shown on each page and should not be
summed to reproduce the 27 unique material B5 issues.

## Decisions required

| Decision ID | Question | Main consequence of delay |
|---|---|---|
| DEC-0015 | What physical collection topology, manifold and fault-state design applies? | infield supply, installation and redundancy remain open |
| DEC-0016 | What compressor packages, train limits, cost boundary and physical ledger apply by architecture? | compression cost/mass and centralisation comparison remain open |
| DEC-0017 | What qualified TCP classes and auditable capacity/cost basis apply? | pipeline count, CAPEX and installation remain open |
| DEC-0007 | How does central platform count and capacity scale? | central platform feasibility/CAPEX remain open |
| DEC-0005 | What variable taxonomy and search specification applies? | pressure/diameter optimum cannot be reproduced |
| DEC-0006 | What availability accounting convention applies? | annual hydrogen can be double- or under-derated |

Inherited DEC-0008, DEC-0009, DEC-0012 and DEC-0013 must also be resolved to
close layout and all hosted-equipment ledgers.

## Proposed correction sequence

| Correction batch | Scope | Issues | Decisions | Validation |
|---|---|---|---|---|
| C5.1 Hydrogen collection closure | coordinate-based topology, manifold, sections, valves, normal/fault flows and physical allowances | ISS-0029, ISS-0076–0078 | DEC-0015, DEC-0008 | coordinate/length conservation; one-turbine/incomplete-row cases; flow balance; isolation states |
| C5.2 Compressor packages | thermodynamic function, train classes/counts, cost normalization, OPEX and physical records | ISS-0079–0083 | DEC-0016 | page/figure/code parity; stage/train thresholds; source-cost reproduction; mass handoffs |
| C5.3 TCP design and supply | receipt pressure, validated hydraulics, qualified product classes, discrete cost and physical inventory | ISS-0084–0089, ISS-0028 | DEC-0017 | pressure-unit tests; source benchmark; product feasibility; pipeline-count thresholds; cost-fit audit |
| C5.4 Platform closure | platform multiplicity, hosted mass ledger, reference structure, jacket/piles, fabrication cost and lift modules | ISS-0027, ISS-0052/0053, ISS-0063, ISS-0083 | DEC-0007, DEC-0009, DEC-0012, DEC-0013, DEC-0016 | mass and ownership conservation; reference design; class/multiplicity thresholds; installation handoff |
| C5.5 Search, lifecycle and endpoint | variable sets, onshore connection owner, OPEX/repair and architecture availability ledger | ISS-0020/0022/0024/0025/0028, ISS-0082/0085/0089 | DEC-0005, DEC-0006 | no double derating; receipt feasibility; time-step/peak separation; full LCOE ledger |

After correction, render all hydrogen-infrastructure and platform pages plus
affected architecture, methodology, turbine and installation pages. Render the
full site when navigation, common ownership or bibliography records change.

## Records created or updated

- New detailed reviews: `H2I-001.md` to `H2I-005.md` and `PLAT-001.md`.
- New issues: ISS-0075 to ISS-0089.
- New inputs: INP-0125 to INP-0166.
- New dependencies: DEP-0077 to DEP-0101.
- New decisions: DEC-0015 to DEC-0017.
