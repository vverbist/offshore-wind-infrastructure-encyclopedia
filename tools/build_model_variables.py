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
from research_articles.turbine_level_hydrogen.analysis.reference_case import quarto_variables
from model.inputs import load_inputs
from model.hydrogen_infra.compressor import cost_coefficient_eur2025, reference_purchase_cost, turbine_reference
from model.hydrogen_production.stack import StackCurve


def main() -> None:
    parameters = load_parameters()
    variables = build_quarto_variables(parameters)
    variables.update(quarto_variables())
    inputs = load_inputs({})
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
