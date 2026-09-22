# METH-003 — Financial and Price-Basis Assumptions

## Review metadata

- **Source page:** [methodology/financial_and_price_basis.qmd](../../methodology/financial_and_price_basis.qmd)
- **Batch:** B1_frame
- **Reviewer:** Codex
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The price-normalisation method is clear and appropriately strict about source
currency, price year and cost boundary. The EUR2025 convention, escalation
order and prohibition on generic market multipliers are suitable for an
auditable screening model. The financial annualisation is incomplete for the
model actually described elsewhere.

## Calculation and evidence checks

The normalisation equation first escalates a source-currency value to 2025 and
then applies a 2025 annual-average exchange rate. Units cancel correctly. The
ECB 2025 average of 1 EUR = 1.1300 USD is correctly cited and represented as
`1/1.1300 EUR/USD`.

The capital recovery factor calculation was independently reproduced:

- at `r = 0.066/year` and `n = 25 years`, `CRF = 0.082741447/year`;
- the displayed 8.27%/year and 12.09-year reciprocal are correct.

The 1.5 manufactured-to-purchased-equipment multiplier is transparently
classified as a modelling assumption rather than attributed to NREL. Its scope
is clearly separated from installation, soft costs and inflation.

## Implementation gaps

The 6.6% real WACC has no evidence, sensitivity, tax convention or statement of
whether financing risk is common across the three architectures. Because the
model compares systems with different capital structures, this is material.

More importantly, the simple CRF equation cannot incorporate timed stack
replacement, other component lifetimes, decommissioning or residual value. The
page acknowledges this but does not provide the discounted-cash-flow equation.
The stack page already expects a replacement within the project life, so the
gap is active rather than hypothetical.

## Findings

| Issue | Severity | Finding |
|---|---|---|
| ISS-0018 | Major | WACC is unsupported and incompletely scoped |
| ISS-0019 | Blocker | Replacement and terminal cash flows are not annualised |

## Conclusion

- **Readiness:** blocked
- **Open blockers:** 1
- **Open major issues:** 1
- **Recommended correction order:** approve the finance/lifecycle convention,
  add the discounted cash-flow annualisation, then select and evidence the WACC
  base case and sensitivities.

## COR-01B correction record

- **Disposition:** partially corrected in COR-01B.
- **Implemented:** the page now defines the provisional 6.6% real WACC, 25-year
  horizon, simple CRF, material replacement rule and 80% decommissioning
  allowance on offshore installation CAPEX.
- **Issue closed:** ISS-0019.
- **Issue remaining:** ISS-0018, because the WACC still needs evidence and
  sensitivity treatment.
- **Readiness after correction:** partially implementable.
- **Validation:** see [COR-01B validation](../correction-validation/COR-01B.md).
