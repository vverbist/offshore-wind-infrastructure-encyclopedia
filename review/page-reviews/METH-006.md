# METH-006 — Energy, Availability, and Annualisation

## Review metadata

- **Source page:** [methodology/energy_availability_and_annualisation.qmd](../../methodology/energy_availability_and_annualisation.qmd)
- **Batch:** B1_frame
- **Reviewer:** Codex
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The page states the energy basis and correctly assigns efficiency losses to
component owners. Hydrogen HHV of 39.4 kWh/kg is technically sound. The
availability section is not yet a reproducible or traceable architecture-level
calculation.

## Calculation reconstruction

The intended energy calculation appears to be:

1. calculate wake-adjusted electrical production over time;
2. apply component efficiencies and auxiliary consumption in physical order;
3. aggregate delivered electricity or hydrogen mass over the year;
4. apply energy-equivalent availability reductions; and
5. convert delivered hydrogen mass to HHV energy with 39.4 kWh/kg.

The page supplies no equation for step 4, no architecture-to-factor mapping and
no rule for whether factors are multiplied, bundled or replaced by component
state models. It also does not state how availability interacts with time-
varying losses, component redundancy, curtailment or partial-capacity states.

## Technical and evidence checks

The displayed HHV rounds the 39.42 kWh/kg value reported in an authoritative
[DOE/NREL technical source](https://www.energy.gov/cmei/fuels/articles/current-2009-state-art-hydrogen-production-cost-estimate-using-water).
It needs an in-repository citation and reference-condition statement.

The shared availability table conflicts with component documentation:
METH-006 gives 98.5% for an electrolyser, while the PEM stack page states 99.5%
"throughout this study." It is not clear whether these represent a facility
and nested component, alternatives, or an accidental mismatch. The other flat
factors are uncited and mostly have no sensitivity. The pipeline values are
properly described as conventions, but 100% must not be interpreted as an
evidenced reliability result.

The page title includes annualisation, yet cost annualisation is owned entirely
by METH-003. Renaming or limiting the title later would improve navigation, but
this is editorial and not recorded as a separate issue.

## Findings

| Issue | Severity | Finding |
|---|---|---|
| ISS-0024 | Blocker | Availability boundaries, mapping and combination conflict |
| ISS-0025 | Major | Availability factors lack evidence and sensitivity |
| ISS-0026 | Moderate | Correct HHV value is uncited |

## Conclusion

- **Readiness:** blocked
- **Open blockers:** 1
- **Open major issues:** 1
- **Recommended correction order:** approve the availability ledger approach;
  reconcile component factors and bundling; add evidence/sensitivities; cite the
  HHV constant.

## COR-01B correction record

- **Disposition:** partially corrected in COR-01B.
- **Implemented:** the page now defines annual subsystem availability,
  component ownership, one-time architecture aggregation and hydrogen energy
  conversion on an HHV basis.
- **Issues closed:** ISS-0024 and ISS-0026.
- **Issue remaining:** ISS-0025, because subsystem availability evidence and
  sensitivities are still unresolved.
- **Readiness after correction:** partially implementable.
- **Validation:** see [COR-01B validation](../correction-validation/COR-01B.md).
