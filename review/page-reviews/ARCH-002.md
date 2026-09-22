# ARCH-002 — Electricity Export with HVDC

## Review metadata

- **Source page:** [architectures/electricity_export_hvdc.qmd](../../architectures/electricity_export_hvdc.qmd)
- **Batch:** B1_frame
- **Reviewer:** Codex
- **Completed:** 2026-08-21
- **Review status:** reviewed
- **Readiness:** partially_implementable

## Model role and boundary

The page defines a coherent physical chain from turbine generation through AC
collection, offshore HVDC conversion, export and onshore conversion to the grid
connection. Included and excluded functions are clear, and every listed
physical component has a plausible canonical owner. Installation is correctly
kept inside the economic boundary but delegated to installation pages.

The page is concise, dependency-led and technically reasonable at architecture
level. It avoids duplicating component equations or costs. The diagram,
inclusion table and interfaces agree with ARCH-001 and ARCH-005.

## Cross-page implementation status

The architecture cannot yet produce a closed model case because:

- the pilot found that the 34-string example does not fit the referenced 2 GW
  platform bay arrangement (ISS-0004);
- array topology, pull-ins and electrical losses remain unresolved
  (ISS-0001 to ISS-0003);
- platform material CAPEX is not parameterised (dependency DEP-0027);
- the full project-cost boundary has missing common owners (ISS-0017); and
- its grid-electricity endpoint is not comparable to hydrogen HHV at a backbone
  connection without the decision in ISS-0015.

These are component and methodology gaps, not defects in this page's physical
description. The architecture page should remain a scope page and link to the
eventual resolved interface rules rather than absorb their calculations.

## Conclusion

- **Readiness:** partially_implementable
- **Direct findings:** none
- **Open blockers:** inherited from collection/platform and comparison boundary
- **Recommended correction order:** close the 2 GW collection/platform design,
  then align the architecture endpoint and common economic boundary.
