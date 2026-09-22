# ABOUT-001 — About

## Review metadata

- **Source page:** [about.qmd](../../about.qmd)
- **Batch:** B7_site_integration
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** reviewed
- **Readiness:** partially_implementable

## Executive assessment

The page accurately identifies the three architectures and the site's main
purpose as documenting a component-level techno-economic model. It is concise
and correctly placed. Its source and reproducibility description no longer
matches the repository.

The site now uses a substantial public bibliography in addition to the working
Word documents. Conversely, several material inputs remain confidential,
opaque or unavailable to an independent implementer. The statement that those
inputs are documented to the level needed for reproducibility is therefore too
strong, particularly for the pipeline cost relation and several equipment
curves and ledgers.

## 1. Page role and boundary

- **Purpose:** explain what the site documents and the architectures covered.
- **Included:** methodology, assumptions, component models and evidence basis.
- **Missing context:** current model maturity, public versus controlled-internal
  reproducibility and the difference between documented structure and a closed
  executable model.

## 2. Claim audit

| Claim | Review result |
|---|---|
| The site documents a component-level techno-economic model | Correct |
| Three architectures are compared | Correct |
| Documentation is limited to methodology and assumptions | Mostly correct, though pages also contain worked calculations and intermediate outputs |
| Source material is a set of working Word documents | Incomplete; 88 formal bibliography keys are actively cited |
| Confidential data are documented sufficiently for model reproducibility | Not currently supportable |

The confidential pipeline material-cost implementation is the clearest
counterexample: coefficients are unavailable, source price/scope metadata are
incomplete and the disclosed fit is not independently reproducible
(ISS-0087). Similar access and physical-ledger gaps occur in stack, BOP and
installation evidence.

## 3. Independent-reader test

- **What is being documented?** Clear.
- **Which architectures?** Clear.
- **Is the site a complete executable model?** Not stated.
- **Which results are publicly reproducible?** Not stated.
- **How are confidential inputs governed?** Not stated.
- **Where should evidence limitations be checked?** No link to the references
  page or a model-status statement.

## 4. Explanation and site placement

The page belongs at the end of the site and should remain short. A correction
needs only a precise evidence-access statement, a link to the reference basis
and one sentence distinguishing the intended model from its current readiness.

## 5. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0108 | cross_page_consistency | major | The About page overstates independent reproducibility and understates the public evidence base | Yes, DEC-0022 |

## 6. Page conclusion

- **Readiness:** partially_implementable
- **Reason:** purpose and scope are clear, but evidence-access and readiness
  claims are inaccurate.
- **Open blockers:** 0
- **Open major issues:** 1
- **Downstream consequences:** reader trust and interpretation of confidential
  model results.
- **Recommended correction order:** decide the public/internal evidence policy,
  then align About and References to the same statement.

## COR-01A correction record

- ISS-0108 closed: About now distinguishes public and controlled-internal
  reproducibility and states the limitation created by confidential evidence
  without a public fallback.
- ISS-0109 closed: About now defines the published readiness vocabulary and the
  sidebar no longer publishes editorial completion as model completion.
- Page readiness remains `partially_implementable`; COR-01A did not revise the
  technical review result.
- Automated checks and the full render are recorded in
  [COR-01A validation](../correction-validation/COR-01A.md).
