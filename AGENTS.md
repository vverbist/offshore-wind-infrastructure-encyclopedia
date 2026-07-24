# Project purpose

This project develops a transparent and traceable techno-economic model of
offshore wind infrastructure. Its purpose is to let a reader understand,
verify, and reproduce the calculations and assumptions behind the model.

Prioritise auditability over breadth. A page is successful when the reader can
reconstruct the relevant calculation, not when it provides the most
comprehensive general description of the subject.

# Approval before implementation

Use a two-stage workflow for every requested repository change.

1. First inspect the relevant context and respond with feedback, a proposed
   approach, or a concrete implementation plan.
2. Wait for explicit user approval in a subsequent message before implementing
   the proposal.

During the first stage:

- Read-only inspection and analysis are allowed.
- Do not create, edit, move, or delete files.
- Do not generate implementation code or repository content.
- Do not run commands that intentionally modify the repository.
- Treat the initial request as a request for a proposal, even when it is phrased
  as an implementation request.

Implementation may begin only after the user explicitly confirms the proposed
approach, for example with "proceed", "implement", "add it", or equivalent
language.

After approval, implement only the agreed scope. If implementation reveals a
materially different approach or requires additional changes, stop, explain the
new requirement, and request approval again.

# Core editorial principles

- Optimise for better information, not more information.
- Organise content around the model calculation and its dependencies.
- Keep prose direct, precise, and concise.
- Include technical background only when it is necessary to understand or
  justify the calculation.
- Do not add general industry context, descriptive detail, or tangential
  discussion merely to make a page appear more complete.
- Discussion, interpretation, limitations, and design insights are welcome,
  but they must remain subordinate to the calculation and its traceability.
- Do not turn the site into a general offshore-wind encyclopedia. Its primary
  function is to document the techno-economic model.

# Calculation-led content

When creating or revising a page:

1. State what is being calculated and why the result is needed by the model.
2. Identify the required inputs and assumptions.
3. Present equations, transformations, and intermediate results in calculation
   order.
4. Give the resulting model output and explain how it is used elsewhere.
5. Document material limitations, uncertainty, and modelling choices.

Prefer dependency order over narrative order. A reader should encounter each
input and assumption before it is used in a calculation.

# Explicit and bottom-up modelling

Make the model as explicit and bottom-up as reasonably possible. Model results
should be derived from physical quantities, design choices, unit rates, and
activities rather than introduced as aggregated benchmark values.

- Decompose composite costs into their material components, installation
  activities, operating requirements, and other relevant cost drivers.
- Calculate required quantities explicitly from the system design. Do not hide
  quantities such as cable length, platform mass, installation duration, or
  equipment count inside a cost factor.
- Express costs as transparent relationships between quantities and unit costs
  wherever the available evidence supports this.
- Keep input parameters separate from calculated quantities and calculated
  costs.
- State clearly what each cost category includes and excludes so that cost
  boundaries are visible and double counting can be detected.
- Show intermediate results needed to inspect and verify the calculation.
- Use aggregated factors only when a more explicit decomposition is not
  supported by available evidence. In that case, label the factor as a
  top-down assumption, document its scope and inclusions, justify its use, and
  identify the missing decomposition as an unresolved limitation.

Decompose the model as far as the evidence allows, but never farther than the
evidence supports.

# Traceability of quantitative information

Every quantitative value that affects the model must be traceable. For each
value:

- State what the value represents.
- Give the value and its units.
- Identify whether it is a sourced input, an explicit modelling assumption, or
  a derived result.
- Cite the source at the point where the value is introduced.
- State the applicable scope, reference year, operating condition, or other
  basis when relevant.
- Explain why the source or assumption is appropriate for this model.
- If the value is derived, show the equation or transformation and identify its
  upstream inputs.
- If sources disagree or a value requires interpretation, explain the choice
  made.
- Preserve meaningful precision. Do not imply more certainty than the source or
  method supports.

A reader must not have to guess where a model input came from, why it was
selected, or how a reported result was obtained.

# Equations and calculations

- Show the equations needed to reproduce the calculation.
- Define every symbol and state its units.
- Make unit conversions, normalisations, correction factors, and scaling steps
  explicit.
- State the system boundary and basis of comparison where relevant.
- Use consistent terminology, notation, and units across related pages.
- Do not introduce unexplained constants, correction factors, or embedded
  assumptions.
- Where practical, include intermediate values that help the reader verify the
  calculation.

# Sources and evidence

- Add bibliographic sources to `references.bib` and cite them where the
  corresponding values or claims are introduced.
- Prefer primary and authoritative sources for model inputs.
- Distinguish clearly between published evidence, modelling judgement, and
  derived results.
- Do not cite a source as support for a value unless the source actually
  provides or justifies that value.
- Never invent a citation, numerical value, derivation, or justification.

# Missing and uncertain information

- Do not insert temporary or illustrative placeholder values for missing model
  inputs.
- Leave missing numerical evidence as an explicit unresolved `TODO` that states
  what evidence or decision is required.
- Do not silently fill evidence gaps using an unsupported estimate.
- If a calculation cannot be completed without an unresolved input, show the
  calculation structure and clearly state why no result is reported.
- Where uncertainty materially affects the model, document the uncertainty and
  its consequences rather than hiding it behind a single value.

# Repository conventions

- The source content is written in Quarto Markdown (`.qmd`).
- Preserve the information architecture defined in `_quarto.yml`.
- Do not edit generated output under `_site/`.
- Do not edit environment or cache directories such as `.venv/`, `.quarto/`,
  and `.uv-cache/`.
- Keep related pages consistent in structure, terminology, symbols, units, and
  citation style.
- Prefer focused changes. Do not broadly rewrite adjacent material unless that
  is needed for calculation consistency or traceability.

# Validation

After making changes:

- Render every affected Quarto page.
- For navigation, shared configuration, styling, bibliography, or site-wide
  changes, render the full website.
- Inspect the rendered output for broken equations, citations, figures, tables,
  cross-references, and links.
- Check that every newly introduced model-relevant number satisfies the
  traceability requirements above.
- Report any validation that could not be completed and explain why.
