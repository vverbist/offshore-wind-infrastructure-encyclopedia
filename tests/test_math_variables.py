"""Render small isolated documents to check the math-variable compatibility filter."""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUARTO = shutil.which("quarto")


@unittest.skipUnless(QUARTO, "Quarto is required for rendering tests")
class MathVariablesTest(unittest.TestCase):
    def render(self, content, variables):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy(ROOT / "tools/math-variables.lua", root)
            (root / "_quarto.yml").write_text(
                "project:\n  type: default\nfilters:\n  - math-variables.lua\n",
                encoding="utf-8",
            )
            (root / "_variables.yml").write_text(variables, encoding="utf-8")
            (root / "example.qmd").write_text(content, encoding="utf-8")
            result = subprocess.run(
                [QUARTO, "render", "example.qmd", "--to", "html"],
                cwd=root, capture_output=True, text=True, encoding="utf-8",
            )
            html = root / "example.html"
            return result, html.read_text(encoding="utf-8") if html.exists() else ""

    def test_prose_inline_table_and_display_math(self):
        result, html = self.render(
            "Prose: {{< var count >}}.\n\n"
            "Inline: $n={{< var count >}}$.\n\n"
            "| Quantity | Value |\n|---|---|\n"
            "| Count | $n={{< var count >}}$ |\n\n"
            "$$\nm={{< var slope >}}P+{{< var offset >}}.\n$$\n\n"
            r"$$\frac{{{< var slope >}}}{{{< var count >}}}$$" + "\n",
            'count: "3"\nslope: "1.915"\noffset: "1910"\n',
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Prose: 3.", html)
        self.assertEqual(html.count(r"\(n=3\)"), 2)
        self.assertIn("m=1.915P+1910.", html)
        self.assertIn(r"\frac{1.915}{3}", html)
        self.assertNotIn("b58fc729", html)
        self.assertNotIn("{{<", html)

    def test_missing_or_empty_values_fail(self):
        for variables in ('other: "1"\n', 'missing: ""\n'):
            with self.subTest(variables=variables):
                result, _ = self.render("$x={{< var missing >}}$\n", variables)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Missing value for math variable 'missing'", result.stderr)


if __name__ == "__main__":
    unittest.main()
