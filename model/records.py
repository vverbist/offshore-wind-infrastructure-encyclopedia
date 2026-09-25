"""Small records shared by the calculation modules."""
from dataclasses import dataclass, field
from typing import Any

import pandas as pd


class MissingInput(ValueError):
    """An adopted parameter or scenario choice is still required."""


class Infeasible(ValueError):
    """A supplied case violates the model's physical constraints."""


@dataclass
class CostLine:
    component: str
    category: str
    amount_eur: float | None
    note: str = ""


@dataclass
class CaseResult:
    name: str
    architecture: str
    status: str = "not_parameterized"
    reasons: list[str] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)
    physical: dict[str, Any] = field(default_factory=dict)
    costs: list[CostLine] = field(default_factory=list)
    tables: dict[str, pd.DataFrame] = field(default_factory=dict)
    inputs: list[dict] = field(default_factory=list)
    scenario: dict = field(default_factory=dict)


def required(record: dict, key: str):
    if key not in record:
        raise MissingInput(f"Scenario field required: {key}")
    return record[key]
