"""Write local run artifacts explicitly, never during module import."""
from dataclasses import asdict
import json
from pathlib import Path
import pandas as pd


def write_result(result, directory: Path):
    directory.mkdir(parents=True, exist_ok=False)
    document = {"name": result.name, "architecture": result.architecture, "status": result.status,
                "reasons": result.reasons, "summary": result.summary, "physical": result.physical,
                "scenario": result.scenario}
    (directory / "result.json").write_text(json.dumps(document, indent=2, allow_nan=False), encoding="utf-8")
    pd.DataFrame(result.inputs).to_csv(directory / "effective_inputs.csv", index=False)
    pd.DataFrame([asdict(row) for row in result.costs], columns=["component", "category", "amount_eur", "note"]).to_csv(directory / "costs.csv", index=False)
    for name, table in result.tables.items():
        table.to_csv(directory / f"{name}.csv", index=False)
