# Model inputs

`inputs.csv` is the authoritative table for scalar values used by the website,
figures and future model. It can be edited directly in Excel or a text editor.

The columns are intentionally limited:

- `id`: permanent, human-readable identifier;
- `value`: numeric value in the stated unit;
- `unit`: the stored unit, not a display conversion;
- `kind`: `sourced`, `assumption`, `conversion` or `reference`;
- `price_year`: required for adopted monetary inputs; and
- `citation`: the key in `references.bib`, without the leading `@`.

`reference` is reserved for contextual monetary evidence that cannot yet be
adopted, for example because its source price year is unresolved.

Do not add formulas to the CSV. Derived values and currency conversions belong
in `parameters.py`. The website build validates the table, calculates derived
values, writes the ignored `_variables.yml` file and regenerates dependent
figures. `_variables.yml` must never be edited directly.

Percentages are stored as fractions: `0.066` is rendered as `6.6%`. If Excel
saves a European semicolon-delimited CSV with decimal commas, the loader accepts
that format as well.
