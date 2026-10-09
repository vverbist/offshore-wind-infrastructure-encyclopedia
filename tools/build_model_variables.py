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
from model.platforms.platform_material_capex import inventory as platform_inventory
from model.inputs import load_inputs
from model.hydrogen_infra.compressor import cost_coefficient_eur2025, reference_purchase_cost, turbine_reference
from model.hydrogen_production.stack import StackCurve
from tools.build_platform_benchmarks import build as build_platform_benchmarks


from model.offshore_installation.turbine_and_foundation_installation import reference_installation


def main() -> None:
    parameters = load_parameters()
    variables = build_quarto_variables(parameters)
    variables.update(quarto_variables())
    inputs = load_inputs({})
    installation = reference_installation(1, load_reference_case()["turbine"]["rated_power_mw"], inputs)
    for key in ("source_gbp2024_per_turbine", "eur2025_per_turbine", "inflation_factor"):
        places = 6 if key == "inflation_factor" else 0
        variables["installation-reference-" + key.replace("_", "-")] = f"{installation[key]:,.{places}f}"
    variables.update(build_platform_benchmarks(inputs, PROJECT_ROOT))
    variables["platform-tennet-pair-billion"] = f"{inputs.reference_number('platform-tennet-framework') / inputs.reference_number('platform-tennet-systems') / 1e9:.2f}"
    for key in ("platform-tennet-framework", "platform-mhb-contract", "platform-petrofac-pair-lower-bound"):
        variables[key] = f"{inputs.reference_number(key) / 1e9:g} billion {parameters.get(key).unit}"
    variables["platform-rte-dunkerque-contract"] = f"{inputs.reference_number('platform-rte-dunkerque-contract') / 1e6:g} million EUR"
    for key in ("platform-mass-scaling-exponent", "platform-jacket-mass-exponent", "platform-jacket-depth-coefficient"):
        variables[key] = f"{inputs.number(key):g}"
    variables["platform-tennet-systems"] = f"{inputs.reference_number('platform-tennet-systems'):.0f}"
    depth = load_reference_case()["site"]["water_depth_m"]
    variables["platform-example-depth"] = f"{depth:g} m"
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
