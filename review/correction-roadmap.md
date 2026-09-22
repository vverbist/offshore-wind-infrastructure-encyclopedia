# Prioritized correction roadmap

## Purpose

This roadmap converts the B1–B7 findings into dependency-led correction stages.
It is a proposal, not approval to change source pages. Each stage still requires
an agreed scope and the repository's normal review-before-implementation step.

The first six foundation decisions are presented in
`review/decision-packs/DP-01_foundation_contract.md`.

## Ordering principle

Correct decisions and shared data contracts before component prose. A downstream
page should not be finalized while its required upstream physical inventory,
cost boundary or availability convention remains undecided.

## Stage 0 — Publication and evidence governance

**Objective:** make model maturity and evidence access honest and maintainable.

- COR-01A replaced published completion percentages with controlled model
  readiness (DEC-0021).
- COR-01A classified all evidence records by access and model use and aligned
  About and References (DEC-0022).
- Detailed source metadata remains open under ISS-0107 and is completed with
  the relevant component evidence.
- Hydrogen-production and installation overview navigation remain as
  lightweight follow-ups under ISS-0059 and ISS-0090.

**Issues:** ISS-0059, ISS-0090, ISS-0105–0109.

**Exit test:** a reader can distinguish editorial progress, model readiness,
evidence access and unresolved results without consulting private review files.

## Stage 1 — Freeze the comparison contract

**Objective:** define one comparison that all component calculations serve.

- Report Tier 1 carrier-specific onshore products and defer common end-use
  service modelling (DEC-0003).
- Use one provisional 6.6% real WACC, a 25-year simple CRF, material short-life
  replacement and decommissioning equal to 80% of offshore installation CAPEX
  (DEC-0004).
- Evaluate one complete user-supplied case deterministically, with explicit
  input, parameter, derived-quantity and output classes and no optimizer
  (DEC-0005).
- Combine component-owned annual energy-equivalent availability factors once
  in a side-by-side architecture ledger (DEC-0006).

**Issues:** ISS-0015–0025 and ISS-0030.

**Exit test:** one executable skeleton can accept component outputs and return
dimensionally valid carrier-specific annualized metrics, explicit failure
states and no double derating. Missing component inputs remain visible rather
than being replaced by zero.

## Stage 2 — Close the common physical backbone

**Objective:** create the geometry, equipment and interface records consumed by
every architecture.

- Reacquire/version the wind input and correct direction representation.
- Set area, setback, spacing and turbine-definition conventions (DEC-0008).
- Define deterministic array topology, platform node and cable-section inventory
  (DEC-0001/0002).
- Adopt architecture-specific turbine equipment and lift ledgers (DEC-0009).
- Adopt foundation/TP physical records and surrogate limits (DEC-0010).

**Issues:** ISS-0001–0014, ISS-0031–0043.

**Exit test:** every candidate produces turbine coordinates, accepted/rejected
layout status, farm area, generation series, equipment masses, foundation
records and routed electrical sections with conserved quantities.

## Stage 3 — Close conversion and transport component packages

### 3A Electrical package

- Adopt converter electrical/offshore cost and physical ledgers (DEC-0013).
- Close export cable system, land route, PCC and onshore connection
  (DEC-0014).
- Add losses, OPEX, availability and physical segment records.

### 3B Hydrogen production package

- Freeze stack curve, module count, degradation/replacement, cost and physical
  package (DEC-0011).
- Freeze BOP scaling, water treatment, power, cost and mass (DEC-0012).
- Close DC integration and power-electronics retained functions and ledgers
  (DEC-0009/0013 as applicable).

### 3C Hydrogen infrastructure package

- Define coordinate-based collection, manifold, connections and fault states
  (DEC-0015).
- Adopt bounded compressor trains, thermodynamic method, cost and physical
  records (DEC-0016).
- Adopt validated hydraulics and discrete qualified TCP product/cost classes
  (DEC-0017).

**Issues:** ISS-0044–0089.

**Exit test:** each architecture emits conserved time-step energy, peak-sized
equipment counts, physical/mass/lift records, CAPEX, OPEX and availability
states with traceable evidence.

## Stage 4 — Close platform and installation

**Objective:** convert component ledgers into structures and installed assets.

- Decide platform multiplicity/capacity and structure/fabrication relationship
  (DEC-0007 plus upstream equipment decisions).
- Select coherent foundation/turbine campaign concepts (DEC-0018).
- Select cable/TCP lay, burial and survey methods and complete spread boundaries
  (DEC-0019).
- Select platform piling, lift and commissioning concept (DEC-0020).
- Correct mobilisation/demobilisation, zero-load, length-conservation, voyage
  and module-duration errors before calibrating rates.

**Issues:** ISS-0027, ISS-0043, ISS-0052/0053, ISS-0063, ISS-0083 and
ISS-0091–0104.

**Exit test:** supply quantities equal installed quantities; every lift, load,
pass, interface and voyage is counted once; class failures are explicit; and
complete installed CAPEX reconciles to non-overlapping spread boundaries.

## Stage 5 — End-to-end integration and validation

**Objective:** prove the corrected model chain rather than only its pages.

1. Run one small deterministic reference case through all three architectures.
2. Reconcile mass, energy, cost, availability and physical inventory at every
   page boundary.
3. Test zero/minimum, nominal, threshold-crossing and infeasible cases.
4. Reproduce every published worked example from the same implementation.
5. Compare selected outputs with independent project or literature ranges.
6. Run the complete search grid and show rejected candidates and reasons.
7. Render the full site and verify citations, equations, figures, tables,
   navigation and status indicators.

**Exit test:** an independent implementer can reconstruct the selected result,
identify every unresolved input and obtain the same feasibility and cost outcome
without undocumented choices.

## Decision order

The recommended sequence is:

`DEC-0021/0022 → DEC-0003/0004/0005/0006 → DEC-0008/0001/0009/0010 →
DEC-0011/0012/0013/0014/0015/0016/0017 → DEC-0007/0018/0019/0020`.

DEC-0002 can be resolved alongside the physical array inventory after DEC-0001.
The order within component packages can be parallelized only when their shared
contracts and output schemas are already fixed.
