# PLAT-001 — Platform Material CAPEX

## Review metadata

- **Source page:** [platforms/platform_material_capex.qmd](../../platforms/platform_material_capex.qmd)
- **Batch:** B5_h2_infra
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The page has an excellent accounting boundary. It separates hosted-equipment
CAPEX from equipment mass, structure supply from offshore installation, and
topside, support structure and foundation scope. It correctly refuses to
report a placeholder CAPEX while evidence is absent.

No calculation can yet be developed. Platform count, hosted-equipment masses,
structural/outfitting mass, jacket/foundation quantities, cost relationship,
price basis and lift modules are all unresolved. These are not isolated gaps:
electrical, hydrogen-production and compressor pages currently fail to emit
the physical ledgers this page requires.

## 1. Model role and boundary

- **Purpose:** convert architecture-specific hosted equipment into platform
  topside/support/foundation material and fabrication CAPEX.
- **Architectures:** electricity export and centralised hydrogen.
- **Included:** topside structural steel/outfitting, jacket and piles or the
  selected equivalent support/foundation.
- **Excluded:** hosted equipment CAPEX and offshore installation/hook-up.
- **Canonical distinction:** component pages own equipment cost and mass; this
  page owns only the added structure and its supply cost.

## 2. Upstream inputs

| Input | Unit | Owner | Status |
|---|---:|---|---|
| Number and rating of platforms | count; MW/platform | Architecture/METH-005 | Missing for variable central H2 designs |
| Converter/collection equipment mass | t by block | ELEC-003 | Missing, ISS-0063 |
| Stack mass | t by module | H2P-003 | Missing, ISS-0052 |
| BOP mass | t by package | H2P-004 | Missing, ISS-0052/0053 |
| Electrolyser power-electronics mass | t by block | H2P-005 | Missing, ISS-0052 |
| Compressor mass/footprint | t; m2 by train | H2I-003 | Missing, ISS-0083 |
| Shared auxiliaries/building inventory | t; m2 | No complete owner | Missing |
| Structural/outfitting relationship | t structure/t equipment or bottom-up quantities | This page | Missing |
| Jacket/foundation quantities | t; pile records | This page/site class | Missing |
| Fabrication/material cost basis | EUR2025 by quantity | This page | Missing |

## 3. Required calculation reconstruction

The page correctly implies the following dependency order, but none of the
steps is parameterized:

1. determine discrete platform count and rating;
2. assemble a mutually exclusive hosted-equipment ledger by platform;
3. add shared auxiliaries once;
4. derive structural and outfitting mass from an evidenced relationship or
   reference design;
5. size the jacket/support and foundations for the adopted site/design class;
6. calculate material/fabrication cost on a stated price and scope basis; and
7. return complete structures and lift modules to installation.

### Boundary and limiting-case checks

- Decentralised hydrogen must return zero central platforms by architecture,
  not a zero-mass platform.
- Equipment shared by trains/platforms must be booked once.
- Platform count, module count and installation-class changes must remain
  discrete.
- A mass-to-cost relation must remain within its source rating/mass/site range.
- Structural supply must not include installation or repeat hosted-equipment
  cost.

## 4. Outputs and downstream consumers

| Output | Unit | Downstream consumer | Interface status |
|---|---:|---|---|
| Platform count and type | count/class | INST-004; METH-002 | Missing |
| Topside equipment/structural mass breakdown | t | cost; lift planning | Missing |
| Jacket and pile inventory | t; count; dimensions | INST-004 | Missing |
| Lift-module records and maximum lift | count; t | INST-004 | Missing |
| Material/fabrication CAPEX | EUR2025 | METH-002/LCOE | Missing |
| Applicability/feasibility state | pass/fail/class change | METH-005 | Missing |

## 5. Technical correctness and model fidelity

There is no equation to verify. The proposed boundary and refusal to use
material CAPEX as an installation proxy are technically correct.

The minimum sufficient model should not jump directly from MW to EUR. A
reference-design or bounded mass-based model is sufficient if it keeps hosted
equipment, added structure, jacket/foundation and installation modules
separate. Detailed structural analysis is unnecessary at this stage, but a
capacity/mass applicability envelope and discrete platform-count rule are
essential.

## 6. Cost and evidence audit

No cost input, source or price year is adopted. That is correctly explicit,
but it makes centralised hydrogen and electricity-export platform supply CAPEX
unresolved. The legacy 750,000 EUR/MW platform coefficient is not documented
on this page and cannot silently fill the gap; it also lacks a visible
structure/equipment/installation boundary.

## 7. Independent-implementer test

- **Can the page be implemented?** No.
- **Missing numerical evidence:** every mass and cost-driving relationship.
- **Missing decisions:** platform count/rating rule, reference structure and
  whether to use bounded reference cases or an evidenced mass relation.
- **Missing rules:** shared auxiliaries, module splitting, feasibility/class
  changes and treatment outside the evidence range.
- **Correctly unresolved:** detailed structural engineering can remain a
  qualification gate after a screening reference is selected.

## 8. Explanation and site placement

The page is direct, concise and correctly located in a common Platforms section
after architecture-specific components. The cost-boundary table should be
preserved. No page move is needed. A future correction should add one visual
input/output ledger before adding broader platform background.

## 9. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0027 | implementation_readiness | blocker | Platform multiplicity, mass feasibility and material-CAPEX method are unresolved | Yes, DEC-0007 |
| ISS-0052 | implementation_readiness | blocker | Hydrogen-production mass and lift ledgers are missing | Yes, DEC-0009 |
| ISS-0053 | model_fidelity | blocker | BOP scaling does not produce defensible central packages/masses | Yes, DEC-0012 |
| ISS-0063 | implementation_readiness | blocker | Converter equipment/block mass ledger is missing | Yes, DEC-0013 |
| ISS-0083 | implementation_readiness | blocker | Compressor mass, footprint and lift ledger is missing | Yes, DEC-0016 |

## 10. Page conclusion

- **Readiness:** blocked
- **Reason:** the boundary is sound but every cost-driving physical input and
  the structural cost relationship remain unresolved.
- **Open blockers:** 5
- **Open major issues:** 0
- **Downstream consequences:** platform supply CAPEX, platform feasibility,
  transport/lift selection and both central-architecture totals remain open.
- **Recommended correction order:** decide platform scaling; complete all
  hosted-equipment ledgers; select a bounded structural reference/cost method;
  then emit jacket, pile and lift-module records to installation.
