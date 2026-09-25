"""Three spreads with explicit loads, interfaces and weather exposure.

Load counts are supplied from a packing plan, never inferred from total mass.
Lay pass length equals physical horizontal product length: one product per pass.
"""
from model.records import required


def calculate(kind: str, physical_horizontal_km: float, interfaces: int, plan: dict, inputs) -> dict:
    p = lambda key: inputs.number(f"install-{kind}-{key}")
    loads_by_campaign = required(plan, "loads_per_campaign")
    if not loads_by_campaign or any(not isinstance(n, int) or n < 1 for n in loads_by_campaign):
        raise ValueError("Provide positive integer load counts for each mobilisation")
    loads = sum(loads_by_campaign)
    reloads = sum(n - 1 for n in loads_by_campaign)
    distance = float(required(plan, "port_distance_km"))
    speed = p("transit-speed")
    qlay, qbury, qsurvey = p("lay-productivity"), p("burial-productivity"), p("survey-productivity")
    if min(speed, qlay, qbury, qsurvey) <= 0:
        raise ValueError("Installation productivities and transit speed must be positive")
    offshore = (len(loads_by_campaign) * distance / speed + 2 * reloads * distance / speed
                + physical_horizontal_km / qlay + interfaces * p("interface-time")
                + int(required(plan, "splices")) * p("splice-time"))
    lay_offshore = offshore * (1 + p("weather-lay"))
    lay = len(loads_by_campaign) * (p("mobilisation-time") + p("demobilisation-time")) + loads * p("load-time") + lay_offshore
    burial_offshore = (float(required(plan, "burial_pass_km")) / qbury
                       + float(required(plan, "burial_other_offshore_days"))) * (1 + p("weather-burial"))
    burial = p("burial-fixed-time") + burial_offshore
    survey = (p("survey-fixed-time")
              + (float(required(plan, "survey_pass_km")) / qsurvey + p("survey-interface-time")) * (1 + p("weather-survey"))
              + p("rov-lay-support") * lay_offshore + p("rov-burial-support") * burial_offshore)
    cost = lay * p("lay-rate") + burial * p("burial-rate") + survey * p("survey-rate") + p("exceptional-cost")
    return {"physical_horizontal_km": physical_horizontal_km, "loads": loads, "reloads": reloads,
            "lay_days": lay, "burial_days": burial, "survey_days": survey, "installation_eur": cost}
