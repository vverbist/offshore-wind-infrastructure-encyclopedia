# Review framework

This directory stores review evidence and findings separately from the published
Quarto pages. A review finding is recorded here before any correction is made to
the source page.

## Source of truth

The registers have distinct roles:

- `issue-register.csv` is the authoritative list of findings from discovery to
  closure.
- `page-register.csv` records review coverage, workflow state and readiness for
  every page.
- `model-input-register.csv` records model-relevant inputs, assumptions,
  equations and their evidence status.
- `dependency-register.csv` records interfaces between page outputs and
  downstream inputs.
- `decision-log.md` records modelling and editorial decisions that resolve one
  or more findings.

Detailed review reasoning belongs in `page-reviews/`. Batch synthesis and the
final integration tests use the templates in `templates/`. The detailed notes
support the registers but do not replace them.

Decision recommendations and approval matrices belong in `decision-packs/`.
They explain proposed choices but do not become approved decisions until the
selected outcome is recorded in `decision-log.md`.

Approved decisions are translated into file-level proposals in
`correction-plans/`. A correction plan defines scope and validation but does
not authorize source edits until the user explicitly approves that plan.

## Review and correction boundary

The review baseline remains unchanged during a review batch. Reviewers record
findings in this directory and do not correct source pages at the same time.

The handoff is:

1. Review a page and record its detailed assessment.
2. Add each actionable finding to `issue-register.csv`.
3. Reconcile findings across the batch.
4. Record required user decisions in `decision-log.md`.
5. Agree a correction batch and enter its identifier in the issue register.
6. Correct only the approved scope.
7. Recheck the affected calculations, pages and dependencies.
8. Close an issue only after the correction and validation evidence have been
   recorded.

This separation preserves the original evidence behind a finding and prevents
an issue from disappearing merely because its wording was changed.

## Identifiers

- Pages use the stable IDs assigned in `page-register.csv`.
- Issues use `ISS-0001`, `ISS-0002`, and so on.
- Decisions use `DEC-0001`, `DEC-0002`, and so on.
- Model inputs use `INP-0001`, `INP-0002`, and so on.
- Dependencies use `DEP-0001`, `DEP-0002`, and so on.
- Correction batches use `COR-01`, `COR-02`, and so on.

Identifiers are never reused, including after an item is rejected or closed.

## Controlled values

### Page review status

- `not_started`
- `in_review`
- `needs_decision`
- `reviewed`
- `remediation_approved`
- `closed`

### Page readiness

- `not_reviewed`
- `ready`
- `ready_with_declared_uncertainty`
- `partially_implementable`
- `blocked`
- `context_only`

### Issue category

- `technical_correctness`
- `model_fidelity`
- `cost_input`
- `reference_evidence`
- `implementation_readiness`
- `clarity`
- `site_structure`
- `cross_page_consistency`

Use the principal category for the issue. Related aspects can be explained in
the finding or consequence fields rather than duplicating the issue.

### Finding type

- `explicit_gap`: the source page already identifies the unresolved item.
- `new_finding`: the review identified an issue not made explicit on the page.
- `cross_page_gap`: ownership or instructions conflict across pages.
- `evidence_maintenance`: the model claim is supportable, but its citation,
  version or source location is not sufficiently stable or precise.

### Issue severity

- `blocker`: prevents implementation or invalidates the comparison.
- `major`: can materially change sizing, energy, cost or conclusions.
- `moderate`: weakens auditability or permits inconsistent implementation.
- `minor`: improves clarity, navigation or editorial quality without changing
  the model result.

### Issue status

- `open`
- `needs_decision`
- `accepted`
- `correction_approved`
- `corrected_pending_validation`
- `closed`
- `rejected`
- `deferred`

An issue is closed only when `resolution` and `validation_evidence` in the issue
register show what changed and how the correction was checked.

### Input class

- `sourced_input`
- `modelling_assumption`
- `scenario_input`
- `derived_result`
- `unresolved_input`

### Verification status

- `not_checked`
- `verified`
- `partially_verified`
- `unsupported`
- `not_applicable`

### Dependency interface status

- `not_checked`
- `defined`
- `defined_with_uncertainty`
- `ambiguous`
- `missing`
- `inconsistent`
- `not_parameterized`

## Page-review workflow

For each substantive page:

1. Identify its model role, boundary, upstream inputs and downstream consumers.
2. Reconstruct the calculation in execution order.
3. Test technical correctness and the accuracy-complexity balance.
4. Verify quantitative inputs and references.
5. perform the independent-implementer test.
6. Review explanation, directness and page placement.
7. Record findings, readiness and downstream consequences.

Overview and contextual pages use the same workflow where applicable, with
greater emphasis on scope, navigation and consistency.

## Review batches

The batches in `page-register.csv` follow model dependency order:

1. `B1_frame`: positioning, methodology and architecture definition.
2. `B2_generation`: wind resource, layout, turbine and foundation.
3. `B3_electrical`: electrical collection, conversion and export.
4. `B4_h2_production`: hydrogen production equipment and integration.
5. `B5_h2_infra`: hydrogen infrastructure and platform material CAPEX.
6. `B6_installation`: offshore installation calculations.
7. `B7_site_integration`: references, about page and whole-site integration.

`electrical_infra/infield_ac_cables.qmd` is the pilot page. Its method review is
completed before the remaining batches begin.
