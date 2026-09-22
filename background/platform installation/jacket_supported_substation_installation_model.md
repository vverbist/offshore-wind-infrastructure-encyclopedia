# Jacket-supported offshore-substation installation cost model

**Research cut-off and access date:** 31 July 2026  
**Cost basis:** constant 2026 EUR, excluding VAT  
**Purpose:** transparent, medium-fidelity screening model for piled jackets and crane-installed topsides.

## 1. Executive recommendation

Model a jacket-supported offshore substation as four separable work packages:

1. foundation-pile/template campaign;
2. jacket transport, lift, set-down, levelling and structural connection;
3. topside transport, lift, set-down and structural connection; and
4. offshore hook-up, testing and commissioning.

The packages may share a mobilisation or vessel in a specific execution plan, but they do not share one universal rate or productivity. This matters because a platform's mass and dimensions primarily determine transport and crane feasibility; pile count and penetration drive foundation work; lift count, connection method and logistics drive installation duration; and electrical scope drives hook-up/commissioning.

The recommended cost equation is

\[
C_{OSS}=\sum_{c\in\{P,J,S,H\}}\left(C_{mob,c}+\sum_v r_{v,c}T_{v,c}\right)
+C_{exceptional}+C_{other},
\]

where \(P\)=piles/template, \(J\)=jacket, \(S\)=topside and \(H\)=hook-up/commissioning. A contracted complete-spread rate may replace a vessel stack for a campaign, never supplement it.

The model is for conventionally crane-lifted jackets and topsides. A float-over, self-installing platform, gravity base or topside/jacket installed by Pioneering Spirit is a different installation class.

## 2. Cost and technical boundary

### Included

- mobilisation/demobilisation of the named installation spread;
- transport from load-out quay to site on the heavy-lift vessel or deck carrier;
- pre-piling template placement/recovery or post-piling through jacket sleeves;
- routine pile handling, upending, lowering, stabbing and normal driving;
- jacket lift, set, level, survey, grouting/welding and release;
- topside lift, mating, welding/grouting and lift-rigging release;
- explicitly defined offshore hook-up, testing and commissioning vessel-days;
- normal tug, ROV/survey and support only where named in the spread boundary.

### Separate or excluded

- jacket, piles and topside fabrication and onshore commissioning;
- load-out quay strengthening, storage and port rent unless explicitly costed;
- export and inter-array cable installation, pull-in and termination;
- seabed preparation, dredging, boulder/UXO work and scour protection;
- relief drilling, pile refusal remediation and project-specific underwater-noise measures;
- accommodation campaign beyond the defined hook-up scope;
- platform electrical equipment cost, offshore-wind development cost, insurance and owner contingency;
- float-over or ultra-heavy single-lift execution requiring another class.

## 3. Accounting quantities

| Quantity | Definition | Modelling consequence |
|---|---|---|
| Substation platform | One functional OSS at one location | May contain one jacket and one topside but several electrical systems |
| Jacket | One lattice support structure placed on or over piles | Jacket mass/footprint controls lift and transport feasibility |
| Jacket leg | Main structural leg | Does not necessarily equal pile count |
| Foundation pile | One driven pile; a leg may have one or several | \(N_{pile}=N_{leg}N_{pile/leg}\) only for a uniform design |
| Pre-piling template | Reusable positioning frame installed before piles | Installed/recovered per location, not per pile |
| Topside module | The lift unit(s) in the execution plan | A split topside has more lifts and interfaces than a single lift |
| Deck-carrier load | Jacket or topside delivery from port/fabrication yard | Public project envelopes commonly assume one large structure/load |
| Heavy lift | One crane pick at specified mass, radius and lift path | Brochure maximum capacity is not sufficient evidence |
| Net installation day | Chargeable work time excluding specified long interruptions | Not the same as total calendar commissioning period |
| Campaign | Continuous deployment sharing mobilisation | Pile, jacket, topside and hook-up campaigns may differ |

## 4. Required inputs

### Structure and site

- number of substations \(N_{OSS}\), water depth \(d_w\), port/fabrication-yard distance \(D_p\), site spacing and season;
- jacket lift mass \(m_J\), height \(H_J\), maximum length/width or seabed footprint \(B_J\times L_J\), centre of gravity, lift points and rigging mass;
- number of legs, piles per leg, pile mass, diameter, length and penetration \(L_e\);
- topside lift mass \(m_S\), width \(B_S\), length \(L_S\), height \(H_S\), centre of gravity, lift points, installation elevation and number of lift modules;
- pre-pile or post-pile method; sleeve/levelling/grout/weld concept; template reuse;
- hook-up/commissioning interfaces and required accommodation/electrical spread.

### Vessels and logistics

- crane safe working load as a function of radius, hook height/depth and configuration;
- usable deck/deck-carrier mass, area, point loads, stability and seafastening limits;
- transit speed, weather limits, DP/mooring requirements and setup time;
- piling plant/hammer limits, pile-handling method and effective site-specific penetration rate;
- day rates, mobilisation terms and exact inclusions for primary, carrier, tug, support, survey/ROV and commissioning vessels.

## 5. Feasibility and vessel-class selection

For each lift \(j\):

\[
\gamma_{dyn}(m_j+m_{rig,j})\le SWL(R_j,config),
\]

\[
H_{hook}\ge H_{required,j},\quad R_{available}\ge R_j,
\]

and the cargo/deck carrier must satisfy

\[
m_j+m_{seafast}\le M_{use},\quad B_jL_j/f_{pack}\le A_{use},\quad p_{local}\le p_{deck,max}.
\]

Also check centre of gravity, lifting-point loads, tandem synchronization, boom/structure clearance, under-hook rigging, carrier stability, quayside load-out, water depth, vessel draft, air gap and DP/mooring footprint. If any gate fails, select a larger crane/carrier or switch installation method. Do not convert failure into “extra days.”

Public fleet specifications demonstrate the class steps:

- Scaldis reports 3,300 t tandem capacity for *Rambiz* and 4,000 t for *Gulliver* ([company profile](https://www.scaldis-smc.com/en/company/company-profile/)).
- Saipem reports 14,000 t combined heavy-lift capacity for the DP3 *Saipem 7000* ([vessel page](https://www.saipem.com/en/solutions-energy-transition/fleet-and-yards/saipem-7000)).
- Heerema reports two 10,000 t cranes and 20,000 t tandem capacity for *Sleipnir*, with a 220 m by 102 m reinforced deck ([vessel page](https://www.heerema.com/heerema-marine-contractors/fleet/sleipnir)); its lift height is reported as 175 m ([Heerema announcement](https://heerema.com/news/sembcorp-marine-completes-worlds-biggest-and-strongest-semi-submersible-crane-vessel-for-heerema)).
- Allseas reports 60,000 t topside and 20,000 t jacket lift capacities for *Pioneering Spirit* ([heavy-lift equipment](https://www.allseas.com/en/who-we-are/our-equipment/heavy-lift-equipment)). That execution is a separate single-lift/float-over class, not an extrapolation of ordinary crane-vessel rates.

These are maximum capability indicators only. The actual lift-radius chart and engineered lift plan govern.

## 6. Dependency-ordered calculation

### 6.1 Physical quantities

For a uniform jacket:

\[
N_{pile}=N_{OSS}N_{leg}N_{pile/leg}.
\]

If designs vary, sum by platform. Calculate lift modules rather than assuming one topside:

\[
N_{lift,S}=N_{OSS}N_{module/OSS},\qquad N_{lift,J}=N_{OSS}.
\]

For large jackets and topsides, default to one structure per carrier load unless the engineered stow plan proves otherwise:

\[
N_{load,J}=\left\lceil\frac{N_{OSS}}{n_{J/load}}\right\rceil,quad
N_{load,S}=\left\lceil\frac{N_{lift,S}}{n_{S/load}}\right\rceil.
\]

CVOW's public construction envelope explicitly uses a deck carrier carrying one jacket or one topside, supporting this conservative screening treatment for large platforms: [BOEM CVOW COP Sections 1–3](https://www.boem.gov/sites/default/files/documents/renewable-energy/state-activities/CVOW-Commercial-COP-Sections-1-3.pdf), Section 3.4.1.3 and associated vessel tables.

### 6.2 Pile/template campaign

For pre-piling:

\[
t_{P,OSS}=t_{pos}+t_{template,set}+N_{pile/OSS}\left(
t_{release,p}+\frac{L_p}{v_{upend,p}}+\frac{d_{lower,p}}{v_{lower,p}}
+t_{stab,p}+\frac{L_e}{q_{drive,eff}}+t_{survey,p}\right)
+t_{template,recover}.
\]

For post-piling, place the jacket first and replace the template terms with pile handling through sleeves; jacket-vessel occupation may remain on the critical path. \(q_{drive,eff}\) is specific to the pile-soil-hammer system. Relief drilling, pile refusal, cut-off and extraordinary noise restrictions are separate.

\[
T_P=t_{setup,P}+\sum t_{P,OSS}+T_{transit,P}+T_{loadout,P}+T_{fieldmove,P}.
\]

### 6.3 Jacket campaign

\[
t_{J,OSS}=t_{pos,J}+t_{carrier,moor}+t_{release,J}
+\frac{H_{path,J}}{v_{crane,J}}+t_{set,J}+t_{level,J}
+t_{connect,J}+t_{survey,J}+t_{rig,release}.
\]

\(t_{connect,J}\) includes only the chosen pile-jacket structural connection—grout, weld or mechanical interface—and must state whether cure/inspection occupies the HLV. With post-piling, add the pile activity or calculate a combined HLV/piling critical path.

### 6.4 Topside campaign

For a single-lift topside:

\[
t_{S,OSS}=t_{pos,S}+t_{carrier,moor}+t_{release,S}
+\frac{H_{path,S}}{v_{crane,S}}+t_{mate,S}+t_{weld/grout,S}
+t_{survey,S}+t_{rig,release}.
\]

For a split topside, sum over modules and add module-to-module connections. Mass and size may lengthen engineered rigging/release, but no public source located supports a universal linear tonnes-to-hours equation. Use project-specific task times after feasibility selection.

### 6.5 Transport and vessel concurrency

For one structure per deck-carrier voyage:

\[
T_{carrier,c}=N_{load,c}\left(t_{load,c}+\frac{2D_p}{v_{carrier,c}}+t_{offload,c}\right).
\]

Heavy-lift-vessel duration is

\[
T_{HLV,c}=t_{setup,c}+\sum t_{site,c}+T_{HLV,transit}+T_{wait,critical}.
\]

The HLV and carrier often operate concurrently. Calculate each vessel's occupied days and cost separately; do not add carrier cycle time serially to HLV time unless the schedule makes it critical. A simple supply-capacity check analogous to feeder logistics is

\[
Q_c=\min\left(1/t_{site,c},\;n_{carrier}/t_{carrier\ cycle,c}\right).
\]

### 6.6 Hook-up and commissioning

\[
T_H=N_{OSS}\left(t_{mechanical}+t_{electrical}+t_{controls}+t_{test}\right)/n_{parallel,H}+t_{setup,H}.
\]

This campaign should use its own accommodation/commissioning spread. BOEM's CVOW documents distinguish about 2.5 net days for topside placement from a much longer complete construction/installation/commissioning window. Therefore full commissioning must not be charged at an HLV rate unless the HLV is contractually retained.

### 6.7 Cost

For each package:

\[
C_c=C_{mob,c}+r_{primary,c}T_{primary,c}+r_{carrier,c}T_{carrier,c}
+\sum_v r_{support,v}T_v+C_{consumables,c}.
\]

Then add exceptional works exactly once. Report vessel-days, not only total cost.

## 7. Public duration and rate evidence

### Net operation durations

The strongest public project-planning anchor located is the Coastal Virginia Offshore Wind commercial COP. It describes a jacket transported by feeder/deck carrier and placed by a floating DP heavy-lift vessel, with either pre-installed piles/templates or post-installed piles. It assigns approximately **5 net days per piled jacket foundation** and **2.5 net days per topside placement**. These figures support typical screening values, not universal productivity. Exact location: [BOEM CVOW COP Sections 1–3](https://www.boem.gov/sites/default/files/documents/renewable-energy/state-activities/CVOW-Commercial-COP-Sections-1-3.pdf), Section 3.4.1.3, around p. 3-43. Later public revisions retain the distinction between short net lift work and long full commissioning: [public Sections 1–3 revision](https://www.boem.gov/sites/default/files/documents/renewable-energy/state-activities/Public_Sec%201-3.pdf).

### Rate evidence

No current public source was found for a consistently scoped complete jacket/topside installation spread. A current ORBIT example reports USD 936,918 for 72 h of generic HLV mobilisation, implying USD 312,306/day. At the stated current ORBIT 2024-USD basis, this is approximately EUR 289,700/day in constant 2026 EUR. It is an **inferred planning proxy**, not a quoted rate and not automatically applicable to a 3,500 t jacket or 9,500 t HVDC topside: [ORBIT available outputs](https://nlrwindsystems.github.io/ORBIT/tutorials/available_outputs.html). A historical NREL vessel table reports USD 500,000/day for an HLV, USD 100,000/day for a feeder and seven mobilisation days, but the source table does not state a sufficiently clear price year for defensible normalization: [NREL/Applied Energy paper, Table 6](https://docs.nrel.gov/docs/fy21osti/78126.pdf). It is contextual only.

The model therefore uses the EUR 289,700/day proxy only as a reproducible placeholder for a generic moderate HLV. Named-vessel contractor rates, mobilisation and complete support scope are required whenever a lift approaches the actual crane envelope, especially for multi-thousand-tonne HVDC platforms.

## 8. Coherent screening scenarios

| Parameter | Favourable | Typical screening | Difficult | Evidence/use |
|---|---:|---:|---:|---|
| Piled-jacket net occupation | activity calculation; <5 d only if demonstrated | 5.0 d/OSS | activity calculation; >5 d when drivers warrant | CVOW supports only the 5 d planning anchor; no defensible universal bounds found |
| Topside net placement | activity calculation; <2.5 d only if demonstrated | 2.5 d/lift | activity calculation; >2.5 d when drivers warrant | CVOW supports only the 2.5 d planning anchor; excludes full hook-up/commissioning |
| HLV day rate | EUR 289.7k/d proxy | supplier input | supplier input/class change | Proxy inferred from current ORBIT generic HLV; not a complete spread |
| HLV mobilisation | 3 d proxy | 7 d | supplier input | 3 d inferred from ORBIT output event; 7 d contextual NREL assumption |
| Carrier loads | one jacket and one topside per load unless proven otherwise | same | same; remote yard | CVOW supports one/load for large structures |
| Pile concept | simple pre-pile template, few piles | ordinary pre- or post-pile | many/long piles or slow soil | Penetration calculated; drilling remains separate |
| Lift class | comfortable margin in 3–4 kt crane class | larger HLV and moderate margin | SSCV/ultra-heavy or method change | Actual radius/rigging governs, not nominal bands |
| Site/logistics | benign weather, close yard | ordinary North Sea-style campaign | remote yard, exposed weather, carrier bottleneck | Coherent scenario description |
| Hook-up/commissioning | project input; high onshore completion | project input | project input; extensive offshore completion | Must never be inferred from lift days alone |

Use the 5 d and 2.5 d typical values only when the detailed activity inputs are unavailable. The evidence does not justify invented numerical endpoints around those anchors. A favourable scenario requires a calculated result below the anchor, supported by proven crane margin, preassembly/onshore completion, a prepared foundation, short transport and benign seasonal access. A difficult case produces a calculated result above it through high crane utilization, large windage/footprint, slow pile penetration, complex connections, long transport or weather exposure. Relief drilling, a second topside module, a float-over, or an ultra-heavy class is an explicit model branch rather than a generic difficult multiplier.

## 9. Size and mass thresholds in context

Public projects show the relevant range:

- Butendiek: 1,032 t jacket, four 238 t piles and 2,250 t topside; the installation scope included jacket, pile lifting/upending/stabbing/hammering, noise mitigation, levelling/grouting and topside placement ([Scaldis project page](https://www.scaldis-smc.com/en/projects/groen-2014-may-butendiek/)).
- Rampion: approximately 2,000 t topside installed by *Rambiz* using its twin cranes ([Rampion announcement](https://www.rampionoffshore.com/news/media-releases/2000-tonne-offshore-substation-installed-rampion/)).
- Dogger Bank A/B: jackets around 2,900–3,100 t and topsides around 8,500 t; water depth approximately 28 m ([Saipem 2020 award release](https://www.saipem.com/sites/default/files/import/press_releases/CS%20Saipem%2022.07.2020.pdf), [Saipem installation milestone](https://www.saipem.com/en/media/press-releases/2023-05-04/saipem-new-milestone-achieved-offshore-wind-0)).
- Dogger Bank C: approximately 3,500 t jacket and 9,500 t topside ([project contract announcement](https://doggerbank.com/supply-chain/dogger-bank-c-offshore-substation-contract-awarded-to-heerema/)).
- Dogger Bank A topside: roughly 65 m by 36 m by 39 m on a four-leg jacket ([project installation article](https://doggerbank.com/construction/worlds-first-unmanned-hvdc-offshore-platform-installed-at-worlds-largest-offshore-wind-farm/)).
- CVOW design envelope: three HVAC platforms up to 900 MW each; public dimensions span roughly 30–62 m width, 54.4–74 m length and 17.8–54 m height depending on alternative ([BOEM public Sections 1–3](https://www.boem.gov/renewable-energy/state-activities/publicsec-1-3-0)).
- Empire Wind public design information describes approximately 5,000 t topside scale and a jacket seabed leg spacing around 60 m by 45 m, illustrating that footprint and pile scheme matter alongside mass ([BOEM Empire Wind alternatives appendix](https://www.boem.gov/sites/default/files/documents/renewable-energy/state-activities/Empire_Wind_EIS_App_O_Alternatives_Analysis_DEIS.pdf), [Empire Wind COP](https://www.boem.gov/sites/default/files/documents/renewable-energy/Public_EOW%20COP_v3.4_Volume%201_Redacted.pdf)).

These examples validate the need for class selection. They do not define a smooth mass-cost curve: the 8,500–9,500 t HVDC topsides require a fundamentally different heavy-lift capability from a 2,000 t HVAC topside.

## 10. Exceptional works

\[
C_{exceptional}=N_{drill}r_{drill}t_{drill}+N_{refusal}C_{remediate}
+N_{noise}C_{noise}+A_{prep}c_{seabed}+A_{scour}c_{scour}
+C_{UXO}+C_{weather\ restriction}+C_{other}.
\]

All inputs are site-specific unless a contractor quote explicitly includes them. A “difficult” normal duration must not absorb relief drilling, extensive seabed preparation or acoustic compliance without documentation.

## 11. Constant-2026-EUR normalization

Maintain separate source currency/year, price escalation, exchange rate and geographic-market factor:

\[
C_{2026EUR}=C_{y,cur}\frac{I_{2026}}{I_y}FX_{cur\to EUR,2026}F_{geo}.
\]

For a 2024-USD proxy, US CPI-U annual average 2024 = 313.689, June 2026 CPI-U = 333.952 and ECB 30 July 2026 EUR 1 = USD 1.1476 give

\[
F_{2024USD\to2026EUR}=0.9276715.
\]

Sources: [BLS annual CPI](https://www.bls.gov/regions/mid-atlantic/data/ConsumerPriceIndexAnnualandSemiAnnual_Table.htm), [BLS June 2026 release](https://www.bls.gov/news.release/archives/cpi_07142026.htm), [ECB exchange rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html). CPI is a transparent baseline, not a heavy-lift-vessel market index. Preserve \(F_{geo}\) as a separate documented adjustment.

## 12. Validation checks

| Case | Available physical/schedule scope | Model output tested | Material mismatch |
|---|---|---|---|
| CVOW COP | Piled jacket ~5 net days, topside ~2.5 net days; one structure/carrier load; pre- or post-pile methods | Net site duration and carrier count | Planning envelope, not measured cost; commissioning much longer than lift |
| Butendiek | 1,032 t jacket; four 238 t piles; 2,250 t topside; stated integrated installation activities | Lift class, pile count and activity completeness | No disclosed vessel-days or package price |
| Dogger Bank A/B/C | 2,900–3,500 t jackets; 8,500–9,500 t topsides; four-leg jacket context | HLV class change and single-lift feasibility | Press releases provide no auditable rate or net duration |
| Rampion | 2,000 t topside and named 3,300 t tandem crane vessel | Capacity-margin check | No jacket/pile duration or full spread cost |
| ORBIT generic HLV output | Implied USD 312,306/day and 3-day mobilization | Reproduce placeholder normalization | ORBIT offshore-substation method is not a jacket-specific commercial quote |

Use each benchmark only for the stated output. No public contract found offers a sufficiently clean allocation of fabrication, transport, jacket installation, topside installation and commissioning to calibrate the entire model.

## 13. Implementation pseudocode

```text
read platform count, water depth, distances, metocean, jacket geometry/mass,
     pile scheme, topside modules/geometry/mass, connection concept and vessel data

for every pile, jacket and topside lift:
    calculate lifted mass including rigging and dynamic factor
    check SWL at actual radius, hook height/depth, reach, clearance and weather
    check carrier/deck usable mass, footprint, point loads, stability and seafastening
    if any constraint fails: select larger class or return INFEASIBLE/METHOD CHANGE

piles = sum(platform legs * piles per leg)
jacket_loads = ceil(jackets / proven jackets_per_load)
topside_loads = ceil(topside_modules / proven modules_per_load)

if pre_pile:
    pile_time = template set/recover + sum(pile handling + effective penetration)
    jacket_time = jacket lift/set/level/connect
else:
    jacket_time = jacket lift/set
                + sum(post-pile handling + effective penetration)
                + level/connect

topside_time = sum(module position + release + lift + mate + connect + release rigging)
commissioning_time = separately scoped mechanical/electrical/control/testing work

for each campaign:
    calculate carrier cycle and installation-vessel productive capacity
    identify supply bottleneck and critical waiting
    calculate occupied days independently for HLV, carrier, tugs and support
    cost either a complete spread OR named vessel stack, never both

add explicit site-specific exceptional campaigns
normalize each source cost from its own currency/year to 2026 EUR
report feasibility margins, piles, lifts, loads, transits, vessel-days,
       mobilisation, cost by package, exceptional cost and total
```

## 14. Evidence gaps and RFI

Unsuccessful searches found no public, current and consistently bounded rate for a complete jacket-piling spread, moderate HLV spread, SSCV spread, deck carrier, or offshore commissioning spread. No defensible generic unit cost was found for pile relief drilling, underwater-noise compliance, structural grouting, seabed preparation or scour protection. Project announcements disclose impressive masses but rarely the actual radius, dynamic lift factor, net vessel occupation or price allocation. These parameters remain unresolved.

Ask the heavy-lift/subsea contractor and vessel owner:

1. What named-vessel 2026-EUR rate, mobilisation/demobilisation and minimum charter apply for each campaign?
2. Which carrier, tug, ROV/survey, piling plant, hammer, rigging, fuel, crew and consumables are included?
3. What SWL applies at the engineered radius/configuration, including rigging and dynamic factors?
4. What hook height/depth, boom clearance, deck/carrier load, footprint and stability margins remain?
5. Is one jacket/topside per carrier load assumed, and what are load-out, fastening and release durations?
6. What pile-template, handling and effective penetration time applies to the site-specific design and soil?
7. Is the jacket pre-piled or post-piled, and how long do levelling, grouting/welding, cure and inspection occupy the HLV?
8. What net topside lift/mating duration and weather criteria apply?
9. Which activities can overlap with carrier transits or grout cure, and what creates critical standby?
10. What offshore hook-up scope and vessel spread remain after onshore commissioning?
11. What conditions force an SSCV, tandem lift, split topside, float-over or Pioneering Spirit class?
12. How are weather standby, cancellation, overruns and pile refusal charged?

## 15. Suggested documentation page

1. Purpose and cost boundary.
2. Accounting units and four work packages.
3. Structure, site and execution inputs before equations.
4. Lift and transport feasibility gates.
5. Pile count and pre-pile/post-pile branch.
6. Jacket lift and connection calculation.
7. Topside module/lift calculation.
8. Carrier logistics and concurrent-vessel logic.
9. Separate hook-up/commissioning calculation.
10. Mobilisation, rate boundaries and 2026-EUR conversion.
11. Intermediate quantities and cost reconciliation.
12. Coherent scenarios and class-switch rules.
13. Project benchmarks as validation only.
14. Exceptional works, evidence gaps and RFI.

The accompanying CSV register provides parameter provenance and evidence grades. Blank numerical cells deliberately identify supplier-, contractor- or site-specific inputs.
