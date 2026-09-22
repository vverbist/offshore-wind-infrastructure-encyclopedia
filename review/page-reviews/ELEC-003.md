# ELEC-003 — HVDC Converter Stations

## Review metadata

- **Source page:** [electrical_infra/hvdc_converter_stations.qmd](../../electrical_infra/hvdc_converter_stations.qmd)
- **Batch:** B3_electrical
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The physical scope, 2 GW reference configuration, current equation and
converter/platform separation are explained clearly. The central cost is
technically incorrect: the page treats the DEA 320 EUR/kW 2025 planning value
as if it were still a 2020 value and escalates it again. The resulting 785
EUR2025/kW pair is about 22.6% above the direct two-terminal application of the
source's 2025 central value (640 EUR/kW). The offshore terminal is also costed
with an onshore coefficient, and no hosted-equipment mass/block inventory is
provided to the platform and installation models.

## 1. Model role and boundary

- **Purpose:** size and cost offshore/onshore VSC converter electrical
  equipment and represent its losses and capacity states.
- **Included:** valves, converter transformers, reactors, cooling, auxiliaries,
  immediate switchgear, control and protection at both terminals.
- **Excluded:** offshore structure/foundation/installation, export cables and
  wider onshore reinforcement.
- **Architectures:** electricity export only.

## 2. Upstream inputs

| Input | Unit | Classification | Source/status |
|---|---:|---|---|
| Link rating and pole voltage | GW; kV | sourced design | TenneT 2 GW standard; verified |
| Terminal equipment coefficient | EUR/kW | sourced cost | DEA 2025; mis-transformed |
| Terminal efficiency | dimensionless | modelling assumption | 0.985 each; limited comparator |
| Terminal availability | dimensionless | legacy assumption | 0.98 each; unsupported |
| Link count/utilisation | count; MW | discrete design rule | incomplete under ISS-0023 |

## 3. Calculation reconstruction

For balanced operation,
$I_\mathrm{pole}=P_\mathrm{dc}/(2V_\mathrm{pole})=1.905$ kA at 2 GW and
525 kV. The page then applies a general-price factor
$1.263/1.030=1.22621$ to the DEA 320 EUR/kW value and doubles the result for
two terminals. This second escalation is not supported by the source.

The source catalogue identifies 0.27 MEUR/MW as the underlying price and 0.32
MEUR/MW as its 2025 central planning value, with 0.25–0.42 MEUR/MW as the 2025
range. It explicitly says that 2025 prices already add 20% to source prices.
See the [DEA Technology Data for Energy Transport](https://ens.dk/media/6705/download),
Table 7. Direct use gives 640 EUR/kW for a pair and 500–840 EUR/kW as the pair
range before any separate offshore adjustment.

### Boundary and limiting-case checks

- $P\geq0$, $V>0$ and efficiency in $(0,1]$ are required.
- Link count and partial final-link utilisation must remain discrete.
- A half-capacity pole state requires every retained component and cable path
  to support that mode.
- Capacity-state availability must replace both flat terminal factors.
- Converter equipment mass, dimensions and block/lift records are required
  before platform feasibility can be asserted.

## 4. Outputs and downstream consumers

| Output | Unit | Downstream consumer | Interface status |
|---|---:|---|---|
| Converter pair CAPEX | EUR2025 | METH-002 | incorrect base transformation |
| Terminal losses | MWh/year | METH-006 | screening constants only |
| Capacity states | MW and hours | METH-006 | conceptual; probabilities absent |
| Hosted equipment mass/blocks | t; dimensions; count | PLAT-001/INST-004 | missing |
| Electrical OPEX | EUR2025/year | LCOE | TBD; legacy code uses 2% |

## 5. Technical correctness

- The pole-current equation and 1.905 kA result are correct.
- Two 98.5% terminal efficiencies multiply to 97.0225%, reasonably rounded to
  97.0%.
- The 4 × 500 MW block, 525 kV bipole, metallic return and degraded 1 GW path
  are supported by the TenneT technical reference.
- The cost escalation is incorrect (ISS-0061).
- The DolWin2 loss statement supports order of magnitude only, as the page
  correctly notes; it does not evidence 1.5% loss for this 2 GW design.

## 6. Model fidelity

An aggregated pair coefficient and fixed terminal efficiency are appropriate
for screening if their scope is correct and sensitivities are used. A detailed
VSC model is unnecessary. Discrete terminal/link blocks and physical hosted
mass are necessary because platform count, partial availability and installation
feasibility depend on them.

## 7. Cost and evidence audit

| Value/relationship | Evidence result | Finding |
|---|---|---|
| DEA 320 EUR/kW 2025 central | directly supported | page escalates it twice; ISS-0061 |
| Onshore coefficient applied offshore | no matched offshore-electrical-only source | ISS-0062 |
| 527 EUR/kW platform/premium proxy | difference of aggregate scopes, not additive item | retain as comparator only |
| Converter OPEX | no adopted source | part of ISS-0070/system OPEX gap |

## 8. Independent-implementer test

The rating and current can be reproduced. A correct complete converter result
cannot: the adopted cost is wrong, offshore electrical scope is a proxy,
equipment mass/block data are absent, the partial-link cost rule is unresolved,
and the executable legacy values differ from the page.

## 9. Explanation and site placement

Clear, direct and in the right place. The green/grey cost convention is useful.
After correction, present the source 2025 value and any separate offshore
premium as distinct rows rather than another general inflation transformation.

## 10. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0061 | technical/cost correctness | blocker | DEA 2025 converter cost is escalated twice | no |
| ISS-0062 | cost evidence | major | onshore cost is used as offshore equipment proxy | yes, DEC-0013 |
| ISS-0063 | implementation readiness | blocker | converter mass, dimensions and block/lift ledger missing | yes, DEC-0013 |
| ISS-0064 | cross-page consistency | blocker | page and executable electrical ledgers differ materially | no |
| ISS-0023 | implementation readiness | major | partial final-link cost/utilisation rule unresolved | yes, DEC-0005 |
| ISS-0025 | reference evidence | major | flat availability is unsupported | yes, DEC-0006 |

## 11. Page conclusion

- **Readiness:** blocked
- **Reason:** the adopted CAPEX is incorrectly transformed and physical/executable
  interfaces are not closed.
- **Open blockers:** 3 page-specific/shared
- **Open major issues:** 3 page-specific/inherited
- **Downstream consequences:** electricity-export CAPEX, platform mass,
  installation and delivered energy.
- **Recommended correction order:** correct DEA basis; decide offshore-cost
  treatment; define equipment ledger; align code; then close discrete links and
  availability.
