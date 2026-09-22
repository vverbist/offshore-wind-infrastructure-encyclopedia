# INST-004 — Platform and Substation Installation

## Review metadata

- **Source page:** [offshore_installation/platform_and_substation_installation.qmd](../../offshore_installation/platform_and_substation_installation.qmd)
- **Batch:** B6_installation
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The page has a sensible minimum-fidelity structure: piled-jacket, topside and
hook-up campaigns are separate; module count creates a discrete lift step; and
lift-class failure blocks cost rather than applying an arbitrary uplift. It
cannot produce installation CAPEX because all complete-spread rates,
mobilisation, logistics and hook-up duration are unresolved, while the upstream
platform page supplies no jacket, pile or module inventory.

The cited CVOW evidence needs tighter use. It supports 5 net days per piled
jacket and 2.5 net days per complete topside—not 2.5 days for every arbitrary
module lift. It also reports 30 days for three piled jackets and 60 days for
complete construction, installation and commissioning of three topsides. Those
totals can constrain the reference campaign, but the 60-day boundary includes
final cable connection and cannot be inserted without reconciling INST-003.

## 1. Model role and boundary

- **Purpose:** calculate installation CAPEX for crane-installed topsides on
  piled jackets.
- **Campaigns:** piled jacket, topside placement, and hook-up/commissioning.
- **Supply boundary:** jacket, piles, topside and hosted equipment excluded.
- **Installation boundary:** normal campaigns, matching logistics and defined
  commissioning included; exceptional seabed and piling work separate.
- **Duplication risk:** cable pull-in/termination is allocated to INST-003,
  while the cited platform commissioning total includes final cable connection.

## 2. Upstream inputs

| Input | Unit | Classification | Owner/source | Status |
|---|---:|---|---|---|
| Platform count and capacity | count; MW | architecture output | ARCH-003/PLAT-001 | Multiplicity rule missing |
| Jacket, pile and topside module records | counts; t; dimensions | physical output | PLAT-001 | Missing |
| Jacket and topside class capacity | t at configuration/radius | contractor input | selected spread | Missing |
| Net site durations | day/OSS; day/topside or lift | sourced/project | CVOW/project | Reference anchors only |
| Logistics and hook-up duration | day/campaign; day/OSS | contractor/owner input | selected execution plan | Missing |
| Three rates and mobilisation | EUR2025/day; EUR2025 | commercial inputs | complete spreads | Missing |
| Exceptional work | scope and EUR2025 | site-specific | project packages | Missing when applicable |

## 3. Calculation reconstruction

The page multiplies platform count by module count, screens the largest jacket
and topside module lifts against selected class capacities, builds three
chargeable durations, and multiplies each by a matching rate. Mobilisation is a
separate lump sum and exceptional work is added only when scoped.

### Boundary and limiting-case checks

- Counts must be positive integers; masses, capacities, durations and rates
  must be non-negative with positive capacities for a screen.
- The largest pile lift/handling case must also pass the selected foundation
  campaign, not only jacket mass.
- Passing nominal SWL is only an exclusion screen; the page states this
  correctly.
- A complete-topside duration cannot be multiplied by module count unless a
  module-specific task basis is supplied.
- Reference campaign totals must be reconciled to net placement, logistics,
  hook-up and cable connection exactly once.

## 4. Outputs and downstream consumers

| Output | Unit | Downstream consumer | Interface status |
|---|---:|---|---|
| Installation-class result | status | METH-005 | Blocked by physical records |
| Jacket/topside lift counts | count | schedule and cost | Module inventory missing |
| Campaign days and costs | day; EUR2025 | METH-002/METH-003 | Blocked |
| Total installation CAPEX | EUR2025 | architecture comparison | Blocked |

## 5. Technical correctness

The campaign-cost equations and discrete module-count relationship are
dimensionally correct. The lift gate is appropriately one-sided.

The source does not support interpreting 2.5 days per complete topside as 2.5
days per module lift. A split-topside branch needs module-specific placement,
mating and hook-up logic or an evidenced aggregate duration. Piles are part of
the piled-jacket campaign, but no pile mass/count/handling feasibility screen
exists.

## 6. Model fidelity

Aggregate site and logistics durations are defensible; pile-driving task
simulation and carrier concurrency are unnecessary without evidence. The
minimum missing fidelity is a reference execution concept that identifies
pre- or post-piling, jacket/pile transport, module split, heavy-lift class,
commissioning scope and matching complete-spread rates. Alternative float-over
or self-installing concepts should remain separate branches, as the page says.

## 7. Cost and evidence audit

| Value/relationship | Exact support checked | Review result | Finding |
|---|---|---|---|
| 5 days/OSS piled jacket | CVOW says each foundation approximately 5 days; 30 days total for three | Valid net anchor; total campaign constraint omitted |
| 2.5 days/topside | CVOW says each topside approximately 2.5 net days | Mislabelled as day/lift when modules may exceed one | ISS-0103 |
| 60 days/three topsides | CVOW complete construction, installation and commissioning total | Useful aggregate check, but includes final cable connection and is not decomposed | ISS-0104 |
| Complete spread rates and mobilisation | No adopted public evidence | Correctly unresolved | ISS-0102 |

## 8. Independent-implementer test

- **Can the page be implemented?** The equations can; no physical class or
  cost result can.
- **Missing numerical evidence:** pile/module masses, class capacities,
  logistics, hook-up duration, rates, mobilisation and exceptional work.
- **Missing decisions:** platform count/design, pre- versus post-piling,
  module split, installation class and commissioning boundary.
- **Missing implementation rules:** pile feasibility and use of reference
  total campaign durations.
- **Correctly unresolved:** detailed lift engineering and task decomposition.

## 9. Explanation and site placement

The page is concise, ordered and in the correct site location. Its input tables
make unresolved values visible. The future correction should explicitly show
the reference-case reconciliation `net + logistics + hook-up + connection =
campaign total` before general equations are applied.

## 10. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0027 | implementation_readiness | blocker | Platform count, capacity and structural/material model are unresolved | Yes, DEC-0007 |
| ISS-0052/0063/0083 | implementation_readiness | blocker | Hosted-equipment physical and lift ledgers are missing | Yes, DEC-0009/0013/0016 |
| ISS-0101 | implementation_readiness | blocker | Jacket, pile and topside module inventory and pile feasibility are absent | Yes, DEC-0020 |
| ISS-0102 | cost_input | blocker | Every complete-spread rate, mobilisation, logistics and hook-up input needed for cost is unresolved | Yes, DEC-0020 |
| ISS-0104 | cost_boundary | blocker | Hook-up/commissioning and final cable-connection scopes are not reconciled | Yes, DEC-0020 |
| ISS-0103 | reference_evidence | major | A sourced duration per complete topside is applied per arbitrary module lift | Yes, DEC-0020 |

## 11. Page conclusion

- **Readiness:** blocked
- **Reason:** the structure is suitable, but physical lift records, execution
  concept and all commercial campaign inputs are missing.
- **Open blockers:** 7
- **Open major issues:** 1
- **Downstream consequences:** central electrical/hydrogen platform
  feasibility, installed CAPEX and architecture comparison.
- **Recommended correction order:** close platform/module/pile inventory;
  select a reference execution concept; reconcile commissioning/cable scope;
  then adopt campaign durations and complete-spread costs.
