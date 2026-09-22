"""Load, validate and calculate values from the canonical scalar-input table."""

from __future__ import annotations

import csv
import io
import json
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = PROJECT_ROOT / "model_data" / "inputs.csv"
EXPECTED_FIELDS = ("id", "value", "unit", "kind", "price_year", "citation")
ALLOWED_KINDS = {"sourced", "assumption", "conversion", "reference"}
ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
KM_PER_MILE = Decimal("1.609344")


class ParameterError(ValueError):
    """Raised when the canonical input table is incomplete or inconsistent."""


@dataclass(frozen=True)
class Parameter:
    id: str
    raw_value: str
    value: Decimal
    unit: str
    kind: str
    price_year: int | None
    citation: str


class ParameterSet:
    """Validated parameters addressable by their human-readable IDs."""

    def __init__(self, parameters: Iterable[Parameter]):
        self._parameters = {parameter.id: parameter for parameter in parameters}

    def __iter__(self):
        return iter(self._parameters.values())

    def get(self, parameter_id: str) -> Parameter:
        try:
            return self._parameters[parameter_id]
        except KeyError as exc:
            raise ParameterError(f"Unknown model-input ID: {parameter_id}") from exc

    def number(self, parameter_id: str, expected_unit: str | None = None) -> Decimal:
        parameter = self.get(parameter_id)
        if expected_unit is not None and parameter.unit != expected_unit:
            raise ParameterError(
                f"{parameter_id} uses {parameter.unit!r}; expected {expected_unit!r}"
            )
        return parameter.value


def _detect_delimiter(text: str) -> str:
    try:
        return csv.Sniffer().sniff(text[:4096], delimiters=",;\t").delimiter
    except csv.Error as exc:
        raise ParameterError("Could not determine the input-table delimiter") from exc


def _parse_decimal(raw_value: str, delimiter: str, line_number: int) -> Decimal:
    normalized = raw_value.strip()
    if delimiter == ";" and "," in normalized and "." not in normalized:
        normalized = normalized.replace(",", ".")
    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise ParameterError(
            f"Line {line_number}: value {raw_value!r} is not numeric"
        ) from exc


def load_parameters(path: Path = DEFAULT_INPUT_PATH) -> ParameterSet:
    """Read and validate the canonical CSV (also accepting Excel-style separators)."""

    text = path.read_text(encoding="utf-8-sig")
    delimiter = _detect_delimiter(text)
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    if tuple(reader.fieldnames or ()) != EXPECTED_FIELDS:
        raise ParameterError(
            "Input columns must be exactly: " + ", ".join(EXPECTED_FIELDS)
        )

    parameters: list[Parameter] = []
    seen_ids: set[str] = set()
    for line_number, row in enumerate(reader, start=2):
        parameter_id = row["id"].strip()
        if not ID_PATTERN.fullmatch(parameter_id):
            raise ParameterError(
                f"Line {line_number}: invalid human-readable ID {parameter_id!r}"
            )
        if parameter_id in seen_ids:
            raise ParameterError(f"Line {line_number}: duplicate ID {parameter_id!r}")
        seen_ids.add(parameter_id)

        raw_value = row["value"].strip()
        if not raw_value:
            raise ParameterError(f"Line {line_number}: {parameter_id} has no value")
        value = _parse_decimal(raw_value, delimiter, line_number)

        unit = row["unit"].strip()
        if not unit:
            raise ParameterError(f"Line {line_number}: {parameter_id} has no unit")

        kind = row["kind"].strip()
        if kind not in ALLOWED_KINDS:
            raise ParameterError(
                f"Line {line_number}: {parameter_id} has invalid kind {kind!r}"
            )

        citation = row["citation"].strip().removeprefix("@")
        if kind in {"sourced", "conversion", "reference"} and not citation:
            raise ParameterError(
                f"Line {line_number}: {parameter_id} requires a citation"
            )

        raw_price_year = row["price_year"].strip()
        price_year = None
        if raw_price_year:
            if not re.fullmatch(r"\d{4}", raw_price_year):
                raise ParameterError(
                    f"Line {line_number}: invalid price year {raw_price_year!r}"
                )
            price_year = int(raw_price_year)

        if kind != "reference" and re.search(r"\b(?:EUR|USD|GBP)\b", unit):
            if price_year is None:
                raise ParameterError(
                    f"Line {line_number}: monetary input {parameter_id} needs a price year"
                )

        parameters.append(
            Parameter(
                id=parameter_id,
                raw_value=raw_value,
                value=value,
                unit=unit,
                kind=kind,
                price_year=price_year,
                citation=citation,
            )
        )

    if not parameters:
        raise ParameterError("The input table is empty")

    bibliography = (PROJECT_ROOT / "references.bib").read_text(encoding="utf-8")
    citation_keys = set(
        re.findall(r"(?m)^\s*@[A-Za-z]+\{([^,]+),", bibliography)
    )
    missing_citations = sorted(
        parameter.citation
        for parameter in parameters
        if parameter.citation and parameter.citation not in citation_keys
    )
    if missing_citations:
        raise ParameterError(
            "Citation keys missing from references.bib: "
            + ", ".join(missing_citations)
        )
    return ParameterSet(parameters)


def _decimal_text(value: Decimal, places: int, strip: bool = False) -> str:
    text = f"{value:.{places}f}"
    if strip:
        text = text.rstrip("0").rstrip(".")
    return text


def _format_parameter(parameter: Parameter) -> str:
    if parameter.unit == "fraction":
        return f"{_decimal_text(parameter.value * 100, 3, strip=True)}%"
    if parameter.unit == "fraction/year":
        return f"{_decimal_text(parameter.value * 100, 3, strip=True)}%/year"
    if parameter.unit == "year":
        suffix = "year" if parameter.value == 1 else "years"
        return f"{parameter.raw_value} {suffix}"
    if parameter.unit == "factor":
        return parameter.raw_value
    return f"{parameter.raw_value} {parameter.unit}"


def capital_recovery_factor(rate: Decimal, years: int) -> Decimal:
    growth = (Decimal(1) + rate) ** years
    return rate * growth / (growth - Decimal(1))


def hvdc_pole_current_ka(parameters: ParameterSet) -> Decimal:
    power_gw = parameters.number("hvdc-link-rated-power", "GW")
    pole_voltage_kv = parameters.number("hvdc-pole-voltage", "kV")
    return power_gw * Decimal(1_000) / (2 * pole_voltage_kv)


def hvdc_conductor_loss(
    parameters: ParameterSet,
    distance_km: Decimal,
    load_fraction: Decimal = Decimal(1),
) -> tuple[Decimal, Decimal]:
    """Return balanced-bipole conductor loss as MW and transferred-power fraction."""

    rating_mw = parameters.number("hvdc-link-rated-power", "GW") * 1000
    voltage_v = parameters.number("hvdc-pole-voltage", "kV") * 1000
    resistance = parameters.number("hvdc-cable-resistance-at-20c", "ohm/km")
    transferred_power_w = load_fraction * rating_mw * Decimal(1_000_000)
    pole_current_a = transferred_power_w / (2 * voltage_v)
    loss_w = 2 * pole_current_a**2 * resistance * distance_km
    return loss_w / Decimal(1_000_000), loss_w / transferred_power_w


def _hvdc_loss_distance(parameters: ParameterSet, target_fraction: Decimal) -> Decimal:
    _, loss_at_one_km = hvdc_conductor_loss(parameters, Decimal(1))
    return target_fraction / loss_at_one_km


def _hvdc_material_costs(parameters: ParameterSet) -> tuple[Decimal, Decimal]:
    source = parameters.number(
        "hvdc-cable-material-source-cost", "million USD/mile"
    )
    usd_per_eur = parameters.number("financial-usd-per-eur-2025", "USD/EUR")
    million_eur_per_km = source / usd_per_eur / KM_PER_MILE
    rating_gw = parameters.number("hvdc-link-rated-power", "GW")
    eur_per_kw_km = million_eur_per_km / rating_gw
    return million_eur_per_km, eur_per_kw_km


def build_quarto_variables(parameters: ParameterSet) -> dict[str, str]:
    """Create display strings while retaining numeric inputs in the canonical CSV."""

    variables: dict[str, str] = {}
    for parameter in parameters:
        variables[parameter.id] = _format_parameter(parameter)
        variables[f"{parameter.id}-value"] = parameter.raw_value

    rate = parameters.number("financial-real-wacc", "fraction/year")
    years = int(parameters.number("financial-project-life", "year"))
    crf = capital_recovery_factor(rate, years)
    variables["financial-capital-recovery-factor"] = (
        f"{_decimal_text(crf * 100, 3)}%/year"
    )
    variables["financial-capital-recovery-factor-value"] = _decimal_text(crf, 7)

    usd_per_eur = parameters.number("financial-usd-per-eur-2025", "USD/EUR")
    eur_per_usd = Decimal(1) / usd_per_eur
    variables["financial-eur-per-usd-2025"] = (
        f"{_decimal_text(eur_per_usd, 4)} EUR/USD"
    )
    variables["financial-eur-per-usd-2025-value"] = _decimal_text(
        eur_per_usd, 8
    )

    turbine_power_mw = parameters.number("wind-turbine-rated-power", "MW")
    string_power_mw = parameters.number("array-usable-string-rating", "MW")
    target_power_mw = parameters.number("array-reference-target-power", "GW") * 1000
    turbines_per_string = int(string_power_mw // turbine_power_mw)
    turbine_count = int(
        (target_power_mw / turbine_power_mw).to_integral_value(rounding="ROUND_CEILING")
    )
    installed_power_gw = Decimal(turbine_count) * turbine_power_mw / 1000
    string_count = (turbine_count + turbines_per_string - 1) // turbines_per_string
    variables["array-turbines-per-string"] = str(turbines_per_string)
    variables["array-reference-turbine-count"] = str(turbine_count)
    variables["array-reference-installed-power"] = (
        f"{_decimal_text(installed_power_gw, 2)} GW"
    )
    variables["array-reference-string-count"] = str(string_count)
    variables["array-five-turbine-string-count"] = str(
        (turbine_count + 4) // 5
    )
    variables["array-four-turbine-power"] = (
        f"{_decimal_text(turbine_power_mw * 4, 0)} MW"
    )
    variables["array-five-turbine-power"] = (
        f"{_decimal_text(turbine_power_mw * 5, 0)} MW"
    )

    pole_current = hvdc_pole_current_ka(parameters)
    variables["hvdc-full-load-pole-current"] = (
        f"{_decimal_text(pole_current, 3)} kA"
    )
    variables["hvdc-full-load-pole-current-value"] = _decimal_text(
        pole_current, 7
    )
    one_pole_power = parameters.number("hvdc-link-rated-power", "GW") / 2
    variables["hvdc-one-pole-transfer"] = (
        f"{_decimal_text(one_pole_power, 3, strip=True)} GW"
    )

    for distance in (80, 150, 250, 300):
        loss_mw, loss_fraction = hvdc_conductor_loss(
            parameters, Decimal(distance)
        )
        variables[f"hvdc-loss-{distance}km-mw"] = (
            f"{_decimal_text(loss_mw, 2)} MW"
        )
        variables[f"hvdc-loss-{distance}km-percent"] = (
            f"{_decimal_text(loss_fraction * 100, 3)}%"
        )

    half_percent_distance = _hvdc_loss_distance(parameters, Decimal("0.005"))
    variables["hvdc-half-percent-loss-distance"] = (
        f"{_decimal_text(half_percent_distance, 0)} km"
    )

    material_million_eur_km, material_eur_kw_km = _hvdc_material_costs(
        parameters
    )
    variables["hvdc-cable-material-cost-eur-per-km"] = (
        f"{_decimal_text(material_million_eur_km, 2)} million EUR/km"
    )
    variables["hvdc-cable-material-cost-eur-per-kw-km"] = (
        f"{_decimal_text(material_eur_kw_km, 2)} EUR/kW/km"
    )

    return variables


def write_quarto_variables(
    variables: dict[str, str], output_path: Path = PROJECT_ROOT / "_variables.yml"
) -> None:
    lines = [
        "# Generated from model_data/inputs.csv. Do not edit this file directly."
    ]
    for key in sorted(variables):
        lines.append(f"{key}: {json.dumps(variables[key], ensure_ascii=False)}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
