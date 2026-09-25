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
| `platforms/` | Declared platform records; structural cost method remains TODO |
| `offshore_installation/` | Turbine/foundation, platform and three-spread line installation |
| `methodology/` | Availability, financial annualisation and technical-scope LCOH |
| `reporting.py` | Explicit local output writing |

Calculation module names follow their calculation-owning Quarto pages. Shared
records and input handling are intentional exceptions. Figure scripts call the
stack, compressor and pipeline functions rather than duplicate those equations.
Rendering the website does not run article scenarios.

## Workflow

1. Resolve the central parameter table and explicit scenario overrides.
2. Establish turbine coordinates and power at the common generator electrical
   output boundary, before architecture-specific conversion/collection losses.
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
uses the central string rating; feeder bays are checked. Route allowance and
two water-depth vertical legs per section give a screening physical length.
Actual termination elevations, slack, charging and sheath losses are not
resolved. The resistance input must be an adopted effective AC resistance.

For hydrogen collection, non-turbine coordinates have `node,x_m,y_m`. Sections
have `section,from,to,vertical_m,route_allowance,flow_share,diameter_m,inlet_bar,
outlet_bar`. Turbine/node IDs must be distinct. Every physical ladder edge is
included, even if its selected healthy-state flow share is zero. Active paths
must be directed and acyclic; outgoing shares sum to unity. Flow is conserved
at the export sink. Diameter is true ID; pressures are absolute. Capacity and
junction pressure are checked, but flow allocation is supplied, not solved as
a hydraulic loop network. No redundancy benefit is assumed.

The export count uses simultaneous summed peak production, not the sum of
non-simultaneous individual peaks. The retained pipeline method remains a
provisional capacity screen, not a hydrogen-product qualification.

## Agreed simplifications

- The entire BOP retains exponent 0.6. Central blocks serve at most 100 MW;
  20/50 MW limits are explicit sensitivity overrides. These are chosen modelling
  bounds, not qualified equipment limits. Equal sharing sizes the blocks.
- BOP capacity follows served wind power, independently of stack overplanting.
- Compression retains exponent 0.8335 with at most 1 MW electrical motor input
  per train. Equal duty sharing applies; no spare train is inferred.
- Existing stack and TCP evidence remain provisional as agreed. The cost
  surface is loaded only when an explicit local path is supplied.
- Redundancy and architecture-dependent structural feedback are deferred.
- O&M follows the retained component inventory; no general distributed premium
  or claim that electrical equipment dominates total maintenance is inserted.
- Replacement development is deferred. The existing fixed-life event-count
  interface is available, but life, intervention cost and lifetime production
  remain missing until adopted. Beginning-of-life yield is not passed off as
  lifetime-average production. The external lifetime-production factor must
  include the adopted degradation and replacement convention consistently.

## Outputs and cost boundary

`result.json` contains status, missing-input/feasibility reasons, summary and
physical quantities. `effective_inputs.csv` records baselines and overrides.
`costs.csv` retains a row for each required included cost, including blank rows.
Other tables include coordinates, state-level power/production and collection
sections. State-level energy accounting includes curtailed power explicitly.

The scope includes technical supply, installation, component O&M, required
replacement and the adopted decommissioning convention. It excludes development,
shared owner engineering, insurance, owner contingency, construction finance,
tax and downstream services. Platform and receipt equipment remain included.
Missing included costs block complete LCOH; known subtotals remain available.

Unresolved interfaces currently include platform fabrication/physical inputs,
price normalisation, electrical cost adjustments/losses, complete installation
rates/plans, turbine-level equipment lifts, and O&M/availability inputs. The
conventional turbine calibration can include unresolved converter scope; the
turbine-level electrical adjustment must reconcile removed scope with the
separately costed interface before adoption.

For decentralised installation, `turbine-hydrogen-equipment-mass` adds the
equipment carried per turbine and `turbine-distributed-maximum-lift` records the
largest lift in the adopted combined installation arrangement. The selected
installation spread and site time must cover that same arrangement. Neither
input is inferred from electrical savings. Connections and manifolds have
their own unresolved O&M allowances; they are not silently omitted.

Production availability must include turbine-generation outages and the
production equipment within its stated scope, excluding the separately applied
compression and transport outages. Supplied wind states represent available
equipment; do not apply these factors to records that already include outages.

Results are local and git-ignored because they can expose confidential supplier
costs. Do not publish result folders or input snapshots automatically. A supplied
private Python cost module must be trusted local code. Its callable contract is
`pipeline_cost_curve(pressure_bar, diameter_inches)` returning the existing quote
unit rate. `pipeline-quote-to-eur2025` must convert that exact rate to EUR2025/m.
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

Run `python -m unittest discover -s tests -v`. Calculation tests use explicitly
synthetic cases, never adopted article inputs; the reference-case tests only check
that the generated article inputs still match their record. They check conservation, curve use, integer
thresholds, documented turbine/foundation masses, calibration, financial scope,
partial availability, incomplete-result handling and complete synthetic cases
for both architectures. With the optional wind dependency, they also exercise
the wake adapter on a synthetic aligned-turbine case. Physical qualification
and real-case calibration are separate from software verification.
