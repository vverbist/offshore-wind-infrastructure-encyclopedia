# METH-004 — Modelling Workflow

## Review metadata

- **Source page:** [methodology/modelling_workflow.qmd](../../methodology/modelling_workflow.qmd)
- **Batch:** B1_frame
- **Reviewer:** Codex
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The page gives a useful vocabulary for fixed inputs, scenarios, derived values
and outputs, but it is a parameter list rather than an executable workflow. It
also conflicts with the next methodology page over the role of key hydrogen
design variables.

## Reconstructed data flow

The intended order can be inferred as wind/resource and site inputs → turbine
layout → wake-adjusted production → architecture-specific collection and
conversion → export sizing → losses and availability → annual delivered energy
and annual cost → LCOE and areal yield. That order is not stated on the page,
and several essential handoffs remain undefined:

- time resolution and production-profile schema;
- dispatch, curtailment and component part-load evaluation;
- architecture branch logic;
- component-sizing and discrete selection order;
- feasibility checks and treatment of rejected designs;
- annual aggregation and output record;
- enumeration/optimisation and result-selection rule.

Stack overplanting, pipeline pressure and pipeline selection appear under
scenario parameters here. METH-005 calls the same quantities optimisation
variables, and the hydrogen infrastructure overview says pressure, diameter
and pipeline count are optimised jointly. Turbine number is also called a
scenario input while spacing and power density are design outcomes, so their
relationship needs an explicit definition.

## Independent-implementer test

An implementer can identify many needed fields but cannot determine when and
how they are evaluated. Units, owners, admissible ranges and missing-input
behaviour are absent from the page. The output list is sensible, but
"optimised component sizing decisions" cannot be reproduced without the search
specification on METH-005.

## Findings

| Issue | Severity | Finding |
|---|---|---|
| ISS-0020 | Blocker | Scenario and optimisation roles conflict |
| ISS-0021 | Blocker | Integrated execution sequence is missing |

## Conclusion

- **Readiness:** blocked
- **Open blockers:** 2
- **Open major issues:** 0
- **Recommended correction order:** approve the variable taxonomy, then write
  the calculation/data-flow sequence with feasibility and output rules.

## COR-01B correction record

- **Disposition:** corrected in COR-01B.
- **Implemented:** the page now separates case inputs, fixed parameters,
  sourced parameters, derived quantities, calculated costs and outputs.
- **Issues closed:** ISS-0020 and ISS-0021.
- **Readiness after correction:** partially implementable; unresolved numeric
  evidence remains visible in the input register.
- **Validation:** see [COR-01B validation](../correction-validation/COR-01B.md).
