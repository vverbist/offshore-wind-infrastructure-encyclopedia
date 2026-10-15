"""Validate canonical inputs and prepare Quarto's generated variables file."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from model_data.parameters import (
    build_quarto_variables,
    load_parameters,
    write_quarto_variables,
)
from research_articles.turbine_level_hydrogen.analysis.reference_case import quarto_variables, load_reference_case
from model.platforms.platform_material_capex import inventory as platform_inventory, estimate_topside_mass, epci_inventory, epci_cost
from model.inputs import load_inputs, read_scenario, DERIVED_ESCALATION_FACTORS
from model.hydrogen_infra.compressor import cost_coefficient_eur2025, reference_purchase_cost, turbine_reference
from model.hydrogen_production.stack import StackCurve, purchase_cost_basis, degradation_diagnostics
from model.hydrogen_production.balance_of_plant import reference_cost_basis as bop_reference_cost_basis
from model.hydrogen_production.elx_power_electronics import efficiency as central_efficiency
from model.turbine_system.wind_turbine import calculate as turbine_calculate
import tomllib
from tools.build_platform_benchmarks import build as build_platform_benchmarks
from model.offshore_installation.turbine_and_foundation_installation import reference_installation, campaign_inputs
from model.offshore_installation.cable_and_pipeline_installation import ac_lay_inputs
from model.methodology.financial_and_price_basis import usd2024_to_eur2025


def main() -> None:
    parameters = load_parameters()
    variables = build_quarto_variables(parameters)
    variables.update(quarto_variables())
    for parameter in parameters:
        if parameter.id.startswith(("install-", "financial-usd-cpi-", "financial-usd-per-eur")) and parameter.value is not None:
            variables["raw-" + parameter.id] = parameter.raw_value
    inputs = load_inputs({})
    selected = read_scenario(PROJECT_ROOT / "research_articles/turbine_level_hydrogen/scenarios/decentralised.toml")
    variables["article-collection-diameter-inches"] = f"{selected['collection']['diameter_inches']:g}"
    for key in DERIVED_ESCALATION_FACTORS:
        variables[key] = f"{inputs.number(key):g}"
        variables[key + "-value"] = variables[key]
    for kind in ("foundation", "turbine"):
        for key, value in campaign_inputs(kind, inputs).items():
            places = 0 if key == "spread-rate" else (3 if key == "port-time" else 2)
            variables[f"install-{kind}-{key}-derived"] = f"{value:,.{places}f}"
    for key, value in ac_lay_inputs(inputs).items():
        variables[f"install-ac-{key}-derived"] = f"{value:,.0f}" if key == "lay-rate" else f"{value:g}"
    variables["install-usd2024-eur2025-factor"] = f"{usd2024_to_eur2025(1, inputs):.7f}"
    variables["hydrogen-hhv-mwh-per-kg"] = f"{inputs.number('hydrogen-hhv', 'kWh/kg') / 1000:g}"
    variables["hvdc-pole-reference-km-per-load"] = f"{inputs.number('install-cable-reference-carousel', 't') / inputs.number('install-hvdc-pole-linear-mass', 't/km'):.1f}"
    # Illustrative scenario: saved, selected article cases. Recalculate from operation rows.
    import pandas as pd
    from model.turbine_system.foundation import calculate as foundation_calculate
    reference_inputs = PROJECT_ROOT / "model_runs"
    for architecture in ("centralised", "decentralised"):
        operations = reference_inputs / f"settled-methods-20261012-{architecture}/p140barg-d8in/operation.csv"
        if operations.exists():
            table = pd.read_csv(operations)
            installed = table.groupby("location").installed_kw.first().sum()
            hours = float((table.stack_kw * table.hours).sum()) / installed
            diagnostic = degradation_diagnostics(hours, inputs.number("financial-project-life", "year"), inputs)
            for key, value in diagnostic.items():
                variables[f"degradation-example-{architecture}-{key.replace('_', '-')}"] = (
                    f"{value * 100:.2f}%" if key.endswith("fraction") or key == "lifetime_production_factor"
                    else f"{value:.1f}" if value is not None else "unresolved")
        else:
            for key in ("full-load-hours-per-year", "terminal-loss-fraction", "cumulative-yield-loss-fraction"):
                variables[f"degradation-example-{architecture}-{key}"] = "TODO: selected article operation table unavailable"
    supported = inputs.number("foundation-reference-rna-mass", "t") + inputs.number("foundation-reference-tower-mass", "t")
    variables["foundation-reference-supported-mass-value"] = f"{supported:,.0f}"
    variables["foundation-mass-depth-coefficient"] = f"{inputs.number('foundation-reference-monopile-mass', 't') / supported / inputs.number('foundation-reference-depth', 'm'):.5f}"
    variables["install-support-reference-rate-eur2025"] = f"{usd2024_to_eur2025(inputs.reference_number('install-support-reference-rate'), inputs):,.0f}"
    variables["install-export-pole-example-interface-days"] = f"{2 * inputs.reference_number('install-export-reference-interface-hours') / 24:.1f}"
    conversion_efficiency = central_efficiency(inputs)
    variables["central-conversion-efficiency"] = f"{100 * conversion_efficiency:.4f}%"
    variables["central-conversion-loss"] = f"{100 * (1 - conversion_efficiency):.4f}%"
    with (PROJECT_ROOT / "turbine_system/wind_turbine_example.toml").open("rb") as stream:
        example = tomllib.load(stream)
    turbine_example = turbine_calculate(**example, inputs=inputs)
    calibration_turbine = turbine_calculate(inputs.number("turbine-calibration-power", "kW"),
        inputs.number("turbine-calibration-diameter", "m"),
        inputs.number("turbine-calibration-hub-height", "m"), inputs)
    raw_reference = calibration_turbine["raw_cost_weights"]
    variables["turbine-example-raw-rna-million"] = f"{sum(v for k,v in raw_reference.items() if k != 'tower') / 1e6:.3f}"
    variables["turbine-example-raw-tower-million"] = f"{raw_reference['tower'] / 1e6:.3f}"
    for key in ("rna_calibration_factor", "tower_calibration_factor"):
        variables["turbine-example-" + key.replace("_", "-")] = f"{turbine_example[key]:.4f}"
    groups = {"blades": ["blade"], "hub": ["hub", "pitch", "spinner"],
              "drivetrain": ["lss", "bearings", "brake", "generator"],
              "nacelle": ["bedplate", "yaw", "hvac", "cover", "platforms"],
              "electrical": ["transformer", "connections", "controls"], "tower": ["tower"]}
    costs = {name: sum(turbine_example["calibrated_component_costs_usd2022"][k] for k in keys)
             for name, keys in groups.items()}
    costs["rna"] = sum(v for k,v in costs.items() if k != "tower")
    costs["total"] = turbine_example["supply_usd2022"]
    for name, cost in costs.items():
        variables[f"turbine-example-{name}-million"] = f"{cost / 1e6:.3f}"
        variables[f"turbine-example-{name}-per-kw"] = f"{cost / example['power_kw']:,.1f}"
    installation = reference_installation(1, load_reference_case()["turbine"]["rated_power_mw"], inputs)
    for key in ("source_gbp2024_per_turbine", "eur2025_per_turbine", "inflation_factor"):
        places = 6 if key == "inflation_factor" else 0
        variables["installation-reference-" + key.replace("_", "-")] = f"{installation[key]:,.{places}f}"
    for key, value in bop_reference_cost_basis(inputs).items():
        places = 6 if key == "water_escalation_factor" else 0
        variables["bop-cost-" + key.replace("_", "-")] = f"{value:,.{places}f}"
    variables.update(build_platform_benchmarks(inputs, PROJECT_ROOT))
    # Compare both architectures at the disclosed HVDC rating; not an article default.
    example_power = inputs.reference_number("platform-mhb-power", "GW")
    for reference in ("electrolysis", "hvdc"):
        mass = estimate_topside_mass(example_power, inputs, reference)
        cost = epci_cost(epci_inventory({"topside_mass_t": mass}, inputs), inputs)
        variables[f"platform-mass-example-{reference}"] = f"{mass:,.0f}"
        variables[f"platform-cost-example-{reference}"] = f"{cost['total_eur'] / 1e6:,.1f}"
        variables["platform-epci-reference-million"] = f"{cost['reference_cost_eur'] / 1e6:,.1f}"
    for reference, source in (("electrolysis", "offsh2ore"), ("hvdc", "mhb")):
        intensity = inputs.reference_number(f"platform-{source}-topside", "t") / inputs.reference_number(f"platform-{source}-power", "GW")
        variables[f"platform-mass-intensity-{reference}"] = f"{intensity / 1000:g}"

    variables["platform-tennet-pair-billion"] = f"{inputs.reference_number('platform-tennet-framework') / inputs.reference_number('platform-tennet-systems') / 1e9:.2f}"
    for key in ("platform-tennet-framework", "platform-mhb-contract", "platform-petrofac-pair-lower-bound"):
        variables[key] = f"{inputs.reference_number(key) / 1e9:g} billion {parameters.get(key).unit}"
    variables["platform-rte-dunkerque-contract"] = f"{inputs.reference_number('platform-rte-dunkerque-contract') / 1e6:g} million EUR"
    for key in ("platform-mass-scaling-exponent", "platform-jacket-mass-exponent", "platform-jacket-depth-coefficient"):
        variables[key] = f"{inputs.number(key):g}"
    variables["platform-tennet-systems"] = f"{inputs.reference_number('platform-tennet-systems'):.0f}"
    depth = load_reference_case()["site"]["water_depth_m"]
    variables["platform-example-depth"] = f"{depth:g} m"
    # Retained solely for archived platform comparison pages; never active EPCI.
    for name in ("mhb", "dragados"):
        masses = platform_inventory({"topside_mass_t": inputs.reference_number(f"platform-{name}-topside")}, depth, inputs)
        for quantity in ("topside_structure_t", "jacket_t", "piles_t"):
            variables[f"platform-example-{name}-{quantity.replace('_', '-')}"] = f"{masses[quantity]:,.0f} t"
    reference = reference_purchase_cost(inputs)
    variables["compressor-cost-coefficient-eur2025"] = f"{cost_coefficient_eur2025(inputs):,.0f} EUR"
    variables["compressor-reference-purchase-cost"] = f"{reference:,.0f} EUR"
    variables["compressor-reference-specific-cost"] = (
        f"{reference / inputs.number('compressor-reference-motor-power', 'kW'):,.0f} EUR/kW")
    curve = StackCurve.read(PROJECT_ROOT / "numerical_inputs/pem_polarisation_curve.xlsx")
    manufacturing_output = load_reference_case()["electrolysis"]["manufacturing_output_mw_year"]
    stack_cost = purchase_cost_basis(manufacturing_output, inputs)
    variables["stack-article-manufacturing-output"] = f"{manufacturing_output:g}"
    for key, value in stack_cost.items():
        places = 4 if key == "rating_conversion_factor" else 0
        variables["stack-cost-" + key.replace("_", "-")] = f"{value:.{places}f}"
    duty = turbine_reference(inputs.number("wind-turbine-rated-power", "MW") * 1000,
                             inputs.number("compressor-reference-inlet-pressure", "bar"),
                             inputs.number("compressor-reference-outlet-pressure", "bar"), curve, inputs)
    for key, places in (("turbine_kw", 0), ("stack_kw", 0), ("bop_kw", 1),
                        ("hydrogen_kg_h", 1), ("compressor_kw", 1), ("trains", 0),
                        ("purchase_eur", 0), ("eur_per_turbine_kw", 1)):
        variables["compressor-turbine-reference-" + key.replace("_", "-")] = f"{duty[key]:,.{places}f}"
    output_path = PROJECT_ROOT / "_variables.yml"
    write_quarto_variables(variables, output_path)
    print(
        f"Validated {sum(1 for _ in parameters)} model inputs and wrote "
        f"{output_path.relative_to(PROJECT_ROOT)}"
    )


if __name__ == "__main__":
    main()
