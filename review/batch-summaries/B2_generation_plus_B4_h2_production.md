# Extended Batch 2 review — Generation and hydrogen production

## Scope

Reviewed on 2026-08-21:

- three wind-resource/layout pages;
- three turbine/foundation pages; and
- five hydrogen-production pages.

This extends the originally planned B2 generation batch to include the complete
`hydrogen_production/` section. No source `.qmd`, model code or source dataset
was changed. The review files and registers are the handoff to a later,
separately approved correction stage.

## Outcome

| Result | Count |
|---|---:|
| In-scope pages reviewed | 11 |
| Partially implementable overview pages | 3 |
| Blocked calculation pages | 8 |
| New issues | 30 |
| Blockers | 18 |
| Major issues | 9 |
| Moderate issues | 3 |
| New decisions proposed | 5 |

The blocker count is concentrated around a small number of shared model
interfaces. It should not be read as thirty unrelated corrections. Closing a
canonical wind/layout definition, an architecture equipment ledger, a stack
lifecycle basis and a BOP scaling basis will resolve several findings at once.

## Overall assessment

The pages are generally strong at explaining why each subsystem matters and
many calculations are unusually transparent. The Weibull equations, WISDEM
component equations, turbine cost calibration structure, monopile surrogate
and hydrogen subsystem boundaries can all be followed.

The integrated model cannot yet be developed solely from the documented pages.
The main obstruction is not a lack of descriptive background. It is missing or
conflicting executable data:

1. the wind dataset is not tied to a reproducible DOWA extraction and its
   direction labels are misaligned with wake evaluation;
2. farm area and spacing feasibility are not defined tightly enough for the
   cost-density optimisation;
3. conventional and direct-DC turbine electrical variants have no complete
   mass/cost/loss ledger;
4. the stack curve, module size, degradation/replacement method and adopted
   cost basis are not canonical;
5. BOP scaling, offshore water cost and auxiliary-power treatment are not on a
   single evidenced executable basis; and
6. central power-electronics cost/efficiency differs between page and code and
   production-equipment mass is absent throughout.

## Review by criterion

### Technical correctness

Verified strengths:

- the conditional Weibull CDF/PDF and sector probabilities are internally
  consistent;
- the wake/AEP aggregation equations are dimensionally correct;
- the WISDEM turbine calculation is pinned to a source revision and exposes
  component equations and aggregation;
- the displayed monopile mass equation and reference checks reproduce;
- the direct-DC page correctly retains power control, voltage matching,
  protection and isolation functions rather than assuming they disappear;
- the BOP manufactured-cost and desalination-power arithmetic is correct; and
- the central power-electronics topology and aggregated boundary are plausible
  for screening.

Corrections required:

- lower-edge wind-sector labels shift representative wake directions by 15
  degrees (ISS-0032);
- the wake turbine/hub height is inconsistent with the turbine page
  (ISS-0036);
- the executable decentralised model applies an undocumented 1.025 energy gain
  (ISS-0046);
- the stack degradation example should give 55,556 full-load hours and about
  15.9 years at 40% capacity factor, not 58,500 hours (ISS-0049); and
- page/code values differ for stack module size, BOP power/cost and central
  conversion efficiency (ISS-0048, ISS-0055 and ISS-0058).

### Model approach: accuracy versus complexity

The basic fidelity choices are mostly good. Twelve directional sectors,
conditional Weibulls, a regular rotated layout, an engineering wake model,
WISDEM scaling and an aggregated transformer–rectifier package are suitable
for a transparent screening model. Adding full micrositing, turbine structural
design or converter circuit simulation would currently add more assumptions
than useful accuracy.

The pages need more fidelity only where material thresholds or architecture
differences are lost:

- reject infeasible spacing and preserve a consistent area boundary;
- use a controlled turbine power/thrust definition and benchmark the wake
  setup;
- treat direct DC as conditional on a capability envelope and a closed
  retained-equipment ledger;
- avoid unsupported linear foundation credits from equipment mass;
- preserve stack-module and BOP-train count steps; and
- do not extrapolate a single 0.6 BOP exponent from 1 MW to a GW-scale plant.

### Cost inputs and references

The turbine NREL calibration and NREL BOP component breakdown are traceable.
Most weaknesses are in transformations and commercial boundaries:

- architecture electrical cost deltas are not reconciled with calibrated RNA
  scope (ISS-0039);
- monopile USD/t pairs cost and mass from different reference designs
  (ISS-0042);
- stack cost alternates between 164 USD2020/kW, 112 USD2020/kW and an
  arithmetically unsupported 100 EUR/kW (ISS-0051);
- offshore water treatment remains an explicit placeholder (ISS-0054); and
- the 185 EUR/kW central conversion cost has no price year and differs from the
  100-per-kW legacy input (ISS-0057).

No affected cost should enter the common EUR2025 ledger until its source year,
currency, commercial scope, markup and architecture ownership are explicit.

### Explanation and directness

The overview pages are concise and well placed. The wind-source page is a good
example of explaining limitations directly. TURB-002 is long, but its length is
justified because the equations are the model rather than general background.
The BOP scope tables and DC function-allocation table are especially useful.

Targeted clarity changes are sufficient:

- add the direct-DC path and architecture applicability to H2P-001;
- replace invalid square-bracket equation markup on H2P-004;
- give each quantitative page one compact adopted-input/output ledger; and
- rename the wake-affected per-turbine output currently described as “gross”.

No page move is recommended.

### Independent model development

The wind-fit table and baseline WISDEM turbine can be independently coded from
the pages. The integrated generation-to-hydrogen calculation cannot. Minimum
missing information/assumptions are:

| Required item | Why it is needed | Finding |
|---|---|---|
| controlled DOWA extraction and centred sectors | reproduce and orient wind input | ISS-0031/0032 |
| area/setback and infeasibility rule | make optimisation and route geometry deterministic | ISS-0034/0035 |
| canonical turbine power/Ct/hub-height record | align wake, mass and cost | ISS-0036 |
| conventional/direct-DC equipment ledger | conserve mass, cost and energy | ISS-0038/0045 |
| generator/PEM capability envelopes | test direct-DC feasibility and curtailment | ISS-0044/0047 |
| stack curve, module dispatch and replacement state | reproduce hydrogen yield and lifecycle | ISS-0047/0048/0050 |
| one normalised stack cost | calculate overplanting economics | ISS-0051 |
| BOP train/scaling and water-treatment basis | compare central/decentral CAPEX fairly | ISS-0053/0054 |
| consistent BOP and central conversion energy models | reproduce annual hydrogen output | ISS-0055/0058 |
| production-equipment mass/lift records | close turbine/foundation/platform/installation | ISS-0052 |

### General site and cross-page structure

The navigation order is logical: wind resource before wakes, turbine before
foundation, and hydrogen overview before component pages. The pages are in the
right sections. The main site-level omission is that H2P-001 does not link or
map the direct-DC architecture path.

Cross-page ownership remains the larger problem:

- H2P-002 and TURB-002 share the direct-DC interface without one canonical
  component record;
- hydrogen-production pages own cost and energy but not equipment mass;
- H2P-005 excludes upstream switchgear that remains unowned for central
  hydrogen (inherited ISS-0012);
- H2P-003 and METH-006 conflict on availability (inherited ISS-0024); and
- component replacement still depends on the unresolved lifecycle convention
  from Batch 1 (ISS-0019/DEC-0004).

## Coverage

| Page ID | Readiness | Page-specific/shared blockers | Major issues | Review note |
|---|---|---:|---:|---|
| WIND-001 | Partially implementable | 0 | 0 | Correct overview; inherits child gaps |
| WIND-002 | Blocked | 2 | 1 | Source and sector alignment unresolved |
| WIND-003 | Blocked | 2 | 2 | Area, feasibility and turbine definition unresolved |
| TURB-001 | Partially implementable | 0 | 0 | Strong dependency overview |
| TURB-002 | Blocked | 1 | 3 | Baseline strong; architecture ledger incomplete |
| TURB-003 | Blocked | 1 | 2 | Auditable surrogate; incomplete physical handoff |
| H2P-001 | Partially implementable | 0 | 0 | Architecture routing incomplete |
| H2P-002 | Blocked | 3 | 0 | Direct-DC envelope and accounting missing |
| H2P-003 | Blocked | 6 | 1 | Curve, module, lifecycle, cost and mass unresolved |
| H2P-004 | Blocked | 4 | 0 | Scaling, water, energy and mass unresolved |
| H2P-005 | Blocked | 4 | 1 | Cost, efficiency and shared boundaries unresolved |

Counts in the last table include material inherited/shared blockers noted on
each page and therefore should not be summed to reproduce the 18 new blockers.

## Decisions required

| Decision ID | Question | Main consequence of delay |
|---|---|---|
| DEC-0008 | What is the area/setback, spacing and orientation convention? | layout optimisation remains non-reproducible |
| DEC-0009 | How are architecture equipment functions, mass, cost and losses booked? | direct-DC comparison and structural interfaces remain open |
| DEC-0010 | Which foundation surrogate and architecture mass-credit rule applies? | foundation CAPEX/installation cannot be treated consistently |
| DEC-0011 | Which stack curve/module/cost/replacement basis is canonical? | hydrogen yield and lifecycle cost remain non-executable |
| DEC-0012 | Which BOP train/scaling and offshore-water basis applies? | centralisation advantage remains assumption-driven |

Batch 1 decisions DEC-0004 (lifecycle cash flow), DEC-0005 (search/variables),
DEC-0006 (availability) and DEC-0007 (central platform scaling) also remain
prerequisites for closing these pages.

## Proposed correction sequence

| Correction batch | Scope | Issues | Required decisions | Validation |
|---|---|---|---|---|
| C2.1 Wind and layout baseline | source extraction, sector centres, area/feasibility, canonical turbine and wake test | ISS-0031–0037, ISS-0060 | DEC-0008 | reproduce fit; empirical/Weibull AEP; direction and layout regression tests; render wind pages |
| C2.2 Turbine/direct-DC/foundation ledger | architecture equipment, calibrated delta rule, capability gate, foundation physical outputs | ISS-0038–0046, ISS-0052 | DEC-0009, DEC-0010 | mass/cost conservation; limiting cases; lift/interface checks; render turbine/DC pages |
| C2.3 Stack operating and lifecycle model | curve, modules, dispatch, degradation, replacement and cost | ISS-0047–0051 plus ISS-0024 | DEC-0011, DEC-0004, DEC-0006 | curve regression; FLH/replacement tests; price normalisation; render stack/methodology pages |
| C2.4 BOP and central electrical package | BOP trains/water/power, PE cost/efficiency/mass | ISS-0053–0058 | DEC-0012, DEC-0007 | architecture symmetry cases; energy balance; EUR2025 audit; platform handoff; render affected pages |
| C2.5 Navigation and presentation | overview dataflow and BOP math markup | ISS-0056, ISS-0059 | none after preceding batches | render full site and inspect links/equations |

Do not correct all pages independently. The equipment-ledger and stack/BOP
decisions should be resolved once and then propagated to the relevant pages and
code together.

## Records created

- Detailed assessments: `review/page-reviews/WIND-001.md` to `WIND-003.md`,
  `TURB-001.md` to `TURB-003.md`, and `H2P-001.md` to `H2P-005.md`.
- Issues: ISS-0031 to ISS-0060.
- Inputs: INP-0049 to INP-0091.
- Dependencies: DEP-0033 to DEP-0059.
- Decisions: DEC-0008 to DEC-0012.
