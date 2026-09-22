# ELEC-004 — HVDC Export Cables

## Review metadata

- **Source page:** [electrical_infra/hvdc_export_cables.qmd](../../electrical_infra/hvdc_export_cables.qmd)
- **Batch:** B3_electrical
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The page correctly distinguishes route-kilometres from cable-kilometres,
separates supply from installation and gives a technically correct balanced-
bipole $I^2R$ screening equation. It cannot yet supply a common-price-basis
CAPEX, a complete physical installation inventory or an underground cable
cost. The preferred hourly loss model is also incomplete because conductor
temperature and degraded pole/return operation are not defined.

## 1. Model role and boundary

- **Purpose:** define the 2 GW ±525 kV cable system, material CAPEX, electrical
  loss and cable availability.
- **Included:** positive/negative poles, return/communications when covered by
  the selected topology and material benchmark, and normal supplied accessories.
- **Excluded:** marine/land installation, exceptional civil works and converters.
- **Architectures:** electricity export only.

## 2. Upstream inputs

| Input | Unit | Classification | Source/status |
|---|---:|---|---|
| Route lengths by marine/land segment | km | site inputs | marine base 80 km legacy; land length missing |
| Pole voltage/current | kV; kA | derived design | 525; 1.905 at 2 GW |
| Conductor/material selection | mm2/material | discrete design | candidate options only |
| Resistance | ohm/km at temperature | sourced indicative | 0.0072 at 20°C Cu only |
| Material rate | EUR/kW/km | converted source | 1.26; source price year unresolved |
| Failure/repair data | faults/100 km-year; days | historical evidence | 0.07; about 60 |

## 3. Calculation reconstruction

Balanced cable loss is
$P_\mathrm{loss}=2I^2R'L$. The four printed examples reproduce, including
4.18 MW at 80 km and 15.67 MW at 300 km. The 0.5% loss distance reproduces at
about 191 km. NREL's 4.57 million USD/mile 2 GW bipole material reference
converts to approximately 2.51 million EUR/km, or 1.26 EUR/kW/km, using
1 EUR = 1.13 USD.

### Boundary and limiting-case checks

- At zero power, variable conductor loss is zero but no-load/accessory losses
  belong elsewhere.
- Underutilised links need current from actual transfer but CAPEX from installed
  rated blocks.
- One-pole operation uses the metallic return and requires a different
  resistance path than balanced two-pole operation.
- Resistance must state operating temperature or an explicit R20 screening
  convention.
- Each physical cable/segment needs length, mass, diameter and accessory records.

## 4. Outputs and downstream consumers

| Output | Unit | Downstream consumer | Interface status |
|---|---:|---|---|
| Material CAPEX by link/segment | EUR2025 | METH-002 | price year and land coefficient missing |
| Cable loss by state/time | MWh/year | METH-006 | balanced R20 only |
| Cable system inventory | cable-km; t; dimensions | INST-003 | incomplete |
| Capacity states/outage exposure | MW-hours | METH-006 | conceptual only |
| Cable OPEX | EUR2025/year | LCOE | TBD |

## 5. Technical correctness

The balanced-bipole equations and arithmetic are correct. The metallic return
does not normally carry balanced load, so its omission from the balanced loss
equation is appropriate. It must be included in degraded operation. The
historical fault and repair values are accurately represented as indicative,
not guarantees, from the ENTSO-E/Europacable report.

## 6. Model fidelity

Load-dependent $I^2R$ is the right minimum fidelity and should replace the flat
99.5% efficiency. A full thermal cable model is not required initially; a
documented operating-temperature resistance with sensitivity is sufficient.
Discrete conductor/link selection, route segmentation and pole-return states
must be retained.

## 7. Cost and evidence audit

The NREL source supports a 525 kV, 2 GW bipole material value with installation
separate, but does not establish the repository's common price year and may not
match TenneT's return/accessory scope. No material-only underground coefficient
is adopted. Legacy code uses 5.5 million per route-km versus about 2.52 million
EUR/km from the page at full 2 GW, before price-basis reconciliation, and adds a
separate 1.5 million/km installation value.

## 8. Independent-implementer test

An implementer can reproduce the balanced R20 examples. They cannot reproduce
a complete supply, installation or annual-loss result without route segments,
selected conductor/return design, operating resistance, physical inventory,
price year, underground coefficient, link-utilisation rule and OPEX/availability
method.

## 9. Explanation and site placement

The explanation is direct and the route-km/cable-km warning is excellent. Keep
installed/EPC comparators visually subordinate. Add an adopted physical system
ledger before the cost equation.

## 10. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0064 | cross-page consistency | blocker | page and executable cable cost/performance differ | no |
| ISS-0065 | cost evidence | blocker | NREL material cost has no adopted price year | no |
| ISS-0066 | cost boundary | major | material topology/accessory scope is not matched | no |
| ISS-0067 | implementation readiness | blocker | underground route and material coefficient are missing | yes, DEC-0014 |
| ISS-0068 | model fidelity | major | hourly/degraded-state loss model is incomplete | no |
| ISS-0069 | implementation readiness | blocker | complete cable mass/segment/accessory inventory is missing | no |
| ISS-0070 | lifecycle cost | major | electrical component OPEX is absent or unsupported | no |
| ISS-0023 | implementation readiness | major | discrete link and partial utilisation rule unresolved | yes, DEC-0005 |
| ISS-0025 | reference evidence | major | flat availability is unsupported | yes, DEC-0006 |

## 11. Page conclusion

- **Readiness:** blocked
- **Reason:** material cost, land segment and physical/loss interfaces do not
  yet form one executable cable system.
- **Open blockers:** 4 page-specific/shared
- **Open major issues:** 5 page-specific/inherited
- **Downstream consequences:** cable supply/installation CAPEX, vessel demand,
  electrical loss, availability and onshore route closure.
- **Recommended correction order:** fix link/route basis; resolve price year and
  topology scope; define physical inventory and R(T)/degraded losses; align code;
  then add OPEX/availability.
