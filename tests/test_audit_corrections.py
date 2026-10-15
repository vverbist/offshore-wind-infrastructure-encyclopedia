"""Accounting boundaries and behaviour-preserving audit corrections."""
import csv
from decimal import Decimal
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

from model.inputs import load_inputs
from model.records import CostLine
from model.methodology.system_boundary_and_lcoe import summarize
from model.electrical_infra.infield_ac_cables import string_counts
from model.wind_resource_and_layout.wind_resource_and_weibull import discretize_weibull, annual_energy_metrics
from model_data.parameters import load_parameters, ParameterError
from tests import test_model as fixtures
from tests.test_model import synthetic_inputs
from model.workflow import run_case


class AuditCorrections(unittest.TestCase):
    def test_onshore_installation_affects_capex_not_offshore_removal(self):
        inputs = synthetic_inputs({"financial-decommissioning-fraction": .8})
        offshore = [CostLine("turbine", "supply", 1000), CostLine("turbine", "installation", 100),
                    CostLine("platform", "epci", 200), CostLine("platform", "decommissioning", 7)]
        first = summarize(offshore, 100, inputs, wind_capacity_kw=10)
        second = summarize(offshore + [CostLine("hydrogen-receipt", "installation", 20)],
                           100, inputs, wind_capacity_kw=10)
        self.assertEqual(first["decommissioning_eur"], 87)
        self.assertEqual(second["decommissioning_eur"], 87)
        self.assertEqual(second["initial_capex_eur"] - first["initial_capex_eur"], 20)
        self.assertEqual(second["initial_capex_eur_per_wind_kw"], 132)

    def test_capital_intensity_remains_missing_for_partial_capex(self):
        result = summarize([CostLine("turbine", "supply", None)], None, load_inputs({}),
                           scope="production_capex", wind_capacity_kw=10)
        self.assertIsNone(result["initial_capex_eur_per_wind_kw"])
        self.assertFalse(any("per_wind_kw" in key and "lifecycle" in key for key in result))

    def test_nonzero_residual_override_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "fixed at zero"):
            load_inputs({"overrides": {"financial-residual-value-fraction": .2}})

    def test_all_adopted_currency_inputs_need_a_year(self):
        source = Path("model_data/inputs.csv")
        rows = list(csv.DictReader(source.open(encoding="utf-8")))
        for currency in ("CAD", "MYR", "EUR", "USD", "GBP"):
            changed = [dict(row) for row in rows]
            changed[0].update(value="1", unit=currency + "/unit", kind="assumption", price_year="")
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "inputs.csv"
                with path.open("w", newline="", encoding="utf-8") as stream:
                    writer = csv.DictWriter(stream, fieldnames=changed[0]); writer.writeheader(); writer.writerows(changed)
                with self.assertRaisesRegex(ParameterError, "price year"):
                    load_parameters(path)

    def test_cpi_factors_follow_upstream_index_override(self):
        inputs = load_inputs({"overrides": {"financial-usd-cpi-2025": 330}})
        self.assertEqual(inputs.number("financial-usd-escalation-2020-2025"), round(330 / 258.811, 5))
        self.assertEqual(load_inputs({}).number("financial-usd-escalation-2022-2025"), 1.10008)

    def test_campaign_weather_excludes_port_and_fixed_days(self):
        from model.offshore_installation.turbine_and_foundation_installation import campaign
        values = {"install-foundation-usable-payload": 10000, "install-foundation-crane-capacity": 5000,
                  "install-foundation-demobilisation-time": 0, "install-foundation-weather-offshore": 0}
        before = campaign("foundation", 3, 100, 80, 10, 1, synthetic_inputs(values, fill_missing=True))
        values.update({"install-foundation-demobilisation-time": 2, "install-foundation-weather-offshore": .5})
        after = campaign("foundation", 3, 100, 80, 10, 1, synthetic_inputs(values, fill_missing=True))
        self.assertAlmostEqual(after["chargeable_days"] - before["chargeable_days"],
                               2 + .5 * (before["site_days"] + before["travel_days"]))
        self.assertEqual(after["port_days"], before["port_days"])

    def test_terminal_degradation_differs_from_lifetime_yield_loss(self):
        from model.hydrogen_production.stack import degradation_diagnostics
        inputs = synthetic_inputs({"stack-degradation-rate": .0018, "stack-end-of-life-degradation": .1})
        result = degradation_diagnostics(5000, 25, inputs)
        self.assertAlmostEqual(result["terminal_loss_fraction"], .025)
        self.assertAlmostEqual(result["cumulative_yield_loss_fraction"],
                               1 - result["lifetime_production_factor"])
        self.assertEqual(degradation_diagnostics(0, 25, inputs)["terminal_loss_fraction"], 0)

    def test_string_capacity_steps(self):
        self.assertEqual(string_counts(4, 15000, 60), (4, 1))
        self.assertEqual(string_counts(5, 15000, 60), (4, 2))
        self.assertEqual(string_counts(134, 15000, 60), (4, 34))

    def test_saved_article_wind_states_are_preserved(self):
        from research_articles.turbine_level_hydrogen.analysis.prepare_common_case import SCENARIOS
        from research_articles.turbine_level_hydrogen.analysis.reference_case import load_reference_case
        case = load_reference_case(); wind = case["wind"]
        sectors = pd.read_csv(SCENARIOS / wind["sector_file"])
        curve = pd.read_csv(SCENARIOS / "common/turbine_power_ct.csv")
        states, remainder = discretize_weibull(sectors, curve, 8760, wind["direction_step_deg"], wind["speed_bin_m_s"])
        saved = pd.read_csv(SCENARIOS / "common/wind_states.csv")
        np.testing.assert_allclose(states.hours, saved.hours.iloc[:len(states)], rtol=1e-12, atol=1e-9)
        self.assertAlmostEqual(remainder + states.hours.sum(), 8760)
        power = pd.read_csv(SCENARIOS / "common/power_states.csv")
        ids = [key for key in power if key not in {"state", "hours"}]
        result = annual_energy_metrics(power, states, curve, ids, 15000, 8760)
        self.assertAlmostEqual(result["wake_mwh"] / 1000, 9639.0614, places=3)

    def test_component_opex_includes_installation_and_epci_once(self):
        fixture = fixtures.Integration("test_partial_case_keeps_inventory_and_no_fake_lcoh")
        fixture.setUp()
        try:
            values = {"install-turbine-usable-payload": 10000, "install-turbine-crane-capacity": 5000,
                      "install-foundation-usable-payload": 10000, "install-foundation-crane-capacity": 5000,
                      "stack-replacement-life": 30, "turbine-generation-availability": .8,
                      "central-production-availability": .9}
            result = run_case(fixture.scenario, synthetic_inputs(values, fill_missing=True), fixture.base)
            for line in result.costs:
                if line.category == "annual_opex":
                    capital = [x for x in result.costs if x.component == line.component
                               and x.category in {"supply", "installation", "epci"}]
                    self.assertAlmostEqual(line.amount_eur, sum(x.amount_eur for x in capital) * .02)
            self.assertAlmostEqual(result.summary["delivered_hydrogen_kg_year_bol"]
                                   / result.summary["preavailability_hydrogen_kg_year_bol"], .8 * .9)
        finally:
            fixture.tearDown()
