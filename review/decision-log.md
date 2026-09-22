# Decision log

This log records decisions that resolve review findings or determine the scope
of a correction batch. It is not used for observations that can be resolved by
applying an already documented convention.

## Decision template

### DEC-0000 — Short decision title

- **Status:** proposed | approved | rejected | superseded
- **Raised on:** YYYY-MM-DD
- **Decided on:** YYYY-MM-DD
- **Context:** Why a decision is required.
- **Options:** The credible alternatives and their consequences.
- **Decision:** The selected option.
- **Rationale:** Why it was selected.
- **Affected issues:** ISS-0000
- **Affected pages:** PAGE-ID
- **Correction batch:** COR-00
- **Approved by:** Name or role

Do not reuse `DEC-0000`; replace it with the next sequential identifier when
recording the first decision.

## Open decisions

### DEC-0001 — Close the reference string and platform design

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** The current 15 MW, 64-66 MW string case produces 34 strings,
  while the cited TenneT 2 GW platform indicates 24 dedicated wind-farm bays
  plus four universal bays. The base string rating is also an interval rather
  than a deterministic input.
- **Options:** Use a conservative 64 MW scalar with a project-specific collector
  of at least 34 bays; select and evidence a cable/interface rating that permits
  a bay-compatible string count; model an additional aggregation stage or
  platform; or treat the competing designs as explicit alternatives.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0001, ISS-0004, ISS-0005
- **Affected pages:** ELEC-002, ELEC-003, ARCH-002, INST-003, PLAT-001
- **Correction batch:**
- **Approved by:**

### DEC-0002 — Select the cable-cost fidelity for the screening model

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** The page uses one blended EUR/m value while providing evidence
  for conductor-specific price and mass. The installation model uses the large
  cable mass for the complete inventory.
- **Options:** Retain a top-down blended cost and explicitly accept inconsistent
  mass/cost detail; or implement a minimum two-class segment allocation that
  returns length, mass and cost by conductor class. The latter is the review
  recommendation because it adds a material physical dependency without a
  detailed cable-engineering model.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0006, ISS-0007
- **Affected pages:** ELEC-002, INST-003
- **Correction batch:**
- **Approved by:**

### DEC-0003 — Select a common comparison endpoint

- **Status:** decided
- **Raised on:** 2026-08-21
- **Decided on:** 2026-08-21
- **Context:** Electricity LCOE is currently measured at the grid connection,
  while hydrogen LCOE is measured as HHV energy at a hydrogen-backbone
  connection. Storage, reconversion, distribution and end use are excluded.
- **Options:** Treat the outputs as two carrier-specific products at different
  interfaces and do not rank them as equivalent; or extend both chains to a
  common end-use service, with scenario-specific demand, storage, reconversion,
  distribution and all associated costs and losses.
- **Decision:** Use carrier-specific Tier 1 endpoints and defer a common-service
  Tier 2. Report total relevant system CAPEX in EUR2025/kW of installed wind
  turbine rated capacity for both carriers. Report electricity annualized cost
  in EUR2025/MWh of electricity landed at the defined onshore electrical
  endpoint. Report hydrogen annualized cost in EUR2025/MWh-H2 on an HHV basis
  for hydrogen landed at the defined onshore hydrogen endpoint, and also in
  EUR2025/kg-H2. Label the electricity and hydrogen energy-cost metrics as
  different delivered carrier products rather than equivalent end-use service
  costs. A direct carrier ranking at a common service is deferred until a
  scenario defines end use, storage, reconversion, distribution and demand
  matching.
- **Rationale:** The end use is intentionally unknown. Normalizing both carrier
  outputs by delivered energy gives a useful transparent comparison, while the
  HHV and endpoint labels prevent it from being presented as a like-for-like
  end-service price. EUR/kg remains useful for hydrogen readers, and EUR/kW-wind
  exposes capital intensity on the same installed-generation basis.
- **Affected issues:** ISS-0015
- **Affected pages:** METH-002, METH-006, ARCH-001, ARCH-002, ARCH-003,
  ARCH-004, ARCH-005
- **Correction batch:** COR-01B
- **Approved by:** User

### DEC-0004 — Adopt the project financial and lifecycle-cost convention

- **Status:** decided
- **Raised on:** 2026-08-21
- **Decided on:** 2026-08-21
- **Context:** The model uses a 6.6% real WACC and 25-year simple annuity, but
  component replacements, decommissioning and residual value require timed
  cash flows and the WACC basis is not evidenced.
- **Options:** Retain one project-wide real WACC with an evidence-based range
  and annualise a complete real discounted cash-flow ledger; or define
  architecture/component-specific financing only where evidence supports it.
  In either case, tax convention, expenditure timing, replacement, residual
  value and decommissioning must be explicit.
- **Decision:** Use one project-wide 6.6% real WACC as the provisional base
  value and a universal 25-year project life with the simple CRF method. The
  6.6% evidence basis and sensitivity range remain open and must be stated as
  unresolved rather than implied by this decision.
  Component pages own their non-overlapping CAPEX and annual OPEX. Ignore
  expenditure timing and do not build a detailed cash-flow model. Components
  with a technical life at least 25 years receive no residual value and are
  evaluated over 25 years. Include replacement only for material components
  with a significantly shorter evidenced life; the component page owns the
  replacement interval, scope and cost. Count required replacements within the
  25-year life without discounting their timing, add them to the capital base,
  and annualize that base with the common CRF. Set decommissioning cost to 80%
  of total offshore installation CAPEX, add it to the same capital base and do
  not create a separate decommissioning cost model.
- **Rationale:** The project prioritizes a transparent screening convention
  over detailed financing. A common CRF preserves comparability, while explicit
  short-life replacement prevents material stack or equipment renewals from
  disappearing. The simplified decommissioning assumption keeps the scope
  visible without unsupported activity decomposition.
- **Affected issues:** ISS-0018, ISS-0019
- **Affected pages:** METH-002, METH-003 and all component cost pages
- **Correction batch:** COR-01B
- **Approved by:** User

### DEC-0005 — Define the model search and variable taxonomy

- **Status:** decided
- **Raised on:** 2026-08-21
- **Decided on:** 2026-08-21
- **Context:** Adjacent methodology pages disagree on whether stack
  overplanting and pipeline choices are scenarios or optimisation variables.
  The design vector, feasible sets, grids and result-selection rule are absent.
- **Options:** Use a transparent enumerated design sweep with explicit discrete
  candidate sets and Pareto filtering; or use an optimisation algorithm with
  the same variables, bounds and constraints explicitly defined. Scenario
  variables must remain external in either option.
- **Decision:** Do not implement optimization or an internal search for now.
  The model is deterministic: one complete set of user-controlled input
  variables and fixed parameters produces one result plus explicit feasibility
  status. Define one canonical taxonomy separating (1) scenario/design inputs
  selected by the user, (2) fixed sourced or assumed model parameters, (3)
  derived quantities, and (4) reported outputs. Sensitivities or alternative
  designs are separate user-supplied cases, not optimizer-generated candidates.
  Repurpose the existing optimization-variable documentation or create a
  dedicated input-and-parameter page if that gives the clearest implementation
  contract.
- **Rationale:** The model chain and evidence are not yet stable enough to make
  an optimizer useful. A deterministic calculation is simpler to audit and
  forces every input and parameter to be explicit. Optimization can be added
  later without changing the component accounting interfaces.
- **Affected issues:** ISS-0020, ISS-0021, ISS-0022
- **Affected pages:** METH-004, METH-005 and all pages producing design-variable
  constraints
- **Correction batch:** COR-01B
- **Approved by:** User

### DEC-0006 — Set the availability accounting convention

- **Status:** decided
- **Raised on:** 2026-08-21
- **Decided on:** 2026-08-21
- **Context:** Shared and component pages use unsupported flat factors with
  unclear boundaries, including conflicting 98.5% electrolyser and 99.5% stack
  values. Some component pages also propose capacity-state models.
- **Options:** Retain one explicitly scoped energy-equivalent factor per
  non-overlapping subsystem with evidence and sensitivities; or implement
  state-based availability for selected material assets and remove the
  corresponding flat factors. Both approaches require an architecture ledger.
- **Decision:** Use annual energy-equivalent availability at subsystem level;
  do not implement time-step outage states or a detailed reliability
  simulation for now. Each component page owns the evidenced or explicitly
  assumed availability of its non-overlapping subsystem. METH-006 owns a
  dedicated side-by-side architecture ledger that identifies every subsystem,
  factor, inclusion boundary and source. Combine serial subsystem factors once
  at architecture level. Where parallel units or redundancy exist, the
  component owner must provide the already-combined subsystem factor rather
  than multiplying unit factors. Do not apply a factor when the same outage or
  derating is already embedded in the energy calculation. Missing data remain
  explicit assumptions with sensitivities rather than being silently set to
  100%.
- **Rationale:** Annual factors match the available evidence and intended model
  simplicity. Central ownership of the architecture ledger prevents double
  derating, while component ownership keeps the technical scope and evidence
  close to the equipment calculation.
- **Affected issues:** ISS-0024, ISS-0025, ISS-0010
- **Affected pages:** METH-006 and all component availability owners
- **Correction batch:** COR-01B
- **Approved by:** User

### DEC-0007 — Define centralised-platform scaling

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** Centralised hydrogen is defined as one integrated physical
  platform, while farm capacity and equipment sizing can vary. The platform
  page has no closed hosted-mass inventory or material-CAPEX method.
- **Options:** Constrain the architecture to a documented one-platform capacity
  range; introduce discrete platform-count steps above that range; or define a
  fixed reference farm for which one platform is an explicit scenario
  assumption. Each option requires a mass, feasibility and cost handoff.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0027
- **Affected pages:** ARCH-003, PLAT-001, INST-004, METH-005
- **Correction batch:**
- **Approved by:**

### DEC-0008 — Define the layout area and feasibility convention

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** Farm area is both a layout input and the denominator of the
  cost-density objective, but no edge/setback convention is defined. Layouts
  below the stated spacing threshold remain eligible, and orientation and wake
  inputs are fixed without a declared scenario/optimisation role.
- **Options:** Define a lease polygon with explicit setbacks and reject all
  spacing violations; or define a screening rectangle with half-spacing edge
  margins and an evidenced minimum-spacing constraint. In either case, state
  whether orientation is fixed, enumerated or optimised and preserve discrete
  row/column changes.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0034, ISS-0035, ISS-0037
- **Affected pages:** WIND-003, METH-005, ELEC-002, H2I-002
- **Correction batch:**
- **Approved by:**

### DEC-0009 — Set the architecture-specific equipment-ledger rule

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** The conventional and direct-DC turbines do not have complete,
  mutually exclusive ledgers for converters, transformers, switchgear,
  protection, DC link and cabling. Hydrogen-production equipment also lacks
  mass/lift outputs, while direct-DC feasibility is not numerically qualified.
- **Options:** Keep direct DC as a conditional architecture and require a
  complete mass/cost/loss/capability ledger before it can rank; or define a
  clearly bounded top-down delta scenario with no structural mass credit until
  detailed evidence is available. Both options must conserve energy and book
  every retained function once.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0038, ISS-0039, ISS-0044, ISS-0045, ISS-0052
- **Affected pages:** TURB-002, TURB-003, H2P-002, H2P-003, H2P-004, H2P-005,
  PLAT-001, INST-002, INST-004
- **Correction batch:**
- **Approved by:**

### DEC-0010 — Choose the foundation screening surrogate and mass-credit rule

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** The current monopile model scales linearly with supported mass
  and water depth but does not represent thrust, dynamics or soil. The
  architecture comparison may therefore award unsupported foundation savings
  from equipment mass changes, and transition-piece/scour/lift inventories are
  incomplete.
- **Options:** Adopt a bounded load- and site-class surrogate; retain the
  current mass/depth equation but award no architecture mass credit; or use
  discrete reference foundation cases. All options require an explicit
  feasibility envelope and complete physical installation inventory.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0041, ISS-0043
- **Affected pages:** TURB-002, TURB-003, INST-002
- **Correction batch:**
- **Approved by:**

### DEC-0011 — Adopt the stack operating, cost and replacement basis

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** Page and code use different module sizes and dispatch details;
  the numerical efficiency curve is not published; degradation/replacement is
  not executable; and 164 USD2020/kW, 112 USD2020/kW and 100 EUR/kW cost cases
  are presented without one adopted transformation.
- **Options:** Use a sourced commercial/reference module and published
  polarisation curve with stateful replacement; or use an explicitly calibrated
  aggregate stack curve with a documented equivalent lifecycle method. Select
  one current-density/manufacturing-volume cost basis and normalise it through
  METH-003 in either case.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0048, ISS-0050, ISS-0051
- **Affected pages:** H2P-003, H2P-002, H2P-004, METH-003, METH-005, METH-006
- **Correction batch:**
- **Approved by:**

### DEC-0012 — Select the offshore BOP scaling and water-treatment basis

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** A generic 0.6 exponent applied from a 1 MW land-based aggregate
  can predetermine the centralisation advantage and suppress train-count and
  redundancy steps. The offshore water cost is an explicit placeholder.
- **Options:** Build grouped BOP packages with evidenced train capacities,
  redundancy and scaling; or define bounded central/decentral reference
  packages with sensitivities and no extrapolation beyond their source range.
  In both cases, replace the water placeholder or leave BOP CAPEX unresolved.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0053, ISS-0054
- **Affected pages:** H2P-004, ARCH-003, ARCH-004, PLAT-001, METH-005
- **Correction batch:**
- **Approved by:**

### DEC-0013 — Select the offshore converter cost and physical-ledger basis

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** The DEA 2025 onshore converter coefficient is currently
  double-escalated and then applied to both terminals. The catalogue's offshore
  value includes the platform, so it cannot be added directly to a separately
  calculated structure. Converter equipment mass, block and lift data are also
  absent.
- **Options:** Use the corrected onshore coefficient for both terminals with an
  explicit offshore-premium sensitivity and no claim of bottom-up precision; or
  use a matched complete offshore/onshore station pair and derive one
  non-overlapping structural/electrical allocation. Either option requires a
  physical 2 GW equipment/block ledger for platform and installation.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0062, ISS-0063
- **Affected pages:** ELEC-003, PLAT-001, INST-004, METH-002
- **Correction batch:**
- **Approved by:**

### DEC-0014 — Define the base onshore connection and land-route scenario

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** The electricity architecture ends at an onshore PCC, but the
  base route stops at shore. Underground supply/installation, the 380 kV bay,
  site/land and wider reinforcement are unresolved, and no grid-node acceptance
  or curtailment rule is selected.
- **Options:** Define one explicit Dutch reference route/PCC with a bounded
  dedicated connection package and scenario-specific reinforcement; define a
  small set of connection classes with route and grid-strength parameters; or
  treat the PCC package as a required external scenario input and withhold a
  closed electricity result when it is absent. All options must allocate the
  converter-yard/TSO-bay boundary once.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0067, ISS-0071, ISS-0072, ISS-0073
- **Affected pages:** ELEC-004, ELEC-005, INST-003, ARCH-002, METH-005,
  METH-006
- **Correction batch:**
- **Approved by:**

### DEC-0015 — Define the decentralised-hydrogen collection network

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** The ladder page uses a smooth square-area length proxy even
  though the wake/layout model emits physical coordinates. It does not define
  segment flows, valves, fault states, the export manifold or the complete
  physical supply/installation inventory.
- **Options:** Adopt a deterministic coordinate-based ladder with explicit
  headers, rungs, manifold, valves, section flows and selected normal/fault
  states; or adopt a simpler single-path radial/tree collection system and
  remove the unsupported two-path redundancy claim. Either option must return
  integer sections, physical allowances, connection counts and infeasibility
  states. The current continuous formula may remain only as a check.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0029, ISS-0076, ISS-0077, ISS-0078
- **Affected pages:** H2I-002, H2I-004, WIND-003, ARCH-004, INST-003,
  METH-005, METH-006
- **Correction batch:**
- **Approved by:**

### DEC-0016 — Adopt the compressor package, cost and physical-ledger basis

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** The energy equation is conditionally usable, but page, figure
  and code property methods differ. The cost coefficient and price boundary
  are omitted, the cited 16 MW compressor limit is ignored, the same smooth
  correlation is applied from turbine to farm scale, and no physical package
  data reach turbine/platform/installation models.
- **Options:** Build architecture-specific compressor packages from bounded
  train types with explicit rating, count, spare philosophy, turndown,
  thermodynamic method, normalized equipment/packaging cost and mass/lift
  records; or define bounded central and turbine reference packages with
  sensitivities and withhold results outside their evidence ranges. Both
  options must separate equipment, offshore packaging, structure, hook-up and
  lifecycle costs.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0079, ISS-0080, ISS-0081, ISS-0083
- **Affected pages:** H2I-003, H2I-004, ARCH-003, ARCH-004, TURB-003,
  PLAT-001, INST-002, INST-004, METH-005, METH-006
- **Correction batch:**
- **Approved by:**

### DEC-0017 — Adopt a qualified and auditable TCP design basis

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** The current capacity method is not benchmarked to the cited gas
  equation, diameter and pressure class do not map to a named qualified
  product, and the confidential bilinear cost regression is neither publicly
  reproducible nor sufficiently validated. Continuous operating pressure also
  erases manufactured pressure-class steps.
- **Options:** Use discrete named hydrogen-qualified TCP product classes with
  true hydraulic dimensions, pressure/temperature/life limits, physical
  installation data and a publishable cost basis; or define governed generic
  product classes with public capacity validation, bounded confidential-cost
  inputs, disclosed fit/uncertainty metadata and a publishable fallback range.
  In either case, use absolute pressure in hydraulics, keep receipt and design
  pressures distinct, reject extrapolation and report alternative outcomes
  when uncertainty crosses a pipeline-count threshold.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0084, ISS-0086, ISS-0087, ISS-0088
- **Affected pages:** H2I-002, H2I-004, H2I-005, H2I-003, INST-003,
  METH-003, METH-005
- **Correction batch:**
- **Approved by:**

### DEC-0018 — Select coherent turbine and foundation installation campaigns

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** INST-002 has a transparent integer logistics model, but turbine
  site occupation is missing and its rate, speed, Sofia load anchors and ORBIT
  example do not form one physical/commercial spread. The ORBIT example also
  uses feeder vessels while the page models self-shuttling, and its seven-day
  mobilisation field is currently treated as combined mobilisation and
  demobilisation.
- **Options:** Adopt separate named self-shuttling reference spreads for
  foundation and turbine campaigns; adopt feeder-supported campaigns with
  explicit carrier concurrency and cost; or retain generic campaign classes
  bounded by coherent payload, lift, productivity and rate ranges. Every
  option must separate mobilisation/demobilisation, define weather treatment
  and return an unresolved state outside its evidenced envelope.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0091, ISS-0092, ISS-0093
- **Affected pages:** INST-002, TURB-002, TURB-003, METH-002, METH-005
- **Correction batch:**
- **Approved by:**

### DEC-0019 — Select linear-asset installation methods and spread boundaries

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** INST-003 has an auditable three-spread framework, but its
  physical inventories and most campaign inputs are unresolved. Cable lay
  duration excludes slack/vertical product and final return transit, the ORBIT
  rate does not prove a complete spread boundary, and integrated methods cannot
  be selected using lay cost alone.
- **Options:** Adopt separated lay, burial and survey reference campaigns for
  each cable subclass with matching complete-spread records; adopt integrated
  lay/bury methods where evidenced and compare total installation cost; and
  define separate TCP campaign classes only after product/contractor
  qualification. Each option must conserve physical product and voyages,
  allocate interface tasks once and preserve unresolved cost terms.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0096, ISS-0097, ISS-0098, ISS-0099, ISS-0100
- **Affected pages:** INST-003, ELEC-002, ELEC-004, H2I-002, H2I-004,
  METH-002, METH-005
- **Correction batch:**
- **Approved by:**

### DEC-0020 — Select the platform installation and commissioning concept

- **Status:** proposed
- **Raised on:** 2026-08-21
- **Decided on:**
- **Context:** INST-004 assumes crane-installed topsides on piled jackets, but
  no jacket/pile/module inventory, installation class, logistics, hook-up or
  complete-spread cost is selected. The CVOW 2.5-day anchor applies per
  complete topside rather than arbitrary module, and its 60-day total includes
  commissioning and final cable connection that overlap the INST-003 boundary.
- **Options:** Adopt a bounded pre-piled or post-piled jacket and single-lift
  topside reference concept; define an evidenced split-topside branch with
  module-specific placement/mating tasks; or define architecture-specific
  reference concepts when converter/hydrogen platforms exceed the common lift
  class. Every option must return pile/jacket/module records, reconcile cable
  interfaces once and attach durations to matching complete-spread rates.
- **Decision:**
- **Rationale:**
- **Affected issues:** ISS-0101, ISS-0102, ISS-0103, ISS-0104
- **Affected pages:** INST-004, PLAT-001, INST-003, ARCH-003, ELEC-003,
  H2I-003, METH-002, METH-005
- **Correction batch:**
- **Approved by:**

### DEC-0021 — Define published completion and model-readiness status

- **Status:** decided
- **Raised on:** 2026-08-21
- **Decided on:** 2026-08-21
- **Context:** The site publishes a sidebar percentage derived from page-level
  `completion:` metadata, but does not define whether it means prose progress,
  evidence completeness, implementation readiness or validation. Fourteen
  blocked pages show at least 80 percent and two blocked architecture pages
  show 100 percent.
- **Options:** Keep the percentage strictly as editorial progress and add a
  separate controlled readiness/evidence badge and legend; replace the
  percentage with statuses such as context, partial, blocked and validated; or
  derive a composite status from explicit evidence, implementation and
  validation gates. Any option must avoid presenting an unresolved model as
  complete and should be generated from one maintained source of truth.
- **Decision:** Use model readiness, not editorial completion percentage, in
  the published sidebar. Readiness must use one controlled status set and one
  maintained source of truth. Editorial completion may remain an internal
  drafting field but must not be shown as model completion.
- **Rationale:** Readers need to know whether a calculation is executable and
  evidenced. The current percentage gives high or complete scores to pages
  with blockers and therefore cannot serve that purpose.
- **Affected issues:** ISS-0109
- **Affected pages:** all navigated pages, `_quarto.yml`, progress-sidebar
  generator, ABOUT-001
- **Correction batch:** COR-01A
- **Approved by:** User

### DEC-0022 — Adopt evidence-access and source-status governance

- **Status:** decided
- **Raised on:** 2026-08-21
- **Decided on:** 2026-08-21
- **Context:** All content citations resolve, but References renders cited,
  uncited, internal, confidential and explicitly unfinished records together.
  About claims confidential inputs are documented sufficiently for
  reproducibility even where coefficients or raw data are unavailable to an
  independent implementer.
- **Options:** Publish only fully qualified active evidence and maintain
  internal/background records separately; publish one catalog with explicit
  public, controlled-internal, validation-only and unresolved classes; or use a
  public fallback/validation range whenever confidential evidence drives a
  result. Every option must map adopted quantitative inputs to exact source
  location, version/date, access status, model use and cost basis where
  relevant.
- **Decision:** Maintain one controlled evidence catalog with explicit statuses
  for public adopted evidence, controlled-internal evidence, validation-only
  evidence, background-only material and unresolved records. Map every adopted
  quantitative input to exact model use, source location, version/date, access
  status and cost basis where relevant. Where confidential evidence materially
  drives a published result, provide a reproducible public fallback or range,
  or label the result as controlled-internal and not independently
  reproducible. Do not present unfinished or uncited background records as
  active support.
- **Rationale:** This retains legitimate confidential evidence while making the
  public audit boundary honest and preventing incomplete bibliography records
  from appearing to validate model inputs.
- **Affected issues:** ISS-0087, ISS-0106, ISS-0107, ISS-0108
- **Affected pages:** REF-001, ABOUT-001 and all pages using internal or
  confidential evidence
- **Correction batch:** COR-01A
- **Approved by:** User
