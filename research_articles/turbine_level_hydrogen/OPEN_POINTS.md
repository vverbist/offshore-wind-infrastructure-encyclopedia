# Open points and to-dos

Last reviewed: 2026-09-25 (O2 scope and execution queue; O1 stack outlet pressure recorded).

Working tracker for the article and its model. Update this file when a point is
resolved, a decision changes, or a new blocker appears. Keep stable IDs, record
the outcome, and link to the adopted evidence or implementation. Keep the next
priorities short; a deferred item is not an immediate request for input.

Numerical assumptions belong in the [central input table](../../model_data/inputs.csv),
with their basis on the owning methodology page. Article case choices belong in
the [scenario files](scenarios/). This tracker does not maintain another set of
parameter values.

## Next priorities

1. **Prepare the agreed common article case (O1).** The
   [reference-case assumptions](reference_case.qmd) and
   [shared input record](scenarios/reference_case.toml) are agreed. Connect them
   to the scenario templates, turbine curves and existing wind data to obtain
   common annual operating states and peak duties.
2. **Build the agreed electrical equipment inventory (O2).** Research component
   costs, losses, voltage ranges and unit-size limits, then implement the
   agreed website discussion. Scope and page placement are settled; the work
   is queued below and needs no further user input to proceed.
3. **Establish a defensible platform basis (O3).** The central platform is an
   included cost and a material part of the comparison. I prepare the method
   and evidence options for us to agree.

Public-source cost and price-basis work (O4–O6) can proceed alongside these.
No need to fill every blank CSV row individually before starting the case.

## To be executed — no further user input needed

These tasks are agreed but intentionally queued for a later work session. They
are not claims that the scenario inputs, model, or encyclopedia pages have
already been updated.

- [x] **Record the stack outlet pressure (O1).** Interpret the agreed 30 bar
  electrolyser stack outlet as 30 bar(g), consistent with the reference case's
  gauge delivery-pressure convention. Record it as a user-specified article
  assumption beside the reference case, state the atmospheric-pressure basis,
  and convert to bar(a) at the model boundary. Check related compressor text
  and scenario inputs for consistent pressure notation.
  *Done 2026-09-25:* recorded in the [shared input record](scenarios/reference_case.toml)
  and [reference case](reference_case.qmd); atmospheric basis is the exact
  standard atmosphere (`standard-atmospheric-pressure`, NIST SP 811), giving
  31.01 bar(a) stack outlet and 67.01 bar(a) delivery via
  [the reference-case calculation](analysis/reference_case.py). Compressor page,
  scenario templates and CSV unit convention now state bar(a). The templates
  still have to take these values when the record is connected (next item).
- [ ] **Finish the common operating case (O1).** Connect the shared reference
  record to both architecture scenarios; generate the rectangular-farm turbine
  coordinates; select traceable turbine dimensions and power/thrust curves;
  prepare common annual wind and peak-duty states. Preserve the agreed 1×
  overplanting reference, with up to 3× reserved for later sensitivity work.
- [ ] **Build the power-conversion equipment inventory (O2).** Research the
  grid-side inverter, electrolyser rectifier, turbine step-up transformer,
  central plant step-down transformer and rectifier transformer; retain the
  dedicated stack-side DC/DC converter as a companion entry for the
  conservative case. Record purchase cost and price basis, loss behaviour and
  operating conditions, maximum documented unit ratings, package inclusions,
  sources and adoption status. Distinguish individual modules from complete
  systems and published product limits from selected model unit sizes. For
  transformers, specify primary voltage, secondary voltage/range and
  insulation class separately; leave unresolved voltage choices explicit.
  Exclude the generator-side rectifier from the comparison cost table: it is
  retained in every case and remains in the common turbine baseline, with its
  losses accounted for consistently. Do not infer separate inverter cost or
  losses by arbitrarily splitting a complete turbine-converter package.
- [ ] **Implement the agreed electrical discussion on the website (O2).** Add
  a shared **Power Conversion Equipment** page under **Electrical
  Infrastructure**, immediately after its overview, to own the inventory and
  its evidence. Follow equipment duty, voltage and rating, unit count, cost,
  losses and evidence gaps. On [DC Integration](../../hydrogen_production/dc_integration.qmd),
  record the agreed cases: centralised hydrogen uses the conventional turbine
  electrical chain, AC collection and central transformer–rectifier package;
  conservative turbine-level hydrogen uses the turbine DC link with a
  dedicated stack-side DC/DC interface; direct DC omits that dedicated
  converter, conditional on electrical matching and protection. Link the
  [electrolyser power-electronics page](../../hydrogen_production/elx_power_electronics.qmd)
  to the inventory for central-chain equipment counts, costs and losses;
  keep turbine removal-credit reconciliation on the
  [turbine page](../../turbine_system/wind_turbine.qmd), and update the
  [component mapping](../../architectures/component_mapping.qmd) with scope
  summaries and ownership links. Keep auxiliary supplies, protection and
  cooling boundaries explicit. Use the inventory as the basis for O2c losses
  and O2d cost/mass reconciliation, without duplicating calculations or
  assuming unsupported mass or cost savings. Store adopted fixed scalar model
  inputs in the central CSV and sources in the bibliography; keep unsupported
  values as explicit TODOs. The discussion and research can proceed without
  further user input; candidate evidence is not automatically adopted.
- [ ] **Study injection pressure and export diameter as design variables
  (O7).** Develop evidence-supported candidate pressure/diameter combinations,
  check compression duty, pipeline capacity and count, pressure feasibility,
  and cost for each architecture, then report the trade-off in the article.
  Choose a baseline from the feasible cases rather than treating either
  variable as an externally supplied fixed value. Keep the onshore delivery
  pressure and physical export route from the agreed reference case.
- [ ] **Reconcile the collection-layout explanation (O7).** Keep the
  encyclopedia's ladder topology but recalculate its geometry and section
  lengths for the agreed rectangular IJmuiden Ver Beta case. Describe the
  physical sections, turbine connections, manifold boundary and healthy-state
  flow allocation used by the model. Correct stale square-farm and export-route
  examples on the relevant hydrogen infrastructure pages, and distinguish
  current flow/pressure checks from deferred redundancy analysis.
- [ ] **Complete the platform basis (O3).** Use the mass and cost chain now
  documented on the [platform page](../../platforms/platform_material_capex.qmd)
  to research hosted-equipment masses, structure and yard-integration rates,
  jacket fabrication cost, platform multiplicity and lift modules. Check cost
  boundaries and installation feasibility before populating the case. Report
  evidence gaps rather than treating the page's illustrative one-platform
  example as an adopted design.
- [ ] **Normalise the compressor cost source (O5).** Use the uninstalled
  motor-power cost correlation in the [Transition Accelerator brief](https://transitionaccelerator.ca/wp-content/uploads/2023/04/TA-Technical-Brief-1.1_TEEA-Hydrogen-Compression_PUBLISHED.pdf),
  cited on the [compressor page](../../hydrogen_infra/compressor.qmd). Convert
  its source-year Canadian-dollar cost to the model's EUR 2025 purchase-cost
  basis and exclude the source's installation factor. Use 15 kW of electrical
  motor input as the agreed reference rating: it is a convenient rounded
  normalisation near the calculated 12.9 kW duty of a full-load 1 MW electrical
  stack compressing from 30 to 100 bar(g). Derive the 15 kW reference cost
  directly from the same source power-law equation. Then the reference rating
  has **no effect on calculated costs**: its cost changes consistently with
  the rating and cancels when the equation is applied to any motor duty. Do
  not independently round the derived reference cost. Check whether the
  source's high-flow pipeline-compressor correlation is applicable to duties
  this small; the reference choice does not resolve that evidence question.

These queued tasks do not yet establish a feasible central platform or a
normalised compressor purchase cost.

## Active open points

Owners: **You** = article/design choice or information you hold; **Me** = research,
preparation, coding or documentation; **Joint** = I prepare a concrete basis and
you decide whether to adopt it. These are work allocations, not automatic
approval of new numerical assumptions.

| ID | Open point and next action | Owner | What it blocks / completion condition |
|---|---|---|---|
| O1 | **Partially resolved:** the [common case](reference_case.qmd) is agreed and recorded with evidence and reasoning in the [shared input record](scenarios/reference_case.toml). Remaining: connect the record to both templates, generate coordinates, select consistent turbine dimensions and power/thrust curves, prepare annual and peak-duty wind states, and pass the converted absolute stack outlet and delivery pressures (recorded 2026-09-25) into both templates. | Me: preparation | First real-case production and equipment inventories. Complete when both scenarios run on the same upstream wind and delivery basis. The assumption note is not an executable-case completion claim. |
| O2 | **Scope and website placement agreed:** build the component inventory and implement the discussion as queued above. The central, conservative turbine-level and direct-DC (`converter_reduced`) definitions are agreed; generator-side rectifier cost stays in the common turbine baseline. Derive losses and cost/mass reconciliation from the evidenced inventory; AC resistance and power factor remain to be established. | Me: research and implementation; Joint: numerical adoption where judgement is required | Comparable energy losses, electrical CAPEX and the basis for O&M. Complete when each electrical function is counted once and any removal credit has an explicit scope. The queued inventory does not yet close numerical inputs or validate the direct-DC operating envelope. |
| O3 | **Method drafted:** the [platform page](../../platforms/platform_material_capex.qmd) now documents the hosted-equipment, topside, jacket and pile mass chain; separate structure, integration and fabrication costs; and the lift handoff. Research the missing masses, unit costs, platform multiplicity and module choices in the execution list above. | Me: evidence and preparation; Joint: adoption | Complete centralised CAPEX and platform installation. The calculation structure exists, but the illustrative one-platform example is not an adopted, costed design. |
| O4 | Adopt stack purchase cost and an offshore water-treatment reference purchase cost. Retain the agreed aggregate BOP scaling. | Me: evidence and normalisation; Joint: adoption | Stack and BOP supply CAPEX. Resolve `stack-purchase-unit-cost` and `bop-water-reference-purchase-cost`; lifetime treatment remains D4. |
| O5 | **Source and reference rating identified:** the [compressor page](../../hydrogen_infra/compressor.qmd) cites a motor-power cost correlation giving uninstalled purchase cost; use the agreed 15 kW reference and derive its cost from that correlation. Convert its Canadian-dollar source price to EUR 2025 and check equipment-class applicability as queued above. The consistent reference-power/cost pair is only a normalisation and does not affect the cost curve. | Me: normalisation and applicability check | Compressor CAPEX. Resolve `compressor-reference-purchase-cost` and `compressor-reference-motor-power` together; the legacy plotted anchor is not an adopted purchase cost. |
| O6 | Complete source-year price escalation and cost scope checks. Recover the separate crane coefficient required by the turbine calibration. Distinguish reference evidence from adopted model prices. | Me | Comparable turbine, foundation, BOP and other supply costs. Resolve the missing escalation factors and `turbine-cost-crane`, with evidence and consistent inclusions. |
| O7 | Select the physical hydrogen collection arrangement, manifold boundary, diameters and pressures. Prepare the complete section inventory and healthy-state flow allocation. Connect the existing confidential TCP cost callable locally and establish its quote-to-model conversion; cost connections and manifolds explicitly. | You: design/private-data access when needed; Me: preparation; Joint: boundaries | Real-case collection/export quantities and CAPEX. Complete when every physical section is included and flow/pressure checks pass. Existing TCP method is retained; replacing it is not an active task. |
| O8 | Assemble coherent installation campaigns: vessel/spread boundaries, rates, loading plans, productivities, weather treatment, connections and lifts. Resolve transition-piece and additional equipment masses, including the turbine-level hydrogen lifting arrangement. | Me: evidence and campaign records; Joint: adoption | Installation costs and payload/lift feasibility. Complete when supplied and installed inventories agree and the selected rates cover the declared activities. |
| O9 | Define the common onshore receipt scope and adopt its supply, installation and operating costs. | Joint | Like-for-like landed hydrogen cost. Resolve the receipt inputs without adding downstream services outside the agreed boundary. |
| O10 | Adopt non-overlapping availability and component O&M assumptions from the retained equipment inventory. Include generation/production, conversion, compression, collection/export, connections/manifold and receipt as applicable. | Me: evidence and scope table; Joint: adoption | Delivered annual production and recurring costs. No blanket decentralised premium; removed electrical equipment must be reflected without assuming an unsupported maintenance share. |
| O11 | Reconcile the article blueprint and section map with the agreed draft: aggregate BOP, bounded compressor trains, retained TCP method, deferred redundancy/replacement and technical-cost scope. Align the financial equation with the implemented annualisation convention. | Me | Consistent methodology and article claims. Complete when older aspirational requirements are clearly separated from the adopted calculation and deferred work. |
| O12 | Run the populated cases, investigate feasibility failures and dominant cost/energy contributions, then generate the article comparison tables and figures from the common model. | Me; Joint: interpretation | Article results. Requires the relevant upstream inputs; report partial physical results while complete cost or lifetime inputs remain open. |

### Where to work

| Points | Main files / methodology owners |
|---|---|
| O1 | [Agreed reference case](reference_case.qmd), [shared inputs](scenarios/reference_case.toml), [centralised scenario](scenarios/centralised.toml), [decentralised scenario](scenarios/decentralised.toml), [wind and layout](../../wind_resource_and_layout/wake_modelling_and_spacing.qmd) |
| O2 | Planned new page: `electrical_infra/power_conversion_equipment.qmd` (Power Conversion Equipment; not yet created). Existing owners: [DC integration](../../hydrogen_production/dc_integration.qmd), [electrolyser power electronics](../../hydrogen_production/elx_power_electronics.qmd), [AC collection](../../electrical_infra/infield_ac_cables.qmd), [turbine](../../turbine_system/wind_turbine.qmd), [component mapping](../../architectures/component_mapping.qmd). Add the new page immediately after the Electrical Infrastructure overview in `_quarto.yml`. |
| O3 | [Platform CAPEX](../../platforms/platform_material_capex.qmd), [platform installation](../../offshore_installation/platform_and_substation_installation.qmd) |
| O4–O5 | [Stack](../../hydrogen_production/stack.qmd), [BOP](../../hydrogen_production/balance_of_plant.qmd), [compressor](../../hydrogen_infra/compressor.qmd) |
| O6 | [Price basis](../../methodology/financial_and_price_basis.qmd), [input ownership notes](../../model_data/README.md) |
| O7 | [Collection](../../hydrogen_infra/infield_infrastructure.qmd), [pipelines](../../hydrogen_infra/hydrogen_pipelines.qmd), [model input formats](../../model/README.md) |
| O8 | [Turbine/foundation installation](../../offshore_installation/turbine_and_foundation_installation.qmd), [cable/pipeline installation](../../offshore_installation/cable_and_pipeline_installation.qmd) |
| O9–O10 | [System boundary](../../methodology/system_boundary_and_lcoe.qmd), [availability](../../methodology/energy_availability_and_annualisation.qmd), [component mapping](../../architectures/component_mapping.qmd) |
| O11–O12 | [Blueprint](model_blueprint.qmd), [section map](section_map.qmd), [article skeleton](article_skeleton.qmd), [model workflow](../../model/workflow.py) |

## Deliberately deferred

| ID | Item | Return to it when / effect of deferral |
|---|---|---|
| D1 | Public provenance or matching curves for the supplied stack curve. Manufacturer disclosure is not requested. | Revisit for publication traceability; use the supplied curve as-is in the current draft. |
| D2 | Additional TCP hydraulic benchmarking, product qualification and public evidence for the confidential cost basis. | Revisit before making claims about qualified products or validated engineering performance. The present model remains provisional; no replacement method is requested now. |
| D3 | Redundancy, spare equipment and failure-state rerouting. | Revisit after the healthy-state comparison. Current runs claim no redundancy benefit. |
| D4 | Further degradation and replacement development, including a consistent lifetime-production adjustment. | Return after the basic comparison is established. Blank lifetime/replacement inputs still block complete LCOH; deferral does not make replacement free or beginning-of-life yield a lifetime average. |
| D5 | Architecture-dependent tower/foundation feedback from changed equipment mass. | Add as a later sensitivity. The present structural comparison retains the common baseline. |
| D6 | Additional sensitivities and break-even analysis: BOP block limit, electrical savings, platform/TCP costs, O&M, pressure/diameter and stack overplanting. | After a traceable baseline runs. Define ranges explicitly and record named overrides; do not silently change central inputs. |
| D7 | Detailed site-polygon/exclusion checks and broader engineering refinement. | Only if required by the selected case or if the added detail can materially change the comparison. Current coordinate separation checks do not establish full site feasibility. |

## Agreed decisions — do not reopen by default

| Decision | Current treatment |
|---|---|
| Article reference case | [IJmuiden Ver Beta case agreed on 2026-09-23](reference_case.qmd), with authoritative inputs beside the article. The note records geometry, depth, wind basis, export, pressure and stack-sizing decisions; integration into executable scenarios remains O1. |
| Wind information | Availability has been acknowledged. Select and connect the record for the case; provenance work is left for now. |
| Stack and TCP evidence | Keep the supplied stack curve and existing TCP model for now; later evidence work is tracked separately. |
| Electrical comparison cases (O2) | Centralised: conventional turbine electrical chain, AC collection and central transformer–rectifier package. Conservative turbine-level: turbine DC link with a dedicated stack-side DC/DC interface. Direct DC (`converter_reduced`): no dedicated stack-side converter, conditional on electrical matching and protection. |
| Electrical inventory boundary (O2) | Exclude generator-side rectifier cost from the comparison table because it is common to all cases; retain it in the turbine baseline and account for its losses consistently. Research the grid-side inverter, electrolyser rectifier and transformer roles, with a companion DC/DC entry for the conservative case. Transformer entries distinguish primary voltage, secondary voltage/range and insulation class. |
| Electrical evidence and website ownership (O2) | The planned Power Conversion Equipment page under Electrical Infrastructure owns the shared component inventory. Existing DC integration, electrolyser power-electronics, turbine and component-mapping pages apply or link to it as queued above. Costs and losses follow the inventory; published package values are not arbitrarily split, and candidate evidence is not an adopted model input. |
| BOP | Keep one aggregate exponent for the entire BOP, including water treatment, and the agreed block limit. Values remain authoritative in `bop-scaling-exponent` and `bop-block-limit`. Stack overplanting does not resize BOP. No new subsystem decomposition is required. |
| Compression | Retain its separate exponent and limit each train by electrical motor input. Values are in `compressor-cost-exponent` and `compressor-train-limit`; larger duties use multiple trains. |
| O&M comparison | Decentralisation removes electrical equipment. Maintenance follows the retained inventory; there is no blanket distributed O&M premium or adopted numerical claim that power electronics dominate all maintenance. |
| Cost boundary | Report technical-scope landed hydrogen cost. Development, shared owner engineering, insurance and owner contingency are excluded. Included platform, installation, receipt and replacement costs cannot be dropped to obtain a complete result. |
| Implementation | Same repository; readable modules follow calculation-owning pages. Fixed scalar inputs come from the central CSV, structured datasets stay separate, and case inputs may live beside the article. |
| Execution | Evaluate declared scenarios deterministically. Sensitivity runs use explicit overrides; the draft does not select an optimum. |

## Completed foundation and result gate

- The modular draft, scenario templates, local result reporting and sensitivity
  runner are implemented. See the [model guide](../../model/README.md).
- Stack/BOP/compression power balance, equipment-count thresholds, network flow,
  cost accounting and incomplete-result handling have software checks.
- At the foundation review on 2026-09-23, the test suite passed, including synthetic complete cases
  for both architectures and an optional wake-adapter check. The website was
  rendered and local references checked. This is software verification, not
  validation of the article reference case or engineering qualification.

For the first article calculation, close O1 and the physical/efficiency inputs
needed by the selected branches. For complete LCOH, also close all included
costs, O&M and availability inputs, plus the lifetime treatment in D4. For
publication, resolve or explicitly bound the evidence limitations underlying
the claims, reconcile the documentation, and regenerate the reported outputs.
