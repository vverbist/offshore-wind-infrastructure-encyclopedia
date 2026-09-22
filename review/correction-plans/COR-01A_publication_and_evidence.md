# COR-01A implementation plan — Publication readiness and evidence governance

## Objective

Make the published site honest about model readiness and evidence access without
changing any technical equation, numerical model result or component boundary.

This plan applies DEC-0021 and DEC-0022 and addresses ISS-0106 to ISS-0109.

## Scope boundary

### Included

- published sidebar readiness status;
- a controlled readiness vocabulary and legend;
- About and References evidence/reproducibility wording;
- evidence access/use classification in the bibliography;
- visible evidence-status labels on the References page; and
- validation of the full rendered site.

### Excluded

- correction of individual component citations or numerical inputs;
- replacement of confidential models or cost correlations;
- methodology equations and financial/availability calculations; and
- any change to a page's technical readiness result.

## Part A — Replace published completion with model readiness

### Readiness source of truth

Add one `readiness:` field to each QMD page's front matter. The controlled
published values will be:

- `not_reviewed`;
- `context_only`;
- `blocked`;
- `partially_implementable`;
- `ready_with_declared_uncertainty`; and
- `ready`.

Initial values will mirror `review/page-register.csv`. POS-001 will be
`not_reviewed` because it was explicitly excluded from review. The QMD front
matter becomes the publication source of truth; the review register remains
the audit record and will be checked against it after corrections.

Existing `completion:` values may remain as internal editorial metadata, but
the published site will not interpret or display them.

### Sidebar behavior

Replace the progress-sidebar implementation with a readiness-sidebar
implementation:

1. scan QMD `readiness:` front matter during pre-render;
2. generate the page-to-status map;
3. add a compact visible readiness badge to every navigated page;
4. use plain-language tooltips and a published legend;
5. give a section the least-ready status of its child pages rather than an
   averaged percentage; and
6. use color plus text so status does not depend on color alone.

Proposed labels:

| Stored value | Sidebar label |
|---|---|
| `not_reviewed` | Not reviewed |
| `context_only` | Context |
| `blocked` | Blocked |
| `partially_implementable` | Partial |
| `ready_with_declared_uncertainty` | Ready — uncertain |
| `ready` | Ready |

### Files affected

- front matter in all 41 QMD pages, one status field per page;
- `_quarto.yml`;
- `tools/build-progress-sidebar.js`, replaced by
  `tools/build-readiness-sidebar.js`;
- generated `progress-sidebar.js` and `progress-sidebar.html`, replaced by
  readiness-named equivalents; and
- `styles.css`.

The rename avoids retaining “progress” terminology for a readiness indicator.

## Part B — Publish evidence access and model use

### Canonical classification

Keep `references.bib` as the single evidence catalog. Each entry will receive
two controlled keyword dimensions:

**Access**

- `access-public`;
- `access-controlled-internal`; or
- `access-unresolved`.

**Model use**

- `use-adopted`;
- `use-validation-only`;
- `use-background-only`; or
- `use-unresolved`.

Where classification cannot be established from the page citations, source
record and completed reviews, use `unresolved`; do not infer adoption.

For adopted quantitative evidence, existing bibliography notes will be checked
for exact model use, version/date, source location and cost basis where
relevant. Missing information remains explicit and is not invented.

### Published References page

Revise `references.qmd` to:

- define the access and model-use classes;
- distinguish public reproducibility from controlled-internal reproduction;
- state that unresolved evidence cannot support a final model result;
- replace the duplicated background-document/source-type lists with a concise
  evidence-governance explanation;
- retain the complete bibliography as the evidence catalog; and
- display a status badge on every bibliography entry so active, validation,
  background and unresolved records are visibly distinct.

A small pre-render/browser helper will read the controlled bibliography
keywords and decorate the rendered bibliography. The catalog remains readable
without JavaScript because the classification is also stored in BibTeX.

### Published About page

Revise `about.qmd` to state:

- the model is under development and page readiness is published in the
  sidebar;
- public and controlled-internal reproducibility are different;
- confidential inputs are not independently reproducible unless a public
  fallback or range is provided; and
- the formal public bibliography is part of the source base, not only the
  working Word documents.

### Files affected

- `references.bib`;
- `references.qmd`;
- `about.qmd`;
- a focused evidence-status helper under `tools/`;
- generated evidence-status script/include files; and
- `_quarto.yml` or page front matter for the generated include.

## Register updates

After implementation:

- synchronize published QMD readiness with `page-register.csv`;
- record the evidence classification and metadata result for ISS-0106/0107;
- record the About correction for ISS-0108;
- record sidebar validation for ISS-0109; and
- close an issue only when its rendered behavior and source-of-truth check pass.

No model-input value or technical dependency will change in COR-01A.

## Validation

1. Validate every QMD page has exactly one allowed `readiness:` value.
2. Compare all 41 QMD readiness values with the page register.
3. Validate every bibliography entry has exactly one access and one model-use
   class.
4. Confirm no citation key is missing or duplicated.
5. Render the full Quarto website.
6. Inspect Home, one page in every readiness class, References and About.
7. Verify badges remain legible in normal, hover and keyboard-focus states.
8. Verify section status reflects the least-ready child.
9. Check equations, citations, figures, tables, cross-references and local links
   remain intact.
10. Confirm generated output under `_site/` is validation output only and is not
    edited manually.

## Expected issue result

| Issue | Expected status after COR-01A |
|---|---|
| ISS-0109 | Closed if readiness source, sidebar and legend reconcile |
| ISS-0108 | Closed if About accurately states evidence access and model maturity |
| ISS-0106 | Closed if every catalog record has visible evidence classes |
| ISS-0107 | Closed only if required metadata/model-use checks pass; otherwise remain open with an enumerated residual list |

## Implementation sequence

1. add and validate QMD readiness fields;
2. replace progress generation and styling with readiness behavior;
3. classify bibliography entries conservatively;
4. revise References and About;
5. generate helper assets;
6. render and inspect the full site; and
7. update issue/page registers with validation evidence.

## Approval requested

Approval of COR-01A authorizes only the files and behavior described above. Any
need to change technical page content, model values or component citations will
be reported separately before implementation.
