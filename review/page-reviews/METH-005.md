# METH-005 — Optimisation Variables

## Review metadata

- **Source page:** [methodology/optimisation_variables.qmd](../../methodology/optimisation_variables.qmd)
- **Batch:** B1_frame
- **Reviewer:** Codex
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The page correctly identifies the physical trade-offs that the model should
preserve: wake loss versus installed density, stack CAPEX versus efficiency,
compression versus pipeline capacity, and discrete export assets. This is the
right level of physical fidelity for a screening model. The actual search
problem is not specified.

## Missing optimisation specification

For each variable the page needs a role, unit, admissible range or candidate
set, and architecture applicability. It currently provides none of the search
bounds, spacing grid, pressure classes, pipeline classes, stack overplanting
range, export-capacity decisions or tie-breaking rules.

The model is described as system cost minimisation, while areal yield is also a
principal output with an explicit cost-density trade-off. Without a constraint,
weight or non-dominated-frontier rule there is no unique optimisation problem.
A transparent enumerated sweep with Pareto filtering would be sufficient; a
more complex optimiser is not required unless the design space demands it.

The 2 GW HVDC step is a material and appropriate discontinuity. The sourced
link-count equation exists on the onshore-grid page, but this page neither cites
it nor makes it the canonical implementation. Partial use of the last block and
associated curtailment must be defined.

## Model fidelity

The proposed variable set preserves material discrete pipeline and HVDC
choices. It should not be expanded into detailed engineering optimisation until
component inputs support that fidelity. The immediate need is a complete,
minimal design vector and feasibility gate, not more variables.

## Findings

| Issue | Severity | Finding |
|---|---|---|
| ISS-0022 | Blocker | Design vector, constraints and objective rule missing |
| ISS-0023 | Major | HVDC block has no canonical sourced implementation here |
| ISS-0020 | Blocker | Several listed variables conflict with METH-004 roles |

## Conclusion

- **Readiness:** blocked
- **Open blockers:** 1 directly assigned, plus ISS-0020
- **Open major issues:** 1
- **Recommended correction order:** approve the search/variable decision;
  define objective outputs and Pareto rule; then specify bounds, discrete sets,
  constraints and the canonical 2 GW link-count handoff.

## COR-01B correction record

- **Disposition:** corrected and repurposed in COR-01B.
- **Implemented:** optimisation has been removed from the current model scope;
  the page now defines a deterministic one-case workflow and explicit status
  outcomes.
- **Issues closed:** ISS-0022 and ISS-0023.
- **Readiness after correction:** partially implementable.
- **Validation:** see [COR-01B validation](../correction-validation/COR-01B.md).
