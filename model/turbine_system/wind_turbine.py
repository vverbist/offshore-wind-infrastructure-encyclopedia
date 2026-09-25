"""Pinned WISDEM/Mehta screening equations; owner: turbine_system/wind_turbine.qmd."""
from math import pi
from model.methodology.financial_and_price_basis import normalize_usd
from model.records import MissingInput


def mass_and_raw_cost(power_kw: float, diameter_m: float, hub_height_m: float,
                      transformer: bool, inputs) -> dict:
    if min(power_kw, diameter_m, hub_height_m) <= 0:
        raise ValueError("Turbine dimensions and capacity must be positive")
    p = lambda name: inputs.number("turbine-" + name)
    n = int(p("blade-count"))
    omega = p("tip-speed") / (diameter_m / 2)
    torque = power_kw * 1000 / p("drivetrain-efficiency") / omega
    # Ratio of rated wind speeds: common rho, Cp and drivetrain efficiency cancel.
    speed_ratio = ((power_kw / p("reference-power")) / (diameter_m / p("reference-diameter")) ** 2) ** (1 / 3)
    blade = p("reference-blade-mass") * (diameter_m / p("reference-diameter")) ** p("blade-mass-exponent") * speed_ratio**2
    mass = {"blade": blade, "hub": p("hub-blade") * blade + p("hub-offset"),
            "pitch": p("pitch-bearing") * (p("pitch-blade") * n * blade + p("pitch-bearing-offset")) + p("pitch-offset"),
            "spinner": p("spinner-diameter") * diameter_m + p("spinner-offset"),
            "lss": p("lss-scale") * (blade * power_kw / 1000) ** p("lss-exponent") + p("lss-offset"),
            "bearings": p("bearing-count") * p("bearing-scale") * diameter_m ** p("bearing-exponent"),
            "brake": p("brake-torque") * torque,
            "generator": p("reference-generator-mass") * torque / p("reference-torque"),
            "bedplate": diameter_m ** p("bedplate-exponent"),
            "yaw": p("yaw-multiplier") * p("yaw-scale") * diameter_m ** p("yaw-exponent"),
            "hvac": p("hvac-power") * power_kw,
            "cover": p("cover-power") * power_kw + p("cover-offset"),
            "transformer": p("transformer-power") * power_kw + p("transformer-offset") if transformer else 0}
    mass["platforms"] = p("platform-bedplate") * mass["bedplate"] + p("crane-mass")
    tower_length = hub_height_m - p("interface-height")
    if tower_length <= 0 or min(mass.values()) < 0:
        raise ValueError("Turbine geometry is outside the screening equation range")
    mass["tower"] = p("tower-scale") * tower_length ** p("tower-exponent")

    def raw_rate(name):
        # Legacy USD coefficients are relative calibration weights, never adopted prices.
        return inputs.reference_number("turbine-cost-" + name)

    costs = {name: value * raw_rate(name) for name, value in mass.items()}
    crane_cost = inputs.parameters.get("turbine-cost-crane").value
    # WISDEM prices the crane separately from the service-platform mass.
    costs["platforms"] = (mass["platforms"] - p("crane-mass")) * raw_rate("platforms")
    if crane_cost is not None:
        costs["platforms"] += inputs.reference_number("turbine-cost-crane", "USD")
    share = p("blade-mass-cost-share")
    anchor = p("reference-blade-mass") * raw_rate("blade")
    costs["blade"] = n * anchor * (share * blade / p("reference-blade-mass")
                                   + (1 - share) * (diameter_m / p("reference-diameter")) ** p("blade-cost-diameter-exponent"))
    costs["connections"] = power_kw * raw_rate("connections")
    costs["controls"] = power_kw * raw_rate("controls")
    rotor = n * blade + mass["hub"] + mass["pitch"] + mass["spinner"]
    nacelle = sum(value for name, value in mass.items() if name not in {"blade", "hub", "pitch", "spinner", "tower"})
    return {"masses_kg": mass, "raw_cost_weights": costs, "raw_cost_complete": crane_cost is not None, "rotor_t": rotor / 1000,
            "known_nacelle_t": nacelle / 1000, "known_turbine_t": (rotor + nacelle + mass["tower"]) / 1000,
            "rated_torque_nm": torque, "rated_rpm": omega * 60 / (2 * pi)}


def calculate(power_kw: float, diameter_m: float, hub_height_m: float, inputs) -> dict:
    """Common conventional-turbine baseline; architecture structural feedback is deferred."""
    result = mass_and_raw_cost(power_kw, diameter_m, hub_height_m, True, inputs)
    if not result["raw_cost_complete"]:
        result["supply_usd2022"] = None
        return result
    ref_power = inputs.number("turbine-calibration-power", "kW")
    reference = mass_and_raw_cost(ref_power, inputs.number("turbine-calibration-diameter", "m"),
                                  inputs.number("turbine-calibration-hub-height", "m"), True, inputs)
    raw, raw_ref = result["raw_cost_weights"], reference["raw_cost_weights"]
    rna_factor = ref_power * inputs.number("turbine-calibration-rna-cost", "USD/kW") / sum(v for k, v in raw_ref.items() if k != "tower")
    tower_factor = ref_power * inputs.number("turbine-calibration-tower-cost", "USD/kW") / raw_ref["tower"]
    result["supply_usd2022"] = sum(v * (tower_factor if k == "tower" else rna_factor) for k, v in raw.items())
    result["rna_calibration_factor"], result["tower_calibration_factor"] = rna_factor, tower_factor
    return result


def supply_eur(result: dict, count: int, inputs) -> float:
    if result["supply_usd2022"] is None:
        raise MissingInput("turbine-cost-crane: separate crane cost is absent from the documented coefficient table")
    return count * normalize_usd(result["supply_usd2022"], inputs.positive("financial-usd-escalation-2022-2025", "factor"), inputs)
