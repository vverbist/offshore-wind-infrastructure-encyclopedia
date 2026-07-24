# HVDC transmission CAPEX

## Linear screening model for complete point-to-point cable links

## 1. Purpose and headline model

This note provides an early-stage CAPEX model for a complete point-to-point HVDC connection between two existing HVAC grids. The model is intended for links of approximately **0.5–2 GW**, with its strongest calibration around **1 GW**.

All costs are:

* In constant **2026 euros**
* Upfront investment CAPEX
* Excluding financing and interest during construction
* Excluding OPEX, losses and decommissioning
* Excluding wider reinforcement of the connected AC grids
* Excluding VAT

The recommended central model is:

[
\boxed{
C_{\mathrm{HVDC}}
=================

P
\left[
K_T
+
2.94L_s
+
3.72L_u
\right]
+
C_{\mathrm{special}}
}
]

where:

* (C_{\mathrm{HVDC}}) = total CAPEX in euros
* (P) = rated transmission capacity in kW
* (L_s) = subsea cable route length in km
* (L_u) = underground onshore cable route length in km
* (K_T) = terminal-station cost in €/kW
* (C_{\mathrm{special}}) = separately estimated major or unusual civil works

The equivalent unit-cost expression is:

[
\boxed{
\frac{C_{\mathrm{HVDC}}}{P}
===========================

K_T
+
2.94L_s
+
3.72L_u
+
\frac{C_{\mathrm{special}}}{P}
\qquad [€/kW]
}
]

The terminal coefficient depends on where the converters are located:

| Configuration                                  |   Central (K_T) |   Planning range |
| ---------------------------------------------- | --------------: | ---------------: |
| Two onshore converter stations                 |     **€915/kW** |    €640–1,190/kW |
| One onshore and one offshore converter station |   **€1,530/kW** |  €1,070–1,990/kW |
| Two offshore converter stations                |   **€2,140/kW** |  €1,500–2,780/kW |
| Installed subsea cable route                   | **€2.94/kW/km** | €2.06–3.82/kW/km |
| Installed underground cable route              | **€3.72/kW/km** | €2.60–4.84/kW/km |

All central coefficients already include a **13% residual project allowance** for costs not fully represented by the main converter and cable packages. The low and high values are calculated as 70% and 130% of the central values.

The two-offshore-converter value has lower confidence than the other terminal configurations: it is constructed by adding two offshore-station unit costs rather than calibrated against a complete offshore-to-offshore project.

---

## 2. Cost boundary

### Included

The terminal-station coefficients cover:

* Converter transformers
* Converter valves and associated power electronics
* Immediate AC switchgear and busbars
* DC-side equipment
* Harmonic filters, reactors and ancillary plant
* Control, protection, cooling and auxiliary systems
* Converter halls and other station buildings
* Foundations and ordinary local station civil works
* Installation, testing and commissioning
* Offshore platform and foundation where the converter is offshore

The Danish Energy Agency defines an HVDC station as including the converter, converter transformers, AC switchgear and busbars, harmonic filters, lightning towers and ancillary plant. Transformers are therefore already included and must not be added separately. 

The cable coefficients cover the complete operating cable system per route kilometre, rather than one individual conductor. They include:

* Cable manufacture and supply
* Joints and terminations
* Ordinary marine laying or terrestrial installation
* Burial, trenching and normal mechanical protection
* Jointing, testing and commissioning
* Ordinary reinstatement and route works included in the turnkey cable package

### Excluded or separately estimated

The following are not included in the standard coefficients:

* Wider reinforcement of either connected HVAC grid
* Major tunnels
* Exceptional horizontal directional drilling
* Extensive rock placement
* Unusually difficult river, shipping-channel, cable or pipeline crossings
* Exceptional urban construction or rock excavation
* Full duplication for independent N-1 transfer capability
* Financing, interest during construction, OPEX and losses

These exceptional items are represented by (C_{\mathrm{special}}). No generic allowance is assigned because their cost is highly site-specific.

There is also no separate generic landfall coefficient. Publicly disclosed contracts generally do not isolate ordinary landfall works from the cable installation package. Ordinary landfalls are therefore assumed to be represented within the installed cable coefficient and the 13% residual allowance. A landfall requiring a major tunnel or unusually long directional drill belongs in (C_{\mathrm{special}}).

---

## 3. Price basis

The source values have been converted to constant 2026 euros using the euro-area Harmonised Index of Consumer Prices as a transparent general-price proxy.

Eurostat’s annual-average HICP index, rebased to 2025 = 100, gives:

* 2020: 81.53
* 2023: 95.64
* 2025: 100.00

The European Commission’s Spring 2026 forecast gives euro-area inflation of 3.0% for 2026. Because the complete 2026 annual index is not yet available, this forecast is used to move from 2025 to the 2026 price basis. ([European Commission][1])

The conversion factors are therefore:

[
F_{2020\rightarrow2026}
=======================

# \frac{100}{81.53}\times1.03

1.263
]

[
F_{2023\rightarrow2026}
=======================

# \frac{100}{95.64}\times1.03

1.077
]

[
F_{2025\rightarrow2026}
=======================

1.03
]

HICP is a general consumer-price index, not an HVDC equipment or construction index. It standardises the price year but does not specifically capture cable-factory utilisation, installation-vessel rates, copper, aluminium, steel or contractor margins. This is one reason for retaining a broad planning range.

---

## 4. Converter-station derivation

### 4.1 Source values

The Danish Energy Agency gives the following 2025 planning costs, stated at the 2020 price level, for stations in the 1.5–2 GW range:

* Onshore HVDC converter station: **€0.32 million/MW**
* Offshore HVDC converter station including platform: **€0.75 million/MW**

The catalogue states that its 2025 values include a 20% real market uplift over the underlying source values, reflecting higher material costs and supply-chain bottlenecks. 

### 4.2 Conversion to 2026 euros

For one onshore station:

[
0.32\times1.263
===============

0.404\text{ million €/MW}
]

Since €1 million/MW is numerically €1,000/kW:

[
0.404\text{ million €/MW}
=========================

€404/kW
]

For one offshore station including its platform:

[
0.75\times1.263
===============

# 0.948\text{ million €/MW}

€948/kW
]

### 4.3 Combining the terminal stations

| Terminal arrangement       |  Calculation | Direct package cost |
| -------------------------- | -----------: | ------------------: |
| Two onshore                | (2\times404) |             €809/kW |
| One onshore + one offshore |    (404+948) |           €1,352/kW |
| Two offshore               | (2\times948) |           €1,895/kW |

Applying the 13% residual project allowance derived in Section 6 gives:

| Terminal arrangement       |       Calculation |                Adopted all-in value |
| -------------------------- | ----------------: | ----------------------------------: |
| Two onshore                |   (809\times1.13) |     €914/kW, rounded to **€915/kW** |
| One onshore + one offshore | (1,352\times1.13) | €1,528/kW, rounded to **€1,530/kW** |
| Two offshore               | (1,895\times1.13) | €2,141/kW, rounded to **€2,140/kW** |

The offshore premium for replacing one onshore station with one offshore station is therefore:

[
1{,}530-915
===========

\boxed{€615/kW}
]

This premium includes the offshore platform and foundation because these are included in the Danish Energy Agency’s offshore-station source value.

---

## 5. Cable-cost derivation

### 5.1 Direct project anchor

The principal cable anchor is the Adriatic Link contract awarded in 2023:

* Contract value: **€630 million**
* Capacity: **1,000 MW**
* Total route: **250 km**
* Subsea route: **210 km**
* Underground route: **40 km**
* Scope: design, supply, installation and commissioning of the complete bipolar HVDC cable link

The contract is therefore an installed cable-system value, not a cable-material-only price. ([Prysmian Corporate][2])

The average mixed-route cost is:

[
\frac{€630\text{ million}}{250\text{ km}}
=========================================

€2.520\text{ million/km}
]

At 1 GW, this is numerically:

[
€2.520\text{ million/km}
========================

€2.520/kW/km
]

However, the route contains both subsea and underground sections, so the two must be separated.

### 5.2 Subsea-to-underground relationship

The Danish Energy Agency gives central costs of:

* DC subsea cable: **€3.22 thousand/MW/km**
* DC underground cable: **€4.07 thousand/MW/km**

Both values apply to systems in the 1.5–2 GW range and use the same methodology and price basis. Their ratio is:

[
r_{\mathrm{underground/sea}}
============================

# \frac{4.07}{3.22}

1.264
]

Thus, the model assumes that underground cable costs 1.264 times the equivalent subsea cable cost. 

Let (S_{2023}) be the pure subsea route rate in € million/km. The Adriatic Link mixed-route cost then satisfies:

[
2.520
=====

S_{2023}
\left[
\frac{210}{250}
+
1.264\frac{40}{250}
\right]
]

Solving gives:

[
S_{2023}
========

€2.418\text{ million/km}
]

Converting the 2023 contract price to 2026 euros:

[
2.418\times1.077
================

€2.604\text{ million/km}
]

At the project’s 1 GW rating:

[
€2.604\text{ million/km}
========================

€2.604/kW/km
]

The corresponding underground route cost is:

[
2.604\times1.264
================

€3.291/kW/km
]

These are direct installed-package values before the residual project allowance.

### 5.3 Adopted all-in cable coefficients

Applying the 13% residual allowance:

[
2.604\times1.13
===============

2.942
]

[
3.291\times1.13
===============

3.719
]

The adopted central values are therefore:

[
\boxed{
K_{\mathrm{subsea}}
===================

€2.94/kW/km
}
]

[
\boxed{
K_{\mathrm{underground}}
========================

€3.72/kW/km
}
]

The underground coefficient is:

[
\frac{3.72}{2.94}-1
===================

26.4%
]

above the subsea coefficient. Expressed the other way around, the subsea coefficient is approximately:

[
1-\frac{2.94}{3.72}
===================

20.9%
]

below the underground coefficient.

This relationship applies to an ordinary installed route. It does not mean every offshore route will be cheaper: deep water, hard seabed, dense cable crossings, rock placement or difficult landfalls can reverse the difference.

---

## 6. Derivation of the 13% residual project allowance

Converter-station and cable contracts do not necessarily include all owner-side, development and project-wide costs. A residual allowance is calibrated against the publicly stated total investment cost of Adriatic Link.

The European Investment Bank gives an approximate 2025 total project cost of:

[
€1.634\text{ billion}
]

Converted to the 2026 price basis:

[
1.634\times1.03
===============

€1.683\text{ billion}
]

([European Investment Bank][3])

The two main direct packages are estimated as follows.

Two onshore converter stations:

[
€809\text{ million}
]

The 2023 cable contract converted to 2026 euros:

[
630\times1.077
==============

€678\text{ million}
]

Direct-package subtotal:

[
809+678
=======

€1.487\text{ billion}
]

The ratio of total project cost to the estimated direct-package subtotal is:

[
\frac{1.683}{1.487}
===================

1.132
]

This is rounded to:

[
\boxed{1.13}
]

The resulting **13% residual project allowance** is therefore a derived calibration assumption, not a separately disclosed Adriatic Link cost category.

It may represent a combination of:

* Owner’s engineering
* Development and project management
* Remaining local works
* Surveys and consenting
* Ordinary interfaces and landfall works
* Project contingency
* Differences between the generic converter benchmark and the actual project scope

Because it is a residual, it should not be interpreted as exactly 13% owner’s cost or exactly 13% contingency. It is an all-purpose uplift that reconciles the principal packages with a current total-project benchmark.

---

## 7. Low and high planning cases

The Danish Energy Agency applies a **minus/plus 30%** uncertainty range to its cable and converter-station planning values. The same convention is adopted here. 

Thus:

[
C_{\mathrm{low}}
================

0.70C_{\mathrm{central}}
]

[
C_{\mathrm{high}}
=================

1.30C_{\mathrm{central}}
]

This produces:

| Cost element                        |         Low |     Central |        High |
| ----------------------------------- | ----------: | ----------: | ----------: |
| Two onshore terminals               |     €640/kW |     €915/kW |   €1,190/kW |
| One onshore + one offshore terminal |   €1,070/kW |   €1,530/kW |   €1,990/kW |
| Two offshore terminals              |   €1,500/kW |   €2,140/kW |   €2,780/kW |
| Installed subsea route              | €2.06/kW/km | €2.94/kW/km | €3.82/kW/km |
| Installed underground route         | €2.60/kW/km | €3.72/kW/km | €4.84/kW/km |

The range is a screening convention, not a statistical confidence interval. Major special works should be estimated separately rather than assumed to fit within ±30%.

---

## 8. Offshore interpretation

There are two distinct meanings of “offshore”, which should not be confused.

### Subsea cable with both converters onshore

An interconnector can cross the sea while both converter stations remain on land. In that case, use:

[
K_T=€915/kW
]

and:

[
K_{\mathrm{route}}=€2.94/kW/km
]

The system incurs subsea cable and landfall costs, but no offshore converter-platform cost.

### One converter located offshore

For an offshore wind connection or another configuration with one converter on a platform, use:

[
K_T=€1{,}530/kW
]

The additional cost relative to two onshore stations is:

[
€615/kW
]

The offshore arrangement may reduce the required underground route on one side and may eliminate one long onshore cable approach. Those savings are automatically reflected by using the actual (L_u) in the model. No separate generic “offshore saving” should be applied.

### Two converters offshore

The two-offshore value of €2,140/kW is an arithmetic extension from two individual offshore-station costs. It should only be used for preliminary screening because the public evidence base for complete offshore-to-offshore systems is limited.

---

## 9. Installation and civil-work breakdown

A reliable universal percentage split between cable manufacture, installation and civil works is not available from the public evidence.

The Adriatic Link contract bundles design, cable supply, installation and commissioning. It therefore supports an installed-route coefficient but cannot be used to separate cable manufacturing from laying and burial. ACER likewise reports that available cable cost-breakdown data are insufficient to determine the underlying cost drivers. ([Prysmian Corporate][2])

For that reason, the defensible breakdown is:

| Model component               | Included scope                                                                                         |
| ----------------------------- | ------------------------------------------------------------------------------------------------------ |
| Terminal-station coefficient  | Converter equipment, transformers, switchgear, station installation and local station civil works      |
| Subsea route coefficient      | Cable supply, marine installation, ordinary burial/protection, joints and testing                      |
| Underground route coefficient | Cable supply, trenching or ducts, ordinary route civil works, installation, jointing and reinstatement |
| 13% residual allowance        | Owner-side and otherwise unallocated project costs and contingency                                     |
| (C_{\mathrm{special}})        | Major tunnels, exceptional crossings, difficult landfalls and other unusual site works                 |

Assigning a fixed percentage such as “60% cable and 40% installation” would imply a level of precision that the available sources do not support.

ACER also finds that terrain can increase underground-line unit investment cost by roughly a factor of two. Difficult urban, mountainous or rocky routes can therefore exceed the ordinary high case. 

---

## 10. Technology and reliability

The model is most representative of modern European cable links, particularly VSC and high-voltage extruded-cable projects. No separate generic VSC-versus-LCC cost adjustment is applied.

VSC and LCC have materially different technical requirements: LCC requires sufficient AC-system short-circuit strength and normally has a larger converter-station footprint, while VSC provides independent active- and reactive-power control. These differences do not translate into one robust, generally applicable public CAPEX multiplier. 

The base model represents one complete rated point-to-point link. It does not include a second fully independent link providing 100% transfer capacity after loss of the first. A fully duplicated system should be modelled as a second set of converters and cables, with any genuine savings from shared sites, trenches or route development deducted separately.

---

## 11. Limitations and recommended use

The model deliberately assumes that total cost is linear in rated power:

* Converter cost is constant in €/kW.
* Cable cost is constant in €/kW/km.
* No explicit economy-of-scale exponent is used.

This is a modelling assumption adopted for transparency because the available recent project sample is too small and heterogeneous to justify a precise nonlinear power relationship.

Within the considered **0.5–2 GW** range, the model will probably tend to:

* Understate unit costs toward the lower end of the range
* Overstate unit costs toward the upper end
* Be most representative around 1 GW

The ±30% planning range is more significant than a finely calibrated power exponent for most early-stage assessments.

Historical regulatory data should also be used cautiously. ACER’s historical sample gives a median of €1.38 million/km for DC submarine cable and €0.21 million/MW for a single converter station, but ACER explicitly notes that recent converter tender awards are well above the historical maximum and that infrastructure costs have risen faster than general inflation. The present model therefore places greater weight on current planning data and recent contract values. 

The model is suitable for:

* Initial route screening
* Comparison of subsea and underground alternatives
* Early business-case calculations
* Order-of-magnitude budgeting

It is not a substitute for route surveys, system design, supplier engagement or a project-specific tender estimate.

[1]: https://ec.europa.eu/eurostat/databrowser/view/tec00027/default/table?category=t_prc.t_prc_hicp&lang=en&utm_source=chatgpt.com "[tec00027] HICP - all items - annual average indices"
[2]: https://www.prysmian.com/en/media/press-releases/prysmian-secures-the-euro-630m-adriatic-link-submarine-able-project-from-terna "Prysmian secures the €630m Adriatic Link submarine cable project from Terna | Prysmian"
[3]: https://www.eib.org/en/projects/all/20250051 "TERNA ADRIATIC LINK"
