# Batch 1 review — Model frame

## Scope

Reviewed on 2026-08-21:

- `index.qmd`;
- six methodology pages; and
- five architecture pages.

`positioning.qmd` was excluded from this batch at the user's request. It was not
given a page assessment or correction recommendation. Where the formal
methodology and architecture pages depend on a comparison-purpose decision,
that dependency is recorded from the reviewed pages themselves.

No source `.qmd` page was changed. This file and the review registers are the
handoff between review and any later approved correction batch.

## Outcome

| Result | Count |
|---|---:|
| In-scope pages reviewed | 12 |
| Context-only pages | 1 |
| Partially implementable pages | 3 |
| Blocked pages | 8 |
| New issues | 16 |
| Blockers | 9 |
| Major issues | 5 |
| Moderate issues | 2 |
| Decisions proposed | 5 |

The high blocker count does not mean the frame is broadly poor. The
architecture descriptions and site order are generally strong. The blockers
are concentrated in a small number of shared conventions that affect many
pages at once.

## Review by criterion

### Technical correctness

The base LCOE definition, CRF equation, price normalisation order and hydrogen
HHV value are technically sound. The CRF arithmetic and ECB exchange-rate
convention reproduce correctly.

Two technical problems require correction:

- electricity at a grid connection and hydrogen HHV at a backbone connection
  are different delivered products, so their EUR/MWh values are not a common
  end-service comparison (ISS-0015); and
- the conceptual `C1/Yield + C2/Capacity Factor + C3` expression is not
  dimensionally defined (ISS-0016).

### Model approach and fidelity

The selected fidelity is mostly appropriate. The frame preserves important
physical and discrete relationships—wake-density trade-offs, stack sizing,
pipeline classes/counts and 2 GW HVDC blocks—without attempting detailed
engineering optimisation.

The missing item is not more physical detail but a reproducible search method:
the scenario/design-variable taxonomy, variable bounds, constraints,
calculation sequence, feasibility treatment and cost-density result-selection
rule are absent or inconsistent (ISS-0020 to ISS-0023).

### Cost inputs and references

The EUR2025 conversion convention is clear and auditable. The ECB value is
properly cited. The 1.5 equipment markup is correctly labelled as an assumption
rather than attributed to its manufactured-cost source.

The model cannot yet produce a complete lifecycle cost because:

- 6.6% real WACC is unsupported and incompletely scoped (ISS-0018);
- replacement and terminal cash flows are not annualised (ISS-0019); and
- common project cost categories do not have canonical owners (ISS-0017,
  ISS-0030).

### Explanation and directness

The home and architecture pages are concise and easy to navigate. Flow diagrams
and the component mapping provide useful scope control without duplicating
component calculations.

The methodology pages are short but currently too short for implementation.
They name concepts instead of specifying calculation order and data contracts.
Corrections should add equations, tables and rules—not general background.

### Independent model development

The reviewed pages are insufficient to reproduce the integrated model. The
minimum missing information is:

1. one comparison endpoint convention;
2. one variable/scenario taxonomy and executable design-search definition;
3. a lifecycle discounted-cash-flow annualisation;
4. an architecture-specific availability ledger; and
5. ownership and sizing rules for the central platform, hydrogen terminal and
   decentralised export manifold.

Component equations can be developed in parallel, but an integrated result
should not be presented until these frame decisions are closed.

### Site structure

The overall order—home, methodology, architectures, physical subsystems,
installation—is logical and dependency-led. All Batch 1 `.qmd` links resolve.
No page move is recommended.

The component mapping is in the right place and should be extended with an
economic-scope ownership table. The Energy/Availability page title mentions
annualisation even though financial annualisation is on METH-003; this can be
cleaned up during correction but is not material enough for a separate issue.

## Strong parts to preserve

- Short, calculation-focused landing pages.
- Separation between architecture inclusion and component calculation owners.
- Explicit distinction between physical co-location and accounting scope.
- EUR2025 normalisation discipline.
- Preservation of discrete equipment choices.
- Clear acknowledgement of known unresolved assumptions rather than invented
  placeholder values.

## Recommended correction sequence

Do not correct pages issue by issue in navigation order. Resolve the shared
decisions first:

1. **DEC-0003:** comparison endpoint and functional unit.
2. **DEC-0005:** scenario/design-variable taxonomy and search method.
3. **DEC-0004:** WACC and lifecycle cash-flow convention.
4. **DEC-0006:** availability ownership and combination.
5. **DEC-0007:** central platform capacity and multiplicity.

After those decisions, correct the methodology pages as one coordinated group,
then close the architecture-interface owners in the component mapping and
individual architecture pages. Validate the full website because the changes
will be site-wide conventions and cross-page links.

## Records created

- Detailed assessments: `review/page-reviews/HOME-001.md`,
  `METH-001.md` to `METH-006.md`, and `ARCH-001.md` to `ARCH-005.md`.
- Issues: ISS-0015 to ISS-0030.
- Inputs: INP-0023 to INP-0048.
- Dependencies: DEP-0014 to DEP-0032.
- Decisions: DEC-0003 to DEC-0007.
