# Batch 6 review — Offshore installation

## Scope

Reviewed and reconciled on 2026-08-21:

- `offshore_installation/overview.qmd`;
- `offshore_installation/turbine_and_foundation_installation.qmd`;
- `offshore_installation/cable_and_pipeline_installation.qmd`; and
- `offshore_installation/platform_and_substation_installation.qmd`.

No source `.qmd`, model code, generated site file or bibliography record was
changed. Findings are stored in the review framework for a separately approved
correction stage.

## Outcome

| Result | Count |
|---|---:|
| Pages reviewed | 4 |
| Partially implementable overview pages | 1 |
| Blocked calculation pages | 3 |
| Unique material B6 issues including inherited findings | 39 |
| Blockers | 22 |
| Major issues | 15 |
| Moderate issues | 2 |
| New issues added in B6 | 15 |
| New B6-specific decisions proposed | 3 |

The installation section has a good modelling philosophy. It generally uses
physical inventories, discrete loads and lifts, chargeable spread-days and
explicit unresolved states rather than aggregated EUR/m proxies. The most
developed page, cable and pipeline installation, is close to a reusable
calculation framework. None of the three calculations currently closes an
installed-CAPEX result because the physical inventories and commercial campaign
records are incomplete.

## Most important results

### 1. Cable duration does not conserve installed length or voyages

INST-003 correctly distinguishes route-km, physical product-km and pass-km.
Its route-production equation nevertheless uses only horizontal route length,
while slack and vertical/structure allowances affect supply and loading but add
no lay time (ISS-0096). The campaign then counts the initial outbound transit
and every reload round trip, but no final site-to-port transit (ISS-0097).

These are material technical corrections independent of later commercial data.
The model must either define the operating rate as product advance and include
all paid-out product, or separately time vertical/slack handling. Every
mobilised campaign must also contain a complete voyage boundary.

### 2. Installation rates are not coherent complete-spread records

The turbine page normalizes a 400,000 USD2024/day ORBIT WTIV example and the
cable page normalizes a 241,171 USD2024/day cable vessel. The currency arithmetic
is transparent, but neither rate proves the complete commercial boundary the
page later claims.

For INST-002, the issue is also physical: the cited ORBIT example is configured
with two feeder vessels, while the page excludes feeders and models a
self-shuttling WTIV. Its seven-day source field means mobilisation to site, not
combined mobilisation and demobilisation (ISS-0092/0093). For INST-003, fuel,
routine support craft, tugs and contractor overhead are included only by page
assumption (ISS-0098). INST-004 adopts no rates at all (ISS-0102).

### 3. The cable/TCP framework is strong but the base case is open

INST-003 makes several important modelling choices correctly:

- one physical asset per modeled lay/burial pass unless contractor evidence
  supports another method;
- product qualification before vessel selection;
- a packing problem rather than total-mass division as the adopted load count;
- separate spread-days for laying, burial and survey/ROV support;
- weather applied once to exposed time; and
- **not parameterized** for missing task/rate inputs.

Its cable example arithmetic reproduces. A full result is blocked by routed
section inventories, campaign grouping, port distance, burial and survey
scope/rates, demobilisation, weather, exceptional work and an evidenced
complete-spread boundary. TCP additionally lacks a qualified product, fittings,
continuous-length plan, vessel/task package and rates (ISS-0086/0099).

### 4. Platform installation uses a source anchor beyond its evidence

The official CVOW plan supports approximately 5 net days per piled jacket and
2.5 net days per complete topside. INST-004 applies the latter as 2.5 days per
topside module lift, although no split-topside relation is provided
(ISS-0103). The same source reports 30 days for the three piled jackets and 60
days for complete construction, installation and commissioning of the three
topsides. Those totals are useful constraints, but the topside total includes
final cable connection, which overlaps INST-003 unless an interface ledger is
defined (ISS-0104).

### 5. Upstream physical ledgers do not reach installation

The installation pages are structured to consume physical records, but upstream
pages do not yet emit them:

- architecture-specific turbine equipment and lift masses;
- transition-piece and foundation section/lift records;
- routed cable sections and complete four-cable export inventory;
- coordinate-based TCP sections, risers, fittings and qualified products; and
- platform, jacket, pile and topside module records.

This is the main cross-batch dependency. Installation should not replace those
missing physical outputs with cost factors.

## Review by criterion

### Technical correctness

Verified:

- turbine/foundation load ceilings, trip counts and time dimensions;
- the 10 kn to approximately 444 km/day conversion;
- cable event arithmetic and spread-day concurrency;
- weather being applied once to offshore-exposed time; and
- platform count/module/lift-class equations as conditional screening logic.

Required corrections:

- return infeasible when turbine/foundation payload permits zero sets
  (ISS-0094);
- separate mobilisation from demobilisation (ISS-0092);
- conserve physical cable/TCP length in production time (ISS-0096);
- add final return transit (ISS-0097); and
- do not apply a per-topside source duration to every module lift
  (ISS-0103).

### Model approach: accuracy versus complexity

The chosen fidelity is generally appropriate. Detailed deck packing, lift
engineering, vessel simulation, pile-driving decomposition and TCP installation
engineering should remain outside the model until evidence supports them. The
minimum missing detail is discrete and physical rather than computationally
complex:

- coherent campaign/spread records;
- packing and module inventories;
- product/vessel qualification gates;
- route-specific burial/survey methods;
- voyage and interface-event conservation; and
- class changes when payload or lift thresholds are crossed.

The lay-vessel selector should remain lay-only for equivalent separated
campaigns. Integrated lay/bury candidates must be compared on complete
non-overlapping installation cost (ISS-0100).

### Cost inputs and references

| Cost area | Status | Main finding |
|---|---|---|
| Foundation/turbine campaigns | Blocked | generic WTIV rate, mismatched feeder concept, turbine occupation and demobilisation missing |
| Cable lay | Blocked commercial result | task defaults traceable; vessel rate boundary incomplete |
| Cable burial and ROV/survey | Blocked | production, complete rates, weather and scope missing |
| TCP installation | Blocked | no qualified product, task package, vessel or rates |
| Platform installation | Blocked | all rates, logistics, hook-up and mobilisation absent |
| Exceptional work | Blocked/conditional | quantities, unit costs and ownership incomplete across pages |

### Explanation and directness

INST-002 and INST-004 are clear, concise and calculation-led. INST-003 is
carefully written but long and repeats unresolved status and limitations. It
should first be tightened around a compact input-status ledger; a separate TCP
page is justified only when TCP develops its own evidenced task model. INST-001
needs direct links to all three calculation pages (ISS-0090).

### Independent model development

An implementer can reproduce the conditional equations and the parameterized
cable example. They cannot produce any final installation CAPEX. The minimum
missing information is:

| Missing item | Consequence | Finding |
|---|---|---|
| coherent foundation/turbine spread records | turbine/foundation CAPEX blocked | ISS-0091–0093 |
| complete routed product inventories | loads, passes and events blocked | ISS-0001/0002/0069/0078 |
| cable/TCP campaign methods and complete rates | linear-asset CAPEX blocked | ISS-0098/0099 |
| length and voyage corrections | duration understated | ISS-0096/0097 |
| platform pile/jacket/module inventory | lift class and logistics blocked | ISS-0101 |
| platform rates/logistics/hook-up | platform CAPEX blocked | ISS-0102 |
| cable/platform commissioning interface | double-count/omission risk | ISS-0104 |

### General site and cross-page structure

The page placement is logical and no new top-level section is needed. The
overview is not yet a complete gateway, and installation ownership requires
cross-page ledgers for:

- normal versus exceptional installation scope;
- product supply versus installed-product inventory;
- pull-in, termination, testing and platform final connection;
- upstream equipment/component mass to transport/lift records; and
- installed CAPEX to METH-002 and feasibility/class records to METH-005.

## Coverage

| Page ID | Readiness | Blockers | Major issues | Review note |
|---|---|---:|---:|---|
| INST-001 | Partially implementable | 0 | 0 | Correct boundary; incomplete gateway links |
| INST-002 | Blocked | 4 | 5 | Good integer logistics; turbine duration and coherent spread missing |
| INST-003 | Blocked | 11 | 9 | Strong framework; inventories, complete rates and two duration corrections open |
| INST-004 | Blocked | 7 | 1 | Suitable aggregate campaigns; all physical/commercial records unresolved |

Counts include inherited/shared issues shown on each page and should not be
summed across future batches without de-duplication.

## Decisions required

| Decision ID | Question | Main consequence of delay |
|---|---|---|
| DEC-0018 | Which coherent foundation and turbine campaign concepts and rates apply? | turbine/foundation installed CAPEX remains open |
| DEC-0019 | Which cable/TCP lay, burial and survey methods and complete spread boundaries apply? | linear-asset installed CAPEX remains open |
| DEC-0020 | Which platform piling, lift and commissioning concept applies? | platform class and installed CAPEX remain open |
| DEC-0001/0002 | What routed array topology and cable-product/cost fidelity apply? | array installation inventory remains open |
| DEC-0010 | What foundation/TP physical surrogate and lift records apply? | foundation payload and lift class remain open |
| DEC-0014 | What onshore export route/endpoint package applies? | complete export installation scope remains open |
| DEC-0015/0017 | What TCP network and qualified product basis apply? | TCP installation cannot be configured |

## Proposed correction sequence

| Correction batch | Scope | Issues | Decisions | Validation |
|---|---|---|---|---|
| C6.1 Duration integrity | mobilisation/demobilisation, zero-load guard, product-length conservation and final transit | ISS-0092/0094/0096/0097 | DEC-0018/0019 | unit checks; one-load/reload cases; slack/vertical conservation; infeasible payload |
| C6.2 Turbine/foundation campaigns | coherent self-shuttle or feeder concepts, site occupation, rates and excluded-scope ledger | ISS-0091/0093/0095 plus upstream mass issues | DEC-0018/0009/0010 | source-config reproduction; load thresholds; cost-boundary reconciliation |
| C6.3 Cable/TCP campaigns | close inventories, packing, burial/survey/weather, candidate selection and complete rates | ISS-0098–0100 plus inherited cable/TCP issues | DEC-0019/0001/0002/0015/0017 | physical/product/pass/load conservation; candidate qualification; benchmark reconciliation |
| C6.4 Platform installation | pile/jacket/module records, lift concept, durations, rates and commissioning boundary | ISS-0101–0104 | DEC-0020/0007/0013/0016 | source total reconciliation; class thresholds; interface ownership; CAPEX sum |
| C6.5 Navigation and handoffs | overview links and common installation output contracts | ISS-0090/0095/0104 | none beyond above | link check; dependency completeness; no duplicated scope |

After correction, render every affected installation and upstream component
page. Render the full site if navigation, common ownership, configuration or
bibliography changes.

## Records created or updated

- New detailed reviews: `INST-001.md` to `INST-004.md`.
- New issues: ISS-0090 to ISS-0104.
- New inputs: INP-0167 to INP-0213.
- New dependencies: DEP-0102 to DEP-0117.
- New decisions: DEC-0018 to DEC-0020.
