"""Piled jacket, topside and hook-up spread calculation."""
from model.records import Infeasible, required


def lift_inventory(platform: dict, case: dict) -> dict:
    """Screen an explicitly selected equal-module crane installation, one platform."""
    modules = required(case, "topside_modules_per_platform")
    if isinstance(modules, bool) or int(modules) != modules or modules < 1:
        raise ValueError("Topside lift modules must be a positive integer")
    return dict(platform, topside_lifts=int(modules), jacket_lift_t=platform["jacket_t"],
                largest_topside_lift_t=platform["topside_t"] / modules)


def calculate(platform: dict, inputs) -> dict:
    p = lambda key: inputs.number("install-platform-" + key)
    if platform["jacket_lift_t"] > p("jacket-crane") or platform["largest_topside_lift_t"] > p("topside-crane"):
        raise Infeasible("Platform lift exceeds the specified crane limit")
    count = platform["platform_count"]
    jacket = count * inputs.number("platform-jacket-site-time", "day") + p("jacket-logistics")
    topside = platform["topside_lifts"] * inputs.number("platform-topside-site-time", "day") + p("topside-logistics")
    hookup = count * p("hookup-time")
    cost = p("mobilisation-cost") + jacket * p("jacket-rate") + topside * p("topside-rate") + hookup * p("hookup-rate")
    return {"jacket_days": jacket, "topside_days": topside, "hookup_days": hookup, "installation_eur": cost}
