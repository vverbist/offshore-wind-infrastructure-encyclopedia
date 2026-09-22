# WIND-003 — Wake Modelling and Spacing

## Review metadata

- **Source page:** [wind_resource_and_layout/wake_modelling_and_spacing.qmd](../../wind_resource_and_layout/wake_modelling_and_spacing.qmd)
- **Batch:** B2_generation
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The page exposes layout geometry, wake equations and discrete row/column counts
well. That is the right fidelity for a screening comparison. It is blocked by
an undefined farm-area boundary and by treating minimum spacing only as a
warning. Its turbine power/thrust definition and hub height do not match the
turbine-system page or the IEA 15 MW reference, while several wake inputs are
unsupported.

## 1. Model role and boundary

- **Purpose:** construct turbine coordinates from area and spacing and calculate
  direction-dependent wake-affected farm power/AEP.
- **Architectures:** all.
- **Included:** rectangular layout, rotation, PyWake wake model and energy.
- **Excluded:** detailed micrositing, geotechnical constraints and electrical
  losses.
- **Ownership concern:** this page owns layout area operationally, but does not
  define whether area includes edge/setback margins.

## 2. Upstream inputs

| Input | Unit | Classification | Owner/source | Status |
|---|---:|---|---|---|
| Turbine count and farm area | count; km2 | design variables | methodology | defined in principle |
| Rotor diameter | m | turbine input | TURB-002 | 236 m in wake code |
| Hub height | m | turbine input | conflicting owners | 150 m here; 133 m default in TURB-002 |
| Turbulence intensity | dimensionless | assumption | no source | 0.058 unsupported |
| Layout orientation | degree | design/fixed choice | no source | fixed 30 degrees |
| Minimum spacing | rotor diameters | feasibility assumption | no source | warning only |

## 3. Calculation reconstruction

The page derives a rectangular aspect ratio, integer row/column counts,
spacings and rotated coordinates, then evaluates a PyWake power matrix over
direction and wind speed. AEP, wake loss, capacity factor and areal yield are
calculated from the weighted matrix. The equations are dimensionally correct.

### Boundary and limiting-case checks

- $N=1$ requires a separate layout case to avoid division by zero.
- Every coordinate must lie within a precisely defined lease/assessment area.
- Minimum spacing must be a feasibility constraint, not a warning.
- Integer row/column and last-row behaviour must remain explicit.
- Probability coverage and no-wake/gross definitions must be identical across
  reported outputs.

## 4. Outputs and downstream consumers

| Output | Unit | Downstream consumer | Interface status |
|---|---:|---|---|
| Coordinates | km | ELEC-002, H2I-002, installation | geometry boundary ambiguous |
| Wake-affected power table | MW | hydrogen/electricity yield | turbine curve inconsistent |
| AEP and capacity factor | MWh/year; dimensionless | METH-006 | calculable conditionally |
| Farm area and areal yield | km2; MWh/km2/year | optimisation | functional area undefined |

## 5. Technical correctness

The aggregation equations and preservation of integer layout changes are
correct. The current implementation is not a consistent turbine definition:
the wake page uses a synthetic 15 MW, 236 m curve with a near-constant thrust
coefficient and 150 m hub height, while TURB-002 defaults to 133 m for the same
diameter. The IEA 15 MW reference has a different rotor and published power/
thrust behaviour. This matters directly to wake loss and energy.

## 6. Model fidelity

A regular rotated grid plus an engineering wake model is appropriate for
architecture screening. Detailed site optimisation is unnecessary. However,
the screening model must reject physically infeasible densities, define the
area being optimised and use a controlled turbine/wake configuration with at
least one benchmark or sensitivity.

## 7. Cost and evidence audit

No direct cost. The 3D spacing limit, 30-degree orientation, turbulence
intensity and wake configuration lack evidence or calibration.

## 8. Independent-implementer test

- **Can the page be implemented?** The legacy geometry and PyWake call can be
  reproduced, but a valid optimisation cannot.
- **Missing decisions:** lease-area/setback convention, infeasibility rule and
  whether orientation is fixed, scenario-based or optimised.
- **Missing evidence:** common turbine curve, turbulence intensity, wake-model
  version/configuration and benchmark.

## 9. Explanation and site placement

The calculation order is strong. Rename the per-turbine wake-affected output
currently called `turbine_gross_yield_MWh`; its name contradicts its content.

## 10. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0034 | implementation readiness | blocker | farm-area boundary is undefined | yes, DEC-0008 |
| ISS-0035 | technical correctness | blocker | infeasible spacing is not rejected | yes, DEC-0008 |
| ISS-0036 | cross-page consistency | major | turbine curve and hub height conflict | no |
| ISS-0037 | reference evidence | major | wake configuration and fixed inputs are unsupported | yes, DEC-0008 |

## 11. Page conclusion

- **Readiness:** blocked
- **Reason:** the optimisation can select invalid or differently interpreted
  layouts and the wake turbine is not canonical.
- **Open blockers:** 2
- **Open major issues:** 2
- **Downstream consequences:** energy yield, cable/pipeline length and the
  cost-density objective.
- **Recommended correction order:** decide area/feasibility convention; align
  turbine definition; validate and freeze the wake configuration.
