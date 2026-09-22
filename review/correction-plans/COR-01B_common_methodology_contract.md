# COR-01B implementation plan — Common methodology contract

## Objective

Apply DEC-0003 to DEC-0006 as one calculation-led methodology contract so that
an implementer can identify the model inputs, execute one deterministic case,
combine energy and cost consistently, and report carrier-specific results on
the approved bases.

COR-01B defines the shared calculation structure. It does not fill missing
component evidence or make the three architecture calculations complete.

## Approved decisions applied

- DEC-0003: Tier 1 carrier-specific endpoints only; no common end-use ranking.
- DEC-0004: provisional 6.6% real WACC, 25-year project life, simple CRF,
  material short-life replacement, and decommissioning equal to 80% of
  offshore installation CAPEX.
- DEC-0005: one deterministic calculation per complete user-supplied case; no
  optimizer or internal search.
- DEC-0006: annual energy-equivalent availability owned by non-overlapping
  subsystems and combined once in an architecture ledger.

## Scope boundary

### Included

- the six Methodology pages;
- narrow endpoint and result-label consistency edits on the five Architecture
  pages;
- an authoritative bibliography record and citation for hydrogen HHV;
- reconciliation of methodology inputs and dependencies in the review
  registers;
- correction records for affected findings; and
- full methodology and site validation.

### Excluded

- Tier 2 end-use, storage, reconversion, distribution and demand matching;
- optimization, automatic design sweeps or Pareto selection;
- detailed discounted cash flow, tax, debt, construction-finance timing or
  architecture-specific financing;
- new component CAPEX, OPEX, efficiency or availability values;
- correction of component calculations outside the narrow endpoint labels;
- selection of a WACC evidence source or sensitivity range;
- invention of availability values where component evidence is missing; and
- physical, installation or platform decisions assigned to later stages.

## Part A — Methodology overview and reader route

### methodology/overview.qmd

Revise the overview so it describes the model actually approved:

1. one user-supplied case is evaluated deterministically;
2. the selected architecture determines the component chain;
3. physical quantities and energy are calculated before cost;
4. feasibility failures remain explicit;
5. annual availability is applied once through the architecture ledger; and
6. carrier-specific cost outputs are reported without claiming a common
   end-use comparison.

Replace optimization terminology. Add direct links to the five detailed
methodology pages in dependency order:

1. System Boundary and Carrier-Cost Metrics;
2. Financial and Price-Basis Assumptions;
3. Inputs, Parameters and Outputs;
4. Modelling Workflow; and
5. Energy and Availability.

This addresses ISS-0105 while keeping the overview concise.

## Part B — System boundary, cost scope and reporting equations

### methodology/system_boundary_and_lcoe.qmd

Retitle the page to avoid using one undifferentiated LCOE label for different
carrier products.

### Delivery endpoints

Define the Tier 1 endpoints exactly:

- electricity: electrical energy landed at the defined onshore electrical
  delivery point;
- hydrogen: hydrogen mass landed at the defined onshore hydrogen delivery
  point, converted to energy on an HHV basis; and
- both endpoints exclude end use, storage, reconversion, downstream
  distribution and demand matching.

State explicitly that EUR/MWh-electricity and EUR/MWh-H2-HHV are different
delivered products. They may be displayed side by side but are not equivalent
end-service prices.

### Capital and annual-cost reporting

Define and distinguish:

- initial installed CAPEX;
- lifecycle capital basis, including required replacement and the simplified
  decommissioning allowance;
- annual OPEX; and
- annualized modelled cost.

Report capital intensity against installed wind-turbine rated capacity:

$$
c_{\mathrm{initial}}
=
\frac{C_{\mathrm{initial}}}{P_{\mathrm{wind,rated}}},
$$

and, separately where useful:

$$
c_{\mathrm{lifecycle}}
=
\frac{C_{\mathrm{lifecycle\ capital}}}{P_{\mathrm{wind,rated}}}.
$$

Both have units EUR 2025/kW-wind. The labels must prevent replacement and
decommissioning from being mistaken for initial installed CAPEX.

Define the carrier-specific annual cost metrics:

$$
LC_{\mathrm{electricity}}
=
\frac{C_{\mathrm{annual,electricity}}}
{E_{\mathrm{electricity,onshore}}},
$$

$$
LC_{\mathrm{H2,HHV}}
=
\frac{C_{\mathrm{annual,H2}}}
{E_{\mathrm{H2,onshore,HHV}}}.
$$

For hydrogen:

$$
LC_{\mathrm{H2,kg}}
=
LC_{\mathrm{H2,HHV}}
\frac{HHV_{\mathrm{H2}}}{1000},
$$

where HHV is in kWh/kg, so a cost in EUR/MWh multiplied by 0.0394 MWh/kg
returns EUR/kg.

### Cost ownership matrix

Replace the dimensionally undefined C1/C2/C3 expression with:

1. the annual-cost equation;
2. the delivered-energy equation; and
3. a scope/ownership matrix.

The matrix will identify, without double counting:

- component supply CAPEX — component owner;
- offshore installation CAPEX — applicable installation owner;
- onshore equipment and connection CAPEX — applicable component owner;
- annual OPEX — component owner;
- material short-life replacement — component owner;
- decommissioning — shared calculation owned by METH-003;
- commissioning — owning installation/component interface;
- development, shared engineering, insurance and owner contingency — shared
  project-cost fields owned by METH-003 but unresolved until parameterized;
- construction finance, taxes and financing fees — excluded by the simplified
  CRF decision, not silently included; and
- residual value — zero under the approved 25-year convention for components
  retained to the project endpoint.

A required unresolved shared field must produce a not-parameterized complete
cost result. The documentation may still report explicitly labelled component
or modelled-cost subtotals; it must not call them total system cost.

## Part C — Financial and lifecycle calculation

### methodology/financial_and_price_basis.qmd

Retain the existing EUR 2025 normalization method, exchange-rate convention,
markup boundary and CRF arithmetic.

Replace the statement requiring discounted cash flows with the approved simple
capital-basis treatment.

Define:

$$
N_{\mathrm{replacement},j}
=
\left\lceil
\frac{n_{\mathrm{project}}}{n_j}
\right\rceil - 1
$$

only for a component whose owner documents a material technical life shorter
than 25 years and identifies the replacement scope and cost. A replacement at
the end of year 25 is not counted.

Define:

$$
C_{\mathrm{replacement}}
=
\sum_j
N_{\mathrm{replacement},j}
C_{\mathrm{replacement},j},
$$

$$
C_{\mathrm{decommissioning}}
=
0.80 C_{\mathrm{offshore\ installation}},
$$

$$
C_{\mathrm{lifecycle\ capital}}
=
C_{\mathrm{initial}}
+
C_{\mathrm{replacement}}
+
C_{\mathrm{decommissioning}},
$$

and:

$$
C_{\mathrm{annual}}
=
CRF\,
C_{\mathrm{lifecycle\ capital}}
+
\sum_j O_j.
$$

State the simplifications explicitly:

- replacement and decommissioning timing is not discounted;
- no residual value is credited;
- components with technical life at least 25 years have no replacement;
- a short life does not imply replacement unless the component owner defines
  the required replacement event and boundary;
- all architectures use the same provisional 6.6% real WACC; and
- the WACC evidence basis and sensitivity range remain unresolved under
  ISS-0018.

The page will own the shared project-cost schema even where values remain
unresolved. No placeholder amount will be inserted.

## Part D — Deterministic model contract

### methodology/optimisation_variables.qmd

Keep the existing file path to avoid breaking links, but retitle and rewrite the
page as Inputs, Parameters and Outputs.

Define one canonical taxonomy:

| Class | Meaning |
|---|---|
| User input | A value or discrete choice supplied for one model case |
| Fixed parameter | A sourced value or explicit modelling assumption |
| Derived quantity | Calculated from inputs and parameters |
| Output | A reported physical, energy, cost or feasibility result |

There are no optimization variables. Alternative designs and sensitivities are
separate complete user-supplied cases.

Publish a master input contract with, at minimum:

- field or symbol;
- description;
- unit;
- architecture applicability;
- owning page;
- source/classification;
- admissibility or feasibility check; and
- current status.

The master table will include only values already documented by the project.
Missing values or allowed sets remain explicit TODOs; COR-01B will not invent
ranges.

The 2 GW HVDC link rating will be classified as a fixed sourced parameter and
linked to the canonical electrical component equation. Link count, partial
final-block use, curtailment and feasibility remain owned by the electrical
component pages rather than duplicated here.

### methodology/modelling_workflow.qmd

Write the executable order for one deterministic case:

1. load and validate the complete user-input record and fixed parameters;
2. select the architecture branch;
3. calculate wind resource, turbine layout and gross production;
4. construct physical component and route inventories;
5. size or select discrete equipment deterministically from the supplied case;
6. reject infeasible or not-parameterized cases with recorded reasons;
7. calculate component efficiencies, auxiliary demand and delivered energy in
   physical order;
8. combine annual subsystem availability once through METH-006;
9. aggregate non-overlapping CAPEX, replacement, decommissioning and OPEX;
10. annualize cost using METH-003; and
11. return the approved physical, energy, capital-intensity, carrier-cost and
    feasibility outputs.

Define the common return status:

- feasible;
- infeasible, with one or more physical/technical reasons; or
- not_parameterized, with the missing input or evidence owner.

An infeasible or not-parameterized case must not silently return a zero cost,
zero quantity or apparently valid carrier-cost result.

Time-varying wind and component-performance calculations may retain their
native documented time step. Availability remains annual and must not be
expanded into a time-step outage simulation in COR-01B.

## Part E — Energy and architecture availability

### methodology/energy_availability_and_annualisation.qmd

Retitle the page Energy and Availability because financial annualisation is
owned by METH-003.

Add an authoritative source for hydrogen HHV and cite the rounded 39.4 kWh/kg
value at introduction, including its reference basis as far as the selected
source supports.

Keep physical efficiency and auxiliary-energy calculations upstream of
availability. Define annual pre-availability energy for each carrier and then:

$$
E_{\mathrm{delivered}}
=
E_{\mathrm{preavailability}}
\prod_{s \in S_a} A_s,
$$

where $S_a$ is the set of non-overlapping subsystem factors for architecture
$a$.

Publish the three architectures side by side in one ledger. Each row will show:

- subsystem and architecture applicability;
- component owner;
- factor symbol;
- inclusion boundary;
- whether redundancy has already been combined;
- whether the effect is already embedded upstream;
- source or explicit assumption status; and
- current adopted value or unresolved status.

Rules:

1. each outage cause appears once;
2. serial non-overlapping subsystem factors may be multiplied;
3. a component owner supplies the already-combined annual subsystem factor for
   parallel units or redundancy;
4. a factor is omitted when the same derating is embedded in the upstream
   energy calculation;
5. unresolved required availability returns not_parameterized for a complete
   delivered-energy result; and
6. 100% may be used only as an explicit zero-outage scenario assumption, never
   as an evidence-backed reliability claim.

The conflicting legacy electrolyser values will not be reconciled by choosing
one without evidence. The ledger will identify their different claimed scopes
and mark the adopted subsystem factor unresolved until the hydrogen component
owner resolves it.

ISS-0025 remains open because COR-01B defines ownership and combination but
does not supply missing evidence or sensitivities.

## Part F — Architecture consistency

Apply narrow edits to:

- architectures/overview.qmd;
- architectures/electricity_export_hvdc.qmd;
- architectures/centralised_hydrogen.qmd;
- architectures/decentralised_hydrogen.qmd; and
- architectures/component_mapping.qmd.

These edits will:

- name the approved onshore endpoint for each architecture;
- use the approved result units;
- state that Tier 1 products are not common end-use services;
- link to the methodology owner; and
- remove or qualify wording that implies a direct equivalent carrier ranking.

No architecture component mapping, physical boundary, cost coefficient or
technical equation will change in COR-01B.

## Registers and decision records

After implementation and validation:

- assign COR-01B to DEC-0003 through DEC-0006;
- update the methodology rows in model-input-register.csv;
- add the shared endpoint, workflow, cost and availability interfaces to
  dependency-register.csv;
- update page-register.csv only where corrected readiness is supported;
- add correction records to METH-001 through METH-006 page reviews;
- update correction-roadmap.md where its original discounted-cash-flow and
  optimization wording is superseded by the approved decisions; and
- create review/correction-validation/COR-01B.md.

Readiness will be reassessed from the corrected calculation contract and
remaining issues. Pages will not be marked ready merely because their prose was
rewritten.

## Expected issue result

| Issue | Expected result |
|---|---|
| ISS-0015 | Close after endpoint and unit reconciliation |
| ISS-0016 | Close after replacing the undefined conceptual expression |
| ISS-0017 | Close after the cost-scope owner matrix and missing-input behavior are defined |
| ISS-0018 | Remain open: 6.6% evidence and sensitivity unresolved |
| ISS-0019 | Close after the approved replacement/decommissioning CRF treatment is reproducible |
| ISS-0020 | Close after one canonical deterministic taxonomy is published |
| ISS-0021 | Close after the executable workflow and return statuses are defined |
| ISS-0022 | Close after optimization claims are removed |
| ISS-0023 | Close after the sourced 2 GW parameter and component handoff are explicit |
| ISS-0024 | Close after the architecture ledger and no-double-derating rule are defined |
| ISS-0025 | Remain open: component evidence and sensitivities unresolved |
| ISS-0026 | Close after an authoritative HHV citation is added |
| ISS-0105 | Close after direct methodology navigation is added |

## Validation

### Automated calculation checks

1. Reproduce CRF = 0.082741447/year for 6.6% and 25 years.
2. Check replacement counts:
   - 25-year life gives 0;
   - 10-year life gives 2; and
   - 5-year life gives 4.
3. Check decommissioning equals 80% of summed offshore installation CAPEX.
4. Check the annual-cost equation dimensionally returns EUR/year.
5. Check 100 EUR/MWh-H2-HHV converts to 3.94 EUR/kg at 39.4 kWh/kg.
6. Check every reported capital-intensity denominator is installed
   wind-turbine rated kW.
7. Check every master-contract field has a class, unit, owner and status.
8. Check each architecture availability ledger contains no duplicate subsystem
   owner and no unresolved factor silently mapped to 1.0.
9. Check deterministic workflow statuses prevent cost reporting for infeasible
   and not-parameterized cases.
10. Check every newly introduced quantitative value is classified and cited or
    explicitly identified as an assumption.

### Site checks

1. Render every affected page and then the full website.
2. Check citations, equations, tables, cross-references and local links.
3. Confirm no optimization or editorial-completion language remains in the
   published methodology contract.
4. Confirm architecture endpoint labels reconcile with METH-002.
5. Confirm readiness metadata reconciles with the page and issue registers.
6. Inspect the affected rendered pages for equation, table and navigation
   layout unless the user explicitly limits validation to rendering only.

## Implementation sequence

1. revise METH-002 and METH-003 as the endpoint and cost contract;
2. repurpose METH-005 as the canonical input/parameter/output contract;
3. revise METH-004 to consume that contract in calculation order;
4. revise METH-006 as the energy and availability ledger;
5. align the methodology overview and architecture endpoint wording;
6. add the HHV evidence record and citation;
7. reconcile registers and issue expectations;
8. run automated checks and render the site; and
9. record validation and close only the issues whose exit tests pass.

## Approval requested

Approval of COR-01B authorizes only the files and behavior described above.
Implementation will stop and return for a new decision if it requires a new
component value, an availability factor, a WACC evidence selection, a Tier 2
boundary, or a materially different cost scope.
