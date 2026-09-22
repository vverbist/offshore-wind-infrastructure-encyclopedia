# Monopile-supported wind-turbine installation cost model

**Research cut-off and access date:** 31 July 2026  
**Cost basis:** constant 2026 EUR, excluding VAT  
**Purpose:** transparent, medium-fidelity screening model—not a marine-operations simulator or contractor quotation.

## 1. Executive recommendation

Model the foundation and turbine as **two independently schedulable campaigns**:

1. monopile and, where applicable, transition-piece/secondary-steel installation; and
2. turbine transport and erection.

Do not fit one EUR/MW or EUR/turbine coefficient. Mass, deck area, diameter, length, hub height and rotor diameter should first determine **feasibility, vessel class and complete sets per load**. Installation time should then be driven by countable operations: positioning, jacking, handling, penetration, lifts, mechanical connections, transits and load-outs. This preserves the important discontinuities when a component exceeds crane capacity, one fewer set fits on deck, relief drilling becomes necessary, or a larger turbine-installation vessel is required.

The recommended total is

\[
C_{WT}=\sum_{c\in\{F,T\}}\left(C_{mob,c}+r_{primary,c}T_{primary,c}+\sum_v r_{v,c}T_{v,c}\right)+C_{exceptional,F}+C_{other},
\]

where \(F\) is the foundation campaign and \(T\) the turbine-erection campaign. A quoted **complete spread rate** may replace the vessel sum, but the two representations must never be added together.

The model should calculate activity-based duration where inputs are known. The favourable/typical/difficult effective durations later in this report are coherent screening fallbacks and validation bands, not extra multipliers to apply on top of the activity model.

## 2. Cost and technical boundary

### Included

- mobilisation and demobilisation of installation vessels and ordinary installation equipment;
- port load-out, sea fastening/release and normal transport;
- offshore positioning and, for jack-ups, jacking;
- monopile upending, lowering and normal impact/vibro driving;
- transition-piece placement and normal bolting or grouting, if used;
- turbine tower, nacelle and blade transport, lifts, attachment and normal mechanical completion;
- ordinary survey/ROV work explicitly included in the selected time envelope;
- ordinary feeder, tug and installation support where included in the selected spread.

### Separate or excluded

- component fabrication and supply; marshalling-port construction and rent;
- export/array cables and offshore substation;
- boulder clearance, unexploded-ordnance work, dredging, seabed levelling and scour protection;
- relief drilling, drive-drill-drive, pile refusal remediation and pile cut-off;
- project-specific underwater-noise systems and restricted-work windows;
- major offshore repairs, component replacement and extraordinary standby;
- electrical commissioning beyond the clearly defined turbine-installation scope;
- development, engineering, insurance and owner contingency.

Any contractor quote must be mapped to this boundary before calibration.

## 3. Accounting quantities

| Quantity | Definition | Common error avoided |
|---|---|---|
| Turbine location | One final wind-turbine position | Not the same as one vessel visit if foundation and turbine are separate |
| Foundation set | One monopile plus one transition piece, or one extended monopile with integrated interface | Avoids assuming every monopile has a separate TP |
| Turbine set | Tower sections, nacelle/RNA and blades required for one turbine | Deck packing, not MW, controls sets/load |
| Component lift | One crane pick from deck/barge to installed position | Blades and tower sections are separate lifts unless preassembled |
| Vessel load | Product actually transported between port and field before reload | A feeder delivery and WTIV shuttle are different logistics modes |
| Load-out | Loading and sea-fastening a vessel or feeder in port | The initial load-out is still a load-out |
| Port reload | Return to port after the first load | \(N_{reload}=N_{load}-1\) for a self-shuttling vessel |
| Installation campaign | Continuous deployment sharing mobilisation | Shared mobilisation does not imply simultaneous work |
| Normal installation day | Chargeable 24-hour day within the selected ordinary-weather envelope | Must not be combined with a second weather multiplier |

## 4. Inputs and physical calculations

### 4.1 Core project inputs

For \(N\) turbines specify water depth \(d_w\), port distance \(D_p\), inter-site distance \(D_i\), monopile mass \(m_{MP}\), length \(L_{MP}\), diameter \(D_{MP}\), embedment \(L_e\), transition-piece mass \(m_{TP}\), effective packed deck areas \(a_{MP},a_{TP}\), tower-section masses and areas, nacelle/RNA mass and area, blade mass, blade rack/deck area, blade length, hub height \(H_h\), rotor diameter \(D_R\), and connection concept.

“Effective packed deck area” includes racks, grillage, access and unusable space; it is not merely the plan area of the steel. If only geometry is available, the packing factor is a provisional engineering input and should be exposed.

### 4.2 Vessel feasibility gates

A vessel is feasible only if all relevant tests pass:

\[
\gamma_{dyn}m_j\le SWL(R_j),\qquad H_{hook}\ge H_{required,j},
\]

\[
\sum_j m_j\le M_{deck,use},\qquad \sum_j a_j\le A_{deck,use},\qquad p_{local,j}\le p_{deck,max},
\]

plus leg length/water-depth, air-gap, stability, boom-clearance, rack, motion, DP/mooring and weather limits. \(SWL(R_j)\) is capacity at the actual lift radius, not the brochure maximum. Failure is a **class change**, not a duration penalty.

Current fleet context confirms these step changes. Cadeler's Wind Peak/Wind Pace class reports more than 2,600 t crane capacity, 5,600 m² deck, over 17,600 t payload and storage for seven complete 15 MW or five 20+ MW sets; its technical specification gives a 180 m hook height above deck and 20 m/s crane wind limit. Jan De Nul's *Voltaire* lists a 3,200 t crane, 162.5 m lift height, 7,000 m² deck and 16,000 t payload. DEME's floating *Orion* lists a 5,000 t crane, 30,000 t payload and 8,000 m² free deck. These are feasibility references, not generic day rates. Sources: [Cadeler vessel page](https://www.cadeler.com/vessels/wind-pace), [Cadeler technical specification](https://www.cadeler.com/assets/uploads/PDFs/Vessels-Specifications/Wind-Peak-Technical-Specification_V4.pdf), [Jan De Nul Voltaire specification](https://www.jandenul.com/sites/default/files/public/Voltaire.pdf), [DEME Orion](https://www.deme-group.com/technologies/orion).

### 4.3 Complete sets per load

For campaign \(c\):

\[
n_{set/load,c}=\min\left[
\left\lfloor\frac{M_{use,c}}{m_{set,c}}\right\rfloor,
\left\lfloor\frac{A_{use,c}}{a_{set,c}}\right\rfloor,
n_{rack,c},n_{stability,c}
\right],
\]

\[
N_{load,c}=\left\lceil\frac{N}{n_{set/load,c}}\right\rceil,\qquad
N_{reload,c}=\max(0,N_{load,c}-1).
\]

For foundations, \(m_{set,F}=m_{MP}+m_{TP}\) if transported together. For turbines, \(m_{set,T}=\sum m_{tower}+m_{nacelle}+N_bm_b\), normally \(N_b=3\). Quantity-specific rack limits can bind before total mass or area.

## 5. Foundation-campaign duration

### 5.1 Normal onsite duration per location

For a straightforward driven monopile:

\[
t_{F,site}=t_{pos}+t_{jack}^{up}+t_{survey}+t_{release,MP}
+\frac{L_{MP}}{v_{upend}}+\frac{d_w}{v_{lower}}
+t_{tool}+\frac{L_e}{q_{drive,eff}}+t_{TP}+t_{jack}^{down}.
\]

\(q_{drive,eff}\) is an effective penetration rate for the stated soil and hammer method. It may include normal pauses and soft-start if explicitly calibrated. It excludes relief drilling, refusal remediation and project-specific noise restrictions unless stated. If geotechnical evidence indicates drilling or drive-drill-drive, create an explicit exceptional activity or another installation class.

For a separate transition piece:

\[
t_{TP}=t_{release,TP}+t_{reequip}+\frac{H_{lower,TP}}{v_{crane}}+
\begin{cases}
t_{bolt},&\text{bolted}\\
t_{grout,pump}+t_{grout,cure,critical},&\text{grouted.}
\end{cases}
\]

If grout can cure while the vessel performs other work, only critical-path occupation belongs in primary-vessel time. Extended monopiles omit \(t_{TP}\), but secondary steel must not disappear: model it as a later campaign or included package.

### 5.2 Transport and campaign logic

For a self-shuttling installation vessel:

\[
T_{F,primary}=t_{setup,F}+Nt_{F,site}+N_{load,F}t_{load,F}
+N_{load,F}\frac{2D_p}{v_{transit,F}}+(N-1)\frac{D_i}{v_{field,F}}.
\]

For feeder supply, the installation vessel remains offshore. Calculate the installation and supply capacities separately:

\[
Q_{install}=1/(t_{F,site}+D_i/v_{field}),
\]

\[
Q_{supply}=n_{feeder}\,n_{set/load,F}/
\left(t_{load,feeder}+2D_p/v_{feeder}+t_{transfer}\right),
\]

\[
T_{F,primary}=t_{setup,F}+N/\min(Q_{install},Q_{supply}).
\]

Feeder vessel-days are calculated from their own cycles. Do not serially add feeder time to WTIV time when they operate concurrently; do add both vessel costs over their occupied periods.

### 5.3 Public operation-time evidence

NREL's ORBIT methodology is the most transparent public decomposition located. Its monopile process uses 12 h port fastening per monopile, 8 h per TP, 2 h positioning, 1 h ROV survey, 3 h monopile release, calculated upending/lowering/driving, 1 h crane re-equipping, and either 4 h bolting or 2 h grout pumping plus 24 h curing. ORBIT explicitly models simple driving and does not currently represent drive-drill-drive. These are planning-model assumptions, not universal measured durations. Exact locations: [current ORBIT monopile method](https://nlrwindsystems.github.io/ORBIT/methods/install/MonopileInstall.html); NREL report [Section 3.1, equations 3.1 and 3.4–3.6, Table 4, pp. 27–32](https://www.nrel.gov/docs/fy20osti/77081.pdf).

## 6. Turbine-erection campaign

### 6.1 Component-count model

Let \(J\) contain tower sections, nacelle/RNA and blades. Then

\[
t_{T,site}=t_{pos}+t_{jack}^{up}+t_{jack}^{down}+\sum_{j\in J}N_j
\left(t_{release,j}+\frac{H_{path,j}}{v_{crane,j}}+t_{attach,j}\right)+t_{reequip}.
\]

Hub/tower height drives hook-height feasibility and lift path. Rotor diameter primarily drives blade length, rack/deck footprint, crane clearance and wind sensitivity. Component mass drives capacity at radius, rigging and deck load. Without a documented crane load-speed curve, mass should not be given an invented continuous time coefficient.

NREL ORBIT's public assumptions are 4 h port fastening for a tower, 4 h for a nacelle and 1.5 h per blade; offshore release times of 3 h for tower and nacelle and 1 h per blade; attachment times of 6 h for tower and nacelle and 3.5 h per blade; 2 h positioning and 1 h crane re-equipping. Lift time is hub height divided by crane rate, with tower-section height logic. Sources: [current ORBIT turbine method](https://nlrwindsystems.github.io/ORBIT/methods/install/TurbineInstall.html) and NREL [Section 3.2, Table 5 and equations 3.7–3.8, pp. 32–37](https://www.nrel.gov/docs/fy20osti/77081.pdf).

Weather is represented either by effective ordinary-condition times/rates or by explicit accessibility:

\[
t_{T,site,eff}=t_{T,site,calm}/A_{lift},\quad 0<A_{lift}\le1.
\]

Do not apply \(A_{lift}\) when the selected effective time already includes normal weather. A monthly or site-specific accessibility analysis is preferable for very large rotors because blade lifts at hub height are wind-critical; daily averages are a weak proxy.

The self-shuttle and feeder equations in Section 5.2 apply with turbine sets. Port fastening for a standard three-bladed, single-tower-set ORBIT turbine totals 12.5 h per set before any tower-section adjustment.

## 7. Cost calculation and spread definitions

For each campaign:

\[
C_c=C_{mob,c}+r_{primary,c}T_{primary,c}+\sum_v r_{v,c}T_{v,c}+C_{consumables,c}.
\]

Two valid rate conventions are:

- **Complete spread:** primary vessel, ordinary onboard crane/piling plant, normal crew, fuel, routine ROV and named support craft are all included in \(r_{spread}\).
- **Vessel stack:** primary, feeder(s), noise-mitigation vessel, survey/ROV and other support are each costed once.

The register uses a current ORBIT planning proxy of USD 400,000/day for the WTIV and USD 93,692/day for a feeder, with seven WTIV mobilisation days. The example vessel fields include 1,200 t maximum lift, 8,000 t cargo and 4,000 m² deck for the generic WTIV; these are not representative of every new-generation vessel. ORBIT states that defaults are updated periodically; treat the values as 2024-USD model proxies, not market quotations. Source: [ORBIT introduction and displayed configuration](https://nlrwindsystems.github.io/ORBIT/tutorials/introduction.html). A historical NREL model gives USD 225,000/day WTIV and USD 100,000/day feeder, but the table's price year is not stated clearly enough for normalization; it is contextual only: [Applied Energy/NREL paper, Table 6](https://docs.nrel.gov/docs/fy21osti/78126.pdf).

The current proxy converts to approximately EUR 371,100/day for the WTIV and EUR 86,900/day per feeder in constant June-2026 EUR using Section 11. These figures exclude any support not present in the ORBIT vessel configuration. A contractor complete-spread quote is required for an investment decision.

## 8. Coherent screening scenarios

The table deliberately links logistics, vessel class and weather. Values marked “model assumption” are fallbacks where public commercial data do not support a universal value.

| Parameter | Favourable | Typical screening | Difficult | Status and use |
|---|---:|---:|---:|---|
| Foundation normal, no-delay site occupation | 2.0 d/location | 3.0 d/location | 4.0 d/location | Supported screening bracket from South Fork's 2–4 d/foundation assumption; includes handling, driving and TP, but explicitly excludes weather and other delays |
| Turbine effective site occupation | activity calculation; benign access | activity calculation with site/month accessibility | activity calculation with adverse site/month accessibility | No transferable public point values; do not force one. Sofia's ~4.7 elapsed calendar d/turbine is contextual, not net WTIV occupation |
| WTIV/FIV proxy rate | EUR 371k/d | EUR 371k/d | Supplier input | Supported model proxy for generic vessel; class escalation likely in difficult case |
| Feeder proxy rate | EUR 86.9k/d each | EUR 86.9k/d each | Supplier input | Supported model proxy; support scope limited |
| WTIV mobilisation | 7 chargeable days | 7 days | supplier input | 7 d supported ORBIT input; difficult-case class change needs a quote |
| Foundation sets/load | calculated; often 4+ only if feasible | calculated | calculated; may be 1–2 | Never hard-code; mass/area/racks determine it |
| Turbine sets/load | calculated; new large vessel may carry 6–7 | calculated; 4–5 illustrative | calculated; 2–3 illustrative | Fleet capability contextual; Sofia achieved six 14 MW sets/load |
| Logistics | feeder continuity or short shuttle | moderate port distance | long port distance/feeder bottleneck | Scenario description |
| Soil/weather | simple drive, low downtime | ordinary drive and seasonal access | slow drive/high wind; relief drilling separate | A drilling requirement is not hidden in 5 d |

Move from favourable to typical when deck capacity, port distance, jacking depth, penetration, seasonal wind or feeder balance reduces productivity. Move to difficult when only one or two sets fit, hub-height blade lifts have poor access, installation is remote, driving is slow, or the vessel class changes. If refusal, relief drilling, an extended noise shutdown or component repair is credible, add an explicit exceptional activity rather than stretching the normal scenario.

The South Fork COP assumes a 24-hour window with no weather/sea delay and approximately 2–4 days per monopile foundation, including a 2–4 h pile-driving interval; use 2/3/4 days only for this explicitly no-delay scope ([BOEM South Fork COP, Section 3, p. 3-28](https://www.boem.gov/Volume-I-Construction-and-Operations-Plan/)). The primary model should calculate the times. For turbine erection, public evidence does not justify universal favourable/typical/difficult point values, so the scenario changes accessibility, logistics and class inputs rather than inventing durations.

## 9. Exceptional works

\[
C_{exceptional,F}=N_{drill}r_{drill}t_{drill}+N_{noise}C_{noise/unit}
+A_{scour}c_{scour}+N_{boulder}C_{boulder}+C_{UXO}+C_{remediation}.
\]

Public evidence does not support transferable unit costs for these items without soil, pile, metocean, acoustic-limit and design information. Keep the equations visible and mark inputs site-specific. Scour installation may be before or after piling; its vessel campaign must not be included in normal monopile time unless the rate boundary explicitly says so.

## 10. Validation cases

| Case | Physical evidence | What it can test | Scope mismatch |
|---|---|---|---|
| Sofia foundations | 100 foundations; 20–35 m water; ~195 km offshore; three monopiles per cycle; May 2024–July 2025 campaign; extended monopiles | Load count, long-distance logistics and elapsed foundation productivity | Calendar period includes weather, support and interruptions; no disclosed cost or net vessel days. [RWE completion](https://www.rwe.com/en/press/rwe-offshore-wind-gmbh/2025-07-15-sofia-offshore-wind-farm-completes-installation-of-foundations/), [RWE start](https://www.rwe.com/en/press/rwe-offshore-wind-gmbh/2024-05-21-rwe-installs-first-turbine-foundation-at-its-flagship-sofia-offshore-wind-farm/) |
| Sofia turbines | 100 SG 14-222 turbines; 222 m rotor; 108 m blades; >200 km offshore; six sets/load; March 2025–10 June 2026 | Sets/load and calendar turbine productivity for a remote large-turbine project | Overlapping campaign calendar is not net WTIV time and disclosed package cost is absent. [RWE completion](https://sofiawindfarm.com/latest/announcements/rwe-completes-installation-of-all-turbines-at-sofia-offshore-wind-farm/) |
| Baltic Power monopiles | 78; roughly 1,300–1,700 t, up to 100 m and >9 m diameter; installation completed by 18 Feb 2026 | Crane/payload class and achieved calendar schedule | Campaign includes a large support fleet and noise mitigation; no clean installation cost. [ORLEN start](https://www.orlen.pl/en/about-the-company/media/press-releases/current/2025/February-2025/ORLEN-and-Northland-Power-Commence-Construction-of-Polands-First-Offshore-Wind-Farm), [ORLEN completion](https://www.orlen.pl/en/about-the-company/media/press-releases/current/2026/february-2026/All-foundations-installed-as-Baltic-Power-moves-closer-to-completion) |
| NREL 15/22 MW reference turbines | 15 MW: 242 m rotor, 150 m hub, 853 t tower and 1,319 t monopile; 22 MW: 284 m rotor, 170 m hub, 1,574 t tower and 2,097 t monopile | Vessel capacity, hook height, deck load and sets/load sensitivity | Reference designs, not projects or measured campaigns. [NREL comparison table](https://www.nrel.gov/docs/fy24osti/89807.pdf) |
| ORBIT 50-turbine example | Calculated 1,015 t, 63.7 m monopile; 407 t TP; generic USD 400k/d WTIV; two feeders; reported model foundation cost | Reproduce equations and prevent cost-boundary errors | Synthetic design and model defaults, not observed market price. [ORBIT tutorial](https://nlrwindsystems.github.io/ORBIT/tutorials/introduction.html) |

Do not calibrate a universal EUR/turbine coefficient to these projects. Use them to test intermediate quantities and flag implausible schedules.

## 11. Constant-2026-EUR normalization

Keep source price year, source currency, escalation and exchange conversion in separate fields:

\[
C_{2026EUR}=C_{y,cur}\times\frac{I_{2026}}{I_y}\times FX_{cur\rightarrow EUR,2026}.
\]

For the 2024-USD ORBIT proxies, this study uses US CPI-U annual average 2024 = 313.689, June 2026 CPI-U = 333.952, and the ECB 30 July 2026 reference rate EUR 1 = USD 1.1476:

\[
F_{2024USD\rightarrow2026EUR}=\frac{333.952}{313.689}\frac{1}{1.1476}=0.9276715.
\]

Sources: [BLS annual CPI table](https://www.bls.gov/regions/mid-atlantic/data/ConsumerPriceIndexAnnualandSemiAnnual_Table.htm), [BLS June 2026 CPI release](https://www.bls.gov/news.release/archives/cpi_07142026.htm), [ECB reference rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html).

CPI is transparent but does not reproduce a tight offshore-vessel market. Prefer a documented offshore-construction or vessel index for vessel rates if its coverage and licensing permit; exchange at a common reference date afterward. Geographic-market adjustments must remain a separate factor, never be silently folded into inflation.

## 12. Implementation pseudocode

```text
read project, component, port, site, vessel, weather, and cost inputs
for campaign in [foundation, turbine]:
    define components and effective packed deck area per complete set
    test crane SWL at radius, hook height, deck mass/area/load,
         water depth, leg length, stability, racks, and operating limits
    if any test fails: select a feasible vessel class or return INFEASIBLE
    sets_per_load = min(floor(usable_mass / set_mass),
                        floor(usable_area / set_area), rack_limit, other_limit)
    loads = ceil(number_of_turbines / sets_per_load)
    reloads = max(0, loads - 1)

foundation_site_time = positioning + jacking + survey + releases
                     + upending + lowering + effective_simple_drive_time
                     + TP_or_secondary_interface + jackdown
if relief_drilling_required: add separate exceptional campaign

turbine_site_time = positioning + jacking + jackdown
                  + sum(component_count * (release + lift + attach))
apply either site-specific accessibility OR effective scenario time, never both

if self_shuttle:
    primary_time = setup + onsite_work + field_moves
                 + loads * (port_loadout + round_trip_transit)
else:
    calculate installation capacity and feeder-supply capacity
    primary_time = setup + units / min(capacities)
    calculate feeder days independently

campaign_cost = mobilisation + primary_rate * primary_time
              + sum(feeder/support rate * their occupied time)
add site-specific exceptional costs once
report feasibility margins, sets/load, loads, reloads, onsite days,
       transit days, vessel-days, cost by campaign, exceptions and total
```

## 13. Evidence gaps and RFI

No public source located provides a current, auditable North Sea **complete spread** quotation split consistently between new-generation WTIV/FIV, feeders, noise mitigation and routine survey. No transferable public relationship was found between component mass and lift time, between rotor diameter and weather downtime, or between monopile diameter/mass and drive rate independent of soil and hammer. Commercial project announcements usually report calendar windows, not net chargeable vessel-days or inclusions. These remain unresolved—not silently estimated.

Ask a foundation/turbine installation contractor or vessel owner:

1. What 2026-EUR day rate and mobilisation applies to the named vessel, port, season and duration?
2. Which feeder, tug, survey/ROV, piling, noise-control, fuel, crew, consumables and port services are included?
3. What crane capacity applies at the required radius, hook height and wind limit for every component?
4. What usable deck mass, effective deck area, point load and rack limits apply, and how many complete project-specific sets fit?
5. What port load-out/fastening and offshore release times apply per component?
6. What positioning, jacking, inter-site and ordinary-weather allowances are embedded in quoted productivity?
7. What effective penetration time applies to the site-specific pile/soil/hammer combination, and what triggers relief drilling?
8. What effective turbine duration applies at the project hub height and blade length by month?
9. How many feeders are needed to avoid starving the installation vessel at the stated distance?
10. How are standby, cancellation, weather risk, repairs, demobilisation and schedule overrun charged?

## 14. Suggested documentation page

1. Why the model needs foundation and turbine installation CAPEX.
2. Cost boundary and excluded exceptional work.
3. Accounting quantities and the two campaign classes.
4. Physical/project inputs, followed by vessel and component inputs.
5. Feasibility gates and class-change rules.
6. Complete sets/load, loads and reloads.
7. Foundation onsite duration and exceptional piling routes.
8. Turbine component-count and lift-path duration.
9. Self-shuttle versus feeder logistics.
10. Vessel/spread cost, mobilisation and normalization.
11. Reported intermediates and cost reconciliation.
12. Coherent scenarios and scenario-switch conditions.
13. Validation cases only after the calculation.
14. Limitations, unresolved inputs and RFI.

The accompanying CSV register contains implementation-ready values, provenance and evidence grades. Unsupported project-specific quantities are intentionally blank.
