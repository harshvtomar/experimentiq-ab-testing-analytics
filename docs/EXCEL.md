# Excel business analytics workbook

File: reports/session3/ExperimentIQ_Business_Analytics_Report.xlsx. Seven worksheets: Executive Dashboard, Scenario Inputs, Revenue & Contribution, Sensitivity Analysis, Experiment Results, Statistical Evidence, Dictionary & Methodology. Three native editable charts bind to worksheet cells.

Edit yellow cells D7:D11 on Scenario Inputs: audience, margin fraction, incremental delivery cost, fixed setup cost, multiplier. Both treatments use the same inputs; control is the zero incremental baseline. Margin is stored as a fraction and displayed as a percentage. Source measurements on Experiment Results and Statistical Evidence remain unchanged. Model outputs update through real Excel formulas. Clear an input for an unavailable state; zero remains a valid input. Validation is also enforced in formulas, because pasted values can bypass Excel data validation.

Money is expressed in source dollars, not INR or converted USD. Gross contribution applies the assumed margin to incremental revenue. Net return on cost is a scenario ratio. Break-even thresholds and affine interval rules are specified in ECONOMICS.md. Formula-based one-at-a-time sensitivity is appropriate for this simple affine model; these are not native What-If Data Tables or probability distributions.

## Rebuild
1. Run the original pipeline and statistical pipeline, then `python -m src.business_pipeline` to create unrounded input JSON.
2. `scripts/build_workbook.mjs` uses `@oai/artifact-tool` in the Codex primary runtime. Copy this single builder into an OS temporary directory, link that directory's node_modules to `$CODEX_PRIMARY_RUNTIME_NODE_MODULES`, then run `$CODEX_PRIMARY_RUNTIME_NODE builder.mjs /absolute/path/to/repository`.
3. The builder calculates real formulas, changes/restores inputs, exports seven preview PNGs, exports the .xlsx, reopens it, recalculates, and saves verification JSON plus SHA-256 hashes. It requires that authoring runtime; ordinary Python CI does not regenerate the workbook. The delivered workbook can be edited in a spreadsheet application without this builder.
4. Run `python -m pytest tests/test_workbook.py -q` to compare recorded recalculation cases and exported caches with the independent Python economics engine. CI checks delivered workbook structure and integrity, rather than falsely claiming a native Excel run.

## Verified scope
Artifact Tool: demo, changed inputs, zero audience, zero costs, zero margin, missing margin, invalid margin. Verified output recalculation, model/report linkage, three range-bound native charts, seven sheets, no formula-error cells, successful XLSX export/reopen and Python agreement. Reviewed rendered sheets; corrected preview ranges and preserved zero inputs with ISNUMBER guards. All seven boundary cases are recorded in excel_recalculation_checks.json, tied to the delivered workbook/builder with a hash manifest.

LibreOfficeDev 26.8 headless: opened and converted a disposable copy; independently checked recalculated E22:F24 against Python/Artifact values and scanned worksheets for error cells (none). Evidence is in libreoffice_verification.json. The delivered file remains the Artifact Tool export, not the converted copy.

**Native Microsoft Excel has not been opened or tested.** Power BI Desktop has not been opened or tested. Session 4 may add these checks where supported. No native Excel/Power BI verification is implied by rendering previews or successful OOXML export.
