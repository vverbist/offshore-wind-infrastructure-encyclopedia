"""Synthetic verification cases, not adopted article scenarios or model inputs."""
from dataclasses import replace
from decimal import Decimal
import copy
import importlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from model.inputs import Inputs, load_inputs, read_scenario
from model.records import MissingInput, Infeasible, CostLine
from model_data.parameters import ParameterSet, load_parameters
from model.hydrogen_production import stack
from model.hydrogen_production.stack import StackCurve, operate
from model.hydrogen_production.balance_of_plant import size as bop_size
from model.hydrogen_infra.compressor import specific_energy, stages, size as compressor_size
from model.hydrogen_infra.hydrogen_pipelines import capacity_kg_h, export_count
from model.hydrogen_infra.infield_infrastructure import section_inventory
from model.turbine_system.wind_turbine import calculate as turbine
from model.turbine_system.foundation import calculate as foundation
from model.platforms import platform_material_capex as platform
from model.offshore_installation import platform_and_substation_installation as platform_install
from model.methodology.system_boundary_and_lcoe import summarize
from model.methodology.financial_and_price_basis import annual_cost
from model.methodology.energy_availability_and_annualisation import delivered_mass
from model.offshore_installation.turbine_and_foundation_installation import campaign
from model.workflow import run_case
from model.wind_resource_and_layout.wind_resource_and_weibull import WindStates
from model.reporting import write_result

ROOT = Path(__file__).resolve().parents[1]


def synthetic_inputs(values=None, fill_missing=False):
    """Test-only numbers deliberately live outside the adopted parameter table."""
    values = values or {}
    parameters = []
    for parameter in load_parameters():
        value = values.get(parameter.id, 1 if fill_missing and parameter.value is None else parameter.value)
        parameters.append(replace(parameter, value=None if value is None else Decimal(str(value)),
                                  raw_value="" if value is None else str(value)))
    return Inputs(ParameterSet(parameters))


class Components(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = load_inputs({})
        cls.curve = StackCurve.read(ROOT / "numerical_inputs/pem_polarisation_curve.xlsx")

    def test_unknown_and_reference_costs_are_not_adopted(self):
        with self.assertRaises(MissingInput):
            self.inputs.number("stack-purchase-unit-cost")
        with self.assertRaises(MissingInput):
            self.inputs.number("compressor-legacy-cost-anchor")

    def test_override_preserves_baseline(self):
        modified = load_inputs({"overrides": {"bop-block-limit": 20000}})
        self.assertEqual(modified.number("bop-block-limit"), 20000)
        record = next(r for r in modified.records() if r["id"] == "bop-block-limit")
        self.assertEqual(record["baseline_value"], "100000")
        self.assertTrue(record["overridden"])
        with self.assertRaises(ValueError):
            load_inputs({"overrides": {"stack-purchase-unit-cost": 1}})

    def test_reference_weight_override_is_used_without_adopting_a_price(self):
        changed = load_inputs({"overrides": {"turbine-cost-blade": 29.2}})
        base = turbine(15000, 236, 133, self.inputs)
        result = turbine(15000, 236, 133, changed)
        self.assertEqual(result["raw_cost_weights"]["blade"], 2 * base["raw_cost_weights"]["blade"])
        self.assertIsNone(result["supply_usd2022"])

    def test_stack_zero_low_and_rated_energy_balance(self):
        work = specific_energy(30, 150, self.inputs)
        for power in (0, 50, 150, 1000, 15000, 50000):
            with self.subTest(power=power):
                result = operate(power, 15000, self.curve, work, self.inputs)
                self.assertAlmostEqual(result.stack_kw + result.bop_kw + result.compressor_kw + result.curtailed_kw, power, places=7)
                self.assertLessEqual(result.active_modules, result.installed_modules)
                self.assertGreaterEqual(result.curtailed_kw, 0)
                self.assertLessEqual(result.current_density_a_cm2, 3)
        self.assertEqual(operate(50, 1000, self.curve, work, self.inputs).active_modules, 0)

    def test_curve_power_not_current_fraction(self):
        result = operate(1000, 1000, self.curve, 0, self.inputs)
        j = result.current_density_a_cm2
        expected_kw = 1000 * j * self.curve.voltage_at(j) / (3 * self.curve.voltage_at(3))
        self.assertAlmostEqual(result.stack_kw, expected_kw)
        self.assertAlmostEqual(result.hydrogen_kg_h * 39.4, result.stack_kw * 1.481 / self.curve.voltage_at(j))

    def test_overplanting_changes_stack_not_bop(self):
        a = operate(15000, 15000, self.curve, 1, self.inputs)
        b = operate(15000, 30000, self.curve, 1, self.inputs)
        self.assertGreater(b.hydrogen_kg_h, a.hydrogen_kg_h)
        self.assertEqual(a.installed_modules, 15)
        self.assertEqual(b.installed_modules, 30)

    def test_block_and_train_thresholds(self):
        self.assertEqual(bop_size(100000, 1, self.inputs).blocks, 1)
        self.assertEqual(bop_size(100001, 1, self.inputs).blocks, 2)
        self.assertEqual(bop_size(100000, 10, self.inputs).blocks, 10)
        sized = compressor_size([0, 1000, 1001], self.inputs)
        self.assertEqual([p.trains for p in sized], [0, 1, 2])
        self.assertEqual(sized[-1].motor_kw_per_train, 500.5)

    def test_compressor_stage_boundary_and_zero_work(self):
        self.assertEqual(stages(30, 99, self.inputs), 1)
        self.assertEqual(stages(30, 100, self.inputs), 2)
        self.assertEqual(specific_energy(30, 30, self.inputs), 0)
        self.assertAlmostEqual(specific_energy(30, 150, self.inputs), 0.8584713457, places=7)

    def test_pipeline_monotonicity_and_count(self):
        small = capacity_kg_h(0.15, 150, 66, 80000, self.inputs)
        large = capacity_kg_h(0.20, 150, 66, 80000, self.inputs)
        self.assertGreater(large, small)
        self.assertLess(capacity_kg_h(0.20, 100, 66, 80000, self.inputs), large)
        self.assertEqual(export_count(large, large), 1)
        self.assertEqual(export_count(large + 1, large), 2)

    def test_documented_turbine_and_foundation_masses(self):
        result = turbine(15000, 236, 133, self.inputs)
        self.assertAlmostEqual(result["known_turbine_t"], 1552.8, delta=0.1)
        self.assertAlmostEqual(result["known_nacelle_t"], 864.1, delta=0.1)
        self.assertIsNone(result["supply_usd2022"])
        pile = foundation(1877, 30, self.inputs)
        self.assertEqual(pile["monopile_t"], 1318)

    def test_turbine_calibration_reproduces_anchor(self):
        inputs = synthetic_inputs({"turbine-cost-crane": 10000})
        result = turbine(12000, 216, 137, inputs)
        self.assertAlmostEqual(result["supply_usd2022"], 12000 * (1462 + 238))

    def test_platform_mass_chain_cost_and_module_step(self):
        values = {"platform-topside-structure-unit-cost": 10,
                  "platform-yard-integration-cost": 2000, "platform-jacket-unit-cost": 5,
                  "platform-pile-unit-cost": 2}
        inputs = synthetic_inputs(values)
        record = platform.inventory({"topside_mass_t": 30000}, 28, inputs)
        self.assertEqual(record["topside_structure_t"], 15000)
        self.assertAlmostEqual(record["jacket_t"], 5221.93, places=2)
        self.assertAlmostEqual(record["piles_t"], 0.0235 * (30000 + record["jacket_t"]) + 534)
        self.assertNotIn("topside_lifts", record)
        cost = platform.supply_cost(record, inputs)
        self.assertAlmostEqual(cost["total_eur"], 15000 * 10 + record["jacket_t"] * 5 + record["piles_t"] * 2 + 2000)
        deeper = platform.inventory({"topside_mass_t": 30000}, 56, inputs)
        self.assertAlmostEqual(deeper["jacket_t"], 2 * record["jacket_t"])
        self.assertGreater(deeper["piles_t"], record["piles_t"])
        single = platform_install.lift_inventory(record, {"topside_modules_per_platform": 1})
        split = platform_install.lift_inventory(record, {"topside_modules_per_platform": 2})
        self.assertEqual((single["topside_lifts"], split["topside_lifts"]), (1, 2))
        self.assertEqual(split["largest_topside_lift_t"], 15000)
        crane = synthetic_inputs({"install-platform-jacket-crane": 10000,
                                  "install-platform-topside-crane": 20000}, fill_missing=True)
        with self.assertRaises(Infeasible):
            platform_install.calculate(single, crane)
        self.assertGreater(platform_install.calculate(split, crane)["installation_eur"], 0)
        with self.assertRaises(ValueError):
            platform.inventory({"count": 2, "topside_mass_t": 30000}, 28, inputs)

    def test_platform_missing_costs_preserve_known_subtotals(self):
        record = platform.inventory({"topside_mass_t": 30000}, 28, self.inputs)
        inputs = synthetic_inputs({"platform-topside-structure-unit-cost": 10,
                                   "platform-jacket-unit-cost": 5, "platform-pile-unit-cost": 2})
        cost = platform.supply_cost(record, inputs)
        self.assertIsNone(cost["yard_integration_eur"])
        self.assertIsNone(cost["total_eur"])
        self.assertEqual(cost["known_subtotal_eur"], cost["structure_eur"])
        self.assertIn("platform-yard-integration-cost", cost["missing_inputs"][0])
        with self.assertRaises(MissingInput):
            self.inputs.number("platform-dnv-topside-rate")
        with self.assertRaises(MissingInput):
            platform.estimate_topside_mass(2, self.inputs)

    def test_platform_mass_scaling_reference_and_exponent(self):
        inputs = synthetic_inputs({"platform-reference-topside-mass": 10000,
                                   "platform-reference-power": 0.5})
        self.assertEqual(platform.estimate_topside_mass(0.5, inputs), 10000)
        self.assertEqual(platform.estimate_topside_mass(2, inputs), 40000)
        nonlinear = Inputs(inputs.parameters, {"platform-mass-scaling-exponent": 0.5})
        self.assertEqual(platform.estimate_topside_mass(2, nonlinear), 20000)

    def test_platform_epci_mass_interface_and_reference(self):
        direct = platform.epci_inventory({"equipment_mass_t": 15000}, self.inputs)
        inferred = platform.epci_inventory({"topside_mass_t": 30000}, self.inputs, 28)
        self.assertEqual(direct["equipment_t"], inferred["equipment_t"])
        self.assertEqual(direct["installation_feasibility"], "not_assessed")
        expected = 60000 * 1.024 * 1.021 * 15000
        self.assertAlmostEqual(platform.epci_cost(direct, self.inputs)["total_eur"], expected)
        deep = platform.epci_inventory({"topside_mass_t": 30000}, self.inputs, 56)
        self.assertEqual(platform.epci_cost(inferred, self.inputs), platform.epci_cost(deep, self.inputs))
        for case in ({}, {"equipment_mass_t": 0}, {"topside_mass_t": float('nan')},
                     {"equipment_mass_t": 1, "topside_mass_t": 2}, {"count": 2, "topside_mass_t": 10}):
            with self.assertRaises(ValueError):
                platform.epci_inventory(case, self.inputs)

    def test_platform_epci_exponent_preserves_anchor(self):
        nonlinear = Inputs(self.inputs.parameters, {"platform-epci-cost-scaling-exponent": 0.5})
        anchor = platform.epci_inventory({"equipment_mass_t": 15000}, self.inputs)
        larger = platform.epci_inventory({"equipment_mass_t": 60000}, self.inputs)
        baseline = platform.epci_cost(anchor, self.inputs)["total_eur"]
        self.assertEqual(platform.epci_cost(anchor, nonlinear)["total_eur"], baseline)
        self.assertEqual(platform.epci_cost(larger, nonlinear)["total_eur"], 2 * baseline)
        self.assertEqual(platform.epci_cost(larger, self.inputs)["total_eur"], 4 * baseline)

    def test_epci_ledger_and_explicit_decommissioning(self):
        inputs = synthetic_inputs({"financial-real-wacc": 0, "financial-project-life": 10,
                                   "financial-decommissioning-fraction": 0.5})
        ledger = [CostLine("platform", "epci", 100), CostLine("cable", "installation", 20),
                  CostLine("platform", "decommissioning", 7)]
        result = summarize(ledger, 100, inputs)
        self.assertEqual(result["initial_capex_eur"], 120)
        self.assertEqual(result["decommissioning_eur"], 17)
        self.assertAlmostEqual(result["annual_cost_eur"], 13.7)
        for category in ("supply", "installation"):
            with self.assertRaises(ValueError):
                summarize(ledger + [CostLine("platform", category, 0)], 100, inputs)
        ledger[-1].amount_eur = None
        self.assertIsNone(summarize(ledger, 100, inputs)["lcoh_eur_kg"])

    def test_partial_capacity_availability(self):
        mass = delivered_mass(np.array([[100, 200]]), np.array([10]), np.array([0, 1]), 1)
        self.assertEqual(mass, 2000)

    def test_financial_boundary_and_zero_discount(self):
        inputs = synthetic_inputs({"financial-real-wacc": 0, "financial-project-life": 10,
                                   "financial-decommissioning-fraction": 0.5})
        result = annual_cost(100, 20, 10, 3, inputs)
        self.assertEqual(result["annual_cost_eur"], 15.5)
        missing = summarize([CostLine("platform", "supply", None)], 100, inputs)
        self.assertIsNone(missing["lcoh_eur_kg"])
        with self.assertRaises(ValueError):
            summarize([CostLine("a", "supply", 1), CostLine("a", "supply", 1)], 100, inputs)

    def test_installation_payload_step(self):
        values = {"install-turbine-sets-per-load": 3, "install-turbine-usable-payload": 6000,
                  "install-turbine-crane-capacity": 3000, "install-turbine-speed": 400}
        inputs = synthetic_inputs(values, fill_missing=True)
        light = campaign("turbine", 6, 2000, 500, 50, 1, inputs)
        heavy = campaign("turbine", 6, 2001, 500, 50, 1, inputs)
        self.assertEqual(light["loads"], 2)
        self.assertEqual(heavy["loads"], 3)


class Integration(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        pd.DataFrame({"turbine": ["a", "b"], "x_m": [0, 1000], "y_m": [0, 0]}).to_csv(self.base / "coordinates.csv", index=False)
        pd.DataFrame({"state": ["annual", "design"], "hours": [8760, 0], "a": [10000, 15000], "b": [5000, 15000]}).to_csv(self.base / "power.csv", index=False)
        plan = {"loads_per_campaign": [1], "port_distance_km": 10, "splices": 0,
                "burial_pass_km": 1, "burial_other_offshore_days": 0, "survey_pass_km": 1}
        self.scenario = {"case": {"name": "synthetic verification only", "architecture": "centralised"},
            "site": {"coordinates_file": "coordinates.csv", "minimum_spacing_m": 500, "farm_area_km2": 10,
                     "water_depth_m": 30, "collection_x_m": -1000, "collection_y_m": 0},
            "turbine": {"rotor_diameter_m": 236, "hub_height_m": 133},
            "wind": {"power_states_file": "power.csv", "design_state_ids": ["design"]},
            "electrolysis": {"stack_curve_file": str(ROOT / "numerical_inputs/pem_polarisation_curve.xlsx"), "overplant_factor": 1},
            "hydrogen": {"stack_outlet_bar": 30, "injection_bar": 150, "delivery_bar": 66, "export_length_km": 80, "export_diameter_m": 0.3},
            "platform": {"topside_mass_t": 0.8},
            "installation": {"port_distance_km": 10, "intersite_distance_km": 1, "collection": plan, "export": plan,
                             "platform": {"topside_modules_per_platform": 1}}}

    def test_unfilled_article_cases_are_explicit(self):
        for name in ("centralised", "decentralised"):
            path = ROOT / "research_articles/turbine_level_hydrogen/scenarios" / f"{name}.toml"
            case = read_scenario(path)
            result = run_case(case, load_inputs(case), path.parent)
            self.assertEqual(result.status, "not_parameterized")
            self.assertIsNone(result.summary["lcoh_eur_kg"])

    def test_partial_case_keeps_inventory_and_no_fake_lcoh(self):
        result = run_case(self.scenario, load_inputs({}), self.base)
        self.assertEqual(result.status, "not_parameterized")
        self.assertIn("bop", result.physical)
        self.assertIn("collection_sections", result.tables)
        self.assertIsNone(result.summary["lcoh_eur_kg"])
        write_result(result, self.base / "report")
        json.loads((self.base / "report/result.json").read_text())
        with self.assertRaises(FileExistsError):
            write_result(result, self.base / "report")

    def test_complete_synthetic_central_case_energy_and_cost(self):
        values = {"array-ac-resistance": 0.05, "array-power-factor": 1,
                  "install-turbine-usable-payload": 10000, "install-turbine-crane-capacity": 5000,
                  "install-foundation-usable-payload": 10000, "install-foundation-crane-capacity": 5000,
                  "stack-replacement-life": 30, "install-platform-jacket-crane": 10000}
        result = run_case(self.scenario, synthetic_inputs(values, fill_missing=True), self.base)
        self.assertEqual(result.status, "feasible", result.reasons)
        self.assertGreater(result.summary["lcoh_eur_kg"], 0)
        summary = result.summary
        accounted = sum(summary[key] for key in ["collection_loss_mwh", "stack_mwh", "bop_mwh", "compressor_mwh", "curtailed_mwh", "conversion_loss_mwh"])
        self.assertAlmostEqual(accounted, summary["generator_energy_mwh"], places=6)
        table = result.tables["operation"]
        self.assertEqual(len(table), 2)
        self.assertEqual(result.physical["stack_installed_kw"], 30000)
        self.assertEqual(sum(p["trains"] for p in result.physical["compressors"]), 1)
        write_result(result, self.base / "complete")

    def test_platform_inventory_survives_missing_lift_plan(self):
        del self.scenario["installation"]["platform"]
        result = run_case(self.scenario, load_inputs({}), self.base)
        self.assertIn("platform", result.physical)
        self.assertIn("platform_costs", result.physical)
        self.assertGreater(result.physical["platform_total_eur"], 0)
        platform_lines = [c for c in result.costs if c.component == "platform"]
        self.assertEqual({c.category for c in platform_lines}, {"epci", "decommissioning", "annual_opex"})
        self.assertEqual(sum(c.category == "epci" for c in platform_lines), 1)
        self.assertTrue(any("platform-decommissioning-cost" in reason for reason in result.reasons))
        self.assertIsNone(result.summary["lcoh_eur_kg"])
        self.assertFalse(any("feeder" in reason for reason in result.reasons))
        self.assertGreater(result.physical["ac_strings"], 0)

    def test_epci_complete_case_still_requires_decommissioning(self):
        values = {"array-ac-resistance": 0.05, "array-power-factor": 1,
                  "install-turbine-usable-payload": 10000, "install-turbine-crane-capacity": 5000,
                  "install-foundation-usable-payload": 10000, "install-foundation-crane-capacity": 5000,
                  "stack-replacement-life": 30, "platform-decommissioning-cost": None,
                  "platform-opex-rate": 0.01}
        self.scenario["platform"] = {"equipment_mass_t": 0.4}
        result = run_case(self.scenario, synthetic_inputs(values, fill_missing=True), self.base)
        self.assertEqual(result.status, "not_parameterized", result.reasons)
        self.assertIsNone(result.summary["lcoh_eur_kg"])
        self.assertTrue(all("platform-decommissioning-cost" in r for r in result.reasons), result.reasons)
        capex = result.physical["platform_total_eur"]
        opex = next(c.amount_eur for c in result.costs if c.component == "platform" and c.category == "annual_opex")
        self.assertEqual(opex, capex * 0.01)
        self.assertNotIn("platform_installation", result.physical)

    def test_distributed_case_preserves_turbine_operation(self):
        self.scenario["case"]["architecture"] = "decentralised"
        self.scenario["electrolysis"]["interface"] = "converter_reduced"
        result = run_case(self.scenario, synthetic_inputs({"converter-reduced-conversion-efficiency": 0.99}), self.base)
        self.assertEqual(result.status, "not_parameterized")
        table = result.tables["operation"]
        self.assertEqual(table.location.nunique(), 2)
        self.assertEqual(len(table), 4)
        self.assertEqual(result.physical["bop"]["blocks"], 2)

    def test_complete_distributed_case_and_pressure_constraint(self):
        self.scenario["case"]["architecture"] = "decentralised"
        self.scenario["electrolysis"]["interface"] = "converter_reduced"
        self.scenario["hydrogen"]["export_inlet_bar"] = 130
        self.scenario["collection"] = {"nodes_file": "nodes.csv", "sections_file": "sections.csv", "sink": "sink"}
        pd.DataFrame({"node": ["sink"], "x_m": [2000], "y_m": [0]}).to_csv(self.base / "nodes.csv", index=False)
        pd.DataFrame({"section": ["one", "two"], "from": ["a", "b"], "to": ["b", "sink"],
            "vertical_m": [0, 0], "route_allowance": [0, 0], "flow_share": [1, 1],
            "diameter_m": [0.3, 0.3], "inlet_bar": [150, 140], "outlet_bar": [140, 130]}
            ).to_csv(self.base / "sections.csv", index=False)
        values = {"install-turbine-usable-payload": 10000, "install-turbine-crane-capacity": 5000,
                  "install-foundation-usable-payload": 10000, "install-foundation-crane-capacity": 5000,
                  "turbine-distributed-maximum-lift": 1000, "stack-replacement-life": 30}
        inputs = synthetic_inputs(values, fill_missing=True)
        result = run_case(self.scenario, inputs, self.base)
        self.assertEqual(result.status, "feasible", result.reasons)
        self.assertGreater(result.summary["lcoh_eur_kg"], 0)
        self.assertNotIn("platform", {line.component for line in result.costs})
        self.assertIn(("pipeline-manifold", "annual_opex"), {(line.component, line.category) for line in result.costs})
        table = result.tables["operation"]
        np.testing.assert_allclose(table.input_kw, table.stack_kw + table.bop_kw + table.compressor_kw
                                   + table.curtailed_kw + table.conversion_loss_kw)
        self.scenario["hydrogen"]["export_inlet_bar"] = 135
        rejected = run_case(self.scenario, inputs, self.base)
        self.assertEqual(rejected.status, "infeasible")
        self.assertIsNone(rejected.summary["lcoh_eur_kg"])

    @unittest.skipUnless(importlib.util.find_spec("py_wake"), "optional wind dependency not installed")
    def test_pywake_adapter_preserves_state_shape_and_wake_loss(self):
        from model.wind_resource_and_layout.wake_modelling_and_spacing import calculate_wakes
        coordinates = pd.read_csv(self.base / "coordinates.csv")
        pd.DataFrame({"state": ["annual"], "speed_m_s": [8], "direction_deg": [270], "hours": [8760]}
                     ).to_csv(self.base / "wind.csv", index=False)
        pd.DataFrame({"speed_m_s": [0, 3, 8, 12, 25, 30], "power_kw": [0, 0, 8000, 15000, 15000, 0],
                      "ct": [0, 0.8, 0.8, 0.7, 0.1, 0]}).to_csv(self.base / "curve.csv", index=False)
        wind, version = calculate_wakes(coordinates, {"wind_states_file": "wind.csv", "turbine_curve_file": "curve.csv"},
                                       self.scenario["turbine"], self.base, load_inputs({}))
        self.assertEqual(wind.power_kw.shape, (1, 2))
        self.assertAlmostEqual(wind.power_kw[0, 0], 8000)
        self.assertLess(wind.power_kw[0, 1], 8000)
        self.assertGreater(wind.power_kw[0, 1], 0)
        self.assertTrue(version)

    def test_network_conservation_and_missing_path(self):
        coordinates = pd.read_csv(self.base / "coordinates.csv")
        nodes = pd.DataFrame({"node": ["sink"], "x_m": [2000], "y_m": [0]})
        sections = pd.DataFrame({"section": ["one", "two"], "from": ["a", "b"], "to": ["b", "sink"],
            "vertical_m": [0, 0], "route_allowance": [0, 0], "flow_share": [1, 1],
            "diameter_m": [0.15, 0.15], "inlet_bar": [150, 140], "outlet_bar": [140, 130]})
        path = self.base / "sections.csv"
        sections.to_csv(path, index=False)
        inventory, flows = section_inventory(path, coordinates, nodes, np.array([[100, 200]]), "sink")
        np.testing.assert_allclose(flows, [[100, 300]])
        self.assertEqual(inventory.physical_km.sum(), 2)
        sections.loc[0, "flow_share"] = 0
        sections.to_csv(path, index=False)
        with self.assertRaises(Infeasible):
            section_inventory(path, coordinates, nodes, np.array([[100, 200]]), "sink")

    def test_design_cases_fill_open_fields_without_overriding(self):
        from research_articles.turbine_level_hydrogen.analysis.run_design_cases import apply_design_values
        open_scenario = copy.deepcopy(self.scenario)
        del open_scenario["hydrogen"]["injection_bar"], open_scenario["hydrogen"]["export_diameter_m"]
        filled = apply_design_values(open_scenario, {"hydrogen.injection_bar": 150,
                                                     "hydrogen.export_diameter_m": 0.3})
        self.assertEqual(filled, self.scenario)
        self.assertNotIn("injection_bar", open_scenario["hydrogen"])
        with self.assertRaises(ValueError):
            apply_design_values(self.scenario, {"hydrogen.injection_bar": 100})

    def test_model_imports_do_not_run_or_write(self):
        with patch("pathlib.Path.write_text", side_effect=AssertionError("import wrote a file")):
            for path in (ROOT / "model").rglob("*.py"):
                name = ".".join(path.relative_to(ROOT).with_suffix("").parts)
                importlib.import_module(name)

    def test_pressure_screen_survives_missing_upstream_inputs(self):
        # Physical impossibility must not be hidden by missing layout/loss data.
        for architecture in ("centralised", "decentralised"):
            for pressure in (51.01325, 61.01325, 67.01325):
                scenario = {"case": {"architecture": architecture},
                            "hydrogen": {"injection_bar": pressure, "delivery_bar": 67.01325}}
                result = run_case(scenario, load_inputs({}), self.base)
                self.assertEqual(result.status, "infeasible")
                self.assertTrue(any("discharge" in reason for reason in result.reasons))
        with self.assertRaises(Infeasible):
            capacity_kg_h(0.15, 60, 67, 100000, load_inputs({}))
        with self.assertRaises(ValueError):
            capacity_kg_h(-0.15, 150, 67, 100000, load_inputs({}))

    def test_agreed_grid_units_and_missing_collection_pressure(self):
        from research_articles.turbine_level_hydrogen.analysis.run_design_cases import read_design_cases, apply_design_values
        scenarios = ROOT / "research_articles/turbine_level_hydrogen/scenarios"
        cases = read_design_cases(scenarios / "pressure_diameter_grid.toml", load_inputs({}))
        self.assertEqual(len(cases), 99)
        self.assertEqual(cases.case.nunique(), 99)
        self.assertEqual(cases["hydrogen.injection_bar"].nunique(), 11)
        self.assertEqual(cases["hydrogen.export_diameter_m"].nunique(), 9)
        self.assertAlmostEqual(cases.iloc[0]["hydrogen.injection_bar"], 51.01325)
        self.assertAlmostEqual(cases.iloc[-1]["hydrogen.injection_bar"], 151.01325)
        self.assertAlmostEqual(cases.iloc[0]["hydrogen.export_diameter_m"], 0.1016)
        self.assertAlmostEqual(cases.iloc[-1]["hydrogen.export_diameter_m"], 0.2032)
        self.assertEqual((cases["hydrogen.injection_bar"] <= 67.01325).sum(), 18)
        values = cases.iloc[-1].to_dict()
        values.pop("case")
        filled = apply_design_values(read_scenario(scenarios / "decentralised.toml"), values)
        self.assertNotIn("export_inlet_bar", filled["hydrogen"])
        self.assertNotIn("sections_file", filled["collection"])


class StackDegradation(unittest.TestCase):
    def test_sawtooth_average_loss(self):
        inputs = synthetic_inputs({"stack-degradation-rate": 0.0018, "stack-end-of-life-degradation": 0.1})
        factor, interval = stack.lifetime_production_factor(5000, 25, inputs)
        self.assertAlmostEqual(interval, 0.1 / 0.009)
        remainder = 25 - 2 * interval
        expected = 1 - (2 * 0.1 * interval / 2 + 0.009 * remainder**2 / 2) / 25
        self.assertAlmostEqual(factor, expected)
        self.assertEqual(stack.lifetime_production_factor(0, 25, inputs)[0], 1.0)


class CompressorCost(unittest.TestCase):
    def test_turbine_reference_closes_power_balance_and_uses_turbine_denominator(self):
        from model.hydrogen_infra.compressor import turbine_reference
        inputs = load_inputs({})
        curve = StackCurve.read(ROOT / "numerical_inputs/pem_polarisation_curve.xlsx")
        duty = turbine_reference(15000, 30, 150, curve, inputs)
        self.assertAlmostEqual(duty["stack_kw"] + duty["bop_kw"] + duty["compressor_kw"], 15000)
        self.assertAlmostEqual(duty["compressor_kw"], duty["hydrogen_kg_h"] * specific_energy(30, 150, inputs))
        self.assertAlmostEqual(duty["eur_per_turbine_kw"] * 15000, duty["purchase_eur"])
        self.assertLess(duty["eur_per_turbine_kw"], duty["purchase_eur"] / duty["compressor_kw"])
        zero = turbine_reference(15000, 30, 30, curve, inputs)
        self.assertEqual((zero["compressor_kw"], zero["trains"], zero["purchase_eur"]), (0, 0, 0))

    def test_reference_power_cancels_and_normalisation_is_explicit(self):
        from model.hydrogen_infra.compressor import Compressor, supply_cost, cost_coefficient_eur2025
        base = load_inputs({})
        moved = load_inputs({"overrides": {"compressor-reference-motor-power": 50}})
        package = [Compressor(2, 400.0, 800.0)]
        self.assertAlmostEqual(supply_cost(package, base), supply_cost(package, moved), places=6)
        n = base.number
        coefficient = (n("compressor-source-cost-coefficient") * n("compressor-source-usd-per-cad-2019")
                       * n("compressor-usd-escalation-2019-2025") / n("financial-usd-per-eur-2025"))
        self.assertAlmostEqual(cost_coefficient_eur2025(base), coefficient)
        self.assertAlmostEqual(supply_cost(package, base), 2 * coefficient * 400 ** n("compressor-cost-exponent"))


class ReferenceCase(unittest.TestCase):
    def test_gauge_pressures_become_absolute_with_standard_atmosphere(self):
        from research_articles.turbine_level_hydrogen.analysis import reference_case as ref
        atmospheric = float(load_parameters().number("standard-atmospheric-pressure", "bar"))
        self.assertEqual(atmospheric, 1.01325)
        case = ref.load_reference_case()
        derived = ref.derive_reference_case(case, atmospheric)
        self.assertAlmostEqual(derived["stack_outlet_pressure_bar_a"],
                               case["electrolysis"]["stack_outlet_pressure_bar_g"] + 1.01325)
        self.assertAlmostEqual(derived["delivery_pressure_bar_a"],
                               case["hydrogen"]["delivery_pressure_bar_g"] + 1.01325)
        variables = ref.quarto_variables()
        self.assertEqual(variables["ijv-stack-outlet-pressure-bar-a"], "31.01")
        self.assertEqual(variables["ijv-delivery-pressure-bar-a"], "67.01")

    def test_generated_common_case_matches_the_record(self):
        from research_articles.turbine_level_hydrogen.analysis import prepare_common_case as prep
        from research_articles.turbine_level_hydrogen.analysis import reference_case as ref
        case = ref.load_reference_case()
        atmospheric = float(load_parameters().number("standard-atmospheric-pressure", "bar"))
        derived = ref.derive_reference_case(case, atmospheric)
        self.assertEqual((prep.SCENARIOS / "common_case.toml").read_text(),
                         prep.common_case_toml(case, derived, atmospheric))
        coordinates = pd.read_csv(prep.SCENARIOS / prep.COORDINATE_FILE, dtype={"turbine": str})
        pd.testing.assert_frame_equal(coordinates, prep.coordinates(case, derived))
        spacing = np.hypot(*(coordinates[["x_m", "y_m"]].to_numpy()[1] - coordinates[["x_m", "y_m"]].to_numpy()[0]))
        self.assertAlmostEqual(spacing, derived["spacing_crosswind_m"], delta=0.02)
        annual_hours = float(load_parameters().number("annual-hours", "h/year"))
        wind = WindStates.read(prep.SCENARIOS / prep.POWER_FILE, coordinates.turbine.tolist(), annual_hours)
        design = wind.state_ids.index(prep.DESIGN_STATE)
        self.assertEqual(wind.hours[design], 0)
        self.assertTrue(np.all(wind.power_kw[design] == case["turbine"]["rated_power_mw"] * 1000))
        self.assertLessEqual(wind.power_kw.max(), case["turbine"]["rated_power_mw"] * 1000)

    def test_generated_collection_network_conserves_flow(self):
        from research_articles.turbine_level_hydrogen.analysis import prepare_common_case as prep
        from research_articles.turbine_level_hydrogen.analysis import reference_case as ref
        case = ref.load_reference_case()
        derived = ref.derive_reference_case(case, float(load_parameters().number("standard-atmospheric-pressure", "bar")))
        coordinates = pd.read_csv(prep.SCENARIOS / prep.COORDINATE_FILE, dtype={"turbine": str})
        nodes, geometry = prep.collection_network(case, derived, coordinates)
        pd.testing.assert_frame_equal(nodes, pd.read_csv(prep.SCENARIOS / prep.NODE_FILE, dtype={"node": str}))
        pd.testing.assert_frame_equal(geometry, pd.read_csv(prep.SCENARIOS / prep.SECTION_GEOMETRY_FILE,
                                                            dtype={"section": str, "from": str, "to": str}))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sections.csv"
            geometry.assign(diameter_m=0.1, inlet_bar=100, outlet_bar=90).to_csv(path, index=False)
            rated = case["turbine"]["rated_power_mw"]
            sections, _ = section_inventory(path, coordinates, nodes, np.full((1, len(coordinates)), rated), prep.MANIFOLD)
        tie_ins = sections[sections["class"] == "tie-in"]
        self.assertTrue(np.allclose(tie_ins.peak_kg_h, len(coordinates) * rated / 2))
        horizontal = (sections.physical_km - sections.vertical_m / 1000).sum()
        # Coordinates are stored to the centimetre.
        self.assertAlmostEqual(horizontal, ref.ladder_geometry(case, derived)["ladder_total_km"], places=3)

    def test_article_templates_share_the_common_case(self):
        folder = ROOT / "research_articles/turbine_level_hydrogen/scenarios"
        central, distributed = (read_scenario(folder / f"{name}.toml") for name in ("centralised", "decentralised"))
        for section in ("site", "turbine", "wind"):
            shared = {key: central[section][key] for key in read_scenario(folder / "common_case.toml")[section]}
            self.assertEqual(shared, {key: distributed[section][key] for key in shared})
        self.assertEqual(central["hydrogen"]["delivery_bar"], distributed["hydrogen"]["delivery_bar"])

    def test_scenario_include_cannot_redefine_shared_inputs(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            (base / "shared.toml").write_text('[site]\nwater_depth_m = 28\n')
            (base / "case.toml").write_text('[case]\ninclude = "shared.toml"\n[site]\nfarm_area_km2 = 1\n')
            self.assertEqual(read_scenario(base / "case.toml")["site"], {"water_depth_m": 28, "farm_area_km2": 1})
            (base / "clash.toml").write_text('[case]\ninclude = "shared.toml"\n[site]\nwater_depth_m = 30\n')
            with self.assertRaises(ValueError):
                read_scenario(base / "clash.toml")


if __name__ == "__main__":
    unittest.main()
