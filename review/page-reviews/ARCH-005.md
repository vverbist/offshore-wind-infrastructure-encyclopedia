# ARCH-005 — Component Mapping

## Review metadata

- **Source page:** [architectures/component_mapping.qmd](../../architectures/component_mapping.qmd)
- **Batch:** B1_frame
- **Reviewer:** Codex
- **Completed:** 2026-08-21
- **Review status:** reviewed
- **Readiness:** partially_implementable

## Executive assessment

This is one of the strongest frame pages. It provides a compact physical-scope
ledger across all three architectures, identifies canonical component owners
and states the no-double-counting rule. The architecture columns agree with the
individual pages, all links resolve, and the table is more useful than repeated
descriptive prose.

## Completeness check

The physical equipment mapping covers the main generation, conversion,
collection and export functions. Three omissions limit its use as the complete
scope-control instrument:

1. common lifecycle categories such as development, engineering, insurance,
   construction finance, contingency, replacement and decommissioning are
   mentioned in prose but have no owner rows;
2. the decentralised header-to-export manifold is absent even though H2I-002
   explicitly excludes it; and
3. the onshore hydrogen connection is assigned to a section overview that does
   not define the interface facility or cost.

The already-recorded central-hydrogen switchgear ambiguity (ISS-0012) is also
not visible in this matrix. A second economic-scope table would address these
items without cluttering the physical component table.

## Site placement and model fidelity

Placement after the individual architecture pages is logical: the reader first
sees each chain and then the consolidated ledger. The page should continue to
control ownership rather than reproduce equations. Adding missing rows is
minimum sufficient detail because it directly prevents omission and double
counting.

## Findings

| Issue | Severity | Finding |
|---|---|---|
| ISS-0030 | Moderate | Economic and interface scope is not fully mapped |
| ISS-0012 | Major | Central-hydrogen collection switchgear owner ambiguous |
| ISS-0028 | Major | Hydrogen onshore connection owner incomplete |
| ISS-0029 | Blocker | Decentralised export manifold owner missing |

## Conclusion

- **Readiness:** partially_implementable
- **Open blockers:** inherited ISS-0029
- **Open major issues:** inherited ISS-0012 and ISS-0028
- **Direct moderate issues:** 1
- **Recommended correction order:** add missing physical interfaces, then add
  an economic-scope ownership table aligned with METH-002 and METH-003.
