"""One scenario, evaluated in the documented physical dependency order."""
from dataclasses import asdict
from pathlib import Path
from math import ceil
import numpy as np
import pandas as pd

from .inputs import Inputs
from .records import CaseResult, CostLine, MissingInput, Infeasible, required
from .wind_resource_and_layout import wake_modelling_and_spacing as layout_model
from .wind_resource_and_layout.wind_resource_and_weibull import WindStates
from .turbine_system import wind_turbine, foundation
from .electrical_infra import infield_ac_cables as ac
from .hydrogen_production import stack, balance_of_plant as bop, elx_power_electronics, dc_integration
from .hydrogen_infra import compressor, hydrogen_pipelines as pipe, infield_infrastructure as network
from .hydrogen_infra.pipeline_pressure_and_capacity import check_sections
from .platforms import platform_material_capex as platform
from .offshore_installation import turbine_and_foundation_installation as turbine_install
from .offshore_installation import cable_and_pipeline_installation as line_install
from .offshore_installation import platform_and_substation_installation as platform_install
from .methodology.energy_availability_and_annualisation import delivered_mass
from .methodology.system_boundary_and_lcoe import summarize


def run_case(scenario: dict, inputs: Inputs, base: Path) -> CaseResult:
    """Return independent intermediate results even when downstream evidence is missing.

    MissingInput is the only recoverable data condition. Programming errors and
    malformed inputs raise normally; physical infeasibility is reported explicitly.
    """
    case = scenario.get("case", {})
    architecture = required(case, "architecture")
    if architecture not in {"centralised", "decentralised"}:
        raise ValueError("This draft supports centralised and decentralised hydrogen")
    central = architecture == "centralised"
    result = CaseResult(case.get("name", architecture), architecture,
                        inputs=inputs.records(), scenario=scenario)
    infeasible = []

    def step(name, function):
        try:
            return function()
        except MissingInput as exc:
            result.reasons.append(f"{name}: {exc}")
        except Infeasible as exc:
            infeasible.append(f"{name}: {exc}")
        return None

    def cost(component, category, function):
        amount = step(component + " " + category, function)
        result.costs.append(CostLine(component, category, amount,
                                    "not parameterized" if amount is None else ""))
        return amount

    def dependent(value, name):
        if value is None:
            raise MissingInput(f"Upstream {name} is unavailable")
        return value

    site = scenario.get("site", {})
    machine = scenario.get("turbine", {})
    wind_case = scenario.get("wind", {})
    h2 = scenario.get("hydrogen", {})
    elx = scenario.get("electrolysis", {})
    coordinates = step("layout", lambda: layout_model.layout(site, base))
    turbine_kw = float(machine.get("rated_power_kw", inputs.number("wind-turbine-rated-power", "MW") * 1000))
    if turbine_kw <= 0:
        raise ValueError("Turbine rating must be positive")
    depth = step("water depth", lambda: float(required(site, "water_depth_m")))
    if coordinates is None:
        result.reasons.extend(infeasible)
        result.status = "infeasible" if infeasible else "not_parameterized"
        result.summary = summarize([], None, inputs)
        return result
    count = len(coordinates)
    farm_kw = count * turbine_kw
    result.tables["coordinates"] = coordinates
    result.physical.update(turbine_count=count, installed_wind_kw=farm_kw)
    overplant = step("stack sizing", lambda: float(required(elx, "overplant_factor")))
    if overplant is not None and overplant <= 0:
        raise ValueError("Stack overplant factor must be positive")
    locations = 1 if central else count
    interface = "central" if central else step("electrical interface", lambda: required(elx, "interface"))
    if not central and interface not in {None, "conservative", "converter_reduced"}:
        raise ValueError("Unsupported turbine-level interface")
    eff = step("electrical conversion", lambda: elx_power_electronics.efficiency(inputs) if central
               else dc_integration.efficiency(dependent(interface, "electrical interface"), inputs))
    wind = None
    if "power_states_file" in wind_case:
        wind = step("wind states", lambda: WindStates.read(base / wind_case["power_states_file"],
                    coordinates.turbine.tolist(), inputs.number("annual-hours", "h/year")))
    else:
        wake_result = step("wake calculation", lambda: layout_model.calculate_wakes(coordinates, wind_case, machine, base, inputs))
        if wake_result:
            wind, version = wake_result
            result.physical["pywake_version"] = version
    if wind is not None and np.any(wind.power_kw > turbine_kw * (1 + 1e-9)):
        raise ValueError("Wind-state power exceeds turbine rated power")
    def peak_basis():
        dependent(wind, "wind power states")
        design_ids = required(wind_case, "design_state_ids")
        if not design_ids or any(str(state) not in wind.state_ids for state in design_ids):
            raise ValueError("Declare the peak-duty design states present in the wind-power table")
        return True
    peak_ready = step("peak sizing basis", peak_basis)

    routes = None
    if central:
        routes = step("AC routes", lambda: ac.radial_routes(coordinates, turbine_kw,
            (float(required(site, "collection_x_m")), float(required(site, "collection_y_m"))),
            dependent(depth, "water depth"), inputs))
        if routes is not None:
            result.tables["collection_sections"] = routes
        bays = step("AC interface", lambda: int(required(scenario.get("platform", {}), "feeder_bays")))
        strings = ceil(count / max(1, int(inputs.number("array-usable-string-rating", "MW") * 1000 // turbine_kw)))
        result.physical["ac_strings"] = strings
        if bays is not None and bays < strings:
            infeasible.append("AC string count exceeds the declared platform feeder bays")

    curve = step("stack curve", lambda: stack.StackCurve.read(base / required(elx, "stack_curve_file")))
    comp_energy = step("compression energy", lambda: compressor.specific_energy(
        float(required(h2, "stack_outlet_bar")), float(required(h2, "injection_bar")), inputs))
    bop_package = step("BOP sizing", lambda: bop.size(farm_kw, locations, inputs))
    if bop_package:
        result.physical["bop"] = asdict(bop_package)

    hydrogen = None
    packages = None
    if wind is not None and all(v is not None for v in (eff, curve, comp_energy, overplant)):
        def operations():
            if central:
                losses = ac.loss_kw(dependent(routes, "AC routes"), wind.power_kw, wind.turbine_ids, inputs)
                bus = (wind.power_kw.sum(axis=1) - losses)[:, None]
            else:
                losses = np.zeros(len(wind.hours))
                bus = wind.power_kw.copy()
            operating_rows = []
            for state in range(len(wind.hours)):
                for location in range(locations):
                    operation = stack.operate(float(bus[state, location]) * eff, farm_kw / locations * overplant,
                                              curve, comp_energy, inputs)
                    operating_rows.append({"state": wind.state_ids[state], "location": str(location),
                        "hours": float(wind.hours[state]), "input_kw": float(bus[state, location]),
                        "conversion_loss_kw": float(bus[state, location]) * (1 - eff), **asdict(operation)})
            table = pd.DataFrame(operating_rows)
            result.tables["operation"] = table
            result.tables["wind_states"] = pd.DataFrame({"state": wind.state_ids, "hours": wind.hours,
                **{name: wind.power_kw[:, i] for i, name in enumerate(wind.turbine_ids)}})
            result.summary["generator_energy_mwh"] = float(np.dot(wind.power_kw.sum(axis=1), wind.hours) / 1000)
            result.summary["collection_loss_mwh"] = float(np.dot(losses, wind.hours) / 1000)
            for column in ("stack_kw", "bop_kw", "compressor_kw", "curtailed_kw", "conversion_loss_kw"):
                result.summary[column.replace("_kw", "_mwh")] = float((table[column] * table.hours).sum() / 1000)
            return table.hydrogen_kg_h.to_numpy().reshape(-1, locations), table.compressor_kw.to_numpy().reshape(-1, locations)

        energy = step("hydrogen operation", operations)
        if energy is not None:
            hydrogen, compression_power = energy
            result.summary["preavailability_hydrogen_kg_year_bol"] = float(np.dot(hydrogen.sum(axis=1), wind.hours))
            if peak_ready:
                packages = compressor.size(compression_power.max(axis=0).tolist(), inputs)
                result.physical["compressors"] = [asdict(p) for p in packages]
            result.physical["stack_installed_kw"] = locations * result.tables["operation"].installed_kw.iloc[0]

    def hydrogen_routes():
        flows = dependent(hydrogen, "turbine hydrogen flows")
        collection = scenario.get("collection", {})
        nodes = pd.read_csv(base / required(collection, "nodes_file"), dtype={"node": str})
        sections, section_flows = network.section_inventory(base / required(collection, "sections_file"),
            coordinates, nodes, flows, str(required(collection, "sink")))
        result.tables["collection_sections"] = sections  # Keep inventory even if capacity fails.
        injection = float(required(h2, "injection_bar"))
        roots = sections[sections["from"].isin(coordinates.turbine)]
        if (roots.inlet_bar > injection).any():
            raise Infeasible("Collection inlet pressure exceeds turbine compressor discharge")
        checked = check_sections(sections, inputs)
        sink_edges = checked[(checked["to"] == str(collection["sink"])) & (checked.flow_share > 0)]
        export_pressure = float(required(h2, "export_inlet_bar"))
        if (sink_edges.outlet_bar < export_pressure).any():
            raise Infeasible("Collection pressure cannot support export inlet pressure")
        result.tables["collection_sections"] = checked
        return checked

    if not central:
        routes = step("hydrogen collection", hydrogen_routes)

    def export_inventory():
        dependent(peak_ready, "peak-duty design states")
        production = dependent(hydrogen, "hydrogen production")
        inlet = float(required(h2, "injection_bar" if central else "export_inlet_bar"))
        length = float(required(h2, "export_length_km"))
        capacity = pipe.capacity_kg_h(float(required(h2, "export_diameter_m")), inlet,
                                    float(required(h2, "delivery_bar")), length * 1000, inputs)
        peak = float(production.sum(axis=1).max())
        number = pipe.export_count(peak, capacity)
        return {"capacity_per_pipe_kg_h": capacity, "peak_kg_h": peak, "pipeline_count": number,
                "route_km": length, "physical_km": number * length,
                "capacity_margin_kg_h": number * capacity - peak}

    export = step("hydrogen export", export_inventory)
    if export:
        result.physical["export"] = export

    turbine = step("turbine screening", lambda: wind_turbine.calculate(turbine_kw,
                   float(required(machine, "rotor_diameter_m")), float(required(machine, "hub_height_m")), inputs))
    if turbine:
        result.physical["turbine_screening"] = turbine
    # Common baseline supported mass: architecture feedback is a deferred sensitivity.
    complete_mass = step("complete turbine mass", lambda: dependent(turbine, "turbine mass")["known_turbine_t"]
                         + inputs.number("turbine-electrical-additional-mass", "t"))
    footing = step("foundation", lambda: foundation.calculate(dependent(complete_mass, "complete supported mass"),
                    dependent(depth, "water depth"), inputs))
    if footing:
        result.physical["foundation"] = footing

    cost("turbine", "supply", lambda: wind_turbine.supply_eur(dependent(turbine, "turbine cost"), count, inputs)
         + (0 if central else count * inputs.number("turbine-electrical-cost-adjustment", "EUR/turbine")))
    cost("foundation", "supply", lambda: foundation.supply_eur(dependent(footing, "foundation cost"), count, inputs))
    cost("stack", "supply", lambda: locations * ceil(farm_kw / locations * dependent(overplant, "overplant factor")
          / inputs.positive("stack-module-rating", "kW")) * inputs.number("stack-module-rating", "kW")
          * inputs.number("stack-purchase-unit-cost", "EUR/kW"))
    cost("bop", "supply", lambda: bop.supply_cost(dependent(bop_package, "BOP sizing"), inputs))
    cost("conversion", "supply", lambda: elx_power_electronics.supply_cost(farm_kw, inputs) if central
         else dc_integration.supply_cost(dependent(interface, "interface"), farm_kw, inputs))
    cost("compressor", "supply", lambda: compressor.supply_cost(dependent(packages, "compressor sizing"), inputs))

    private_pipeline_curve = None

    def pipeline_rate(diameter_m, pressure_bar):
        nonlocal private_pipeline_curve
        private = scenario.get("data", {}).get("pipeline_cost_module")
        if private:
            # Preserve the existing confidential callable without copying its quote data.
            if private_pipeline_curve is None:
                import importlib.util
                path = base / private
                spec = importlib.util.spec_from_file_location("private_pipeline_cost", path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                private_pipeline_curve = module.pipeline_cost_curve
            # The fit is read at operating pressure in bar(g), without a design
            # margin (project owner, 2026-09-25); model pressures are bar(a).
            gauge_bar = pressure_bar - inputs.positive("standard-atmospheric-pressure", "bar")
            raw = float(private_pipeline_curve(gauge_bar, diameter_m / 0.0254))
            return raw * inputs.positive("pipeline-quote-to-eur2025", "factor")
        return inputs.number("pipeline-supply-unit-cost", "EUR/m")

    collection_owner = "ac-collection" if central else "hydrogen-collection"
    def collection_supply():
        table = dependent(routes, "collection routes")
        if central:
            return ac.supply_cost(table, inputs)
        return sum(pipe.supply_cost(row.physical_km, pipeline_rate(row.diameter_m, row.inlet_bar)) for row in table.itertuples())
    cost(collection_owner, "supply", collection_supply)
    cost("hydrogen-export", "supply", lambda: pipe.supply_cost(dependent(export, "export inventory")["physical_km"],
         pipeline_rate(float(required(h2, "export_diameter_m")), float(required(h2, "injection_bar" if central else "export_inlet_bar")))))
    cost("pipeline-connections", "supply", lambda: inputs.number("pipeline-connections-cost", "EUR"))
    if not central:
        cost("pipeline-manifold", "supply", lambda: inputs.number("pipeline-manifold-cost", "EUR"))
    cost("hydrogen-receipt", "supply", lambda: inputs.number("hydrogen-receipt-supply-cost", "EUR"))
    cost("hydrogen-receipt", "installation", lambda: inputs.number("hydrogen-receipt-installation-cost", "EUR"))
    platform_inventory = None
    if central:
        platform_inventory = step("platform inventory", lambda: platform.inventory(scenario.get("platform", {}), inputs))
        if platform_inventory:
            result.physical["platform"] = platform_inventory
        cost("platform", "supply", lambda: platform.supply_cost(dependent(platform_inventory, "platform inventory"), inputs)["total_eur"])

    installation = scenario.get("installation", {})
    for kind in ("turbine", "foundation"):
        def campaign(kind=kind):
            mass = dependent(complete_mass, "complete turbine mass")
            if kind == "foundation":
                lift = dependent(footing, "monopile mass")["monopile_t"]
                mass = lift + inputs.number("foundation-transition-piece-mass", "t")
            else:
                lift = dependent(turbine, "nacelle mass")["known_nacelle_t"] + inputs.number("turbine-electrical-additional-mass", "t")
                if not central:
                    mass += inputs.number("turbine-hydrogen-equipment-mass", "t")
                    # Includes the declared turbine and hydrogen-equipment lifting arrangement.
                    lift = inputs.positive("turbine-distributed-maximum-lift", "t")
            record = turbine_install.campaign(kind, count, mass, lift,
                float(required(installation, "port_distance_km")), float(required(installation, "intersite_distance_km")), inputs)
            result.physical[kind + "_installation"] = record
            return record["installation_eur"]
        cost(kind, "installation", campaign)

    def collection_installation():
        table = dependent(routes, "collection routes")
        # Supply verticals are not lay-pass length.
        if central:
            horizontal = float(table.horizontal_km.sum()) * (1 + inputs.number("array-route-allowance", "fraction"))
        else:
            horizontal = float((table.physical_km - table.vertical_m / 1000).sum())
        record = line_install.calculate("ac" if central else "tcp", horizontal, len(table),
                                         installation.get("collection", {}), inputs)
        result.physical["collection_installation"] = record
        return record["installation_eur"]
    cost(collection_owner, "installation", collection_installation)

    def export_installation():
        record = dependent(export, "export inventory")
        campaign = line_install.calculate("tcp", record["physical_km"], record["pipeline_count"],
                                          installation.get("export", {}), inputs)
        result.physical["export_installation"] = campaign
        return campaign["installation_eur"]
    cost("hydrogen-export", "installation", export_installation)
    if central:
        cost("platform", "installation", lambda: platform_install.calculate(dependent(platform_inventory, "platform inventory"), inputs)["installation_eur"])

    # Annual allowances belong to equipment; neither architecture receives a blanket premium.
    for line in list(result.costs):
        if line.category != "supply":
            continue
        owner = line.component
        if owner == "turbine":
            owner = "turbine-central" if central else "turbine-distributed"
        if owner == "conversion":
            owner = "central-conversion" if central else f"{(interface or 'conservative').replace('_', '-')}-conversion"
        cost(line.component, "annual_opex", lambda line=line, owner=owner:
             dependent(line.amount_eur, line.component + " supply cost") * inputs.number(owner + "-opex-rate", "fraction/year"))

    def replacement():
        life = inputs.positive("stack-replacement-life", "year")
        count_events = max(0, ceil(inputs.positive("financial-project-life", "year") / life) - 1)
        if not count_events:
            return 0.0
        initial = next(c.amount_eur for c in result.costs if c.component == "stack" and c.category == "supply")
        return count_events * (dependent(initial, "stack supply cost") * inputs.fraction("stack-replacement-cost-fraction")
                               + inputs.number("stack-replacement-intervention-cost", "EUR"))
    cost("stack", "replacement", replacement)

    def annual_delivery():
        flows = dependent(hydrogen, "hydrogen production")
        production = inputs.fraction("central-production-availability" if central else "distributed-production-availability")
        compression = inputs.fraction("compressor-central-availability" if central else "compressor-distributed-availability")
        transport = inputs.fraction("hydrogen-export-availability") * inputs.fraction("hydrogen-receipt-availability")
        if central:
            transport *= inputs.fraction("ac-collection-availability")
        else:
            transport *= inputs.fraction("hydrogen-collection-availability")
        return delivered_mass(flows, wind.hours, np.full(locations, production * compression), transport)
    annual = step("annual availability", annual_delivery)
    result.summary["delivered_hydrogen_kg_year_bol"] = annual
    def lifetime_factor():
        table = dependent(result.tables.get("operation"), "stack operation")
        installed_kw = locations * float(table.installed_kw.iloc[0])
        full_load_hours = float((table.stack_kw * table.hours).sum()) / installed_kw
        factor, interval = stack.lifetime_production_factor(
            full_load_hours, inputs.positive("financial-project-life", "year"), inputs)
        result.physical["stack_full_load_hours_per_year"] = full_load_hours
        result.physical["stack_degradation_interval_years"] = interval if interval != float("inf") else None
        result.summary["stack_lifetime_production_factor"] = factor
        return factor
    lifecycle_mass = step("lifetime production", lambda: dependent(annual, "annual delivered hydrogen")
                          * lifetime_factor())
    result.summary["delivered_hydrogen_kg_year_lifetime_average"] = lifecycle_mass
    if lifecycle_mass is not None:
        hhv_energy = lifecycle_mass * inputs.number("hydrogen-hhv", "kWh/kg") / 1000
        result.summary["delivered_hydrogen_mwh_hhv_year"] = hhv_energy
        result.summary["spatial_yield_mwh_hhv_km2_year"] = hhv_energy / float(site["farm_area_km2"])
    result.summary.update(summarize(result.costs, lifecycle_mass, inputs))
    result.reasons.extend(infeasible)
    result.reasons = list(dict.fromkeys(result.reasons))
    result.status = "infeasible" if infeasible else ("not_parameterized" if result.reasons else "feasible")
    if result.status != "feasible":
        result.summary["lcoh_eur_kg"] = None
        result.summary.pop("lcoh_eur_mwh_hhv", None)
    result.summary["method_limits"] = ["Existing TCP hydraulics retained provisionally; no product qualification claim",
        "Beginning-of-life operating states; lifetime production adjustment remains an explicit unresolved input",
        "No redundancy credit or structural-feedback sensitivity", "Aggregate availability; no failure-state redispatch",
        "AC cable losses use upstream generated power without a load-flow iteration"]
    return result
