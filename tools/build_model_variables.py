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


def main() -> None:
    parameters = load_parameters()
    variables = build_quarto_variables(parameters)
    output_path = PROJECT_ROOT / "_variables.yml"
    write_quarto_variables(variables, output_path)
    print(
        f"Validated {sum(1 for _ in parameters)} model inputs and wrote "
        f"{output_path.relative_to(PROJECT_ROOT)}"
    )


if __name__ == "__main__":
    main()
