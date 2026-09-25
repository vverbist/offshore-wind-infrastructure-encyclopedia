"""Resolve central inputs and explicit scenario overrides once per run."""
from dataclasses import asdict
from decimal import Decimal
from math import isfinite
from pathlib import Path
import tomllib

from model_data.parameters import ParameterSet, load_parameters
from .records import MissingInput


class Inputs:
    def __init__(self, parameters: ParameterSet, overrides: dict | None = None):
        self.parameters = parameters
        self.overrides = overrides or {}
        for key, value in self.overrides.items():
            parameter = parameters.get(key)
            if parameter.value is None:
                raise ValueError(f"{key}: adopt missing baseline in inputs.csv before overriding it")
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(value):
                raise ValueError(f"{key}: override must be a finite number in {parameter.unit}")

    def number(self, key: str, unit: str | None = None) -> float:
        parameter = self.parameters.get(key)
        if unit is not None and unit != parameter.unit:
            raise ValueError(f"{key}: expected {unit}, found {parameter.unit}")
        if parameter.value is None:
            raise MissingInput(f"Central parameter required: {key} ({parameter.unit})")
        if parameter.kind == "reference":
            raise MissingInput(f"Reference-only input needs an adopted basis: {key}")
        value = float(self.overrides.get(key, parameter.value))
        if not isfinite(value):
            raise ValueError(f"{key} must be finite")
        return value

    def fraction(self, key: str) -> float:
        value = self.number(key, "fraction")
        if not 0 <= value <= 1:
            raise ValueError(f"{key} must lie between zero and one")
        return value

    def reference_number(self, key: str, unit: str | None = None) -> float:
        """Explicit reference/calibration use only; never an adopted additive price."""
        if self.parameters.get(key).kind != "reference":
            raise ValueError(f"{key} is not reference-only evidence")
        baseline = self.parameters.number(key, unit)
        return float(self.overrides.get(key, baseline))

    def positive(self, key: str, unit: str | None = None) -> float:
        value = self.number(key, unit)
        if value <= 0:
            raise ValueError(f"{key} must be positive")
        return value

    def records(self) -> list[dict]:
        records = []
        for parameter in self.parameters:
            row = asdict(parameter)
            row["baseline_value"] = parameter.raw_value
            row["value"] = self.overrides.get(parameter.id, parameter.value)
            row["overridden"] = parameter.id in self.overrides
            records.append({k: str(v) if isinstance(v, Decimal) else v for k, v in row.items()})
        return records


def read_scenario(path: Path) -> dict:
    with path.open("rb") as stream:
        return tomllib.load(stream)


def load_inputs(scenario: dict, path: Path | None = None) -> Inputs:
    parameters = load_parameters(path) if path else load_parameters()
    return Inputs(parameters, scenario.get("overrides", {}))
