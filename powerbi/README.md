# Power BI integration package

**Status: aggregate import assets and measure specifications. No native .pbix report has been created or validated.** The execution environment is Linux with no supported Power BI Desktop session. Use a Windows Power BI Desktop installation to import, render, validate and save a native report. This does not block the working Streamlit simulator or Excel workbook.

## Refresh and import
1. Clone the repository, install requirements, run `python -m src.pipeline`, `python -m src.statistical_pipeline`, then `python -m src.business_pipeline`.
2. Open Power BI Desktop on Windows. Create a text parameter `DataFolder` pointing to this directory's `data` subfolder (trailing slash/backslash included).
3. Create a blank query named `LoadCsv` using `import_function.pq`. For each file, create `LoadCsv("filename.csv")`, name the query exactly as the filename without extension. Inspect types explicitly: counts/order = whole number; rates/effects/costs/p-values = decimal number; identifiers/labels = text; flags = true/false. Use English (United States) locale for dot decimals. Empty numeric CSV fields must be null, never zero.
4. Import `dim_arm`, `arm_performance`, `binary_inference`, `revenue_inference`, `segment_effects`, `interactions`, `scenario_snapshot`, `sensitivity_snapshot`; `descriptive_comparisons` is optional and disconnected.
5. Configure the relationships below. Turn off automatic relationship inference. Add each measure from `measures.dax` individually. These specifications have not been executed in a DAX engine.
6. Build the five pages in `REPORT_LAYOUT.md`, reconcile against the canonical CSVs and workbook, then save a .pbix. Record Windows/Desktop versions, screenshots, input filters and actual results before claiming native verification.

## Model grains and relationships

|Table|Unique grain|Relationship from dim_arm[arm]|
|---|---|---|
|dim_arm|arm|Dimension, sort by arm_order|
|arm_performance|arm|To arm_performance[arm]|
|binary_inference|outcome + treatment + reference|To binary_inference[treatment]|
|revenue_inference|treatment + reference|To revenue_inference[treatment]|
|segment_effects|variable + level + treatment|To segment_effects[treatment]|
|interactions|variable + treatment|To interactions[treatment]|
|scenario_snapshot|treatment, one documented input set|To scenario_snapshot[treatment]|
|sensitivity_snapshot|driver + driver_value + treatment|To sensitivity_snapshot[treatment]|

Use one-to-many, single-direction filtering from the dimension. No fact-to-fact relationships. Do not create an active reference-arm relationship to the same dimension; that changes the comparison meaning. Control has no treatment-effect row, which is appropriate. Do not join overlapping subgroup partitions into a customer count. Only arm_performance counts may be summed across mutually exclusive arms.

## Interpretation and dictionary
Arm counts/rates/spend follow docs/KPI_DEFINITIONS.md. `effect` and interval endpoints are binary fractions or spend dollars/customer, determined by outcome. Primary conversion, secondary visit, secondary revenue and exploratory comparisons have separate Holm families. P-values, CIs, rates and contrasts must not be summed or averaged across contrast rows.

Scenario columns follow docs/ECONOMICS.md. `assumption_basis` is hypothetical. N, m, c, F, k are explicit columns on each scenario/sensitivity row. Snapshots do not become an editable economic model merely by adding slicers: rerun the Python pipeline for a new input set or implement separately verified What-If parameters. Current interactive economics is provided by Streamlit and Excel.

## Native verification checklist
- Assignment count 64,000 and total observed spend $67,258.13; weighted conversion/visit rates.
- Match both control contrasts and all nine endpoint/contrast rows to Session 2 CSVs. Enforce one outcome and one contrast before showing a scalar inference measure.
- One subgroup variable at a time; show n_t/n_c and adjusted interaction p. No validated targeting claim.
- Demo net values agree with demonstration_scenarios.csv; baseline is zero and net/cost is blank at zero costs.
- Totals for nonadditive contrasts/returns are blank; sensitivity axis selects one driver and one value per mark.

References: https://learn.microsoft.com/en-us/dax/selectedvalue-function-dax ; https://learn.microsoft.com/en-us/dax/divide-function-dax ; https://learn.microsoft.com/en-us/power-bi/guidance/star-schema .
