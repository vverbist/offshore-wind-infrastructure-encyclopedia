# TURB-002 — Wind Turbine Mass and Cost

## Review metadata

- **Source page:** [turbine_system/wind_turbine.qmd](../../turbine_system/wind_turbine.qmd)
- **Batch:** B2_generation
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

This is one of the strongest calculation pages reviewed: equations, symbols,
units, pinned source revision, aggregation and a worked result are exposed in
calculation order. Its main limitation is structural rather than editorial.
The architecture-specific electrical ledger has no quantitative mass/cost for
converter, switchgear, DC link, protection or internal cabling, so neither
turbine variant has a closed mass and cost boundary.

## 1. Model role and boundary

- **Purpose:** calculate one turbine's component masses, supply cost, lifts and
  architecture-specific electrical changes.
- **Included:** WISDEM CSM relationships and calibrated RNA/tower costs.
- **Excluded:** transport, installation and foundation.
- **Canonical owner:** turbine-side transformer/converter/switchgear and their
  architecture deltas.

## 2. Upstream inputs

| Input | Unit | Classification | Source | Status |
|---|---:|---|---|---|
| Rated power, rotor diameter, hub height | MW; m; m | design inputs | scenario | defined |
| Tip speed and drivetrain efficiency | m/s; dimensionless | assumptions | WISDEM setup | defined, sensitivity absent |
| WISDEM coefficients | mixed | sourced implementation | pinned revision | traceable |
| RNA/tower calibration | USD2022/kW | sourced cost | NREL COWE | traceable at reference |

## 3. Calculation reconstruction

The page calculates rated speed/torque, blade and rotor components, drivetrain
and nacelle components, electrical additions, tower mass, aggregate masses,
raw WISDEM costs and separate RNA/tower calibration. The 15 MW/236 m example
reports 1,552.8 t for known complete-turbine components and USD 25.783 million
at the stated calibrated boundary.

### Boundary and limiting-case checks

- Equations are explicit and dimensionally interpretable.
- Drivetrain branch choices and discrete bearing/crane choices are visible.
- The default $H_h=D/2+15$ must be reconciled with site clearance and WIND-003.
- Architecture components must have mutually exclusive include/remove rules.
- Positive geometry, rating and efficiency assertions are required.

## 4. Outputs and downstream consumers

| Output | Unit | Downstream consumer | Interface status |
|---|---:|---|---|
| Component and complete turbine mass | t | TURB-003, installation | incomplete by architecture |
| Component lifts | t; dimensions | installation | electrical items missing |
| Turbine supply CAPEX | EUR2025 | LCOE | architecture adjustment ambiguous |

## 5. Technical correctness

The documented WISDEM baseline and use of a pinned revision are sound for a
transparent surrogate. The default hub height is 133 m for a 236 m rotor, not
the 150 m used in WIND-003. The source itself acknowledges older regression
content; it should not be presented as a detailed structural design.

## 6. Model fidelity

Component-level WISDEM scaling is suitable for screening. The length-only
tower regression cannot respond to architecture-induced supported mass or
loads, so claimed secondary tower savings cannot currently be calculated.
Adding a detailed TowerSE model is justified only if its inputs can be
credibly supplied; otherwise the limitation and sensitivity should remain.

## 7. Cost and evidence audit

| Value/relationship | Exact support | Basis | Finding |
|---|---|---|---|
| 1,700 USD2022/kW turbine | NREL reference cited | 12 MW offshore turbine | traceable |
| 1,462 RNA / 238 tower | NREL split cited | calibration point | traceable |
| architecture electrical deltas | no quantitative source | turbine variants | ISS-0038/0039 |

The calibration may already include commercial electrical supply scope. A
rule is needed for removing/replacing components without double counting the
calibrated reference.

## 8. Independent-implementer test

- **Baseline WISDEM turbine:** implementable.
- **Architecture variants:** not implementable.
- **Missing evidence:** converter, switchgear, protection, cable and DC-link
  masses/costs; calibration treatment of those items.
- **Missing implementation rule:** architecture delta before/after calibration.

## 9. Explanation and site placement

Long but justified: the equations are the model. Background remains
subordinate. A compact final ledger would make the result easier to audit.

## 10. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0038 | implementation readiness | blocker | architecture electrical ledger is incomplete | yes, DEC-0009 |
| ISS-0039 | cost boundary | major | calibrated cost-delta rule is ambiguous | yes, DEC-0009 |
| ISS-0040 | model fidelity | major | tower mass cannot respond to architecture changes | no |
| ISS-0036 | cross-page consistency | major | hub height conflicts with wake page | no |

## 11. Page conclusion

- **Readiness:** blocked
- **Reason:** complete mass/cost by architecture cannot be calculated.
- **Open blockers:** 1
- **Open major issues:** 3
- **Downstream consequences:** foundation mass, vessel/lift feasibility,
  platform interfaces and architecture CAPEX.
- **Recommended correction order:** close component ledger and calibration
  boundary; reconcile hub height; then evaluate whether a tower sensitivity is
  sufficient.
