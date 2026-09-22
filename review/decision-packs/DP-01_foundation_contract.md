# Decision pack 01 — Publication and model foundation contract

## Purpose

This pack groups the six decisions that should be resolved before component
corrections begin. It recommends defaults that preserve auditability, avoid
unsupported precision and keep the first executable model manageable.

No source correction is authorized by accepting this pack. Accepted decisions
will first be recorded in `review/decision-log.md`; a separate correction scope
will then be proposed for approval.

## Recommended decisions at a glance

| Decision | Recommended selection | Why it is the default |
|---|---|---|
| DEC-0021 | Keep editorial progress and model readiness as separate controlled fields | Avoids calling polished but blocked pages complete |
| DEC-0022 | Use one evidence catalog with explicit access/status classes and public fallback treatment | Preserves confidential evidence without overstating public reproducibility |
| DEC-0003 | Use a two-tier endpoint: carrier-specific outputs may be reported, but carrier ranking requires a common-service scenario | Keeps the core model bounded while preventing invalid like-for-like claims |
| DEC-0004 | Use one project-wide real discounted-cash-flow convention with a WACC sensitivity range | Makes replacements and different lifetimes comparable without unsupported financing detail |
| DEC-0005 | Use an enumerated design sweep with explicit candidate sets, feasibility filtering and Pareto output | Preserves discrete thresholds and is easiest to audit |
| DEC-0006 | Use one architecture event/state ledger, with simple factors only for minor non-overlapping subsystems | Prevents double derating without requiring a full reliability simulation |

## DEC-0021 — Published progress and model readiness

### Recommended selection

Maintain two separate fields:

1. **Documentation progress:** an editorial percentage describing how much of
   the intended page content has been drafted and checked.
2. **Model readiness:** one controlled status: `context_only`, `blocked`,
   `partially_implementable`, `implementable_with_declared_uncertainty`, or
   `validated`.

The sidebar may retain the percentage only when it is explicitly labelled
“documentation progress.” Model readiness should be visible independently and
must be generated from one maintained record rather than inferred from the
percentage.

### Why

Fourteen blocked pages currently show at least 80% completion. Editorial
progress and executable readiness answer different questions; collapsing them
creates false confidence.

### Alternative

Replace the percentage entirely with readiness statuses. This is simpler for
readers but loses useful internal drafting progress.

### Consequence of approval

A small publication-governance correction can align page metadata, the sidebar,
About and a status legend. It does not change any model calculation.

## DEC-0022 — Evidence access and source status

### Recommended selection

Keep one controlled source catalog, with every model-relevant source assigned
one status:

- `public_adopted` — publicly accessible and used directly;
- `controlled_internal` — available only within the governed project;
- `validation_only` — used to test or contextualize, not as an input;
- `background_only` — informed development but does not support a current
  quantitative claim; or
- `unresolved` — incomplete and not valid for a final model result.

For each adopted quantitative input, record exact model use, source location,
version/date, access status and—where relevant—currency, price year, scope and
normalization. When confidential evidence materially drives a published
result, publish a reproducible fallback/range or label the result
controlled-internal and not independently reproducible.

### Why

This preserves legitimate confidential data while making the public audit
boundary honest. It also prevents uncited or unfinished bibliography records
from appearing to support the model.

### Alternatives

- Publish only public active evidence and keep all internal/background records
  outside the site. This maximizes clarity but hides useful provenance.
- Publish confidential-source descriptions without a fallback. This is
  acceptable only when outputs using them are clearly restricted to
  controlled-internal reproducibility.

### Consequence of approval

References, About and the input/source ledger can be aligned before individual
cost inputs are corrected.

## DEC-0003 — Common comparison endpoint

### Recommended selection

Adopt a two-tier comparison contract:

1. **Carrier-specific system outputs:** report electricity at the defined PCC
   and hydrogen at the defined backbone receipt point as different products.
   Compare cost, efficiency and density within each carrier, but do not rank
   their EUR/MWh values as equivalent.
2. **Common-service scenarios:** rank electricity and hydrogen only when a
   scenario defines the same end-use service, location and time basis and adds
   all required storage, reconversion, distribution, demand matching, losses
   and costs for both carriers.

The first executable release should implement tier 1 and expose the tier-2
interface without inventing end-use assumptions. Tier 2 becomes a separately
scoped extension.

### Why

Forcing a common service now would add storage, reconversion and demand models
that the evidence base does not yet support. Ranking different delivered
products is technically invalid. The two-tier contract keeps current component
work usable without making an unsupported cross-carrier claim.

### Alternatives

- Extend both chains to one common service immediately. This gives the strongest
  carrier ranking but materially expands scope and evidence needs.
- Keep only carrier-specific endpoints. This is simplest but cannot answer
  which carrier is preferable for a shared end use.

### Consequence of approval

METH-002 and architecture pages can define valid denominators and result labels.
The model will not publish a single electricity-versus-hydrogen ranking until a
common-service scenario exists.

## DEC-0004 — Financial and lifecycle convention

### Recommended selection

Use one project-wide **real, unlevered, pre-tax discounted-cash-flow ledger** in
constant EUR2025:

- adopt one evidenced real WACC base value with a sensitivity range;
- place initial CAPEX at the agreed investment timing;
- record OPEX annually by non-overlapping scope;
- record component replacements in their actual model years;
- include decommissioning and residual value explicitly when evidenced;
- use component-specific technical lives without giving them unsupported
  financing rates; and
- derive annualized comparison metrics from the complete discounted ledger.

Architecture-specific financing may be added only as a documented sensitivity,
not embedded in component costs.

### Why

One common convention isolates physical and cost differences between
architectures. Timed cash flows are necessary for electrolyser-stack
replacement and assets with different lives; a simple project CRF cannot
represent them reliably.

### Alternative

Use architecture/component-specific discount rates. This may be useful later,
but the current evidence does not support the additional distinctions and they
could predetermine the architecture result.

### Consequence of approval

The current 6.6% value becomes provisional until evidenced. All component pages
must emit dated cost categories rather than self-annualized totals where
replacement timing matters.

## DEC-0005 — Search and variable taxonomy

### Recommended selection

Use a transparent enumerated design sweep:

1. define external scenario variables separately from design variables;
2. list every continuous grid and discrete candidate set, including bounds and
   resolution;
3. construct each candidate deterministically;
4. reject infeasible candidates with recorded reasons;
5. evaluate time-step energy, physical quantities and lifecycle cost;
6. retain threshold alternatives where uncertain evidence crosses a discrete
   choice; and
7. report the non-dominated cost-versus-energy-density Pareto set rather than a
   hidden weighted objective.

Optimization algorithms may later accelerate the same declared search space,
but they must reproduce the enumerated reference cases and constraints.

### Why

The model contains many integer steps—cable/string counts, trains, modules,
pipelines, vessel loads and platform classes. Enumeration is easier to audit
and less likely to smooth away those decisions.

### Alternative

Adopt a formal optimizer immediately. This can be faster for large spaces but
adds convergence, constraint and reproducibility questions before the model
chain is stable.

### Consequence of approval

METH-004 and METH-005 can establish one canonical variable table, evaluation
order, feasibility record and result-selection rule.

## DEC-0006 — Availability accounting

### Recommended selection

Create one architecture event/state ledger:

- define whether each outage is represented in the generation time series, as
  a component state, or as an energy-equivalent factor;
- apply each cause once at its owning subsystem;
- model discrete states for material shared assets where failure changes
  available capacity materially, such as export links, central compressors,
  platforms and electrolyser trains;
- use evidenced energy-equivalent factors for minor or genuinely aggregate
  non-overlapping subsystems; and
- calculate architecture availability from the resulting time-step capacity,
  not by multiplying every published percentage indiscriminately.

Flat 100% or 99% values remain unresolved assumptions unless supported.

### Why

This captures material common-mode and partial-capacity failures without
building a detailed reliability simulation for every component. It also
prevents double derating when a time series already contains an outage effect.

### Alternatives

- Use only flat subsystem factors. This is simpler but weak for central/shared
  assets and redundancy choices.
- Use full event simulation for all components. This adds more parameters and
  apparent precision than the current evidence supports.

### Consequence of approval

METH-006 becomes the architecture ledger owner, while component pages provide
state capacities, failure/maintenance evidence or explicitly unresolved inputs.

## Approval matrix

For each row, record `accept recommended`, `choose alternative` with a note, or
`defer`.

| Decision | Selection | Notes or constraints |
|---|---|---|
| DEC-0021 | Decided | Publish model readiness in the sidebar; keep editorial completion internal |
| DEC-0022 | Decided | Accepted the recommended classified evidence catalog and public-fallback rule |
| DEC-0003 | Decided with clarification | Tier 1 only for now: EUR/kW-wind, electricity EUR/MWh, hydrogen EUR/MWh-H2 HHV and EUR/kg; no equivalent end-use claim |
| DEC-0004 | Decided with simplification | Provisional 6.6% real WACC and 25 years; simple CRF; component OPEX; material short-life replacement only; decommissioning equals 80% of installation CAPEX |
| DEC-0005 | Alternative selected | Deterministic model only; distinguish user inputs, fixed parameters, derived quantities and outputs |
| DEC-0006 | Decided with simplification | Annual subsystem availability owned by components and combined once on a side-by-side architecture page |

## Proposed correction batches after decisions

### COR-01A — Publication and evidence governance

Applies DEC-0021/0022 to About, References, evidence metadata and published
status indicators. Validation: full-site render, citation/source-status audit,
and readiness-versus-open-issue reconciliation.

### COR-01B — Common methodology contract

Applies DEC-0003 to DEC-0006 to system boundary/LCOE, finance, workflow,
optimization and availability pages. Validation: dimensional checks, one
minimal scenario schema, timed-cash-flow example, candidate-filter example and
no-double-derating example.

The two batches should remain separate so editorial/evidence governance can be
validated without mixing it with model-method changes.
