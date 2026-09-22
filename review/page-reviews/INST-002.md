# INST-002 — Turbine and Foundation Installation

## Review metadata

- **Source page:** [offshore_installation/turbine_and_foundation_installation.qmd](../../offshore_installation/turbine_and_foundation_installation.qmd)
- **Batch:** B6_installation
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The page has an appropriate screening structure: foundation and turbine
campaigns are separate, loads and trips are integer, mass constrains a sourced
sets-per-load value, and detailed packing is not invented. The duration
equation is dimensionally correct for a self-shuttling vessel.

A numerical turbine result cannot be produced because turbine site occupation
and a coherent vessel configuration are missing. The provisional cost package
also combines a generic ORBIT WTIV day rate from an example configured with
feeders with a self-shuttling, no-feeder model. More importantly, ORBIT defines
the seven-day field as time to mobilise the vessel to site; the page uses it as
combined mobilisation and demobilisation. The implementation also needs an
explicit infeasibility guard when payload permits zero sets.

## 1. Model role and boundary

- **Purpose:** calculate base monopile/foundation and turbine installation
  CAPEX as two campaigns.
- **Included:** port work, normal site occupation, self-shuttling travel and a
  time-based vessel/spread cost.
- **Excluded:** supply, feeder logistics, port construction/rent, scour,
  pre-clearance/remediation, extraordinary work and some commissioning.
- **Boundary risk:** excluded scopes are not assigned to an aggregate
  exceptional-cost owner, and the provisional ORBIT configuration includes
  feeder vessels even though this page excludes them.

## 2. Upstream inputs

| Input | Unit | Classification | Owner/source | Status |
|---|---:|---|---|---|
| Turbine count and rating | count; MW | scenario/derived | WIND/TURB | Available with scenario dependence |
| Port and inter-location distance | km | design/derived | port selection; WIND-003 | Port choice unresolved |
| Complete turbine and nacelle mass | t | derived | TURB-002 | Architecture equipment ledger incomplete |
| Monopile and transition-piece mass | t | derived | TURB-003 | TP mass missing; surrogate uncertain |
| Rate, mobilisation, payload, SWL, speed and sets/load by campaign | mixed | sourced/project inputs | selected spread | No coherent named configuration |
| Port and site occupation by campaign | day/set; day/location | sourced/project inputs | ORBIT/project schedules | Turbine site time missing |

## 3. Calculation reconstruction

For each campaign, the page:

1. constructs a transported set mass;
2. floors usable payload divided by set mass;
3. caps that result at the evidenced deck/logistics limit;
4. ceilings turbine count divided by sets per load;
5. adds combined mobilisation, per-set port and site time, round trips and
   inter-turbine travel; and
6. multiplies chargeable days by a campaign rate.

The mass-versus-reference minimum is a good minimum-fidelity rule: mass can
reduce a demonstrated load but cannot prove that more sets fit.

### Boundary and limiting-case checks

- `N` must be a positive integer; masses, rates, times, speeds and capacities
  must be positive; distances must be non-negative.
- If `floor(M_use/m_set) < 1`, return **infeasible**, not `ceil(N/0)`.
- Lift checks require positive SWL and should return unresolved when upstream
  lift mass is missing.
- A seven-day mobilisation input must not also represent demobilisation unless
  the selected source explicitly states that combined boundary.
- Mass uncertainty crossing an integer load threshold is correctly retained
  as alternative outcomes.

## 4. Outputs and downstream consumers

| Output | Unit | Downstream consumer | Interface status |
|---|---:|---|---|
| Feasibility and sets/load | status; count | METH-005 | Conditional; physical package missing |
| Loads and campaign days | count; day | schedule/CAPEX | Foundation partly parameterized; turbine blocked |
| Campaign and total CAPEX | EUR2025 | METH-002/METH-003 | Blocked |
| EUR/turbine and EUR/MW | EUR/unit | comparison | Correctly derived only after total cost |

## 5. Technical correctness

The load, trip and duration equations are dimensionally correct for the stated
self-shuttling concept, and the 10 kn conversion to approximately 444 km/day
is correct. The port-task arithmetic is also correct.

The ORBIT documentation defines `mobilization_days` as days required to
mobilise a vessel to site, not combined mobilisation and demobilisation. Using
seven days as the combined term understates cost if demobilisation is separately
chargeable. The zero-load case is mathematically undefined without a guard.

## 6. Model fidelity

The model correctly stops before deck layout, rigging, stability and crane
geometry. The missing fidelity is not a marine simulation; it is one coherent
campaign record per spread containing the vessel concept, support vessels,
payload/deck limit, lift envelope, task productivity and matching rate. Coarse
nacelle and monopile checks are acceptable only while missing tower-section,
TP and architecture-package lifts remain explicit blockers.

## 7. Cost and evidence audit

| Value/relationship | Exact support checked | Review result | Finding |
|---|---|---|---|
| 400,000 USD2024/day | ORBIT introduction example lists WTIV day rate 400,000 | Value traceable, but not a complete project spread quotation | ISS-0093 |
| Seven mobilisation days | ORBIT defines `mobilization_days` as mobilisation to site | Mislabelled as combined mobilisation/demobilisation | ISS-0092 |
| 10 kn transit | ORBIT example; conversion shown | Correct |
| 0.833 and 0.521 day/set port work | ORBIT task sums | Arithmetic correct; scope remains task-model evidence |
| 3 day/foundation | South Fork 2–4 day planning range without weather | Transparent midpoint and sensitivity |
| Six turbines/load; three foundations/cycle | Sofia project logistics | Suitable validation anchors, not coherent with the generic rate by themselves |

The ORBIT example configuration also states two feeder vessels. The page
correctly warns against automatic mixing, but still presents the generic WTIV
rate as the provisional rate in a self-shuttling calculation without a matching
commercial boundary.

## 8. Independent-implementer test

- **Can the page be implemented?** The algorithm can; the base case cannot.
- **Missing numerical evidence:** turbine occupation, named spread payload,
  lift envelope, foundation load limit, demobilisation and matching rates.
- **Missing decisions:** self-shuttling versus feeder strategy and separate
  foundation/turbine spread selections.
- **Missing implementation rule:** zero-load infeasibility and validation of
  all positive inputs.
- **Correctly unresolved:** deck packing, detailed lift engineering and
  weather-inclusive productivity.

## 9. Explanation and site placement

The page is well ordered and unusually clear about why extra detail is not
added. The parameter-status table should appear earlier, because the present
flow lets the reader reach cost equations before learning that the turbine
campaign has no site duration. No page move is needed.

## 10. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0038 | implementation_readiness | blocker | Architecture-specific turbine equipment mass/cost ledger is incomplete | Yes, DEC-0009 |
| ISS-0043 | implementation_readiness | blocker | TP mass and foundation lift/section records are missing | Yes, DEC-0010 |
| ISS-0091 | implementation_readiness | blocker | Turbine site occupation and a coherent campaign configuration are absent | Yes, DEC-0018 |
| ISS-0093 | cost_input | blocker | The provisional WTIV rate is not matched to the self-shuttling/no-feeder campaign boundary | Yes, DEC-0018 |
| ISS-0040 | model_fidelity | major | Tower/lift response to architecture mass remains incomplete | No |
| ISS-0041 | model_fidelity | major | Foundation mass surrogate remains weakly validated | Yes, DEC-0010 |
| ISS-0092 | technical_correctness | major | Seven ORBIT mobilisation days are treated as combined mobilisation and demobilisation | Yes, DEC-0018 |
| ISS-0094 | technical_correctness | major | A payload result of zero sets leads to division by zero instead of infeasibility | No |
| ISS-0095 | cost_boundary | major | Excluded normal/exceptional installation scopes have no complete owner or cost interface | No |

## 11. Page conclusion

- **Readiness:** blocked
- **Reason:** the transparent algorithm is implementable, but its turbine
  duration and coherent physical/commercial campaign inputs are absent.
- **Open blockers:** 4
- **Open major issues:** 5
- **Downstream consequences:** installed turbine/foundation CAPEX,
  architecture mass credit and feasibility comparisons.
- **Recommended correction order:** select campaign concepts and complete
  spread records; correct mobilisation boundary; close upstream mass/lift
  records; add assertions; then parameterize site occupation and rates.
