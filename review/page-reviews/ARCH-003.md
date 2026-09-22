# ARCH-003 — Centralised Hydrogen

## Review metadata

- **Source page:** [architectures/centralised_hydrogen.qmd](../../architectures/centralised_hydrogen.qmd)
- **Batch:** B1_frame
- **Reviewer:** Codex
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Model role and boundary

The page gives a clear centralised chain: conventional turbine electrical
equipment and AC collection feed one integrated electrolysis platform;
compression is separately accounted on that platform; hydrogen is exported to
an onshore backbone connection. The distinction between physical co-location
and accounting ownership is strong and helps prevent double counting.

The component list and interfaces are internally consistent. Installation is
appropriately delegated. The explicit one-platform rule is understandable as
an architecture definition but is not yet connected to farm capacity or
feasibility.

## Implementation gaps

One platform is fixed while turbine count and equipment size can vary. No
maximum platform duty, equipment mass envelope, module count or transition to
additional platforms is defined. The platform page has no closed hosted-mass
inventory or mass-to-material-CAPEX method. A complete centralised architecture
therefore cannot be sized or costed across the stated design space (ISS-0027).

The AC collection switchgear owner is also missing for this architecture:
ELEC-002 excludes offshore bays, the HVDC station page is not architecture-
applicable and the electrolyser power-electronics page excludes upstream 66 kV
switchgear (ISS-0012).

Finally, the included onshore hydrogen-backbone connection links to an overview
that does not define its equipment, acceptance specification or cost boundary
(ISS-0028).

## Findings

| Issue | Severity | Finding |
|---|---|---|
| ISS-0027 | Blocker | One-platform capacity/scaling and CAPEX are unresolved |
| ISS-0028 | Major | Onshore hydrogen connection has no component model |
| ISS-0012 | Major | Offshore collection switchgear has no owner |

## Conclusion

- **Readiness:** blocked
- **Open blockers:** 1
- **Open major issues:** 1 directly assigned, plus ISS-0012
- **Recommended correction order:** decide platform scaling; assign collection
  switchgear; define the hydrogen connection interface; then reconcile the
  common endpoint and lifecycle boundary.
