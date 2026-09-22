import unittest
from decimal import Decimal

from model_data import build_quarto_variables, hvdc_conductor_loss, load_parameters


class ModelDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parameters = load_parameters()
        cls.variables = build_quarto_variables(cls.parameters)

    def test_financial_derivations(self):
        self.assertEqual(
            self.variables["financial-capital-recovery-factor-value"],
            "0.0827414",
        )
        self.assertEqual(
            self.variables["financial-eur-per-usd-2025-value"],
            "0.88495575",
        )

    def test_hvdc_current_and_losses(self):
        self.assertEqual(self.variables["hvdc-full-load-pole-current"], "1.905 kA")
        loss_mw, loss_fraction = hvdc_conductor_loss(
            self.parameters, Decimal(80)
        )
        self.assertAlmostEqual(float(loss_mw), 4.1796, places=4)
        self.assertAlmostEqual(float(loss_fraction), 0.0020898, places=7)

    def test_array_reference_case(self):
        self.assertEqual(self.variables["array-turbines-per-string"], "4")
        self.assertEqual(self.variables["array-reference-turbine-count"], "134")
        self.assertEqual(self.variables["array-reference-string-count"], "34")
        self.assertEqual(self.variables["array-five-turbine-string-count"], "27")

    def test_hvdc_currency_only_reference(self):
        self.assertEqual(
            self.variables["hvdc-cable-material-cost-eur-per-km"],
            "2.51 million EUR/km",
        )
        self.assertEqual(
            self.variables["hvdc-cable-material-cost-eur-per-kw-km"],
            "1.26 EUR/kW/km",
        )


if __name__ == "__main__":
    unittest.main()
