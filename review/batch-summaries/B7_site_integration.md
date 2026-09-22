# Batch 7 review — References, About and whole-site integration

## Scope

Reviewed on 2026-08-21:

- `references.qmd`;
- `about.qmd`;
- `_quarto.yml` navigation and progress-status behavior;
- all QMD local links, citation keys and cross-references; and
- the B1–B6 findings, decisions, inputs and dependency interfaces as one model
  chain.

`positioning.qmd` remains excluded at the user's earlier request. No source QMD,
configuration, bibliography, code or generated site output was changed.

## Outcome

| Result | Count |
|---|---:|
| Registered QMD pages | 41 |
| Pages covered by review | 40 |
| User-excluded pages | 1 |
| Blocked pages | 28 |
| Partially implementable pages | 11 |
| Context-only pages | 1 |
| Total open/decision findings after B7 | 109 |
| Blockers | 54 |
| Major issues | 44 |
| Moderate issues | 11 |
| New B7 issues | 5 |
| New B7 decisions | 2 |

The site structure is logical and technically intact. The model is not ready
for end-to-end implementation or architecture comparison. Its main constraints
are shared method and interface decisions rather than missing pages.

## Structural integrity

| Test | Result |
|---|---:|
| QMD pages absent from page register | 0 |
| Registered pages absent from navigation | 0 |
| Local page/file links checked | 196 |
| Broken local links | 0 |
| Bibliography entries | 128 |
| Citation keys used by content pages | 88 |
| Missing used citation keys | 0 |
| Duplicate bibliography keys | 0 |
| Undefined or duplicate cross-references | 0 |

No site-wide page move is recommended. Methodology, hydrogen production and
installation overviews need gateway-link corrections, but their sections are
in the right place.

## References and reproducibility

The bibliography works mechanically, but References is a catalog rather than
an evidence ledger. `nocite: @*` displays 40 uncited records alongside active
evidence. Five entries explicitly remain incomplete; 36 entries have no
year/date and 29 URL records have no access date. Some undated web resources
are legitimate, but the site has no enforced metadata convention by evidence
type or mapping from source to adopted input.

About correctly states the project purpose and architectures. Its claim that
confidential data are documented sufficiently for reproducibility is not
consistent with component findings such as the unavailable TCP cost
coefficients and other controlled physical/cost packages. Public independent
reproduction and controlled-internal reproduction need separate definitions.

## Site status and reader context

The progress sidebar is potentially misleading. Fourteen blocked pages show
80% completion or higher, including ARCH-003 and ARCH-004 at 100%. The site
does not say whether percentage means writing progress, evidence coverage,
implementation readiness or validation.

A reader can navigate the subject matter successfully but cannot determine
which calculations are executable without consulting the review directory.
DEC-0021 therefore asks for a published readiness convention separate from—or
replacing—the current percentage.

## Model integration result

The dependency register contains:

| Interface status | Count |
|---|---:|
| Missing | 64 |
| Ambiguous | 11 |
| Inconsistent | 9 |
| Not parameterized | 9 |
| Defined with uncertainty | 19 |
| Defined | 2 |

The independent reader path breaks at four levels:

1. **Comparison contract:** different delivered products/endpoints, incomplete
   lifecycle cost, undefined search and availability aggregation.
2. **Physical backbone:** unresolved area/layout, topology, equipment mass,
   platform, cable/TCP section and lift inventories.
3. **Component packages:** missing or inconsistent loss, cost, OPEX,
   replacement, qualification and price-basis records.
4. **Installation closure:** no complete coherent spread package converts all
   supplied assets to installed CAPEX.

## New findings

| Issue ID | Severity | Finding |
|---|---|---|
| ISS-0105 | Moderate | Methodology overview has no direct child-page links |
| ISS-0106 | Major | Bibliography conflates active, background and unfinished evidence |
| ISS-0107 | Major | Source metadata and model-use mapping are inconsistent |
| ISS-0108 | Major | About overstates independent reproducibility |
| ISS-0109 | Moderate | Completion percentages conflict with model readiness |

## Decisions required

| Decision ID | Question | Consequence of delay |
|---|---|---|
| DEC-0021 | What does published completion mean, and how is model readiness shown? | readers can mistake blocked pages for complete models |
| DEC-0022 | How are public, internal, confidential, validation-only and unresolved sources classified? | evidence access and reproducibility remain ambiguous |

The highest-priority inherited decisions remain DEC-0003 to DEC-0006 because
they define the comparison endpoint, lifecycle basis, executable workflow/search
and availability ledger. Component and installation decisions should follow
those shared contracts.

## Final correction order

1. publication/readiness and evidence governance;
2. common comparison, lifecycle, workflow/search and availability contract;
3. wind/layout, turbine, topology and physical equipment backbone;
4. electrical and hydrogen component packages;
5. platform and installation closure; and
6. end-to-end reference-case validation and full-site render.

The detailed sequence and exit tests are recorded in
`review/correction-roadmap.md`.

## Records created or updated

- Detailed reviews: `REF-001.md` and `ABOUT-001.md`.
- Whole-site synthesis: `review/site-review.md`.
- Final correction roadmap: `review/correction-roadmap.md`.
- New issues: ISS-0105 to ISS-0109.
- New dependencies: DEP-0118 and DEP-0119.
- New decisions: DEC-0021 and DEC-0022.
- No new model input was introduced by the two contextual/reference pages.
- Page coverage: 40 of 41 pages, with POS-001 retained as user-excluded.
