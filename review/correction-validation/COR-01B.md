# COR-01B validation — Common methodology contract

## Scope

This record validates the approved COR-01B methodology correction. The batch
implements DEC-0003 to DEC-0006 without adding Tier 2 endpoints, optimisation,
component cost values, WACC evidence or subsystem availability values.

The correction establishes:

- carrier-specific Tier 1 cost endpoints;
- the provisional finance and lifecycle convention;
- a deterministic input, parameter and output taxonomy;
- a one-case modelling workflow; and
- annual subsystem availability with component ownership and one-time
  architecture aggregation.

## Implemented contract

| Area | Implemented rule |
|---|---|
| Capacity-normalised cost | EUR/kW-wind, based on installed wind-turbine rated capacity |
| Electricity endpoint | EUR/MWh of electricity at the defined onshore delivery point |
| Hydrogen endpoints | EUR/MWh-H2-HHV and EUR/kg of hydrogen landed onshore |
| Comparison boundary | Carrier costs are comparable accounting outputs, not equivalent end-use service costs |
| Finance | 6.6% provisional real WACC, 25-year horizon and simple CRF |
| Replacement | Included only for a component with a material life below 25 years |
| Decommissioning | 80% of non-overlapping offshore installation CAPEX; no separate activity model |
| Model mode | Deterministic: one defined input case produces one result set; no optimisation |
| Availability | Annual subsystem factors, owned by component pages and combined once at architecture level |
| Hydrogen energy basis | 39.4 kWh/kg-H2-HHV, sourced to NREL/BK-6A1-46676 |

## Automated checks

| Check | Result |
|---|---|
| Financial identity | Pass: CRF(6.6%, 25 years) = 0.082741447 |
| Replacement rule examples | Pass: 25-, 10- and 5-year component lives give 0, 2 and 4 replacements respectively |
| Hydrogen unit conversion | Pass: 100 EUR/MWh-H2-HHV corresponds to 3.94 EUR/kg at 39.4 kWh/kg |
| Input register | Pass: 223 records; no duplicate input IDs |
| Dependency register | Pass: 140 records; no duplicate dependency IDs or unknown page IDs |
| Issue reconciliation | Pass: 11 COR-01B issues closed; ISS-0018 and ISS-0025 remain open |
| Source links | Pass: all local QMD links resolve |
| Bibliography | Pass: 129 entries; NREL HHV source present and cited |
| Rendered coverage | Pass: 41 HTML pages, including all six methodology pages |
| Rendered links | Pass: no broken local links detected across the rendered site |
| Rendered citations | Pass: no unresolved citation markers detected |
| Legacy expression | Pass: no rendered `C1 / Yield` expression remains |
| Full Quarto render | Pass: exit code 0; `_site/index.html` produced |
| Git whitespace check | Pass: no whitespace errors reported |

## Issue disposition

Closed in COR-01B:

- ISS-0015, ISS-0016 and ISS-0017: Tier 1 boundary, cost ownership and
  reproducible endpoint equations;
- ISS-0019: finance, replacement and decommissioning convention;
- ISS-0020 and ISS-0021: variable taxonomy and canonical fixed-parameter
  treatment;
- ISS-0022 and ISS-0023: deterministic workflow replaces the incomplete
  optimisation specification;
- ISS-0024 and ISS-0026: annual availability architecture and cited HHV basis;
- ISS-0105: methodology overview aligned to the implemented contract.

Remaining open:

- ISS-0018: the provisional 6.6% WACC still needs evidence and sensitivity
  treatment; and
- ISS-0025: annual subsystem availability factors still need evidence and
  sensitivity treatment.

These gaps remain explicit. No unsupported values were inserted.

## Visual-validation limitation

The full render and static rendered-output checks completed successfully. A
browser-based visual inspection could not be completed because the configured
in-app browser runtime rejected its trusted plugin path during startup. No
claim is made here about visual layout, responsive behaviour or interactive
states.
