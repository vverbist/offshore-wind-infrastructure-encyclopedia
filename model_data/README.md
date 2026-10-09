# Model inputs

`inputs.csv` is the authoritative table for scalar values used by the website,
figures and future model. It can be edited directly in Excel or a text editor.

The columns are intentionally limited:

- `id`: permanent, human-readable identifier;
- `value`: numeric value in the stated unit;
- `unit`: the stored unit, not a display conversion;
- `kind`: `sourced`, `assumption`, `conversion` or `reference`;
- `price_year`: required for adopted monetary inputs; and
- `citation`: the key in `references.bib`, without the leading `@`.

A blank `value` is an explicit unresolved TODO, not zero. Blank entries retain
their required unit and cannot be used in a numerical calculation. Website
display renders them as TODO. Adopt the evidence/assumption and monetary price
basis on the owning page before filling them. Sensitivity overrides apply only
to adopted numeric baselines and are recorded without changing this file.

`reference` is reserved for contextual monetary evidence that cannot yet be
adopted, for example because its source price year is unresolved.

Do not add formulas to the CSV. Derived values and currency conversions belong
in `parameters.py`. The website build validates the table, calculates derived
values, writes the ignored `_variables.yml` file and regenerates dependent
figures. `_variables.yml` must never be edited directly.

Percentages are stored as fractions: `0.066` is rendered as `6.6%`. If Excel
saves a European semicolon-delimited CSV with decimal commas, the loader accepts
that format as well.

## Executable model parameter ownership

The draft model uses these additional groups. Page paths below identify the
point-of-use equations and scope; `reference` rows remain non-combinable evidence.

| IDs | Owner and adoption basis |
|---|---|
| `turbine-inverter-efficiency`, `turbine-inverter-unit-cost` | `electrical_infra/power_conversion_equipment.qmd`; inverter-only DC-to-AC efficiency and purchase cost per rated AC kW; both remain unresolved, with boundary equations on `turbine_system/power_electronics.qmd` |
| `annual-hours`, `hydrogen-hhv` | `methodology/energy_availability_and_annualisation.qmd`; non-leap screening year and adopted rounded HHV |
| `stack-*` | `hydrogen_production/stack.qmd`; existing curve used as supplied, reference current density and module/minimum-load assumptions; HHV voltage and figure cutoff migrated from the existing figure builder |
| `bop-*` | `hydrogen_production/balance_of_plant.qmd`; NREL categories include internal water handling; DEA thermal treatment anchors the aggregate at 15 MW with 0.75 scaling. EUR2023 is an explicit quote-year assumption; shared HICP converts it to EUR2025 |
| `*-conversion-*` | `hydrogen_production/elx_power_electronics.qmd` and `dc_integration.qmd`; only the central efficiency is adopted; unnormalised cost and turbine-level interfaces remain TODO |
| `compressor-*`, `hydrogen-heat-capacity-ratio`, `universal-gas-constant`, `hydrogen-molar-mass` | `hydrogen_infra/compressor.qmd` and its existing figure builder; migrated thermodynamic assumptions and legacy rounded constants, existing sourced exponent, agreed motor-power cap; sourced 2019 CAD coefficient, the brief's own USD/CAD rate and the compressor PPI escalation, from which code derives the EUR2025 reference cost at the agreed 15 kW reference |
| `standard-atmospheric-pressure` | `research_articles/turbine_level_hydrogen/reference_case.qmd` (gauge-to-absolute conversion of article pressures) and the pressure convention on `hydrogen_infra/compressor.qmd`; exact standard atmosphere adopted as the atmospheric basis |
| `pipeline-*` | `hydrogen_infra/hydrogen_pipelines.qmd`; existing gas-property and friction method; the confidential quote fit returns material price in EUR2025/m (basis confirmed by the project owner on 2026-09-25), so `pipeline-quote-to-eur2025` is 1; the operating-to-rated pressure mapping, product unit prices without the private module and connection/manifold costs remain TODO |
| `array-*` | `electrical_infra/infield_ac_cables.qmd`; existing voltage, routing and blended supply assumptions; AC resistance and power factor require adoption |
| `wind-turbulence-intensity` | `wind_resource_and_layout/wake_modelling_and_spacing.qmd`; existing provisional legacy assumption |
| `turbine-*` | `turbine_system/wind_turbine.qmd`; pinned WISDEM coefficients and Mehta replacements, source calibration; electrical additions/adjustments remain TODO |
| `foundation-*` | `turbine_system/foundation.qmd`; reference design, fabricated unit cost and transition-piece allowance; supported reference mass is summed in code |
| `platform-*` | `platforms/platform_material_capex.qmd`; active complete-topside-mass EPCI model, including installation; mass references and linear scaling documented in `platforms/topside_mass.qmd`. Installed DC rating follows wind-farm capacity, overplanting and whole stack modules. Legacy DNV fabrication and installation inputs are inactive comparisons, not current blockers. |
| `install-*` | The three `offshore_installation/` pages; coherent spread inputs remain TODO rather than combining incompatible reference vessels |
| `*-availability`, `*-opex-rate` | Component owners and `methodology/energy_availability_and_annualisation.qmd`; deliberately unresolved pending non-overlapping scope adoption |
| `financial-usd-escalation-*` | `methodology/financial_and_price_basis.qmd`; U.S. CPI-U annual-average fallback (2020 and 2022 to 2025); components with a better-matched index use their own factor |

Pressures stored with unit `bar` are absolute. Gauge values are converted
with `standard-atmospheric-pressure` before they enter a calculation.

The BOP block limit and compressor train limit are the explicitly agreed
screening choices (100 MW served electrolysis and 1 MW motor input). BOP limit
sensitivities of 20 and 50 MW belong in scenario overrides. These limits are
modelling assumptions, not claims about supplier qualification.

WISDEM coefficients with unit `coefficient` retain the dimensions implied by
their specific kg/m/kW/Nm regression on the turbine page; they are not
dimensionless physical constants. Raw USD rates have unknown common price age
and are used only as relative calibration weights. The separate crane price
is unresolved; a documented mass subtotal does not establish a complete price.

Stack degradation is an ex-post energy penalty: `stack-degradation-rate`
(fraction per 1000 full-load hours) and `stack-end-of-life-degradation` give the
lifetime-average production factor in code (`hydrogen_production/stack.qmd`).

`turbine-distributed-maximum-lift` is the largest lifted assembly [t] in the
adopted combined turbine/hydrogen installation plan. It and the additional
hydrogen-equipment mass remain TODOs. Connections and manifolds have separate
O&M rates, also unresolved, to retain their scope in the component ledger.

Electrical operation uses unresolved `turbine-inverter-efficiency`,
`turbine-transformer-efficiency` and `array-ac-loss-fraction`; the former AC
resistance and power-factor inputs are retired. The loss fraction applies to
aggregate transformer output. `turbine-electrical-cost-adjustment` excludes the
transformer reallocation and unclaimed inverter credit.

Stack purchase cost is derived in `model/hydrogen_production/stack.py` from the
NREL manufacturing anchors, source jV rating, supplied curve and shared markup,
inflation and exchange inputs. Manufacturing output is an article scenario choice.
There is no independently stored `stack-purchase-unit-cost` result.

### First-article turbine installation

`installation.turbine_method = "reference"` selects the BVG fixed normal-turbine
benchmark. `install-turbine-reference-*` and `financial-gbp-*` inputs belong to
`offshore_installation/turbine_and_foundation_installation.qmd`. GBP2024 cost,
UK CPI and 2025 GBP/EUR derive the EUR2025 result in code. There is no mass
discount. The default `campaign` method and all previous inputs remain intact;
foundation installation still uses it. The article assumes hydrogen-equipment
installation and commissioning replace comparable work for removed power
electronics. Both turbines use the same installation benchmark, without a
separate hydrogen-equipment charge. This is a modelling assumption, not a
supplier-verified equivalence. Central-platform installation stays within EPCI.
