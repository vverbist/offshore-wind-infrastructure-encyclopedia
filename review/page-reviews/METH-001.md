# METH-001 — Methodology overview

## Review metadata

- **Source page:** [methodology/overview.qmd](../../methodology/overview.qmd)
- **Batch:** B1_frame
- **Reviewer:** Codex
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Model role and assessment

This page is a concise landing page for the shared modelling conventions. Its
placement before the architecture and component sections is logical, and its
links correspond to the six methodology pages in the site navigation.

The stated calculation scope is clear: component costs, conversion, losses,
availability and installation are intended to form one turbine-to-delivery
model. The page appropriately leaves component-specific assumptions to their
owners.

The overview is not independently executable, and it inherits four unresolved
method decisions from the detailed pages:

1. electricity and hydrogen do not currently share a comparable delivery
   product or endpoint (ISS-0015);
2. the full lifecycle cost numerator has no complete ownership ledger
   (ISS-0017);
3. the integrated workflow is not specified in calculation order (ISS-0021);
4. the optimisation problem and variable taxonomy are not closed (ISS-0020,
   ISS-0022).

The phrase "deterministic techno-economic optimisation framework" is therefore
an intended model description, not yet a reproducible method. Once the detailed
pages are corrected, this overview should summarize the actual execution and
comparison convention in two or three sentences and retain its current brevity.

## Findings and conclusion

No separate issue is needed; the page is affected by ISS-0015, ISS-0017,
ISS-0020, ISS-0021 and ISS-0022.

- **Readiness:** blocked
- **Open blockers:** inherited from the detailed methodology pages
- **Open major issues:** inherited
- **Recommended correction order:** decide endpoint, finance/lifecycle method
  and search method; then align this overview to those decisions.

## COR-01B correction record

- **Disposition:** corrected in COR-01B.
- **Implemented:** the overview now states the deterministic model contract,
  carrier-specific Tier 1 outputs and links to the detailed methodology pages.
- **Issues closed:** ISS-0105.
- **Readiness after correction:** partially implementable; the remaining
  evidence limitations are inherited from METH-003 and METH-006.
- **Validation:** see [COR-01B validation](../correction-validation/COR-01B.md).
