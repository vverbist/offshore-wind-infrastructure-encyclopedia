# WIND-002 — Wind Resource and Weibull Distribution

## Review metadata

- **Source page:** [wind_resource_and_layout/wind_resource_and_weibull.qmd](../../wind_resource_and_layout/wind_resource_and_weibull.qmd)
- **Batch:** B2_generation
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The Weibull equations and the legacy-data audit are clear and reproducible.
The page commendably identifies its own main gaps. Two items block adoption:
the source series cannot be reconstructed from DOWA, and lower-edge sector
labels are supplied as wake directions, producing a 15-degree directional
offset. A further empirical-versus-Weibull energy validation is required.

## 1. Model role and boundary

- **Purpose:** reduce hourly wind speed and direction to twelve conditional
  Weibull distributions used by the wake/yield model.
- **Architectures:** all.
- **Included:** source-series description, sector frequencies, Weibull fit and
  numerical integration grids.
- **Excluded:** layout and wake physics.
- **Canonical assumptions:** sector convention and resource dataset should be
  owned here.

## 2. Upstream inputs

| Input | Unit | Classification | Owner or source | Status |
|---|---:|---|---|---|
| Hourly wind speed and direction | m/s; degree | sourced input | legacy workbook, intended DOWA | source extraction missing |
| Sector width | degree | modelling choice | fitting script | defined as 30 |
| Weibull location | m/s | modelling choice | fitting script | fixed at zero |
| Wind-speed grids | m/s | numerical choice | wake and hydrogen routines | inconsistent but documented |

The inspected workbook contains 87,601 consecutive records from 2008-01-01 to
2017-12-29 with no gaps in the timestamp, speed or direction columns. This
confirms the page's workbook audit, but does not recover its DOWA provenance.

## 3. Calculation reconstruction

1. Bin each observation with lower edge
   $s=30\lfloor(\theta\bmod360)/30\rfloor$.
2. Calculate $p_s=n_s/N$.
3. Fit a two-parameter Weibull with location fixed at zero in each sector.
4. Pass $p_s,k_s,c_s$ to the wake model and integrate power over wind speed.

The fitted CSV agrees with the twelve values printed on the page and the
direction probabilities sum to one within rounding.

### Boundary and limiting-case checks

- The Weibull CDF/PDF and units are correct.
- Direction is circular; a 0-degree sector must wrap consistently if centres
  are adopted.
- Probability omitted by finite wind-speed bounds must be reported before any
  renormalisation.
- The wake and hydrogen integrations require a convergence and reconciliation
  tolerance.

## 4. Outputs and downstream consumers

| Output | Unit | Downstream consumer | Interface status |
|---|---:|---|---|
| Direction probabilities | dimensionless | WIND-003 | defined, label convention wrong |
| Weibull shape and scale | dimensionless; m/s | WIND-003 | numerically available |
| Representative directions | degree | WIND-003 | offset by 15 degrees |

## 5. Technical correctness

- The statistics and fitted table are internally consistent.
- The stored sector value is a lower edge, not its representative direction.
  Passing it to PyWake rotates every sector by 15 degrees relative to the
  observations.
- The official-period statement and observed shortened series are transparent,
  but a model input cannot be reproduced without point, height, time basis,
  version and direction convention.

## 6. Model fidelity

Directional Weibull fitting is an appropriate minimum-sufficient reduction for
screening layout effects. It should be retained only after its energy impact is
benchmarked against the empirical hourly distribution. A more complex wind
model is not presently justified.

## 7. Cost and evidence audit

No cost input. DOWA is an appropriate authoritative source, but the actual
extraction metadata are absent (ISS-0031).

## 8. Independent-implementer test

- **Can the page be implemented?** The legacy fit can; the intended resource
  input cannot be independently reacquired.
- **Missing datasets/source locations:** exact DOWA point, height, filename,
  release/version, timezone and direction convention.
- **Missing validation:** empirical-hourly versus fitted-Weibull AEP, grid
  convergence and reconciliation of the two integration grids.

## 9. Explanation and site placement

The page is direct and in the right place. Its explicit source-gap and next-
step sections are strong. The correction should turn those warnings into a
controlled input specification and validation result.

## 10. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0031 | reference evidence | blocker | DOWA extraction is not reproducible | no |
| ISS-0032 | technical correctness | blocker | sector directions are offset by 15 degrees | no |
| ISS-0033 | model fidelity | major | Weibull and grid reductions are not validated | no |
| ISS-0060 | implementation readiness | moderate | transformed wind input is not version-controlled | no |

## 11. Page conclusion

- **Readiness:** blocked
- **Reason:** source and direction input cannot yet be adopted safely.
- **Open blockers:** 2
- **Open major issues:** 1
- **Downstream consequences:** all wake, yield and layout-density results.
- **Recommended correction order:** recover source metadata; centre sectors;
  validate empirical and fitted AEP; then freeze the controlled dataset.
