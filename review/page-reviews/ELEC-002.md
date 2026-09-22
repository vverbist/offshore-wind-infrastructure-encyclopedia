# ELEC-002 — Infield AC Cables

## Review metadata

- **Source page:** [electrical_infra/infield_ac_cables.qmd](../../electrical_infra/infield_ac_cables.qmd)
- **Batch:** B3_electrical
- **Reviewer:** Codex
- **Started:** 2026-08-21
- **Completed:** 2026-08-21
- **Review status:** needs_decision
- **Readiness:** blocked

## Executive assessment

The page is clear, unusually transparent about limitations and technically
sound in its basic capacity arithmetic, three-phase power conversion and
length/cost equations. The chosen level of detail is broadly appropriate for a
screening model: it preserves string-count discontinuities and avoids pretending
to perform detailed cable engineering.

It is not yet a complete implementation specification. Four issues block a
closed model result:

1. no deterministic construction of the radial edge set;
2. no pull-in/vertical length input;
3. no electrical loss model; and
4. no bay-compatible resolution of the 34-string reference array.

The page also needs a more physical link between section loading, conductor
class, mass and cost. The current blended cost can produce a screening number,
but that number and the installation inventory do not describe the same cable
system.

## 1. Model role and boundary

- **Purpose:** size the radial 66 kV infield network, calculate cable supply
  length and material CAPEX, and apply cable OPEX and availability assumptions.
- **Architectures:** electricity export and centralised hydrogen. Decentralised
  hydrogen replaces the main AC array network.
- **Included:** static three-core cable supply, conductor/string capacity,
  horizontal and vertical length, stated normal accessories, OPEX allowance and
  array availability.
- **Excluded:** turbine transformer and switchgear, offshore collection bays,
  platform/J-tubes, and installation activities.
- **Ownership concern:** offshore collection switchgear is not assigned to an
  architecture-valid owner for centralised hydrogen (ISS-0012).

## 2. Upstream inputs

| Input | Symbol | Unit | Classification | Owner or source | Status |
|---|---|---:|---|---|---|
| Target capacity | $P_\mathrm{target}$ | MW | Scenario input | Scenario definition | Defined |
| Turbine rating | $P_\mathrm{turb}$ | MW | Scenario/model input | TURB-002 | Defined, threshold treatment unresolved |
| Usable string rating | $P_\mathrm{string}$ | MW | Modelling assumption | TenneT 2015 basis | Ambiguous interval |
| Array voltage | $V_\mathrm{array}$ | kV | Sourced reference | Multiple project/industry sources | Defined at 66 kV |
| Rotor diameter and spacings | $D,s_x,s_y$ | m; rotor diameters | Upstream inputs | WIND-003/TURB-002 | Defined in principle |
| Farm area/aspect ratio | $A_\mathrm{farm}$ | km2 | Scenario inputs | Scenario definition | Defined in principle |
| Turbine coordinates | $(x_j,y_j)$ | km | Derived result | WIND-003 | Defined in principle |
| Substation coordinate | $(x_\mathrm{OSS},y_\mathrm{OSS})$ | km | Required derived/input value | No owner | Missing |
| Route allowance | $r$ | dimensionless | Modelling assumption | Internal model description | Unsupported base value |
| Pull-in length | $L_\mathrm{pull-in}$ | km | Required input/result | No owner | Missing |
| Cable unit cost | $c_\mathrm{cable}$ | EUR2025/m | Modelling assumption | ORBIT and project comparator | Aggregate only |
| OPEX rate | $f_\mathrm{OPEX}$ | 1/year | Modelling assumption | No quantitative source | Unsupported |
| Availability | $A_\mathrm{array}$ | dimensionless | Modelling assumption | No quantitative source | Unsupported |

The detailed input records are in
[model-input-register.csv](../model-input-register.csv).

## 3. Calculation reconstruction

The documented execution order is:

1. Calculate installed turbine count and actual installed capacity:
   $N_\mathrm{turb}=\lceil P_\mathrm{target}/P_\mathrm{turb}\rceil$ and
   $P_\mathrm{farm}=N_\mathrm{turb}P_\mathrm{turb}$.
2. Calculate turbines per string with
   $\lfloor P_\mathrm{string}/P_\mathrm{turb}\rfloor$.
3. Calculate the minimum feeder count with a ceiling over turbine count.
4. Obtain turbine coordinates from the layout model.
5. Partition and order turbines into radial strings, producing edge set
   $\mathcal{E}$. This step is required but not specified.
6. Sum Euclidean section lengths to obtain $L_\mathrm{horizontal}$.
7. Apply pre-route allowance and add total pull-in length to obtain
   $L_\mathrm{array}$.
8. Multiply length by a blended cable supply rate.
9. Apply the top-down OPEX percentage to supply CAPEX.
10. Apply a flat 99.0% annual energy multiplier. No electrical cable loss is
    calculated.

### Boundary and limiting-case checks

- The turbine-count, string-count and cost equations are dimensionally correct.
- The three-phase capacities in the public cable table reproduce correctly:
  445 A at 66 kV gives 50.87 MVA and 775 A gives 88.59 MVA.
- 630 A at 66 kV gives 72.02 MVA and 64.82 MW at power factor 0.9.
- A feasibility assertion is required when
  $P_\mathrm{turb}>P_\mathrm{string}$; otherwise turbines per string becomes
  zero and the feeder-count equation divides by zero.
- Inputs must assert positive power, non-negative lengths and route allowance,
  and coordinate feasibility inside the site boundary.
- Discrete string and bay jumps are correctly preserved rather than smoothed.
- A detailed outage-state calculation must replace, not multiply with, the flat
  availability factor.

## 4. Outputs and downstream consumers

| Output | Unit | Downstream consumer | Interface status |
|---|---:|---|---|
| Turbine and string count | count | Offshore collection/platform; installation | Inconsistent with reference platform |
| Radial section list | section records | Installation; loss model | Ambiguous |
| Length by conductor class | km | Supply cost; installation | Missing |
| Total horizontal length | km | Supply and installation | Not reproducible until topology is defined |
| Total supply length | km | Supply and installation | Not parameterized until pull-ins are defined |
| Cable mass by section/load | t | Installation | Ambiguous |
| Supply CAPEX | EUR2025 | LCOE | Defined with material uncertainty |
| Annual OPEX | EUR2025/year | LCOE | Executable but unsupported |
| Electrical loss | MWh/year | Delivered-energy calculation | Missing |
| Availability multiplier | dimensionless | Delivered-energy calculation | Defined but unsupported |

## 5. Technical correctness

### Verified or appropriate

- The radial-string explanation is correct and easy to understand.
- The use of floor and ceiling functions is correct and preserves material
  equipment-count discontinuities.
- The 2 GW/15 MW example gives 134 turbines and 34 four-turbine strings.
- The 24 plus four candidate-bay interpretation is supported by TenneT's
  [2024 2 GW programme presentation](https://www.hvdccentre.com/wp-content/uploads/2024/07/3.2_TenneT-2GW-Program-Kabul.pdf).
- The ORBIT 185 mm2 and 630 mm2 input values were reproduced from the reviewed
  [185 mm2](https://github.com/NLRWindSystems/ORBIT/blob/dev/library/cables/XLPE_185mm_66kV.yaml)
  and [630 mm2](https://github.com/NLRWindSystems/ORBIT/blob/dev/library/cables/XLPE_630mm_66kV.yaml)
  files. The USD2024-to-EUR2025 calculations reproduce to 219.38 and
  590.36 EUR/m before rounding.
- Public validation quantities checked for Borssele, Moray East and Dogger Bank
  A reproduce the reported project length ratios. They are appropriately used
  as validation ranges rather than calibration coefficients.
- It is appropriate not to implement voltage-drop, short-circuit and detailed
  thermal design at screening level, provided cable selection is treated as a
  qualification gate.

### Conditional or incorrect as a basis

- The internal source for the 20% route addition states that subsea cables
  cannot cross. Crossings are technically possible with engineered agreements
  and protection. Avoidance may be a project objective, but it does not derive
  a universal 20% addition.
- IEC 63026 describes rated voltages up to 60 kV with maximum system voltage
  72.5 kV. The page should state the applicable cable voltage designation rather
  than assume every item described commercially as 66 kV falls unambiguously
  under that wording. Manufacturer literature also uses IEC 60840 for some
  66 kV designs.
- The page's aggregate string rating is sufficient for screening only after a
  deterministic base value or branching convention is selected.

## 6. Model fidelity

The page mostly follows minimum-sufficient-fidelity principles. It exposes
physical coordinates and discrete string counts, while leaving project cable
engineering outside the numerical model. A full optimal routing or thermal
finite-element model is not justified for the current evidence level.

Two additional details are justified because they materially affect the result
and can be represented without speculative engineering:

1. a deterministic radial layout heuristic from coordinates to cable sections;
2. at least two conductor classes selected from downstream segment load.

These additions would make length, mass, cost, installation and resistive losses
respond to the same physical network. The page should stop at that level and
retain detailed ampacity, protection, mechanical and project-route checks as
qualification gates.

The aggregate availability factor can remain a temporary highest-defensible
model only if its basis, scope and sensitivity are documented. The OPEX factor
currently lacks enough evidence to be adopted under the project's
evidence-constrained rules.

## 7. Cost and evidence audit

| Value or relationship | Review result | Finding |
|---|---|---|
| 185/630 mm2 ORBIT current, mass and cost | Exact current file values verified; source is mutable | ISS-0013 |
| USD2024 to EUR2025 conversion | Arithmetic verified; CPI-U is a disclosed fallback index | — |
| 64-66 MW usable string rating | 64 MW conservative basis support found; interval/selection rule not established | ISS-0005 |
| 400 EUR2025/m blended rate | Explicit judgement, not a reproducible routed-cable cost | ISS-0006, ISS-0007 |
| Hollandse Kust Zuid 172 km and about EUR 30m | Both quantities verified; value is 2019 nominal and report link is withdrawn | ISS-0007, ISS-0014 |
| 20% route addition | Internal ad hoc assumption; no external derivation | ISS-0008 |
| 2%/year OPEX | Not supported by SPARTA or ELECTRODE | ISS-0009 |
| 99.0% availability | No quantitative evidence or calibration | ISS-0010 |
| 132 kV future option | Technology direction and savings claim verified; executable inputs absent | ISS-0011 |

The [ORBIT changelog](https://nlrwindsystems.github.io/ORBIT/about/changelog.html)
supports the 2024 USD basis and describes industry outreach plus commodity,
inflation and labour adjustments. It does not disclose the underlying cable
quotes or define the accessory boundary.

The Prysmian contract page verifies 172 km including design, testing, cable and
accessories. The approximately EUR 30 million value is in the approved 2019
annual report; the bibliography currently links to the withdrawn version.

The [SPARTA portfolio report](https://cms.ore.catapult.org.uk/wp-content/uploads/2022/06/SPARTA-Review-2021-Final.pdf)
supports the quoted 7.46% of wind-farm months and 61% of wind farms reporting
cable outages. [ELECTRODE](https://ore.catapult.org.uk/resource-hub/projects/electrode)
supports the combined repair/lost-generation severity statement. Neither source
derives the adopted OPEX rate or 99.0% array availability.

## 8. Independent-implementer test

An implementer can reproduce turbine count, feeder count for a chosen scalar
rating, the length and cost equation forms, and the worked arithmetic. The
implementer cannot produce the complete model output without undocumented
choices.

- **Missing numerical evidence:** OPEX percentage, availability factor, route
  allowance and accessory-supply boundary.
- **Missing modelling decisions:** exact string rating, reference platform
  closure and blended versus segment-specific cable costing.
- **Missing equations:** load-dependent electrical loss and pull-in length.
- **Missing implementation rules:** radial topology construction, substation
  placement, conductor allocation and threshold feasibility behaviour.
- **Missing datasets/source locations:** immutable ORBIT revision and stable
  versions of several cited documents.
- **Correctly unresolved:** detailed thermal, mechanical, short-circuit and
  project routing checks; these should remain qualification gates rather than
  be filled with unsupported detail.

## 9. Explanation and site placement

The page is well placed and generally easy to read. Its strongest editorial
features are the early scope table, physical-tree explanation, worked example,
visible platform warning and limitations table. Background on 66 kV and cable
construction is concise and relevant to the sizing calculation.

The principal explanation problem is not prose style but calculation status.
Losses and incomplete pull-in length appear mainly near the end, while the page
otherwise reads like a complete model specification. A future correction should
state near the calculation overview that supply cost and delivered-energy output
remain incomplete until those inputs are resolved.

Cross-page ownership is clear for installation but not for centralised-hydrogen
collection switchgear. The page should link directly to the eventual canonical
owner rather than say only that switchgear bays are accounted elsewhere.

## 10. Findings

| Issue ID | Category | Severity | Short finding | Decision required |
|---|---|---|---|---|
| ISS-0001 | Implementation readiness | Blocker | Radial topology algorithm and substation placement missing | Yes |
| ISS-0002 | Implementation readiness | Blocker | Pull-in length not parameterized | No |
| ISS-0003 | Implementation readiness | Blocker | Electrical loss model missing | No |
| ISS-0004 | Cross-page consistency | Blocker | 34 strings do not fit the reference platform | Yes |
| ISS-0005 | Implementation readiness | Major | String-rating interval has no deterministic rule | Yes |
| ISS-0006 | Model fidelity | Major | No conductor allocation by segment | Yes |
| ISS-0007 | Cost input | Major | Blended cost and accessory boundary are not reproducible | Yes |
| ISS-0008 | Reference evidence | Major | Route allowance is unsupported | No |
| ISS-0009 | Cost input | Major | OPEX factor is unsupported | No |
| ISS-0010 | Reference evidence | Major | Availability factor is unsupported | No |
| ISS-0011 | Model fidelity | Major | 132 kV sensitivity is not executable | No |
| ISS-0012 | Cross-page consistency | Major | Central-hydrogen switchgear owner is missing | No |
| ISS-0013 | Reference evidence | Moderate | ORBIT inputs are not pinned | No |
| ISS-0014 | Reference evidence | Moderate | Several citations need stable editions/links | No |

## 11. Page conclusion

- **Readiness:** blocked
- **Reason:** basic screening arithmetic is implementable, but complete cable
  length, electrical performance and a physically compatible reference
  collection system cannot yet be produced.
- **Open blockers:** 4
- **Open major issues:** 8
- **Downstream consequences:** supply CAPEX, installation inventory, platform
  collection design, delivered energy and LCOE are not yet one closed chain.
- **Recommended correction order:** close the string/platform architecture;
  define topology and substation placement; allocate conductor classes; define
  pull-in length; implement losses; then replace or resolve cost, OPEX,
  availability and routing assumptions.
