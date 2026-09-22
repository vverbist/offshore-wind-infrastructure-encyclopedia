# Offshore cable and hydrogen-pipeline installation cost model

**Medium-fidelity research basis and implementation specification**  
**Price basis:** constant 2026 EUR, where normalization is possible  
**Evidence cut-off and access date:** 31 July 2026  
**Scope:** 66–132 kV inter-array cables; 320–525 kV HVDC export systems; spoolable thermoplastic-composite-pipe (TCP) hydrogen infield and export systems

## Executive decision

The proposed model is directionally right but should not be implemented as one vessel rate multiplied by one campaign duration. The defensible common structure is a **sum of work packages and campaigns**:

\[
C_{\mathrm{inst}}=\sum_{c\in\mathcal C}\left(C_{\mathrm{mob},c}+r_{\mathrm{spread},c}T_{\mathrm{charge},c}\right)+C_{\mathrm{exceptional}}+C_{\mathrm{unit}}
\]

This matters because simultaneous lay-and-bury, separate lay and burial, pre-trenching, post-lay protection and completion work can use different spreads and may run as separate campaigns. A shared mobilisation is not simultaneous installation. A complete-spread rate is not the same as the primary vessel's day rate.

The evidence supports a usable screening model for cables, provided that:

- public operating speeds are converted into deliberately provisional effective campaign rates;
- the public vessel-rate values are treated only as cross-checks until a complete-spread quotation is obtained;
- array and export circuits are counted as physical cable sections, not merely route-kilometres; and
- bundled HVDC installation is used only when the actual cable system and vessel are engineered for it.

The evidence does **not** support a numerical offshore hydrogen-TCP installation-cost model today. Public sources support physical feasibility envelopes and installation concepts, but not a complete-spread day rate, achieved production rate, connection duration, effective vessel load, or more than one pipe per pass. For TCP the model structure is ready, but cost calculation is gated by supplier and contractor inputs. Transferring steel reel-lay or conventional flexible-pipe rates would create false precision.

### Model readiness by class

| Installation class | Physical model | Duration model | Cost model | Screening status |
|---|---:|---:|---:|---|
| 66–132 kV inter-array cable | Ready | Ready with provisional `q_eff` | Primary-vessel proxy only; complete spread required | Usable for sensitivity studies |
| 320–525 kV HVDC export system | Ready, including pole/return counting | Ready with provisional `q_eff` and campaign logic | Primary-vessel proxy only; complete spread required | Usable for sensitivity studies after cable configuration is fixed |
| Spoolable TCP H2 infield | Ready as a gated class | Not numerically supported | Not publicly supported | Structure only; supplier/contractor RFI required |
| Spoolable TCP H2 export | Conceptual only at long-route scale | Not numerically supported | Not publicly supported | Do not produce a base-case cost until qualified product and installation concept exist |

## 1. Cost boundary and critique of the proposed formulation

### 1.1 Recommended boundary

The installation CAPEX boundary begins when the contracted installation spread mobilises for the campaign and ends after the installed asset has completed the offshore tests included in the installation contract. It includes:

- mobilisation and demobilisation;
- port load-out and reload turnaround when charged to the installation campaign;
- route preparation only when it is routine and explicitly included in the chosen work package;
- offshore laying and, if applicable, burial;
- ordinary positioning, minor interruptions, normal installation survey and normal weather exposure through `q_eff`;
- pull-ins, hang-offs, field end fittings, terminations or tie-ins only to the extent they occupy the charged spread or are separately priced under `C_unit`;
- campaign-required offshore joints; and
- explicitly identified exceptional work.

It excludes cable/pipe manufacture, onshore electrical equipment, converter stations, substations, hydrogen compression, development/consenting, owner engineering, financing, contingency, operational expenditure and decommissioning unless a project deliberately broadens the boundary.

### 1.2 Why the original single-spread equation is insufficient

The original form has five problems:

1. The signs in the supplied expression appear as subtraction. All time and exceptional-work contributions must add to cost.
2. One `r_spread` cannot represent both a cable-lay vessel and a separate burial spread without hiding double counting or omission.
3. A pull-in may occupy the lay vessel, while final electrical termination may be performed later by another team. Both should not automatically be multiplied by the lay-spread rate.
4. Port reloads and offshore joints are different events. A return to port can include transit, loading and repositioning; an inline joint can take place offshore and has its own count.
5. A single campaign duration obscures shared mobilisation across multiple passes and separate mobilisation for follow-on burial or protection.

### 1.3 Recommended cost architecture

For work package/campaign `c`:

\[
T_{\mathrm{charge},c}=t_{\mathrm{fixed},c}+T_{\mathrm{route},c}+T_{\mathrm{interface},c}+T_{\mathrm{load},c}+T_{\mathrm{joint},c}
\]

\[
T_{\mathrm{route},c}=\sum_j \frac{L_{\mathrm{pass},cj}}{q_{\mathrm{eff},cj}}
\]

\[
T_{\mathrm{interface},c}=\sum_i N_{\mathrm{conn},ci}t_{\mathrm{conn},ci}
\]

\[
T_{\mathrm{load},c}=I_{0,c}t_{\mathrm{initial\ load},c}+N_{\mathrm{reload},c}t_{\mathrm{reload},c},\qquad
T_{\mathrm{joint},c}=N_{\mathrm{joint},c}t_{\mathrm{joint},c}
\]

`I_0` is 1 only when initial load-out is charged as spread time. It is 0 when the initial load is already included in mobilisation or another fixed contract item. `t_reload` includes the defined return transit, port handling/load and repositioning; it is not merely the six-hour ORBIT product-loading task.

Then:

\[
C_{\mathrm{campaign},c}=C_{\mathrm{mob},c}+r_{\mathrm{spread},c}T_{\mathrm{charge},c}
\]

`C_unit` captures connection or completion work priced per item or performed by a different spread outside the charged critical path:

\[
C_{\mathrm{unit}}=\sum_k N_k c_k
\]

Exceptional work remains outside normal production:

\[
C_{\mathrm{exceptional}}=N_{\mathrm{cross}}C_{\mathrm{cross}}+L_{\mathrm{protection}}c_{\mathrm{protection}}+N_{\mathrm{landfall}}C_{\mathrm{landfall}}+C_{\mathrm{other}}
\]

All terms are positive. A value is entered only once: for example, a burial ROV and support vessel belong either in `r_spread` or in another work package, never both.

## 2. Accounting quantities

| Quantity | Definition | Common error prevented |
|---|---|---|
| Route-kilometre | Horizontal centreline distance between route endpoints. One 100 km corridor is 100 route-km even if it contains three cables. | Treating a tripole HVDC system as only 100 installed km |
| Physical cable-kilometre | Sum of manufactured/installed cable lengths, including each pole/conductor system and approved installation slack or vertical allowances. | Applying a single-cable rate to the whole HVDC corridor |
| Physical pipeline-kilometre | Sum of installed pipe lengths for all parallel lines, including defined riser/pull-through allowances. | Ignoring two H2 lines in one corridor |
| Section | One continuous product length installed between interfaces or joints. Array sections normally run foundation-to-foundation; TCP sections can be reel-length limited. | Confusing a string with one continuous cable |
| Parallel asset | A distinct physical cable or pipe following the route. A symmetric HVDC bipole normally has two power cables; some 2 GW systems add a metallic return. | Assuming every HVDC scheme has exactly two cables |
| Installation pass | One traversal in which `g` physical assets are actually laid. | Equating shared carriage or mobilisation with simultaneous lay |
| Campaign | A mobilisation-to-demobilisation use of one contracted spread. Several passes can share a campaign. | Charging mobilisation per pass |
| Load-out | Product transferred to the vessel for an initial load or later load. | Counting only port visits |
| Port reload | Return/turnaround event after the initial load. `N_reload = N_load - 1` within a campaign. | Charging an initial load as a reload |
| Pull-in | Bringing a cable/pipe end into a structure, J-tube or shore interface. | Combining physical handling with final testing without scope clarity |
| Termination | Electrical preparation, connection and testing of a cable end. | Multiplying shore-based completion time by CLV rate |
| End fitting | Mechanical pressure-containing TCP termination applied to a pipe end. | Treating TCP like a continuously welded steel line |
| Tie-in | Connection of an installed pipeline end to a manifold, riser or other subsea system. | Counting only pipe ends, not subsea interfaces |
| Joint | Connection between two product lengths. Cable joints can be offshore inline or factory/land; TCP field end-fitting connections are not assumed equivalent. | Hiding joint discontinuities in km rate |
| Crossing | Engineered interaction with existing infrastructure requiring a dedicated crossing design. | Hiding mattresses/rock in normal burial rate |
| Landfall | Offshore-to-onshore transition; HDD, direct pipe, open cut and shore-end pull have materially different packages. | Treating landfall as normal route production |

### 2.1 Relationships

For asset type `a` with route length `L_route,a`, parallel count `N_parallel,a`, installation slack fraction `s_a`, and separately modelled vertical/structure allowance `L_vert,a`:

\[
L_{\mathrm{physical},a}=N_{\mathrm{parallel},a}L_{\mathrm{route},a}(1+s_a)+L_{\mathrm{vert},a}
\]

Do not apply slack twice if the project-supplied section lengths already include it.

For an installation method that truly lays `g_a` physical assets per pass:

\[
N_{\mathrm{pass},a}=\left\lceil \frac{N_{\mathrm{parallel},a}}{g_a}\right\rceil
\]

\[
L_{\mathrm{pass},a}=N_{\mathrm{pass},a}L_{\mathrm{route},a}
\]

For non-identical sections, use explicit pass groups instead of the shortcut:

\[
L_{\mathrm{pass}}=\sum_{p}\max_{m\in p} L_m
\]

where group `p` contains assets installed simultaneously. The maximum is appropriate only when assets in the group share substantially the same alignment; otherwise sum the actual traversed paths.

### 2.2 HVDC rate interpretation

An installation rate applies to **one vessel route traversal**. It applies to a complete HVDC system-route only when all physical cables represented by that system are actually laid in that traversal. BOEM/BSEE guidance distinguishes bundled synchronous installation from separate cables and notes that separate cables require separate passes; it also warns that some vessels carry only one cable. Hansa PowerBridge and Caithness–Moray demonstrate bundled bipole installation, while Ariadne's two cables were laid in separate campaign completions. Therefore `g_HVDC` is a project design variable, not a voltage-based default.

## 3. Dependency-ordered calculation

### 3.1 Inputs

Inputs are grouped so that physical design is not mixed with commercial assumptions.

1. **Design:** class, route geometry, number and type of physical assets, section lengths, slack policy, connection inventory, crossings, landfalls and protection.
2. **Method:** bundled/separate lay, simultaneous/separate burial, pass grouping, spread definition, port, campaign split and product-per-load.
3. **Scenario:** `q_eff`, complete-spread rate, mobilisation, fixed time, connection times, reload time and joint time.
4. **Economic basis:** source currency/year, escalation index, exchange rate and explicit geographic factor.

### 3.2 Physical asset quantities

For each section `s`:

\[
L_{\mathrm{physical},s}=n_s\left[L_{\mathrm{route},s}(1+s_s)+L_{\mathrm{vertical},s}\right]
\]

Project total:

\[
L_{\mathrm{physical}}=\sum_sL_{\mathrm{physical},s}
\]

### 3.3 Passes and pass length

Create feasible pass groups with no more than `g` physical assets. Calculate `N_pass` and `L_pass` by work package. Burial passes can differ from lay passes: a bundled cable pair may be laid once but buried in separate trenches/passes if the protection design requires it.

### 3.4 Effective load and reload count

Gross mass-limited capacity is:

\[
L_{\mathrm{load,mass}}=\frac{M_{\mathrm{usable}}}{\lambda_{\mathrm{product}}}
\]

Effective physical product length per load is:

\[
L_{\mathrm{load}}=\min(L_{\mathrm{load,mass}},L_{\mathrm{reel/partition}},L_{\mathrm{manufacturing}},L_{\mathrm{handling}})
\]

Within campaign `c`:

\[
N_{\mathrm{load},c}=\left\lceil\frac{L_{\mathrm{physical,loaded},c}}{L_{\mathrm{load},c}}\right\rceil,qquad
N_{\mathrm{reload},c}=\max(0,N_{\mathrm{load},c}-1)
\]

`L_load` is physical product-km. If two equal cables are bundled, system-route km per load is `L_load/2`. If products have different linear masses, use total loaded mass rather than an average. Initial load-out must then be charged exactly once: through mobilisation, `t_fixed`, or `I_0 t_initial load`.

### 3.5 Route duration

\[
T_{\mathrm{route},c}=\sum_jL_{\mathrm{pass},cj}/q_{\mathrm{eff},cj}
\]

`q_eff` is achieved progress over chargeable campaign time under ordinary conditions. It includes routine positioning, normal preparation, expected minor interruption, ordinary installation survey and the normal weather regime chosen for the scenario. It includes both lay and burial only for an integrated lay/bury work package. It excludes mobilisation, major reloads, joints, enumerated interfaces, landfalls, engineered crossings and unusual protection.

### 3.6 Interface duration

\[
T_{\mathrm{interface},c}=\sum_iN_{\mathrm{conn},ci}t_{\mathrm{conn},ci}
\]

Use separate categories only when the connection type has a different physical driver and evidence. Recommended initial categories are:

- array: foundation pull-in/hang-off plus termination/test; offshore-substation interface; offshore repair/joint;
- HVDC: landfall pull; offshore-platform pull-in; termination/joint;
- TCP: J-tube pull-through; field end fitting; subsea or topside tie-in; pressure test/commissioning.

### 3.7 Total duration and cost

Apply the equations in section 1.3 by campaign, then sum campaign, unit and exceptional costs. Report every intermediate quantity: physical km, pass count, pass-km, loads, reloads, joints, route days, interface days, total chargeable days, mobilisation, spread cost and exceptions.

## 4. Installation-class definitions

### 4.1 66–132 kV inter-array cables

**Normal method.** Three-core AC sections are installed foundation-to-foundation. The CLV loads multiple sections, performs pull-ins at each end, lays the section, and either buries simultaneously or leaves it for a separate burial vessel. ORBIT explicitly models both strategies and returns to port when storage is exhausted.

**Normal spread.** CLV with cable-handling and lay equipment; burial tool/ROV if simultaneous; workboat/tugs and project support as required; survey capability. Public project plans show that actual campaigns can involve multiple lay, burial and support vessels, so a CLV day rate alone is not a complete spread.

**Included in `q_eff`.** Routine section positioning and survey, ordinary lay and selected normal burial method, normal weather and minor interruptions. **Separate:** load/reload, two end interfaces per section, major crossings, difficult trenching/pre-trench, extra protection and repair joints.

**Applicable envelope.** This class is aimed at 66–132 kV inter-array products. Public 66 kV examples span roughly 20–50 t/km in the Thor environmental material; a Danish technology catalogue gives 50–70 t/km for 66 kV and 125 t/km for 132 kV, which is contextual rather than a universal product specification.

**Discrete thresholds.** Carousel mass/partition capacity; number and length of sections; section end count; transition from simultaneous to separate burial; trenching/cutter requirement; and cable-protection or crossing count.

**Different class required.** Dynamic cable/floaters, deep-water free-hanging installation, unusually heavy 132 kV designs, repair campaigns, or pre-installed cable protection systems should be separate methods or work packages.

### 4.2 320–525 kV HVDC export systems

**Normal method.** Shore-end pull/landfall followed by long-route installation toward the offshore converter platform, or the reverse, using a large CLV. Cable(s) may be bundled and laid synchronously or laid separately. Post-lay burial remains common where a bundled product cannot be buried simultaneously.

**Physical counting.** Count every pole cable, metallic return and separately installed communications cable. A `±525 kV system` is not a single cable. A symmetric bipole is normally two power cables; current 2 GW Dutch designs include two poles plus a metallic return. Fibre may be bundled but should not be counted as another pass unless installed separately.

**Normal spread.** High-capacity CLV, cable handling/bundling equipment, lay control, survey/ROV and—if integrated—burial tool; otherwise a separate burial spread. Modern public vessel capacities range from about 10,000–23,000 t, but usable capacity is product and partition specific.

**Included in `q_eff`.** Routine long-route laying, ordinary positioning/survey and normal weather; burial only if the chosen work package actually integrates it. **Separate:** landfall, offshore-platform pull-in, inline joints, reloads, major crossings, pre-sweeping, rock placement and separate burial.

**Discrete thresholds.** Number of physical conductors; `g=1`, `2` or qualified `3`; gross and partitioned cable capacity; maximum factory length; inline-joint count; landfall method; burial-class change; and whether a follow-on protection campaign is needed.

**Different class required.** Mass-impregnated cable, dynamic export cable, deepwater vertical lay, repair, or a three-cable system whose vessel cannot bundle all three requires its own method configuration.

### 4.3 Spoolable TCP hydrogen infield pipelines

**Normal concept.** Manufacturer evidence supports horizontal lay from a small multipurpose vessel, multiple transport-and-installation reels, J-tube pull-through and field end fittings. Strohm describes up to 7.5 in internal diameter, 689 bar and 121 °C for its generic TCP flowline portfolio and continuous lengths of about 3–6 km depending on size and pressure. These are product-family maxima, not a qualified H2 design point.

**Normal spread.** Candidate small MPSV or flexible-lay vessel with reel drive/overboarding equipment, tension control, survey/ROV and pull-through equipment; burial or stability equipment when required. The exact spread is not public.

**Included in `q_eff`.** Only routine overboarding/lay, positioning/survey, normal weather and—if demonstrated by the selected spread—routine burial. **Separate:** each end fitting, J-tube pull-through, tie-in, hydro/pneumatic test, intermediate connector, crossing, protection and qualification-specific work.

**Feasibility limits.** Qualified hydrogen permeation, pressure/diameter/temperature combination, collapse and installation loads, minimum bend radius, reel capacity, on-bottom stability and J-tube geometry. DNV-ST-F119 is the relevant offshore TCP standard, while DNV's H2 JIP explicitly identifies hydrogen-specific gaps in existing non-metallic-pipe rules.

**Discrete thresholds.** Whether a section fits one manufactured length/reel; number of reels onboard; every field end fitting/intermediate connection; J-tube pull force; burial/stability method; and vessel-class change.

**Evidence status.** Offshore O&G deployments demonstrate analogous installation, not commercial offshore H2 service. The public HOPE project was still in permitting/demonstration preparation in the latest reporting period. Cost and productivity remain RFI inputs.

### 4.4 Spoolable TCP hydrogen export pipelines

The physical method may extend the infield concept through repeated reels or a large carousel, but no public source found demonstrates a long offshore hydrogen export TCP with commercial installation performance. A 100 km route would far exceed the public 3–6 km continuous-length range unless multiple lengths are carried and joined, or a project-specific factory-to-vessel spooling concept changes the limit. Every connector then becomes a duration, integrity and cost discontinuity.

This class must pass a stage gate before cost calculation:

1. named product and H2 qualification envelope;
2. route-specific hydraulic diameter/pressure and on-bottom-stability design;
3. continuous-length and field-connection concept;
4. vessel/reel/carousel and overboarding design;
5. installation analysis including bend, tension, collapse and J-tube loads;
6. contractor spread, production and connection quotation.

Until these are met, a numeric export-TCP result should be reported as **not parameterized**, not as zero and not as a steel-pipeline proxy.

## 5. Evidence-graded parameter table

Evidence labels mean: **supported** = directly stated or mechanically derived from an authoritative source; **provisional** = transparent screening recommendation anchored to evidence but requiring confirmation; **contextual only** = useful boundary/benchmark but not a model input; **site-specific input required**; **supplier/contractor input required**; **unresolved TODO**.

| Parameter / symbol | Class | Source value or public envelope | Recommended favourable / typical / difficult | Unit | Included activities / scope | Source, price year | Evidence | Limitation |
|---|---|---|---|---|---|---|---|---|
| Assets per lay pass, `g_lay` | Array | One three-core section is installed at a time in ORBIT | 1 / 1 / 1 | physical cables/pass | Actual lay only | S1 §3.4; S2 | Supported | Parallel strings share campaign, not pass |
| Effective lay/bury rate, `q_eff` | Array | Burial 0.05–0.5 km/h, typical 0.2; ORBIT integrated default 0.3 km/h | **5.0 / 3.0 / 0.8** km/day screening values | route-km/day/pass | Routine integrated lay/bury, positioning, minor downtime, normal weather/survey | S1 p.29 & Table 8; S2; non-cost | Provisional | Recommended values are deliberately below operating rates; replace with contractor achieved data |
| Operating burial rate, `q_oper` | Array/HVDC | 0.05–0.5, typical 0.2; project-owner tables: plough/jet 0.3, cutter 0.03–0.08 | Do not use directly as `q_eff` | km/h | Tool working speed | S1 p.29; S5 Table 6.14 | Supported | Excludes weather, interfaces and campaign logistics |
| CLV day-rate proxy, `r_primary` | Array | USD 225,000/day in $2023; normalized **EUR 214,882/day** | Same public cross-check in all scenarios; request complete spread | 2026 EUR/day | Primary CLV only | S3 Table F7; $2023; S12–S14 normalization | Supported proxy | Not a current commercial quote and not complete spread |
| Complete spread rate, `r_spread` | Array | No defensible current public value found | RFI / RFI / RFI | 2026 EUR/day | CLV, burial tool, ROV, support, crew, fuel, overhead as contracted | — | Contractor input required | Never add proxy support costs twice |
| Mobilisation, `C_mob` | Array | ORBIT example mobilises 72 h; applied study uses 7 days | 3 days × quoted spread / 7 days × quoted spread / contractor plan | 2026 EUR/campaign | Mobilisation and demobilisation per quote | S2 outputs; S15 Table 6 | Provisional | Determine whether demob and port/transit are included |
| Connection time, `t_conn` | Array | Pull-in 5.5 h plus terminate/test 5.5 h | 11 / 11 / 11 h per cable end pending quote | h/end | Pull-in plus termination/test when CLV-blocking | S1 Table 7; S2 | Supported proxy | If completion team works later, move termination to `C_unit` |
| Port cable load time, `t_port_load` | Array/HVDC | 6 h default | 6 h plus actual return/reposition transit | h/load | Cable loading only | S1 Table 7 | Supported proxy | Not full port turnaround |
| Inline splice time, `t_joint` | Export cable | 48 h default | 48 / 48 / contractor-specific | h/joint | Offshore inline splice | S1 Table 7 and §3.5 | Supported proxy | Technology and joint design specific |
| Cable mass, `lambda` | 66 kV array | 20–50 t/km in Thor; 50–70 t/km catalogue context | Product datasheet / product datasheet / product datasheet | t/physical km | Installed cable mass | S6 Table 7.1; S16 Table 5.2 | Supported range/context | Do not infer 132 kV from 66 kV |
| Cable mass, `lambda` | 132 kV array | 125 t/km catalogue value | Product datasheet required | t/physical km | Installed cable mass | S16 Table 5.2 | Contextual only | One generic catalogue value |
| Assets per pass, `g_lay` | HVDC | 1 separate; 2 demonstrated bundled; emerging vessels advertise 3–4 cable capacity | 2 bundled / 1 or 2 project-specific / 1 plus separate burial | physical power cables/pass | Actual simultaneous lay | S4 §5.3; S7–S10 | Supported options | `g=3` only for a qualified poles-plus-return system and spread |
| Effective route rate, `q_eff` | HVDC | Cable burial operating evidence as above; no public achieved HVDC campaign rate found | **5.0 / 3.0 / 0.8** km/day/pass screening values | route-km/day/pass | Routine selected lay/bury package | S1, S2, S5 | Provisional | Larger cable and burial design may change value materially |
| CLV day-rate proxy, `r_primary` | HVDC export | USD 300,000/day in $2023; normalized **EUR 286,510/day** | Same public cross-check; complete spread RFI | 2026 EUR/day | Primary export CLV only | S3 Table F7; S12–S14 | Supported proxy | U.S. floating-wind model, not European HVDC quote |
| Complete spread rate, `r_spread` | HVDC | No defensible current public value found | RFI / RFI / RFI | 2026 EUR/day | Large CLV and all routinely contracted support | — | Contractor input required | Burial may be a second work package |
| Mobilisation, `C_mob` | HVDC | Public model examples 3–7 days | 3 days × spread / 7 days × spread / contractor plan | 2026 EUR/campaign | Mobilisation/demobilisation | S2 outputs; S15 | Provisional | Long international mobilisation may be much larger |
| 525 kV cable mass, `lambda` | HVDC | Indicative 65 kg/m for 2,500 mm² Cu submarine cable | Selected cable datasheet | t/physical km | One physical power cable | S17 datasheet | Supported example | Not universal; Al/conductor/design differ |
| Vessel storage, `M_gross` | HVDC | Aurora 10,000 t; Victoria 11,000 t; Leonardo 17,000 t split; Electra 13,500 t; Eleonora >23,000 t | Selected vessel usable/partitioned value | t | Gross advertised cable capacity | S7–S11 | Supported equipment facts | Gross is not usable product mass and may be split among carousels |
| Effective length/load, `L_load` | HVDC | Example: 10,000/65 ≈154 physical km gross; ≈77 system-km for two equal cables | Calculate from selected product/vessel; no fixed scenario value | physical cable-km/load | Product on one effective load | Derived from S7 & S17 | Provisional calculation | Must apply utilisation, partitions and accessory constraints |
| Continuous manufactured length | TCP infield/export | 3,000–6,000 m depending on diameter/pressure | Supplier-confirmed / supplier-confirmed / supplier-confirmed | m/continuous length | One factory length | S18 p.4 and flowline page | Supported manufacturer claim | Not necessarily one vessel load; not H2-qualified for every size |
| Generic product envelope | TCP | Up to 7.5 in ID, 689 bar, 121 °C | Named H2-qualified product required | in, bar, °C | Generic TCP flowline family | S18 | Contextual only | Maxima are not simultaneous design point or H2 qualification statement |
| Assets per pass, `g_lay` | TCP | No public evidence found for more than one pipe simultaneously | 1 / 1 / 1 | physical pipes/pass | Actual pipe lay | Search record; S18–S20 | Provisional conservative | Scenario `g>1` remains unresolved, not assumed |
| Effective production, `q_eff` | TCP | No public achieved offshore H2-TCP rate found | RFI / RFI / RFI | route-km/day/pass | Routine lay and only demonstrated burial scope | — | Supplier/contractor input required | Steel and conventional flexible rates prohibited as substitutes |
| Complete spread rate, `r_spread` | TCP | No public complete-spread rate found | RFI / RFI / RFI | 2026 EUR/day | Named MPSV/flex-lay spread and ordinary support | — | Contractor input required | Vessel class depends on pipe/reel/overboarding analysis |
| End fitting / pull-through / tie-in time | TCP | No public duration found | Separate RFI categories | h/interface | Field fitting, J-tube operation, tie-in and test | S18 shows activities, not time | Supplier/contractor input required | Likely material for short infield sections |
| Minimum bend radius and linear mass | TCP | No public project-grade H2 datasheet located | Supplier datasheet required | m; kg/m | Installation design inputs | — | Supplier input required | Cannot calculate reel/load/overboarding from public maxima |
| Mobilisation | TCP | No public value found | RFI / RFI / RFI | 2026 EUR/campaign | Selected spread | — | Contractor input required | Do not transfer cable-vessel mobilisation |
| Exceptional crossing cost, `C_cross` | All | No transferable public unit cost with consistent boundary found | Site estimate | 2026 EUR/crossing | Engineered crossing package | S4 lists preparatory/protection scope | Site-specific input required | Geometry, owner requirements and materials dominate |
| Protection unit cost, `c_protection` | All | No transferable public unit cost found | Site estimate | 2026 EUR/km or EUR/t | Mattresses, rock or other designed protection | S4 | Site-specific input required | Avoid allowance hidden in `q_eff` |
| Landfall cost, `C_landfall` | Cable/TCP export | Public project packages combine HDD/open-cut, cable/pipe and civil scope | Site estimate | 2026 EUR/landfall | Defined shore crossing and transition | S4 §5.3 | Site-specific input required | Treat shore-end pull separately if inside CLV campaign |

### 5.1 Rate evidence and boundary audit

| Reported value | Original currency / price year | Geography and method | Included | Excluded or unknown | 2026-EUR treatment | Applicability and uncertainty | Exact source |
|---|---|---|---|---|---|---|---|
| Array CLV USD 225,000/day | USD / 2023 | U.S. West Coast floating-wind model; array simultaneous lay/bury assumption | Primary CLV vessel model, crew/fuel only to the extent implicit in the model day rate | Separate support, contractor commercial terms and complete spread boundary not stated | EUR 214,882/day using CPI-U and ECB fallback | Best recent authoritative public primary-vessel proxy; high uncertainty as a European complete-spread input | S3, Appendix F Tables F6–F7, printed p. 83–84 / PDF p. 96 |
| Export CLV USD 300,000/day | USD / 2023 | U.S. West Coast floating-wind model; generic export cable | Primary CLV only | HVDC-specific bundling, burial spread, support and commercial terms not established | EUR 286,510/day using CPI-U and ECB fallback | Primary-vessel cross-check only; high market/scope uncertainty | S3, Appendix F Table F7, printed p. 84 / PDF p. 96 |
| CLV USD 140,000/day | USD / price year not explicitly stated | NREL reference offshore-wind installation study; 0.2 km/h and 4,000 t vessel assumption | Model CLV | Complete-spread inclusions not reported in the extracted table | Not normalized because source price year is unresolved | Contextual older model point, not an adopted input | S15, Table 6 |
| Array USD 100,000–160,000/day; export USD 100,000–250,000/day | USD / price year not explicitly stated; report issued 2013 | U.S. offshore-wind vessel assessment; array and export cable installation | Broad cable-vessel categories | Current spread, support, fuel and commercial boundary unresolved | Not normalized | Historical context only; vessel market and technology are stale | S25, p. 52 |
| TCP/H2 complete spread | No public value | No commercial offshore H2-TCP campaign found | — | All commercial inclusions unresolved | RFI | A numeric value would be unsupported | Unsuccessful-search record in §10.1 |

For every contractor replacement, the database should require: value/range, unit, original currency, price date, market, method, vessel and support inventory, burial/ROV/crew/fuel/overhead treatment, standby/weather rules, mobilisation treatment, exclusions, validity date and evidence owner.

## 6. Coherent scenarios

These scenarios are **method-consistent bundles**, not independent triangular distributions. Cable `q_eff` values are screening recommendations; complete spread rates remain quotations. The 5.0/3.0/0.8 km/day values are not source observations: they are auditable priors anchored to the public 1.2–12 km/day burial-tool envelope (with 4.8 km/day identified as typical). The favourable prior is near that typical operating point, the typical prior is lower, and the difficult prior is below the slowest tool rate to represent ordinary campaign losses. They must be replaced or calibrated against achieved contractor data. TCP scenarios intentionally contain unresolved commercial cells.

### 6.1 Array cable

| Input | Favourable | Typical screening | Difficult |
|---|---|---|---|
| Site/method | Homogeneous sand/silt; long simple sections; integrated plough/jet lay-bury; moderate metocean | Mixed soils; ordinary section count and pull-ins; integrated tool or tightly coordinated lay/bury | Hard/variable ground; cutter/pre-trench or separate burial; crossing/protection density high |
| `g_lay` | 1 | 1 | 1 |
| `q_eff` for integrated package | 5.0 km/d, provisional | 3.0 km/d, provisional | 0.8 km/d only if one integrated slow package remains credible; otherwise split work packages |
| Primary-vessel cross-check | €214.9k/d (2026 EUR fallback normalization) | Same | Same; separate burial spread additionally required |
| `r_spread` | Contractor quote for integrated spread | Contractor quote | Separate lay, trench/bury and possibly protection quotes |
| Mobilisation | 3 chargeable days proxy | 7 days proxy | Contractor campaign plan |
| Connection | 11 h/end proxy | 11 h/end proxy | Contractor value; do not bury repeat interventions in `q_eff` |
| Load | Mass/partition/section calculation | Same | Same, with port/route constraints |
| Scenario transition | — | More interfaces, ordinary mixed soil/weather | Tool class changes, pre-trench, many crossings, short fragmented sections or restricted seasons |

### 6.2 HVDC export

| Input | Favourable | Typical screening | Difficult |
|---|---|---|---|
| System/method | Two equal pole cables engineered as a bundle; integrated or efficient post-lay protection; few crossings | Project-specific `g=1` or `2`; separate pole campaigns may share contractor programme; ordinary landfall | Poles/return installed separately, hard ground, deep water or numerous crossings; separate burial/protection |
| `g_lay` | 2 | 1 or 2, fixed by system/vessel | 1 |
| `q_eff` | 5.0 km/d/pass provisional | 3.0 km/d/pass provisional | 0.8 km/d/pass for slow package, or split lay/bury packages |
| Primary-vessel cross-check | €286.5k/d (2026 EUR fallback normalization) | Same | Same plus separate spreads |
| `r_spread` | Current complete quote | Current complete quote | Separate CLV, burial and protection quotes |
| Mobilisation | 3-day proxy | 7-day proxy | Contractor plan, potentially multiple campaigns |
| `L_load` | Product/vessel calculation; bundled system-route capacity = physical capacity/2 | Product/vessel calculation | Partition/joint/campaign constrained |
| Joint/reload | 48 h inline-joint proxy plus actual port turnaround | Same | Technology-specific joint and restricted-port plan |
| Scenario transition | — | Separate poles, capacity-triggered reload/joint, average burial | Metallic return adds a pass; route exceeds load; tool/vessel class or landfall changes |

### 6.3 TCP hydrogen infield

| Input | Favourable | Typical screening | Difficult |
|---|---|---|---|
| Site/method | Named H2-qualified product; each line fits one or few factory lengths; horizontal lay from small MPSV; simple J-tubes; stable/buried by demonstrated method | Multiple reels and end fittings; ordinary J-tube pull-through; burial or weight/stability system | Qualification extension, tight bend/pull limits, many connectors, difficult burial/protection or larger vessel |
| `g_lay` | 1 | 1 | 1 |
| Continuous length | 3–6 km manufacturer envelope, subject to selected product | Supplier value | Supplier value; may force many joints |
| `q_eff` | RFI | RFI | RFI; change class if installation analysis fails |
| `r_spread`, mobilisation | RFI | RFI | RFI |
| Connections | Count J-tube pull-through, each field end fitting, tie-in and test separately; duration RFI | Same | Same plus intermediate connectors |
| Scenario transition | — | Reel/connector and stability requirements | Product qualification or installation limit exceeded |

### 6.4 TCP hydrogen export

| Input | Favourable concept | Typical concept | Difficult / stop gate |
|---|---|---|---|
| Preconditions | Named product, route and installation concept fully qualified; direct sea access/factory spooling or manageable repeated reels | Multiple factory lengths/reels with validated field connector and integrity plan | No qualified size/pressure/length or credible connector/lay concept |
| `g_lay` | 1 unless contractor proves otherwise | 1 | Not applicable |
| `q_eff`, spread, mobilisation, connections | All RFI | All RFI | Do not calculate |
| Status | Parameterizable after RFI | Parameterizable after front-end engineering | Different technology or installation class required |

## 7. Constant-2026-EUR normalization

### 7.1 Preferred method

Escalate in the source currency first, then convert using a consistent 2026 exchange-rate convention:

\[
C_{2026,EUR}=C_{y,s}\frac{I_{s,k}(2026^*)}{I_{s,k}(y)}FX_{EUR/s}(2026^*)G_{market}
\]

where:

- `C_y,s` is the source value in currency `s` and source price year `y`;
- `I_s,k` is the index for cost type `k` in the source market;
- `2026*` is the latest available 2026 month or a documented year-to-date average;
- `FX_EUR/s` is EUR per unit of source currency;
- `G_market` is a separate, explicit geographic-market factor.

If the ECB quote is units of source currency per EUR, use its reciprocal. Never apply a source-year FX conversion and a 2026 FX conversion to the same value.

### 7.2 Index hierarchy

1. Contract-specific escalation formula or an agreed offshore vessel/construction index.
2. Relevant producer/service price index, such as sea transport or construction services, if its coverage matches.
3. General CPI/HICP only as a transparent fallback.

General inflation does not capture cable-vessel scarcity, fuel, charter-cycle or regional content requirements. Geographic difference is not inflation and remains `G_market`; default it to 1 only for a same-market comparison or label it unresolved.

### 7.3 Reproduced normalization of the NREL rate proxy

NREL Table F7 reports `$225,000/day` for an array CLV and `$300,000/day` for an export CLV; the report states costs in 2023 dollars. The fallback calculation uses U.S. CPI-U 304.702 (2023 annual average), CPI-U 333.952 (June 2026), and ECB 30 July 2026 rate `1 EUR = 1.1476 USD`:

\[
F=\frac{333.952}{304.702}\frac{1}{1.1476}=0.9550326\;EUR_{2026}/USD_{2023}
\]

Thus:

- array CLV: `225,000 × F = EUR 214,882/day`;
- export CLV: `300,000 × F = EUR 286,510/day`.

These are 2026-EUR **fallback-normalized model proxies**, not observed 2026 market quotations. The 2026 year is incomplete as of the access date, the exchange rate is spot rather than a full-year average, CPI-U is not vessel-specific, and the source is a U.S. model. Retain the original value, source year, index values, FX date and all caveats in the model audit trail.

## 8. Implementation logic

```text
function installation_cost(project, scenario):
    validate project.installation_class
    class_data = select_class(project.installation_class)
    method = select_method(class_data, project.design, scenario)

    # Physical inventory
    for section in project.sections:
        section.physical_length = section.count * (
            section.route_length * (1 + section.slack_fraction)
            + section.vertical_allowance
        )
    total_physical_length = sum(section.physical_length)

    # Work packages: e.g., integrated lay/bury OR separate lay + burial
    campaigns = build_campaigns(method)
    assert no asset/activity is charged in more than one campaign unless repeated physically

    for campaign in campaigns:
        pass_groups = group_assets_for_real_simultaneous_installation(
            campaign.assets, campaign.assets_per_pass
        )
        campaign.pass_count = count(pass_groups)
        campaign.pass_length = sum(actual_traversed_length(group) for group in pass_groups)

        campaign.loaded_physical_length = sum(product_length_loaded_by(campaign))
        campaign.length_per_load = min(
            usable_mass / product_linear_mass,
            reel_or_partition_limit,
            manufacturing_limit,
            handling_limit
        )
        campaign.load_count = ceil(
            campaign.loaded_physical_length / campaign.length_per_load
        )
        campaign.reload_count = max(0, campaign.load_count - 1)

        campaign.route_days = sum(
            pass.length / scenario.q_eff[campaign.method] for pass in pass_groups
        )
        campaign.connection_days = sum(
            connection.count * scenario.connection_time[connection.type]
            for connection in campaign.blocking_connections
        ) / 24
        campaign.joint_days = sum(
            joint.count * scenario.joint_time[joint.type] for joint in campaign.joints
        ) / 24
        campaign.initial_load_days = (
            scenario.initial_load_time_days if campaign.initial_load_is_spread_charged
            else 0
        )
        campaign.reload_days = campaign.reload_count * (
            2 * campaign.port_distance / campaign.transit_speed / 24
            + scenario.port_load_time_days
            + scenario.reload_reposition_days
        )
        campaign.chargeable_days = (
            scenario.fixed_days[campaign]
            + campaign.route_days
            + campaign.connection_days
            + campaign.joint_days
            + campaign.initial_load_days
            + campaign.reload_days
        )
        campaign.cost = (
            scenario.mobilisation_cost[campaign]
            + scenario.complete_spread_rate[campaign] * campaign.chargeable_days
        )

    unit_completion_cost = sum(item.count * item.unit_cost for item in nonblocking_items)
    exceptional_cost = (
        crossings.count * crossing_unit_cost
        + protection.length * protection_unit_cost
        + landfalls.count * landfall_unit_cost
        + other_exceptional_cost
    )

    if any required parameter has evidence status RFI or unresolved:
        return "NOT PARAMETERIZED", intermediate_results, missing_inputs

    return sum(campaign.cost) + unit_completion_cost + exceptional_cost,
           intermediate_results,
           evidence_register
```

### 8.1 Required model assertions

- `physical_length >= route_length` for one asset and increases with every parallel asset.
- `g >= 1` and `g` is supported by the selected vessel/system, not inherited from another class.
- burial appears either in integrated `q_eff` or in a separate package.
- every connection is either spread-blocking time or separately priced, not both.
- initial load is not counted as a reload.
- every numerical cost has currency, price year and normalization record.
- missing required TCP inputs return `NOT PARAMETERIZED`, not zero.

## 9. Validation cases

Benchmarks test scale, counting and boundary; they do not set the parameters.

| Case | Technology and physical quantities | Public cost scope / year | Material mismatch | Model output tested |
|---|---|---|---|---|
| ORBIT published example | Array sections and six 38.0 km export cables in worked output; array and export installation cost breakdowns | Model output, current ORBIT library assumptions | Discrete-event weather/logistics; illustrative design; not 66 kV/HVDC contract | Reproduce section, load, interface and campaign logic before simplifying |
| Hornsea 2 | 165 inter-array sections, about 382 km of 66 kV cable | No public exact installation price | T&I project data only | Section/end count and physical-km scaling |
| Hornsea 3 | 192 inter-array sections, about 500 km of 66 kV cable | Contract described qualitatively, not exact value | Full T&I scope | Section and connection discontinuities |
| Dogger Bank | About 650 km of 66 kV inter-array cable | EPCI supply, install and protection; no separated install price | Manufacture/protection included | Physical-km and campaign-scale plausibility |
| Gennaker | About 140 km, 63 turbines, 66 kV; complete inter-array system | Boskalis “sizable,” its published category is EUR 50–150m; announced 2026 | Supply, installation and broad system scope; category not exact price | Model total should remain below broad package unless its boundary is intentionally widened |
| Shetland HVDC | 253 km offshore route; 506 km offshore physical cable; two poles; three cable-laying campaigns; 320 kV, 600 MW | NKT turnkey order EUR 235m, 2020 | Supply, protection, onshore cable and accessories included | Route-vs-physical counting, pass/campaign and reload logic—not installation €/km |
| East Anglia THREE | 2×147 km offshore plus 2×37 km onshore; 320 kV, 1.4 GW | NKT reference, no separated public installation cost | System supply/project scope | Two-pole physical length and connection count |
| Caithness–Moray | About 160 km transmission length; bundled 320 kV HVDC plus fibre | No separated installation price | Owner/contractor reference only | `g=2` bundled physical feasibility |
| Ariadne | Two HVDC cables, each 335 km; lay completions in separate months/campaigns | Whole interconnector investment about EUR 1.2bn | Converter stations, civil works and entire project included | Separate pole campaigns and shared-vs-separate mobilisation scenarios |
| 2 GW Dutch framework examples | Two 525 kV poles plus metallic return per link | Multi-project EPCI packages around EUR 1–1.8bn depending award | Manufacture, onshore/offshore install, civil, accessories and commissioning | Three physical cable accounting and `g` threshold |
| Strohm SASBU analogue | 4 km TCP, 7.1 in ID, 159 bar, two T&I reels, two J-tubes, small MPSV | No public rate, duration or price; O&G service | Not hydrogen; short field flowline | TCP section/reel, J-tube and end-interface inventory only |
| HOPE demonstrator | 10 MW offshore H2 demonstrator concept with TCP to shore | Whole project EUR 40.287m, 2023–2028 | Demonstrator-wide cost; pipeline not yet a commercial installed benchmark | Readiness/qualification gate only; not cost validation |

### 9.1 Validation acceptance checks

1. A 100 km bipole with `g=1` reports 200 physical cable-km and 200 pass-km; with a verified `g=2`, it reports 200 physical cable-km but 100 pass-km.
2. Adding a metallic return changes the physical count from two to three and can create a new pass or reduce system-route load capacity.
3. Crossing a load threshold adds exactly one reload and, when applicable, one joint—creating a visible cost step.
4. Adding an array section adds two cable ends even if total route length barely changes.
5. Switching from integrated to separate burial creates another work package and does not leave burial inside the lay `q_eff`.

## 10. Research gaps, unsuccessful searches and RFI

### 10.1 Unsuccessful or inconclusive searches

No defensible public source was found for:

- a current European **complete** inter-array or HVDC installation-spread day rate with inclusions;
- an achieved, weather-inclusive HVDC route production rate tied to a stated cable configuration and burial method;
- offshore H2-TCP achieved installation production, spread rate, mobilisation, connection duration or effective load capacity;
- simultaneous installation of more than one TCP pipeline per pass;
- project-grade H2-TCP linear mass and minimum bend radius over a useful diameter/pressure matrix;
- a commercial long-distance offshore hydrogen TCP export installation;
- transferable unit costs for crossings, mattresses, rock placement or landfalls with a consistent boundary.

Searches did find mechanical payout/tool speeds, broad turnkey contracts, vessel specifications, manufacturer claims and steel/flexible-pipeline analogues. Those were retained as contextual evidence and were not silently converted into missing inputs.

### 10.2 Cable installation contractor / CLV owner RFI

For each of array cable and HVDC, request one favourable, one expected and one difficult method case:

1. What is the 2026 EUR/day complete spread rate? List primary vessel, burial tool, ROV, survey, support vessels, crew, fuel, ordinary consumables and contractor overhead separately as included/excluded—not as additive prices unless excluded.
2. What achieved route-km/day does the contractor recommend for the stated product, water depth, soil/burial class and season? Define weather, routine survey, positioning and minor interruption treatment.
3. Is lay and burial simultaneous, separate within one campaign, or separate campaigns? How many burial passes are required for bundled cables?
4. How many physical cables are carried and actually laid simultaneously? Distinguish two-pole bundle, fibre, metallic return and dual-lane deck preparation.
5. What mobilisation/demobilisation amount or days are chargeable, and which port/transits are included?
6. What usable cable mass and effective physical cable-km can be loaded for each product? Identify carousel partitions, accessory space and utilisation limits.
7. What is the port reload turnaround, including return transit, load, test and repositioning?
8. What pull-in, hang-off, termination/test and inline-joint durations block the primary spread? Which tasks occur later under a different team/rate?
9. Which crossings, pre-sweeping, pre-trenching, landfall, mattress, rock and post-lay survey scopes are excluded?
10. Provide the quote validity, geography, fuel/indexation mechanism, weather standby rules and cancellation/standby rates.

### 10.3 TCP manufacturer RFI

1. Provide the H2-qualified product matrix: ID/OD, design pressure, temperature, design life, permeation basis and DNV/API qualification status.
2. For each product, provide dry/submerged/weighted linear mass, axial stiffness, collapse capacity, minimum storage/installation bend radii and allowable installation tension.
3. What continuous factory length and reel/carousel load are available? Is 3–6 km a product length, reel length or typical shipment length?
4. Provide reel dimensions/mass, number of reels transferable to candidate vessels, spooling limits and factory/port loading concept.
5. Define field end-fitting and intermediate connection designs, installation time, tooling, personnel, test requirements and whether connection can be made offshore on the lay vessel.
6. Provide J-tube pull-through limits, bend/pull analysis requirements and demonstrated cases relevant to H2.
7. Define integrated weight coating, burial and other on-bottom-stability options and their effect on mass, bend radius and installation method.
8. State whether two lines can be carried or laid simultaneously and identify the demonstrated equipment/configuration.

### 10.4 Subsea pipeline installation contractor RFI

1. Name the vessel/spread proposed for each TCP product and water depth; give complete 2026 EUR/day rate and inclusions.
2. Give achieved effective km/day for horizontal lay, vertical/flex lay and any simultaneous burial option; separate payout speed from campaign progress.
3. Give mobilisation/demobilisation, engineering and equipment-installation charges/days.
4. Give reel exchange, port reload and offshore reel-change durations and capacity per load.
5. Give duration by connection type: J-tube pull, end fitting, manifold/topside tie-in, intermediate connector and pressure test.
6. State assets per actual lay pass and whether supporting evidence is a demonstration, commercial O&G project or H2-qualified project.
7. Identify stability, burial, crossing, route-clearance, survey and commissioning inclusions/exclusions.
8. Identify feasibility triggers that require a larger vessel, vertical lay, tow method or a different pipe technology.

## 11. Calculation-led documentation-page outline

One consolidated **Cable and Pipeline Installation** page should use this order:

1. Why installation cost is required and which design comparisons it must respond to.
2. Cost boundary and explicit exclusions.
3. Accounting units, with a visual example distinguishing 100 route-km from 200 physical cable-km.
4. Inputs grouped as design, method, scenario and economic basis; show evidence labels.
5. Common work-package/campaign equation.
6. Four class cards: method, spread, included `q_eff` activities, separate activities, limits and class-change triggers.
7. Dependency-ordered calculation: physical inventory → pass groups → load/reload → route time → interfaces/joints → campaign duration → spread cost → exceptional work → total.
8. Intermediate-results table, never only total EUR or EUR/km.
9. Coherent favourable/typical/difficult scenarios and conditions that change scenario.
10. Currency normalization audit trail.
11. Validation benchmarks with scope-mismatch column.
12. Limitations, unresolved inputs, RFI status and last evidence review date.

Visually distinguish **user inputs**, **sourced assumptions**, **provisional screening recommendations**, **derived quantities**, and **blocked/RFI values**.

## 12. Quality-control checklist

- [x] Route length and physical asset length are separate.
- [x] Shared mobilisation and simultaneous lay are separate concepts.
- [x] Vessel-only rate proxies are not called complete spread rates.
- [x] Integrated and separate burial methods cannot be charged simultaneously.
- [x] `q_eff` boundary is explicit.
- [x] Pass, connection, load/reload and joint discontinuities are preserved.
- [x] Exceptional work is outside routine production.
- [x] TCP values are not transferred from steel or conventional flexible pipe.
- [x] Every normalized value retains source currency/year, index and FX convention.
- [x] Unsupported parameters remain RFI/site-specific and stop the cost calculation.

## 13. Source register

All links were accessed 31 July 2026. Page numbers below refer to the PDF page label where clear; `PDF p.` gives the viewer page when the printed label differs.

**S1 — NREL ORBIT technical report.** Nunemaker et al. (2020), *ORBIT: Offshore Renewables Balance-of-System and Installation Tool*, NREL/TP-5000-77081. Section 3.4, pp. 29–32; Tables 7–8, p. 30; Section 3.5, pp. 32–33. Burial 50–500 m/h, typical 200 m/h; port load 6 h; pull-in 5.5 h; terminate 5.5 h; splice 48 h; lay 1 km/h; simultaneous lay/bury 0.3 km/h; pre-trench 0.1 km/h; bury 0.5 km/h. https://www.nrel.gov/docs/fy20osti/77081.pdf

**S2 — Current ORBIT documentation/code methodology.** *Array Cabling System Installation Methodology*, process and defaults tables; *Cable Laying and Burying* guide; *Available Outputs* example; *Introduction* vessel schema; changelog entry noting vessel-rate update to 2024 USD. https://nlrwindsystems.github.io/ORBIT/methods/install/ArrayCableInstall.html ; https://nlrwindsystems.github.io/ORBIT/topical_guides/cable_installation.html ; https://nlrwindsystems.github.io/ORBIT/tutorials/available_outputs.html ; https://nlrwindsystems.github.io/ORBIT/tutorials/introduction.html ; https://nlrwindsystems.github.io/ORBIT/about/changelog.html

**S3 — NREL floating-wind port network report.** *The Impacts of Developing a Port Network for Floating Offshore Wind Energy on the West Coast of the United States* (2023), Appendix F, Table F6 and Table F7, printed pp. 83–84 / PDF p. 96. Array CLV USD 225,000/day; export CLV USD 300,000/day; each 13,000 t storage; array lay/bury 0.4 km/h. Report states costs in 2023 dollars. https://docs.nrel.gov/docs/fy23osti/86864.pdf

**S4 — BOEM/BSEE cable spacing guidance.** *Offshore Wind Submarine Cable Spacing Guidance* (2014), Section 5.3, pp. 35–37. Bundled synchronous versus separate HVDC installation, separate passes, post-lay burial, vessel/load/joint constraints, route preparation and protection/landfall scope. https://www.boem.gov/sites/default/files/renewable-energy-program/Studies/TAP/722AA.pdf

**S5 — East Anglia TWO project description.** Environmental Statement Chapter 6, Table 6.14. Indicative plough 300 m/h, jetting 300 m/h, trenching 30–80 m/h and vertical injector 30–80 m/h. https://nsip-documents.planninginspectorate.gov.uk/published-documents/EN010078-001107-6.1.6%20EA2%20Environmental%20Statement%20Chapter%2006%20Project%20Description.pdf

**S6 — Thor Offshore Wind Farm environmental material.** Table 7.1: 66 kV, 240–1,000 mm² Al, about 120–195 mm diameter and 20–50 kg/m; total array-cable length about 205 km for 72 turbines; purpose-built CLV and support vessel. https://www.eib.org/attachments/registers/213994748.pdf

**S7 — Nexans Aurora.** Manufacturer vessel page: 10,000 t split turntable; two lay lines and bundling capability. https://www.nexans.com/electrification-solutions/markets/transmission/cable-laying-vessel-nexans-aurora/

**S8 — NKT Victoria.** Manufacturer vessel page: approximately 11,000 t cable carrying capacity and bundled-lay capability. https://www.nkt.com/products-solutions/high-voltage-cable-solutions/nkt-victoria

**S9 — Prysmian Leonardo da Vinci.** Manufacturer page: 7,000 t and 10,000 t carousels, bundled lay and simultaneous lay/bury capability. https://www.prysmian.com/en/new-vessel-leonardo-da-vinci

**S10 — Nexans Electra.** Manufacturer page, 2026: three turntables totalling 13,500 t and up to four cables installed simultaneously. https://www.nexans.com/electrification-solutions/markets/transmission/cable-laying-vessel-nexans-electra/

**S11 — NKT Eleonora.** Manufacturer page: more than 23,000 t and three-power-cable capacity, relevant to 525 kV systems with metallic return. Treat as emerging fleet capability, not default. https://www.nkt.com/products-solutions/high-voltage-cable-solutions/nkt-eleonora

**S12 — ECB exchange-rate methodology and reference rate.** Euro base-currency quote; 30 July 2026: 1 EUR = 1.1476 USD and 0.85715 GBP. https://data.ecb.europa.eu/methodology/exchange-rates ; https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html

**S13 — U.S. Bureau of Labor Statistics CPI-U.** 2023 annual average CPI-U 304.702; June 2026 unadjusted CPI-U 333.952. https://www.bls.gov/cpi/tables/supplemental-files/historical-cpi-u-202312.pdf ; https://www.bls.gov/news.release/archives/cpi_07142026.htm

**S14 — Eurostat HICP.** Official HICP indexing/data documentation; monthly and annual indices and 2026 re-reference information. Appropriate general euro fallback, not a vessel-market index. https://ec.europa.eu/eurostat/web/hicp/information-data ; https://ec.europa.eu/eurostat/web/hicp/methodology

**S15 — NREL Applied Energy study.** Shields et al. (2021), Table 6: cable-lay vessel 0.2 km/h, 4,000 t cargo, seven-day mobilisation and USD 140,000/day in the study assumptions. Contextual older proxy. https://docs.nrel.gov/docs/fy21osti/78126.pdf

**S16 — Danish Energy Agency technology catalogue.** Table 5.2 contextual cable weights: 66 kV 50–70 t/km; 132 kV 125 t/km. https://ens.dk/media/3859/download

**S17 — Prysmian 525 kV XLPE submarine cable datasheet.** Indicative 2,500 mm² copper design: about 160 mm diameter and 65 kg/m. https://www.prysmian.com/staticres/525-kv-hvdc-new-cable-systems/documents/XLPE-DATASHEET---Submarine.pdf

**S18 — Strohm TCP flowline sources.** Product/installation page and 2024 brochure, especially brochure pp. 4 and 10–11: horizontal lay, small MPSV, 3,000–6,000 m continuous lengths, field end fittings and J-tube pull-through; generic envelope up to 7.5 in ID, 121 °C and 689 bar. Manufacturer evidence. https://strohm.eu/tcp-flowlines ; https://cdn.bluenotion.nl/069cc4293e4752d887c9d3ab16d173768843b4e22ee7b4ac8db49f676b51c4fc.pdf

**S19 — Strohm SASBU case.** 4 km, 7.1 in ID, 159 bar flowline; two T&I reels; small multipurpose vessel; J-tubes at both ends. O&G analogue, no public time or cost. https://strohm.eu/project-case-sasbu-tcp-flowline

**S20 — DNV TCP standard and H2 JIP.** DNV-ST-F119 (2019, amended 2021) and *Non-metallic composite pipes for transportation of H2* JIP page. The JIP identifies H2 gaps relative to existing DNV-ST-F119/API 15S coverage. https://www.dnv.com/energy/standards-guidelines/dnv-st-f119-thermoplastic-composite-pipes/ ; https://www.dnv.com/group/joint-industry-projects/non-metallic-composite-pipes-for-transportation-of-h2/

**S21 — HOPE project.** EU CORDIS project record and latest reporting: 2023–2028 offshore H2 demonstrator, total project cost EUR 40.287 million; reporting through May 2025 describes pipeline permitting and demonstration planning rather than a commercial installed TCP export benchmark. https://cordis.europa.eu/project/id/101111899 ; https://cordis.europa.eu/project/id/101111899/reporting

**S22 — HVDC bundled/separate validation references.** Hansa PowerBridge RFI: two HVDC submarine cables plus bundled fibre; NKT Caithness–Moray: bundled 320 kV cables; Ariadne project: two 335 km cables completed separately. https://www.svk.se/en/grid-development/grid-projects/hansa-powerbridge/news/hansa-powerbridge-is-proceeding-via-a-request-for-information-rfi-for-the-stations-and-cables/ ; https://www.nkt.com/news-press-releases/nkt-completes-the-hvdc-power-cable-system-for-scottish-caithness-moray-link-supporting-transition-to-a-low-carbon-economy ; https://www.ariadne-interconnection.gr/en

**S23 — Shetland HVDC.** NKT reference: 253 km offshore route, 506 km offshore physical cable, 320 kV, 600 MW and three cable-laying campaigns. NKT order release: EUR 235 million turnkey supply and installation/protection scope in 2020. https://www.nkt.com/references/shetland-hvdc-link-uk ; https://www.nkt.de/presse-events/nkt-er-tildelt-turnkey-ordre-til-on-og-offshore-projektet-shetland-hvdc-link

**S24 — Array validation references.** Seaway7 Hornsea zone/reference and Hornsea 3 award; Dogger Bank owner release; Boskalis Gennaker release. https://www.seaway7.com/projects/hornsea-offshore-wind-zone/ ; https://www.seaway7.com/seaway7-awarded-offshore-wind-contract-in-uk/ ; https://doggerbank.com/press-releases/deme-offshore-signs-contract-for-largest-ever-inter-array-cable-order-with-dogger-bank-wind-farm/ ; https://ml-eu.globenewswire.com/Resource/Download/b974cb84-807d-43b7-900e-b94b90074ef0

**S25 — DOE/Douglas-Westwood vessel assessment.** *Assessment of Vessel Requirements for the U.S. Offshore Wind Sector* (2013), p. 52. Historical array-cable vessel USD 100,000–160,000/day and export-cable vessel USD 100,000–250,000/day; the price basis and complete-spread boundary are not explicit, so values are contextual only. https://www.energy.gov/sites/prod/files/2013/12/f5/assessment_vessel_requirements_US_offshore_wind_report.pdf

## Final use recommendation

Implement the model now with hard evidence flags. Permit cable sensitivity calculations using the provisional `q_eff` scenarios and clearly labelled primary-vessel cross-checks, but show a commercial-input warning until a complete-spread rate is supplied. Keep both TCP classes in the same code path and reporting system, but make missing product/spread inputs a blocking validation error. This preserves transparency and allows the model to mature without rewriting its accounting logic when contractor data arrive.
