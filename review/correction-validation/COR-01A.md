# COR-01A validation — Publication readiness and evidence governance

## Scope

This record validates the approved COR-01A publication and evidence changes.
It does not validate technical component calculations or change any page's
reviewed model-readiness result.

## Automated source and render checks

| Check | Result |
|---|---|
| QMD readiness metadata | Pass: 41/41 pages have exactly one allowed value |
| Page-register reconciliation | Pass: 41/41 published values match the register; POS-001 maps from not_started to published not_reviewed |
| Bibliography evidence classes | Pass: 128/128 records have exactly one access and one model-use class |
| Bibliography keys | Pass: 128 unique records; 88 keys cited by content pages; no cited key missing |
| Generated readiness map | Pass: 41 page records |
| Generated evidence map | Pass: 128 source records |
| Rendered page coverage | Pass: 41 HTML pages |
| Published helper inclusion | Pass: all 41 rendered pages include the readiness and evidence helpers; no obsolete progress helper remains |
| Rendered bibliography coverage | Pass: 128 bibliography entries |
| Full Quarto render | Pass: completed with exit code 0 and produced _site/index.html |

Evidence-class totals:

- access: 112 public, 11 controlled internal, 5 unresolved;
- model use: 78 adopted, 10 validation only, 38 background only, 2 unresolved.

## Residual issue

ISS-0107 remains open. The controlled classes now expose the status, but five
records still have unresolved access and the wider catalog still contains
missing date/access-date, exact source-location, cost-basis and
source-to-model-input metadata. COR-01A did not invent those missing details.

## Validation boundary

Per the user's instruction, validation stopped after automated checks and the
full render. No visual inspection of rendered pages, badge layout, hover state
or keyboard-focus appearance was performed.
