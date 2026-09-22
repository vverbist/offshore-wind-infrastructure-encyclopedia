# Whole-site integration review

## Review metadata

- **Review date:** 2026-08-21
- **Reviewer:** Codex
- **Coverage:** 40 of 41 registered QMD pages
- **Excluded by user request:** `positioning.qmd` (POS-001)
- **Detailed batches:** B1 to B7

## Executive assessment

The site has a strong information architecture and an unusually good intended
model boundary. Navigation follows a defensible dependency order, all 41 QMD
pages are registered and present in the sidebar, all 196 checked local links
resolve, all 88 used citation keys exist, and no duplicate citation or
cross-reference identifier was found.

The content is not yet a closed techno-economic model. Of the 40 reviewed
pages, 28 calculation or synthesis pages are blocked, 11 are partially
implementable and one is context-only. The dependency register contains 64
missing, 11 ambiguous and 9 inconsistent interfaces out of 117. The largest
gaps are not page placement or prose volume; they are the common comparison
contract, executable workflow, physical equipment/inventory ledgers and
evidence-backed cost/availability packages.

## Information architecture

### Navigation order

The primary order is logical:

1. purpose and positioning;
2. shared methodology;
3. architecture definitions;
4. wind resource and layout;
5. turbine system;
6. electrical and hydrogen subsystems;
7. shared platforms;
8. offshore installation; and
9. references and about.

Platforms and installation correctly remain separate from hosted equipment and
material supply. No page move is recommended.

### Section gateways

Most section overviews state their role and point to their child calculations.
Three gateway corrections remain:

- METH-001 describes six methodology pages but links none directly
  (ISS-0105);
- H2P-001 omits DC Integration and does not show the architecture paths
  (ISS-0059); and
- INST-001 links only cable/pipeline installation (ISS-0090).

### Published progress indicator

The sidebar derives a percentage from each page's `completion:` field, but no
definition connects that percentage to calculation readiness, evidence quality
or editorial completion. Fourteen blocked pages display 80% or higher; ARCH-003
and ARCH-004 display 100% despite open blockers. This can cause a reader to
treat prose completion as model completion (ISS-0109).

## Automated integrity checks

| Check | Result |
|---|---:|
| Registered QMD pages | 41 |
| QMD pages absent from register | 0 |
| Registered pages absent from sidebar navigation | 0 |
| Local QMD/file targets checked | 196 |
| Broken local targets | 0 |
| Bibliography entries | 128 |
| Duplicate bibliography keys | 0 |
| Content citation keys | 88 |
| Used citation keys missing from bibliography | 0 |
| Defined cross-reference labels | 11 |
| Cross-reference uses | 13 |
| Undefined or duplicate cross-references | 0 |

These tests establish structural integrity, not correctness of the cited claim
or completeness of quantitative evidence. Those were assessed page by page.

## Model coverage

### Functions with a clear intended owner

- architecture definitions and physical component mapping;
- wind resource reduction and wake/layout generation;
- turbine and foundation supply;
- electrical collection, conversion, export and grid connection;
- hydrogen DC integration, stack, BOP, compression and pipelines;
- platform material/fabrication boundary; and
- turbine/foundation, linear-asset and platform installation.

### Material ownership gaps

| Missing or incomplete owner | Consequence | Principal findings |
|---|---|---|
| Common delivered product and endpoint | Architecture LCOE is not comparable | ISS-0015 |
| Development, finance, replacement, decommissioning and residual value | Lifecycle numerator is incomplete | ISS-0017/0019 |
| Executable calculation/search sequence | Independent model build cannot be ordered or reproduced | ISS-0020–0022 |
| Architecture availability and fault-state ledger | Annual output can be double- or under-derated | ISS-0024/0025 |
| Export manifold and onshore hydrogen receipt package | Hydrogen chain has missing physical endpoints | ISS-0028/0029 |
| Architecture-specific equipment mass/cost/lift records | Turbine, platform and installation effects cannot close | ISS-0038/0045/0052/0063/0083 |
| Complete routed cable and TCP inventory | Supply and installation do not share one physical system | ISS-0001/0002/0069/0078 |
| Platform multiplicity and structure | Central architectures have no physical/cost platform result | ISS-0027 |
| Complete installation spreads | Installed CAPEX is not available | ISS-0091/0098/0099/0102 |

## Cross-page consistency

### Terminology and symbols

Most component pages define symbols and units locally. The largest semantic
conflicts are conceptual rather than typographic:

- operating, receipt, design and rated pipeline pressure are conflated;
- system, cable, route, physical and pass counts are not consistently inherited
  across electrical/hydrogen pages;
- availability can mean component uptime, architecture derating or an already
  derated energy series; and
- “complete spread,” “installed cost” and commissioning scopes do not yet use a
  common inclusion ledger.

### Financial and price basis

The common EUR2025 method is well explained, but several component costs bypass
it, apply it twice or lack a source price year. Cost boundaries are generally
more problematic than currency arithmetic: equipment, offshore packaging,
support vessels, installation, OPEX and replacement are frequently mixed or
unowned.

### Unresolved information

The best pages explicitly return **not parameterized** rather than zero. This is
not consistent site-wide: some pages use smooth legacy assumptions or
unsupported percentages while adjacent pages leave the same evidence class
unresolved. Correction should preserve explicit gaps and remove placeholders
before adding more model detail.

## Architecture symmetry

The three architecture descriptions are physically clear, but the comparison
is not symmetric:

- electricity is delivered as electricity at a grid interface;
- hydrogen is delivered as HHV at a backbone interface;
- reconversion, storage and demand matching are not consistently represented;
- onshore reinforcement/receipt packages are incomplete for both carriers; and
- shared lifecycle and availability scopes are not applied through one ledger.

Until DEC-0003 to DEC-0006 are resolved, downstream component precision cannot
make the architecture result comparable.

## Reader-path tests

| Reader question | Result |
|---|---|
| What is being compared and why? | Clear from Home, Positioning and Architectures, but POS-001 was outside this review |
| What are the outputs and boundaries? | Intended boundaries are clear; the common endpoint and lifecycle boundary are not closed |
| Which components belong to each architecture? | Clear from ARCH-005, with lifecycle and interface omissions |
| Where does each input originate? | Mixed: citations resolve, but many quantitative inputs are unsupported or opaque |
| How does each calculation feed the next? | Partly visible; 84 of 117 interfaces are missing, ambiguous or inconsistent |
| Which results remain blocked and why? | Available in review artifacts, but not communicated reliably by the published completion indicator |

## Evidence and reproducibility

The public citation layer is technically healthy: every used key resolves.
The published source page does not distinguish the 88 actively cited sources
from 40 uncited/background entries because it renders `@*`. Five records are
explicitly unfinished, and metadata conventions are uneven.

The site's claim that confidential evidence is documented sufficiently for
reproducibility is not currently defensible. A result may be reproducible only
inside a controlled environment when coefficients or raw points cannot be
published. That is acceptable if stated and governed, but it is different from
independent public reproduction.

## Model-fidelity conclusion

The project generally chooses the right level of computational detail. It does
not need CFD, transient gas networks, detailed vessel simulation, compressor
maps or structural finite-element models. The missing fidelity is bottom-up
accounting at decision thresholds:

- physical sections and flows;
- equipment/train/module counts;
- discrete qualified product and vessel classes;
- peak versus time-step sizing;
- replacement/fault states; and
- non-overlapping cost and installation packages.

Adding those records will improve both accuracy and simplicity because it
replaces scattered percentages and proxies with shared interfaces.

## Findings

### New B7 findings

| Issue ID | Category | Severity | Finding | Affected pages |
|---|---|---|---|---|
| ISS-0105 | site_structure | moderate | The methodology gateway has no direct links to its six child pages | METH-001 |
| ISS-0106 | reference_evidence | major | The published bibliography conflates active evidence, background records and unfinished placeholders | REF-001; all pages |
| ISS-0107 | reference_evidence | major | Evidence metadata and model-use mapping are incomplete and inconsistent | REF-001; quantitative pages |
| ISS-0108 | cross_page_consistency | major | About overstates independent reproducibility and understates the public evidence base | ABOUT-001; REF-001; H2I-004 |
| ISS-0109 | site_structure | moderate | Published completion percentages conflict with model readiness and open blockers | site-wide |

### Highest-priority inherited findings

| Priority group | Findings | Reason |
|---|---|---|
| Comparison contract | ISS-0015/0017/0019–0024 | Determines what the model is calculating and whether architectures are comparable |
| Physical design backbone | ISS-0001/0004/0027/0029/0034–0038/0043 | Supplies discrete topology, area, equipment and platform records used everywhere downstream |
| Evidence-backed component packages | ISS-0045/0052/0060–0069/0079–0088 | Closes cost, loss, mass and qualification without unsupported extrapolation |
| Installation closure | ISS-0091–0104 | Converts supplied physical assets into installed CAPEX once |

## Review-framework limitation

The review registers use more input-class, verification-status and issue-category
labels than the controlled values listed in `review/README.md`. This does not
change the site findings, but the register taxonomy should be normalized before
automated correction dashboards or closure reporting are built.

## Whole-site conclusion

- **Structure:** logical; no page relocation required.
- **Technical model:** not executable end to end.
- **Comparison readiness:** blocked by the endpoint, lifecycle, workflow and
  availability contract before component gaps are considered.
- **Evidence readiness:** public citations resolve, but active-source and
  confidential-evidence governance are incomplete.
- **Editorial quality:** generally direct and calculation-led; status signaling
  and a few overview gateways need correction.
- **Recommended next action:** decide the comparison/governance contract, then
  execute the dependency-led correction roadmap rather than correcting pages in
  navigation order.
