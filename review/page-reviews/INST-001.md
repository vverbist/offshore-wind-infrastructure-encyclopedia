# INST-001 — Offshore Installation Overview

## Review metadata

- **Source page:** [offshore_installation/overview.qmd](../../offshore_installation/overview.qmd)
- **Batch:** B6_installation
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** reviewed
- **Readiness:** partially_implementable

## Executive assessment

The page gives the correct high-level boundary: installation is separate from
material CAPEX, and cable and pipeline campaigns share a time-and-rate
accounting framework while retaining asset-specific methods. It is too short
to function as the section gateway it claims to be. It links only the cable
and pipeline page, leaving the turbine/foundation and platform/substation
calculations undiscoverable from the overview.

## 1. Model role and boundary

- **Purpose:** introduce offshore installation as the conversion of supplied
  components into installed assets.
- **Included classes:** turbines, foundations, cables, pipelines, platforms
  and substations.
- **Canonical boundary:** component supply and installation CAPEX are
  separate.
- **Missing gateway content:** direct links, short scope distinctions, result
  status and the shared cost boundary are absent.

## 2. Upstream inputs

This overview owns no quantitative input. It should point readers to the
physical inventories and campaign inputs owned by INST-002 to INST-004.

## 3. Calculation reconstruction

No calculation is presented or expected. The claimed shared framework is
implemented on INST-003, not defined here.

## 4. Outputs and downstream consumers

The page is navigational and produces no model output. Its downstream consumer
is the reader selecting the relevant installation calculation.

## 5. Technical correctness

The supply-versus-installation distinction is correct. Saying cable and
pipeline installation can use the same framework is also appropriately
qualified by asset-specific constraints and rates.

## 6. Model fidelity

No added technical background is needed. A compact map of the three
calculation pages and their applicability would be sufficient.

## 7. Cost and evidence audit

No number or cost input is introduced.

## 8. Independent-implementer test

- **Can the page be implemented?** Not applicable as a calculation.
- **Can it guide an implementer?** Only partially; two of the three detailed
  calculation pages are not linked.

## 9. Explanation and site placement

The page is in the correct location and is direct. It should link all detail
pages and state that current numerical readiness differs by subclass. No page
move or additional overview page is needed.

## 10. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0090 | site_structure | moderate | The section overview links only cable/pipeline installation and does not route the reader to the other two calculation pages | No |

## 11. Page conclusion

- **Readiness:** partially_implementable
- **Reason:** the boundary is correct, but the page is not yet a complete
  section gateway.
- **Open blockers:** 0
- **Open major issues:** 0
- **Downstream consequences:** discoverability and interpretation only.
- **Recommended correction order:** add links and one-line applicability and
  result-status descriptions for INST-002 to INST-004.
