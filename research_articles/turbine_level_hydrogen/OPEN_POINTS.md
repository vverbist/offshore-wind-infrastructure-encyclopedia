# Open points and to-dos

Last reviewed: 2026-10-02.

Remaining work for the turbine-level hydrogen article and its model. Completed
tasks are removed; existing O/D identifiers are retained for cross-references.
Fixed model inputs belong in the [central input table](../../model_data/inputs.csv),
case choices in the [scenario files](scenarios/), and evidence on the owning
methodology pages. Missing evidence stays explicit; no placeholder values.

## Next priorities

1. Close the electrical operating inputs (O2) and central platform mass basis (O3).
2. Complete collection sections for the agreed pressure/diameter grid (O7), then run the
   production and physical-feasibility comparison (O12).
3. Close the remaining cost packages, availability and O&M (O4–O10), and make
   lifetime production and replacement costs consistent (D4), before reporting
   complete LCOH. Platform CAPEX and its bundled installation model are resolved.

Research, implementation and documentation are assistant work; design choices
and adoption of uncertain assumptions are joint decisions. Supplier/project
information and confidential-data access may require the user. These allocations
are not approval to adopt unsupported numerical assumptions.

## Production and physical feasibility

### O2 — Electrical operation and equipment accounting

Owner: [Power Conversion Equipment](../../electrical_infra/power_conversion_equipment.qmd),
with [DC Integration](../../hydrogen_production/dc_integration.qmd),
[Electrolyser Power Electronics](../../hydrogen_production/elx_power_electronics.qmd),
[AC Collection](../../electrical_infra/infield_ac_cables.qmd) and
[Turbine Cost](../../turbine_system/wind_turbine.qmd).

- [ ] **Losses (O2c):** reconcile the supplied generator-output curve with the
  adopted inverter-AC-output boundary on [Turbine Power Electronics](../../turbine_system/power_electronics.qmd).
  Generator and rectifier remain common; do not add their losses again to a
  reconciled curve. Recover inverter losses by dividing by inverter efficiency
  in decentralised cases; apply transformer losses downstream in AC cases.
  Adopt inverter-only and turbine-level interface efficiencies.
- [ ] Replace the AC I²R screening calculation with the agreed fixed-percentage
  loss approach; choose its value and application point. Resistance and power
  factor remain required by the current implementation until it is replaced.
- [ ] Select converter/DC-link and stack DC voltages, equipment unit ratings and
  counts; establish the matching and protection conditions for direct DC.
- [ ] **Costs and masses (O2d):** adopt supported electrical package costs and
  reconcile retained/removed equipment with turbine, platform and lift records.
  Reallocate the legacy calibrated turbine-transformer cost to electrical
  infrastructure for AC cases without changing the combined package cost.
  Leave the grid-side inverter credit unclaimed without separable evidence;
  seek standalone DC/DC evidence for the conservative case.

Completion: each electrical function is counted once, with comparable losses
and explicit cost/mass boundaries across the three comparison cases.

### O7 — Hydrogen pressures, diameters and complete section records

Owners: [Collection](../../hydrogen_infra/infield_infrastructure.qmd),
[Pipelines](../../hydrogen_infra/hydrogen_pipelines.qmd),
[scenario formats](../../model/README.md) and the
[design-case runner](analysis/run_design_cases.py).

- [ ] Declare the distributed export inlet pressure after collection losses,
  and join section diameters and absolute inlet/outlet pressures to the existing
  [collection geometry](scenarios/common/collection_sections_geometry.csv).
- [ ] Run compression, section-flow, pressure, capacity and pipe-count checks
  for each architecture. Report feasible alternatives and their cost trade-offs;
  the user selects a baseline from the reported cases.
- [ ] Connect the confidential TCP callable to the local scenarios and record
  the quoted diameter/pressure range without disclosing prices, so case
  extrapolation can be checked. Retain the established quote conversion.
- [ ] Cost connections and the manifold explicitly, with supply and installation
  boundaries that agree with the physical section inventory.

Pressure and diameter are explicit inputs of each scenario, not central CSV
parameters. Keep the agreed delivery pressure, export route, ladder topology and
central manifold location. No redundancy benefit is claimed.

The agreed [design grid](scenarios/pressure_diameter_grid.toml) uses compressor
discharge pressure 50–150 bar(g) in 10 bar steps and export internal diameter
4–8 inches in 0.5 inch steps: 99 combinations per architecture. The runner
converts to absolute bar and metres, retains 50/60 bar(g) as infeasible against
66 bar(g) delivery, and leaves collection pressures/sizes unresolved. The grid
does not establish supplier qualification or select a baseline.

## Complete cost comparison

### O3 — Central platform scenario mass

Owners: [Platform CAPEX](../../platforms/platform_material_capex.qmd) and
[Platform Installation](../../offshore_installation/platform_and_substation_installation.qmd).

- [ ] Establish the scenario equipment mass or complete hydrogen topside mass,
  including retained electrical equipment. A matching reference power is needed
  only when using optional power-to-mass scaling; concept masses require scope checks.

The commercial-benchmark EPCI model is implemented and includes platform
installation. Separate fabrication rates and installation costs are no longer
required. Further benchmark calibration is a refinement, not an implementation blocker.

### O4 — Stack and water-treatment purchase costs

Owners: [Stack](../../hydrogen_production/stack.qmd) and
[Balance of Plant](../../hydrogen_production/balance_of_plant.qmd).

- [ ] Implement the documented stack purchase-cost basis in the shared inputs
  and calculations; `stack-purchase-unit-cost` remains unset.
- [ ] Establish the offshore water-treatment reference purchase cost
  (`bop-water-reference-purchase-cost`) and its inclusions. Retain the agreed
  aggregate BOP exponent and block limit.

### O5 — Compressor cost applicability

Owner: [Compressor](../../hydrogen_infra/compressor.qmd).

- [ ] Check the underlying H2A delivery vendor data (Table 2-18 and Figure 2-21)
  for the correlation's equipment class and fitted size range. Establish or
  explicitly bound applicability to turbine-level duties. Currency normalisation
  is settled; installation scope belongs to O8.

### O6 — Remaining price and turbine-cost evidence

Owners: [Price Basis](../../methodology/financial_and_price_basis.qmd),
[Turbine Cost](../../turbine_system/wind_turbine.qmd) and
[input ownership](../../model_data/README.md).

- [ ] Recover the separate `turbine-cost-crane` coefficient needed to reproduce
  the turbine calibration. Close remaining source-year and cost-scope gaps for
  adopted supply costs; keep reference evidence distinct from model inputs.

### O8 — Installation campaigns and equipment integration

Owners: [Turbine/Foundation Installation](../../offshore_installation/turbine_and_foundation_installation.qmd),
[Cable/Pipeline Installation](../../offshore_installation/cable_and_pipeline_installation.qmd)
and [Platform Installation](../../offshore_installation/platform_and_substation_installation.qmd).

Central platform installation is already included in EPCI; do not cost it again.

- [x] First-article turbine installation: fixed BVG normal-turbine benchmark,
  converted from GBP2024 to EUR2025, equal in both architectures with no mass
  discount. The shared scenario selects `reference`; the original `campaign`
  model and its inputs remain available.
- [x] First-article hydrogen installation and commissioning are assumed comparable
  to the work for removed power electronics. Use the same turbine installation
  benchmark with no additional hydrogen-equipment charge. Detailed integration
  work below is deferred for this article, rather than an installation-cost blocker.
  Foundation installation retains its common campaign method. The remaining turbine mass,
  lift and vessel work below applies to the retained campaign method and no
  longer blocks the first-article fixed turbine benchmark.

- [ ] Populate turbine/foundation and cable/pipeline vessel/spread rates,
  loading plans, productivities, weather treatment, connections and lifts, with
  explicit campaign inclusions.
- [ ] Resolve `foundation-transition-piece-mass`, additional turbine electrical
  and hydrogen-equipment masses, and the turbine-level hydrogen lifting
  arrangement. Check payload/lift feasibility against the supplied inventories.
- [ ] Treat central compressor integration within the platform EPCI scope;
  check any proposed extra charge for overlap. Define turbine-level compressor
  integration, connections and commissioning beyond equipment transport and
  lifting. Cost each activity
  once; unresolved installation is not zero. Consider the source installation
  factor only as an explicitly adopted aggregate for otherwise uncosted work,
  after checking overlap and offshore applicability.

### O9 — Common onshore hydrogen receipt

Owner: [System Boundary](../../methodology/system_boundary_and_lcoe.qmd).

- [ ] Define and adopt the common receipt supply, installation and operating
  scope and costs. Keep downstream services outside the agreed boundary excluded.

### O10 — Availability and component O&M

Owners: [Availability](../../methodology/energy_availability_and_annualisation.qmd)
and [Component Mapping](../../architectures/component_mapping.qmd).

- [ ] Adopt non-overlapping availability assumptions for generation/production,
  conversion, compression, collection/export, connections/manifold and receipt
  as applicable. Reconcile page-only stack and AC availability values with the
  executable inputs.
- [ ] Adopt O&M assumptions from the retained equipment inventory. Reflect
  removed equipment without assuming an unsupported maintenance share or a
  blanket decentralised premium. Platform O&M remains unresolved; its rate applies
  to the bundled platform EPCI cost.
- [ ] Establish the separate `platform-decommissioning-cost` input. It remains
  unresolved and blocks complete LCOH; do not apply an installation-removal factor
  to the whole EPCI package.

### D4 — Lifetime consistency required before complete LCOH

Owner: [Stack](../../hydrogen_production/stack.qmd) and the
[model workflow](../../model/workflow.py).

- [ ] Make efficiency resets and replacement costs follow one schedule, or
  block complete LCOH when their schedules disagree. Check architecture and
  overplanting cases: the current degradation interval can disagree with
  `stack-replacement-life`, giving replacement benefits without their costs.
- [ ] Resolve the lifetime/replacement inputs needed for the selected treatment.
  Beginning-of-life production must not be presented as lifetime-average yield.

This consistency is required for credible LCOH. Economic optimisation of the
replacement decision remains deferred below.

## Article and results

### O11 — Align article claims with the implemented model

Owners: [Blueprint](model_blueprint.qmd), [Section Map](section_map.qmd) and
[Article Skeleton](article_skeleton.qmd).

- [ ] Reconcile aggregate BOP, bounded compressor trains, the retained TCP
  method, technical-cost scope and the implemented annualisation convention.
  Separate evaluated design cases from optimisation claims and deferred work.
- [ ] State the common structural baseline on the turbine and foundation pages:
  turbine-level hydrogen equipment and removed transformer mass do not yet
  feed back into their structural calculations (D5).
- [ ] Correct stale preparation/blocker statements in the reference-case page
  and scenario comments to match the current implementation.

### O12 — Execute cases and generate article results

Owners: [Model Workflow](../../model/workflow.py),
[centralised case](scenarios/centralised.toml),
[decentralised case](scenarios/decentralised.toml) and
[Article Skeleton](article_skeleton.qmd).

- [ ] Run the populated comparison cases, investigate feasibility failures and
  dominant energy/cost contributions, and generate tables and figures from the
  common model. Report partial physical results while costs remain unresolved.
- [ ] Report complete LCOH only when all included costs, O&M, availability and
  lifetime treatment are closed. Reconcile documentation and regenerate results
  before publication; software checks alone do not validate the engineering case.

### O1 — Remaining wind-evidence limitations

Common-case preparation is closed and removed from the task list. Preserve these
limitations in the [reference case](reference_case.qmd) and
[wake methodology](../../wind_resource_and_layout/wake_modelling_and_spacing.qmd):
wind extraction height and direction metadata are unrecorded, minimum-spacing
screening lacks a sourced design basis, and wake-model/turbulence assumptions
need benchmarking or uncertainty bounds before publication claims rely on them.
Wind provenance work remains deferred; do not treat it as missing scenario setup.

## Deliberately deferred

| ID | Remaining work | Return to it when |
|---|---|---|
| D1 | Public provenance or matching curves for the supplied stack curve; manufacturer disclosure is not requested. | Publication traceability; use the supplied curve for the current draft. |
| D2 | Additional TCP hydraulic benchmarking, product qualification and public evidence for the confidential cost basis. | Before qualified-product or validated-engineering claims; retain the current method provisionally. |
| D3 | Redundancy, spares, isolation and failure-state rerouting. | After the healthy-state comparison; no current redundancy credit. |
| D4 | Economic replacement: replace only when restored production lowers LCOH after replacement cost; further degradation refinement. | After the basic comparison. This would replace the fixed end-of-life rule and independent replacement-life input; it does not defer the consistency requirement above. |
| D5 | Architecture-dependent tower/foundation feedback from changed equipment mass. | Later sensitivity; retain the common structural baseline meanwhile. |
| D6 | Further sensitivities and break-even analysis: BOP block limit, electrical savings, platform/TCP costs, O&M, pressure/diameter and overplanting. | After a traceable baseline; use named overrides and preserve baseline values. Initial pressure/diameter design cases remain O7. |
| D7 | Detailed site-polygon/exclusion checks and broader engineering refinement. | When material to the selected case; coordinate spacing checks alone do not establish site feasibility. |

## Agreed boundaries — do not reopen by default

- Both architectures use the [shared reference case](reference_case.qmd) and
  generated common operating inputs. The central platform and hydrogen export
  manifold are at the farm centre.
- Compare centralised hydrogen, conservative turbine-level DC/DC and conditional
  direct DC. Generator-side rectifier cost stays in the common turbine baseline;
  its losses are upstream of the adopted inverter-output power-curve boundary;
  the supplied curve still needs reconciliation. The turbine transformer is
  outside turbine cost and power-output scope even when housed inside it.
  Published package values are not arbitrarily
  split to infer separate inverter costs or losses.
- Retain aggregate BOP scaling and its block limit; stack overplanting does not
  resize BOP. Compressor trains remain bounded by electrical motor input.
- Use one central platform and the implemented commercial-benchmark EPCI model,
  scaled by equipment mass with a linear baseline and optional exponent sensitivity.
  Complete topside mass can be converted using the documented DNV assumption.
  Installation is bundled; hosted equipment purchase costs remain separate.
  Platform O&M (`platform-opex-rate`) applies to the bundled EPCI cost, and
  decommissioning is the separate `platform-decommissioning-cost` input, not a
  factor on EPCI; both remain unresolved (O10). The former structural and
  installation models are retained as archived comparisons.
- Report compressor reference purchase cost in EUR2025 per turbine kW. Central
  integration is covered by platform EPCI; reconcile turbine-level installation
  under O8. No automatic source
  installation factor or indirect-cost uplift.
- Retain the supplied stack curve and existing TCP method. The TCP fit uses
  operating gauge pressure without a design margin and the established EUR2025
  quote basis; model pressure calculations use absolute pressure.
- Report technical-scope landed hydrogen cost. Development, shared owner
  engineering, insurance and owner contingency are excluded. Included platform,
  installation, receipt and replacement costs cannot be dropped to close LCOH.
- Evaluate explicit scenarios deterministically; the draft does not select an
  optimum. Shared model functions own calculations used by pages, figures and
  article results; see the [model guide](../../model/README.md).
