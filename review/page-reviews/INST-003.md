# INST-003 — Cable and Pipeline Installation

## Review metadata

- **Source page:** [offshore_installation/cable_and_pipeline_installation.qmd](../../offshore_installation/cable_and_pipeline_installation.qmd)
- **Batch:** B6_installation
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

This is the strongest installation page structurally. It separates route,
physical and pass kilometres; makes loading discrete; qualifies vessels before
cost selection; keeps lay, burial and survey spread-days separate; and returns
**not parameterized** rather than zero. The worked example correctly exposes
why total mass is only a lower bound on cable loads.

Two duration equations require correction. Route-lay time uses horizontal
route pass-km, so slack and vertical product that affect supplied length and
loading add no laying time. The campaign then counts the initial port-to-site
transit and reload round trips, but not the final site-to-port transit. The
provisional ORBIT vessel rate also does not evidence the complete all-in spread
boundary claimed by the cost equation. Burial, survey, demobilisation, weather
and exceptional scopes remain unresolved, so no complete cable result is
available; TCP is additionally blocked by product and contractor qualification.

## 1. Model role and boundary

- **Purpose:** calculate laying, burial and ROV/survey spread-days and multiply
  them by matching complete-spread rates.
- **Subclasses:** array cable, HVDC export cable, TCP infield and TCP export.
- **Included:** mobilisation, loading, transit, lay events, burial, survey,
  testing and explicit exceptional work.
- **Excluded:** product supply, converter/platform equipment, development,
  finance, OPEX and decommissioning.
- **Boundary strength:** concurrency is correctly represented as additive
  spread-days rather than additive elapsed project days.
- **Boundary risk:** the ORBIT operating-vessel proxy is assumed to include
  fuel, routine support craft and contractor overhead without evidence.

## 2. Upstream inputs

| Input | Unit | Classification | Owner/source | Status |
|---|---:|---|---|---|
| Route, section, asset and interface inventory | km; counts | derived design | ELEC-002/ELEC-004/H2I-002/H2I-004 | All four interfaces incomplete |
| Slack and vertical/structure allowance | fraction; km | design assumption | asset pages/project route | Incomplete |
| Product mass, continuous length, reel and handling limits | t/km; km | product input | cable/TCP supplier | Cable proxies only; TCP missing |
| Vessel payload and product qualification | t; binary | contractor/product input | selected lay method | Commercial/project qualification missing |
| Task times and production | h/event; km/day | sourced/contractor | ORBIT for cables | Cable screening only |
| Lay, burial and ROV rates | EUR2025/day | commercial input | complete spreads | Lay proxy only; boundary unverified |
| Mobilisation/demobilisation, transit and port loading | day; km; km/h | campaign input | project/contractor | Demobilisation and port distance unresolved |
| Weather, survey, burial and exceptional work | mixed | project/contractor | metocean/site packages | Unresolved |

## 3. Calculation reconstruction

The page:

1. derives physical product length from parallel assets, route, slack and
   separately calculated vertical allowance;
2. creates one modeled lay/burial pass per physical asset;
3. screens every candidate spread against payload, storage, manufacturing,
   handling and qualification gates;
4. solves a discrete loading/packing problem, or reports a mass-only lower
   bound;
5. counts initial loads, reloads, route production, interfaces and splices;
6. builds separate lay, burial and ROV/survey spread-days;
7. applies weather once to exposed time; and
8. multiplies each time by a non-overlapping all-in rate and adds exceptional
   work.

The cable worked-example arithmetic is correct: `134 × 27/24 = 150.8` array
event days, two export pole interfaces give 2.2 days, and two 51.5-hour
splices give 4.3 days.

### Boundary and limiting-case checks

- All lengths and rates must be non-negative; production and transit speeds
  must be positive when the matching activity exists.
- Physical product conservation must hold across route, slack, vertical
  allowances, loading and installed sections.
- The length basis of `q_lay` must be explicit. If it is product-km/hour, slack
  and vertical product must enter production time; if it is route advance,
  their handling time needs a separate term.
- Each mobilised campaign needs its outbound and final return transit, plus
  every reload round trip, unless a quoted demobilisation term explicitly
  includes final return.
- Empty feasible sets return infeasible; missing qualification or rates return
  **not parameterized**.
- Integrated lay-and-bury candidates must be compared on the matching total
  integrated cost, not lay cost alone.

## 4. Outputs and downstream consumers

| Output | Unit | Downstream consumer | Interface status |
|---|---:|---|---|
| Physical/pass inventory | km; counts | supply reconciliation/METH-005 | Blocked upstream |
| Candidate qualification and selected spread | status/class | feasibility | Cable screening conditional; TCP blocked |
| Load/reload/event inventory | counts | campaign duration | Packing/campaign grouping unresolved |
| Lay, burial and ROV spread-days | day | installation CAPEX | Lay partly parameterized only |
| Cost by spread and exceptional scope | EUR2025 | METH-002/METH-003 | Blocked |

## 5. Technical correctness

The distinction between physical inventory, passes, loads and campaigns is
technically valuable and the weather/concurrency equations are dimensionally
consistent. The four-cable interpretation of the TenneT reference is clearly
labelled as a conservative ORBIT convention rather than contractor evidence.

However, `L_pass = N_parallel L_route` omits both slack and vertical allowance
from route-production time even though those lengths are physically installed.
This breaks conservation between supply, loading and lay duration. The lay
aggregation explicitly calls `T_site_transit` the initial offshore transit and
adds reload round trips, but contains no final return transit. Demobilisation is
separately unresolved and is not defined as including that voyage.

## 6. Model fidelity

Three explicit spreads with aggregate task events are the right minimum
fidelity for screening. A detailed vessel simulation is not required. The
missing fidelity is evidence-backed campaign configuration: complete upstream
sections, packing, route-specific burial method, survey passes, weather basis,
and matching spread inclusions. Cable task defaults must not be transferred to
TCP, which the page correctly avoids.

The candidate selector is sound for a separated lay campaign. When one
candidate integrates burial or changes support scope, minimising only
`r_lay*T_lay + fixed` can select the wrong total installation method.

## 7. Cost and evidence audit

| Value/relationship | Exact support checked | Review result | Finding |
|---|---|---|---|
| ORBIT executable task defaults | Pinned commit and exact source locations cited | Strong source traceability for screening tasks |
| 241,171 USD2024/day | ORBIT operating cable-vessel record | Does not prove all-in commercial inclusions | ISS-0098 |
| CPI/FX conversion to 219,041 EUR2025/day | Arithmetic reproduces | Transparent screening normalization; service-specific index sensitivity not shown |
| Burial/survey rates | No complete source adopted | Correctly unresolved | ISS-0099 |
| Van Oord benchmark | User-provided, scope and price basis unavailable | Correctly excluded from model; reconciliation record lacks governed source metadata | ISS-0099 |
| 0.4 km/h cable laying | Pinned executable default; differs from methodology publication | Difference disclosed and executable value reproducible |
| TCP rates and tasks | No qualified evidence | Correctly not substituted from cable or steel-pipe proxies | ISS-0086/ISS-0099 |

## 8. Independent-implementer test

- **Can the page be implemented?** The framework can; no complete base-case
  installation result can.
- **Missing numerical evidence:** burial/survey production and rates,
  demobilisation, weather, port route, exceptional unit costs and TCP package.
- **Missing modelling decisions:** cable campaign grouping, separate versus
  integrated burial, candidate spread set and TCP installation method.
- **Missing implementation rules:** consistent product-versus-route length
  basis and final-return transit.
- **Missing upstream datasets:** routed cable sections, all TenneT cable types,
  TCP sections/fittings and qualified products.
- **Correctly unresolved:** commercial total cost, packing where section data
  are absent, and all TCP installation cost.

## 9. Explanation and site placement

The page is calculation-led, explicit and mostly easy to audit, but at more
than 7,000 words it carries four asset subclasses, vessel selection, three
spread models, costing and evidence. A correction should first reduce repeated
status/limitation text and add a compact input-status ledger; splitting is only
justified later if TCP gains a genuinely different task model. Its current
site placement is correct.

## 10. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0001/0002/0004 | implementation_readiness | blocker | Array topology, vertical allowance and compatible collector design are unresolved | Yes, DEC-0001 |
| ISS-0065/0067/0069 | cost/implementation_readiness | blocker | Export product price basis, land route and complete installation inventory are missing | Yes in part, DEC-0014 |
| ISS-0078 | implementation_readiness | blocker | TCP sections, risers, slack and connections are missing | Yes, DEC-0015 |
| ISS-0086/0087 | implementation_readiness/cost_input | blocker | TCP product and auditable material basis are absent | Yes, DEC-0017 |
| ISS-0098 | cost_input | blocker | ORBIT operating-vessel rate does not evidence the complete lay-spread boundary | Yes, DEC-0019 |
| ISS-0099 | implementation_readiness | blocker | Burial, survey, demobilisation, weather and exceptional campaign inputs block complete cost | Yes, DEC-0019 |
| ISS-0005/0006/0007/0008 | model/cost/reference | major | Array section allocation, cable cost and slack basis remain unresolved | Yes in part, DEC-0001/0002 |
| ISS-0066 | cost_boundary | major | Export material/accessory boundary does not match a complete system | No |
| ISS-0075 | cross_page_consistency | major | Hydrogen overview contradicts the one-pipe-per-pass convention | No |
| ISS-0088 | model_fidelity | major | TCP rated product classes are not discrete | Yes, DEC-0017 |
| ISS-0096 | technical_correctness | major | Lay production time excludes slack and vertical installed product | Yes, DEC-0019 |
| ISS-0097 | technical_correctness | major | Final site-to-port transit is missing from lay duration | Yes, DEC-0019 |
| ISS-0100 | model_fidelity | moderate | Lay-only spread minimisation is insufficient for integrated installation candidates | Yes, DEC-0019 |

## 11. Page conclusion

- **Readiness:** blocked
- **Reason:** a strong framework lacks complete upstream inventories and
  campaign evidence, and two duration equations are incomplete.
- **Open blockers:** 11
- **Open major issues:** 9
- **Downstream consequences:** cable/TCP installation CAPEX, pressure and
  architecture optimisation, and total project CAPEX.
- **Recommended correction order:** repair length/transit conservation;
  close physical inventories; select subclass campaign methods; define
  complete spread boundaries; then parameterize burial, survey, weather and
  exceptional work.
