# METH-002 — System Boundary and LCOE

## Review metadata

- **Source page:** [methodology/system_boundary_and_lcoe.qmd](../../methodology/system_boundary_and_lcoe.qmd)
- **Batch:** B1_frame
- **Reviewer:** Codex
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The annual-cost-over-annual-energy definition is the right high-level LCOE
structure, and the page correctly puts export infrastructure inside the model
boundary. It is not yet a valid common comparison specification because the
denominator is electricity at the grid connection for one pathway and hydrogen
HHV at a backbone connection for the others.

## Calculation reconstruction

The documented calculation is only:

1. obtain component CAPEX and OPEX;
2. annualise CAPEX with the shared capital recovery factor;
3. obtain annual delivered energy at the architecture-specific interface; and
4. divide annual cost by annual delivered energy.

The equation is dimensionally correct if the numerator is EUR/year and the
denominator MWh/year. The page does not yet define a complete numerator or a
common denominator.

The secondary expression
`LCOE = C1/Yield + C2/Capacity Factor + C3` is not dimensionally reproducible as
written. The symbols have no units, and monetary costs and energy losses are
grouped in the same additive term. It should not guide implementation.

## Independent-implementer test

- **Can it be implemented?** Only as two different carrier-specific cost
  metrics, not as a like-for-like carrier comparison.
- **Missing decision:** whether the endpoint is carrier-specific or one common
  end-use service.
- **Missing cost ownership:** development, engineering, insurance, contingency,
  construction finance, decommissioning and other common project terms.
- **Missing lifecycle treatment:** replacement and terminal cash flows are not
  in the simple annuity.
- **Correctly delegated:** component cost, loss and availability methods belong
  on their component pages.

## Findings

| Issue | Severity | Finding |
|---|---|---|
| ISS-0015 | Blocker | Delivery products and endpoints are not comparable |
| ISS-0016 | Major | Conceptual LCOE expression is dimensionally undefined |
| ISS-0017 | Blocker | Lifecycle cost boundary has missing owners |

## Conclusion

- **Readiness:** blocked
- **Open blockers:** 2
- **Open major issues:** 1
- **Recommended correction order:** decide the common endpoint; define the
  complete cost ledger and annualisation handoff; replace the conceptual
  expression with auditable cost and energy equations.

## COR-01B correction record

- **Disposition:** corrected in COR-01B.
- **Implemented:** the page now defines the Tier 1 carrier endpoints, cost
  ownership, lifecycle-cost handoff and reproducible cost equations.
- **Issues closed:** ISS-0015, ISS-0016 and ISS-0017.
- **Readiness after correction:** partially implementable; component cost
  evidence remains owned by the component pages.
- **Validation:** see [COR-01B validation](../correction-validation/COR-01B.md).
