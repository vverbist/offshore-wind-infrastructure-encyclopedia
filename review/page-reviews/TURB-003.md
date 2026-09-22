# TURB-003 — Foundation

## Review metadata

- **Source page:** [turbine_system/foundation.qmd](../../turbine_system/foundation.qmd)
- **Batch:** B2_generation
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The page is transparent and its arithmetic is reproducible. The linear
supported-mass/depth surrogate matches the three displayed reference cases
reasonably near its calibration range, but those comparisons do not isolate
the supported-mass relationship because turbine/load and depth change
together. The cost-per-tonne basis combines a cost range and mass from
different reference designs. Missing transition-piece mass, scour quantity and
lift records block downstream installation and complete supported mass.

## 1. Model role and boundary

- **Purpose:** estimate monopile mass, supply cost and transition-piece cost
  from supported mass and water depth.
- **Architectures:** all, conditional on monopile feasibility.
- **Excluded:** transport/installation, site-specific soil/loads and detailed
  structural design.

## 2. Upstream inputs

| Input | Unit | Classification | Source | Status |
|---|---:|---|---|---|
| Complete turbine mass | t | derived | TURB-002 | incomplete by architecture |
| Additional supported equipment | t | derived/input | architecture pages | not closed |
| Water depth | m | site scenario | site definition | defined in principle |
| 1,318 t, 1,877 t, 30 m anchor | mixed | sourced surrogate | IEA 15 MW | traceable |
| Monopile unit cost and TP fraction | USD2022/t; fraction | derived/sourced | NREL + BVG | scope pairing uncertain |

## 3. Calculation reconstruction

$m_\mathrm{MP}=1{,}318(m_\mathrm{top}/1{,}877)(d/30)$, then monopile cost is
mass times a USD2022/t factor and transition-piece cost is a fraction of
monopile cost. Price normalisation is delegated to METH-003. The worked
monopile result from 1,552.8 t at 30 m is about 1,090 t.

### Boundary and limiting-case checks

- The equations are dimensionally correct.
- Zero depth/mass gives zero foundation, which is mathematical but not a valid
  offshore case.
- The stated 15–22 MW and 30–60 m envelope must be enforced.
- Monopile feasibility needs a foundation-type gate outside that envelope.
- Transition-piece mass and lifts must be non-negative explicit outputs.

## 4. Outputs and downstream consumers

| Output | Unit | Downstream consumer | Interface status |
|---|---:|---|---|
| Monopile mass | t | installation, CAPEX | calculable conditionally |
| Transition-piece mass | t | installation, supported mass | missing |
| Scour quantity | t/m3 | supply/installation | missing or unowned |
| Supply CAPEX | EUR2025 | LCOE | source-scope uncertainty |
| Lift/section records | t; dimensions | installation | missing |

## 5. Technical correctness

The printed formula and reference checks reproduce. Agreement with three
design points supports rough interpolation, not the causal assumption that
foundation mass varies linearly with supported static mass and water depth.
Rotor thrust, dynamics and soil are material omitted drivers.

## 6. Model fidelity

A transparent surrogate is defensible for screening if it is labelled and
bounded. For architecture comparisons, however, using turbine equipment mass
as the sole architecture-sensitive driver can imply unsupported foundation
savings. A load-responsive surrogate or an explicit no-credit rule is needed.

## 7. Cost and evidence audit

The NREL 250–350 USD2022/kW finished-monopile range is a credible source, but
dividing it by a separate BVG 1,850 t design assumes matching fabrication,
scope, turbine and site. Transition-piece cost as 50–75% of monopile cost is
traceable; its mass and installation boundary are not.

## 8. Independent-implementer test

The monopile screening calculation is implementable. A complete foundation
inventory and installation handoff are not. Soil/site qualification and the
rule for unsupported foundation types are also missing.

## 9. Explanation and site placement

The page is direct and correctly follows the turbine page. Its limitations are
clear. The next correction should focus on boundary/data contracts, not more
general foundation background.

## 10. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0041 | model fidelity | major | foundation scaling is causally under-specified | yes, DEC-0010 |
| ISS-0042 | cost evidence | major | unit cost combines unmatched references | no |
| ISS-0043 | implementation readiness | blocker | TP/scour/lift inventory is incomplete | yes, DEC-0010 |

## 11. Page conclusion

- **Readiness:** blocked
- **Reason:** screening mass exists, but complete cost/installation interfaces
  do not.
- **Open blockers:** 1
- **Open major issues:** 2
- **Downstream consequences:** installation vessel selection, foundation CAPEX
  and architecture mass credits.
- **Recommended correction order:** decide surrogate/credit rule; close
  transition-piece and scour boundaries; align cost references; emit lift data.
