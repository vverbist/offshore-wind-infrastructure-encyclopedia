# Offshore hydrogen model draft

This package evaluates one declared centralised or turbine-level hydrogen case.
It is a deterministic calculation, not an optimiser. The methodology pages own
the equations and evidence; the Python modules own their executable form.

## Run a case

From the repository root, with the project Python environment:

```powershell
uv run python tools/run_model.py research_articles/turbine_level_hydrogen/scenarios/centralised.toml --output model_runs/my-case
```

The two supplied TOML files are **partially parameterized article case
templates**. Their common inputs come from the generated `common_case.toml`;
they contain no invented design or financial values. Running one reports the
remaining missing scenario inputs. Fill the commented architecture fields and
adopt missing scalar parameters in `model_data/inputs.csv` before expecting full
results. All data paths in a scenario are relative to that scenario's directory.
Existing result directories are never overwritten.

A scenario may declare `include = "<file>.toml"` under `[case]` to add a shared
file from the same directory. An input may be defined in only one of the two
files; a repeated key is an error, not an override. The article templates
include the generated `common_case.toml`, written by
`research_articles/turbine_level_hydrogen/analysis/prepare_common_case.py`
from the agreed reference record.

The optional `wind` dependency group provides PyWake (`uv sync --extra wind`).
It is not required when a turbine-power-state CSV is supplied. The PyWake
adapter records the installed version; it still requires benchmarking against
the adopted turbine curves before article results. It is not validated by the
core test suite when PyWake is absent.

## Structure and ownership

| Location | Owner/responsibility |
|---|---|
| `workflow.py` | Explicit order of one case; recover known missing inputs only |
| `inputs.py` | Existing central CSV loader plus named scenario overrides |
| `records.py` | Small result records and explicit missing/infeasible conditions |
| `wind_resource_and_layout/` | Coordinate layout, supplied power states, Weibull weights and optional wake calculation |
| `turbine_system/` | Documented turbine mass/cost scaling and monopile screening |
| `electrical_infra/infield_ac_cables.py` | Radial-string inventory, supply cost and resistive losses |
| `hydrogen_production/` | Stack polarisation, aggregate BOP and electrical interfaces |
| `hydrogen_infra/` | Compression, physical collection network and existing pipeline hydraulics |
| `platforms/` | One platform: direct equipment or complete topside mass to one commercial EPCI package; legacy DNV helpers retained |
| `offshore_installation/` | Turbine/foundation and three-spread line installation; legacy platform module inactive |
| `methodology/` | Availability, financial annualisation and technical-scope LCOH |
| `reporting.py` | Explicit local output writing |

Calculation module names follow their calculation-owning Quarto pages. Shared
records and input handling are intentional exceptions. Figure scripts call the
stack, compressor and pipeline functions rather than duplicate those equations.
Rendering the website does not run article scenarios.

## Workflow

1. Resolve the central parameter table and explicit scenario overrides.
2. Establish turbine coordinates and power after the inverter, before the turbine
   transformer and architecture-specific downstream losses.
3. Build AC strings or read every physical hydrogen-collection section.
4. Calculate each operating state: collection losses, electrical conversion,
   module selection, stack power, hydrogen flow, BOP and compression auxiliaries.
5. Size equipment from declared design states and operating peaks, preserving
   module, block, compressor-train and export-pipeline counts.
6. Calculate supply and installation costs from the physical inventory.
7. Apply non-overlapping availability and component O&M; retain missing
   replacement/lifetime-production inputs explicitly.
8. Annualise the declared technical-cost boundary and report intermediate tables.

Central production aggregates power after AC losses. Distributed production
retains each turbine's power until after conversion. Within each production
location, the stack calculation searches integer active-module counts, finds
the current that satisfies stack plus BOP plus compressor demand, and selects
the greatest hydrogen output. This is the documented module dispatch rule,
not a search over project designs. The common post-conversion bus supplies the
auxiliaries in this screening implementation; no separate auxiliary converter
is inferred.

The supplied curve is interpolated in current density and voltage. Module power
is proportional to current density times voltage, not current density alone.
Reference rating and minimum load come from the CSV. No curve extrapolation,
switching penalty, transient start-up or chronological degradation is added.

## Inputs and units

The central CSV holds fixed scalar assumptions and source values. Blank values
are intentional TODOs; they cannot be used numerically or silently become zero.
The source year is required before a monetary value can be adopted. `reference`
values are display/calibration evidence, not additive EUR2025 model costs.

The source trail for migrated parameters is in `model_data/README.md` and the
owning pages. Legacy turbine USD coefficients are used only as relative cost
weights; absolute costs require the published calibration and price conversion.

Scenario files hold physical choices and references to structured datasets.
An override must name an existing, numerically adopted central input and use
its units. The baseline and effective value are recorded separately.

Public module boundaries use kW, kWh/kg, kg/h, tonnes, kilometres, absolute bar
and constant EUR2025. Coordinate files use metres. Turbine component equations
use kg internally, gas equations use SI internally, and annual output is MWh.
Conversions are explicit. Display rounding does not feed calculations.

### Wind power states

The wide CSV columns are `state,hours,<turbine IDs>`. Each power column is kW.
Weights must cover the central annual-hour basis; they are not renormalised.
Retain zero-production states. Declare `design_state_ids` in the scenario.
Zero-hour design states can establish peak duty without adding annual energy.
The selected curve's electrical-output boundary must match the common input
boundary; the model does not invent a generator-to-terminal correction.

The alternative wind CSV has `state,speed_m_s,direction_deg,hours`, accompanied
by a turbine curve with `speed_m_s,power_kw,ct`. Direction convention and source
provenance remain responsibilities of the supplied article data.

### Layout and collection

Coordinates have `turbine,x_m,y_m`. Alternatively, the scenario declares count,
columns, spacing and rotation; incomplete rows are centred. Farm area is an
independent reporting boundary, not a multiplier on lengths. Minimum separation
is checked. Detailed site-polygon/exclusion validation remains TODO.

For AC collection, coordinate row order defines string assignment. The count
uses the central string rating; feeder bays are not a required input. Electrical
equipment remains in the complete topside package. Route allowance and
two water-depth vertical legs per section give a screening physical length.
Actual termination elevations, slack, charging and sheath losses are not
resolved. Active AC operation uses a fixed loss fraction, not a resistance input.

For hydrogen collection, non-turbine coordinates have `node,x_m,y_m`. Sections
have `section,from,to,vertical_m,route_allowance,flow_share,diameter_m,inlet_bar,
outlet_bar`. Turbine/node IDs must be distinct. Every physical ladder edge is
included, even if its selected healthy-state flow share is zero. Active paths
must be directed and acyclic; outgoing shares sum to unity. Flow is conserved
at the export sink. Diameter is true ID; pressures are absolute. In the default hydraulic mode, capacity and
junction pressure are checked, but flow allocation is supplied, not solved as
a hydraulic loop network. No redundancy benefit is assumed.

The export count uses simultaneous summed peak production, not the sum of
non-simultaneous individual peaks. The retained pipeline method remains a
provisional capacity screen, not a hydrogen-product qualification.

## Agreed simplifications

- The entire BOP uses exponent 0.75 around a fixed 15 MW reference (0.6 is a named sensitivity override). Central blocks serve at most 100 MW;
  20/50 MW limits are explicit sensitivity overrides. These are chosen modelling
  bounds, not qualified equipment limits. Equal sharing sizes the blocks.
- BOP capacity follows served wind power, independently of stack overplanting.
- Compression retains exponent 0.8335 with at most 1 MW electrical motor input
  per train. Equal duty sharing applies; no spare train is inferred.
- Existing stack and TCP evidence remain provisional as agreed. The cost
  surface is loaded only when an explicit local path is supplied.
- Redundancy and architecture-dependent structural feedback are deferred.
- Provisional annual O&M is 2% of each component's initial supply + installation
  + EPCI capital, counted once. Detailed activity-based O&M is deferred.
- Replacement development is deferred. The existing fixed-life event-count
  interface is available, but life and intervention cost remain missing until
  adopted. Lifetime production is calculated from operating full-load hours. Beginning-of-life yield is not passed off as
  lifetime-average production. Degradation is applied afterwards as an energy
  penalty: the lifetime production factor follows from the degradation rate,
  the end-of-life threshold and the calculated stack full-load hours.

## Outputs and cost boundary

`result.json` contains status, missing-input/feasibility reasons, summary and
physical quantities. `effective_inputs.csv` records baselines and overrides.
`costs.csv` retains a row for each required included cost, including blank rows.
Other tables include coordinates, state-level power/production and collection
sections. State-level energy accounting includes curtailed power explicitly.

The scope includes technical supply, installation, component O&M, required
replacement and the adopted decommissioning convention. It excludes development,
shared owner engineering, insurance, owner contingency, construction finance,
tax and downstream services. Platform and receipt equipment remain included by default.
For the current article's `production_capex` scope, `reporting.excluded_components`
explicitly omits `pipeline-connections`, `pipeline-manifold` and `hydrogen-receipt`
from cost rows and lists them under `excluded_costs`; this never inserts zero costs.
With neglected collection pressure drop, `collection.diameter_inches` supplies a
uniform internal diameter, rejects conflicting section sizes and leaves hydraulic
feasibility unassessed. The article selects 6 inches and connects its confidential
local pipeline callable through the shared scenario's data section.
Missing included costs block complete LCOH; known subtotals remain available.

Unresolved interfaces currently include qualified platform applicability and decommissioning inputs,
price normalisation, electrical cost adjustments/losses, complete installation
rates/plans, turbine-level equipment lifts, and activity-based O&M/availability evidence. The
conventional turbine calibration can include unresolved converter scope; the
turbine-level electrical adjustment must reconcile removed scope with the
separately costed interface before adoption.

For decentralised campaign installation, the selected screening assumption is
equal complete turbine mass across architectures, also for payload. A separate
`turbine-distributed-maximum-lift` remains necessary for the combined lifting
arrangement. No transformer mass saving or unsubstantiated hydrogen-equipment
mass addition is used. The fixed article turbine benchmark already treats both
architectures equally. Foundation payload is independently monopile plus TP.
Campaign demobilisation and offshore weather allowances are explicit unresolved
inputs; the reference turbine benchmark remains a separate bundled method.

Centralised generation availability uses `turbine-generation-availability`,
separate from central production outages. Distributed production availability
retains its integrated generation/production boundary, excluding separately applied
compression and transport outages. Supplied wind states represent available
equipment; do not apply these factors to records that already include outages.

Results are local and git-ignored because they can expose confidential supplier
costs. Do not publish result folders or input snapshots automatically. A supplied
private Python cost module must be trusted local code. Its callable contract is
`pipeline_cost_curve(pressure_bar, diameter_inches)` returning the existing quote
unit rate in EUR2025/m, read at operating pressure in bar(g) (the workflow
subtracts the standard atmosphere). `pipeline-quote-to-eur2025` is therefore 1.
The module is a fitted bilinear surface; do not evaluate design cases far outside
the quoted diameter and pressure classes.
No price basis or missing supplier point is invented.

## Sensitivity and verification

Run `research_articles/turbine_level_hydrogen/analysis/run_sensitivity.py` with a
scenario, central parameter ID, explicit values and a new output directory.
It runs separate cases and writes a comparison CSV; it does not choose an optimum.

Design variables such as injection pressure and export diameter are scenario
inputs, not central parameters. Run explicit design cases with
`research_articles/turbine_level_hydrogen/analysis/run_design_cases.py`: each
row of its CSV names a case and supplies dotted scenario fields (for example
`hydrogen.injection_bar`). It fills only fields the template leaves open and
writes one result folder per case plus a comparison CSV; it selects nothing.
The article's `scenarios/pressure_diameter_grid.toml` can replace the cases CSV.
It expands the agreed gauge-pressure/internal-diameter arrays and writes
`design_cases.csv` in model units alongside the results. The comparison includes
reason text. Pressure boundaries are screened even when operating inputs are
missing: insufficient discharge pressure is infeasible, while unparameterized
collection pressures remain missing inputs. In hydraulic mode, distributed export inlet pressure
must account for collection losses. The article explicitly neglects that drop,
so its workflow derives export inlet from discharge.

Run `python -m unittest discover -s tests -v`. Calculation tests use explicitly
synthetic cases, never adopted article inputs; the reference-case tests only check
that the generated article inputs still match their record. They check conservation, curve use, integer
thresholds, documented turbine/foundation masses, calibration, financial scope,
partial availability, incomplete-result handling and complete synthetic cases
for both architectures. With the optional wind dependency, they also exercise
the wake adapter on a synthetic aligned-turbine case. Physical qualification
and real-case calibration are separate from software verification.

### Central-platform interface

One platform is fixed. Supply `[platform] topside_mass_t`, including equipment
and structure, in tonnes. Equipment-only mass is rejected. No structural fraction
enters active EPCI. Depth is optional applicability metadata, not a multiplier.

Alternatively use `mass_method = "power_scaling"` with `mass_reference =
"electrolysis"`. The workflow derives DC rating from farm capacity times
overplanting, rounded up to whole stack modules, using the same sizing as stack
purchase and operation. It is available independently of operating efficiency
and wind-state inputs. A separate `rated_power_gw` is rejected for this branch.
The `"hvdc"` and `"custom"` references retain an explicit `rated_power_gw`; custom
also requires reference mass/power inputs. Direct and scaled masses cannot be combined.

The active functions are `estimate_topside_mass`, `epci_inventory` and `epci_cost`
in `platforms/platform_material_capex.py`. The renamed coefficient
`platform-epci-topside-unit-cost-source` is EUR2023/complete topside tonne,
converted to EUR2025 using the page's HICP proxy. It and the screening endpoints
are rebased to half their former equipment-tonne values, preserving calibration.
Alpha's complete topside is the mass anchor, not adoption of its fabrication price.
Cost is coefficient times reference mass times `(topside_mass / reference_mass) ** beta`.
Recorded exponent overrides preserve cost at the reference mass.

`physical.platform_costs` retains the coefficient, reference, mass, exponent,
price basis and scope; `physical.platform_total_eur` gives the package total.
The ledger books one `platform / epci` entry, with no separate supply or
installation entries. The summarizer rejects such double counting. The EPCI
cost covers delivered offshore structure and integration, not hosted equipment
purchase. Legacy `inventory`, `supply_cost` and installation helpers remain
inactive comparison tools; the old methodology is also archived.

Platform annual O&M uses the common provisional rate times EPCI cost.
The separate `platform-decommissioning-cost` input is initially unresolved;
it is added once to lifetime costs. The installation-fraction decommissioning
proxy applies only to separate installation entries, never to EPCI. Missing
OPEX or decommissioning blocks complete LCOH but does not erase platform CAPEX.

No installation plan or feasibility approval follows from the aggregate cost.
`installation_feasibility` is `not_assessed`; legacy `[installation.platform]`
lift settings are not used by the active workflow. Engineering applicability
must be checked independently before adopting an unusually large/deep case.

## Electrical boundary and stack purchase basis

Hydrogen operation requires `wind.power_boundary = "inverter_ac_output"`. The user
confirmed that measurement point for the article source on 9 October 2026. The
common-case generator records it without altering curve or power-state numbers. AC cases multiply by turbine-transformer efficiency,
then subtract the fixed collection-loss fraction before central conversion.
Distributed cases divide by inverter efficiency before their DC interface.
Outputs distinguish inverter-output energy, transformer loss, collection loss
and recovered inverter loss; `generator_energy_mwh` is retired.

The calibrated turbine purchase is split into turbine supply excluding the
transformer and an AC-only transformer supply entry, preserving the combined
AC purchase. No inverter credit is claimed. Distributed transport payload omits
the known transformer mass; tower/foundation sizing retains the common baseline.

`electrolysis.manufacturing_output_mw_year` selects the stack supply-chain case.
`physical.stack_purchase_cost_basis` reports the shared derivation from NREL's
manufacturing anchors to the model's reference-rated EUR2025/kW purchase cost.
The article records the canonical `stack-manufacturing-reference-output`;
other manufacturing volumes are rejected until separately evidenced.
`physical.bop_purchase_cost_basis` reports the aggregate 15 MW BOP purchase
reference, including NREL internal water handling and the DEA thermal-treatment
allowance. The assumed EUR2023 quote basis is converted with shared HICP inputs.
Thermal integration, package interfaces and offshore intake remain limitations.

### First-article turbine installation

`installation.turbine_method = "reference"` selects the BVG fixed normal-turbine
benchmark. `install-turbine-reference-*` and `financial-gbp-*` inputs belong to
`offshore_installation/turbine_and_foundation_installation.qmd`. GBP2024 cost,
UK CPI and 2025 GBP/EUR derive the EUR2025 result in code. There is no mass
discount. The default `campaign` method and all previous inputs remain intact;
foundation installation still uses it. The article assumes hydrogen-equipment
installation and commissioning replace comparable work for removed power
electronics. Both turbines use the same installation benchmark, without a
separate hydrogen-equipment charge. This is a modelling assumption, not a
supplier-verified equivalence. Central-platform installation stays within EPCI.

## Current article reference: production and CAPEX

The shared article scenario selects `[reporting] scope = "production_capex"`.
Other scenarios default to `lifecycle`. Production and CAPEX readiness are
reported separately as `summary.production_status` and `summary.capex_status`.
`initial_capex_eur` is available only when all included capital rows are populated;
`known_capex_subtotal_eur` and `missing_capex` explain partial results. Lifecycle
categories are explicitly deferred, not booked as zero. No LCOH, lifetime-average
yield or availability-adjusted delivery is calculated in production/CAPEX mode.

Run the user-selected reference with the existing grid, for example:

```powershell
uv run python research_articles/turbine_level_hydrogen/analysis/run_design_cases.py research_articles/turbine_level_hydrogen/scenarios/centralised.toml research_articles/turbine_level_hydrogen/scenarios/pressure_diameter_grid.toml --case p140barg-d8in --output model_runs/reference-centralised
```

Use `decentralised.toml` and `--interface converter_reduced` with a separate
output directory for the direct-DC case. `--interface conservative` is retained
for a later DC/DC sensitivity, not the current comparison. Selection and interface are recorded with the outputs; no grid values or
central parameters are overridden silently.

The article declares `[collection] pressure_drop = "neglected"`: export inlet is
derived from compressor discharge, and conflicting explicit pressures are rejected.
Collection geometry and mass balance remain active, but collection hydraulic
feasibility is not assessed. Geometry-only section files are allowed in this mode;
missing diameters block collection supply cost, not independent production.
The default `hydraulic` mode still requires all hydraulic columns and capacity
checks. Export hydraulics remain active in both modes. The 8-inch reference is
export internal diameter only. Missing efficiencies and other capital inputs
remain explicit; this reference does not make an incomplete case fully parameterized.

### Provisional loss and crane assumptions (2026-10-09)

Current electrical-stage efficiencies and the collection-loss fraction are
explicit user assumptions in `model_data/inputs.csv`, pending references. Central
conversion multiplies separate plant-transformer, rectifier-transformer and
rectifier efficiencies; no independent aggregate input remains. Direct DC has
one residual interface allowance and no DC/DC converter. Non-electrical efficiency
inputs are unchanged. The article currently runs centralised and direct DC only.

The service-crane purchase weight is omitted from both sides of turbine cost
calibration; its mass remains. The historical crane-cost input is not consumed.
The NREL absolute-price anchor is unchanged. Article turbine masses and fixed
installation costs remain equal; purchase prices are not forced equal. The
existing transformer reallocation and unresolved retained-equipment cost
adjustment remain in place.


## Current audit corrections (15 October 2026)

The [canonical scenario contract](../methodology/optimisation_variables.qmd)
provides field names, units, architecture applicability and missing-input behaviour.
Only hydrogen branches are executable. Complete initial CAPEX reports
`initial_capex_eur_per_wind_kw`; no lifecycle-capital intensity is returned.
`physical.ac_routing` records physical cable km/turbine, without a topology change.
Residual value is always zero and nonzero overrides are rejected. Offshore
removal excludes onshore receipt installation and adds explicit platform removal.
CPI escalation factors are derived from the canonical indices with existing
five-decimal rounding. Historical component `*-opex-rate` inputs are inactive;
`financial-provisional-opex-rate` owns the common 2% assumption. No generation or
production availability value has been invented. The current bus solver already
closes stack + BOP + compression + curtailment jointly. Local-only source and
scenario storage remains selected; a Git commit alone cannot reproduce the model.
