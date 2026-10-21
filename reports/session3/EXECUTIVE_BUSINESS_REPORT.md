# ExperimentIQ — Executive business report

## Objective and evidence
Determine which explicit campaign assumptions could make historical email effects economically attractive. Hillstrom randomized 64,000 customers across two merchandise emails and no-email control. Outcomes span two weeks. Conversion is primary; visits and spending are secondary.

### 1. Is there statistical evidence of an effect?
- Men's email: conversion difference 0.6805 pp; 95% pointwise CI [0.5014, 0.8641]; primary Holm p=2.33485e-13.
- Women's email: conversion difference 0.3111 pp; 95% pointwise CI [0.1502, 0.4745]; primary Holm p=0.000164999.

### 2. How large is the effect?
- Men's email: $0.7698 additional revenue per assigned customer, 95% percentile bootstrap CI [$0.4888, $1.0573].
- Women's email: $0.4244 additional revenue per assigned customer, 95% percentile bootstrap CI [$0.1690, $0.6810].

### 3. Under which assumptions is it attractive?
Illustration only: 10,000 eligible customers; 40% contribution margin on incremental sales; $0.05 incremental delivery cost per customer; $500 fixed incremental setup; multiplier 1. All commercial assumptions are invented demonstration inputs, not measured facts.
|Intervention|Revenue ($)|Gross contribution ($)|Total costs ($)|Net contribution ($)|Conditional lower–upper ($)|Break-even margin|Maximum delivery cost ($)|
|---|---:|---:|---:|---:|---:|---:|---:|
|Men's email|7,698.27|3,079.31|1,000.00|2,079.31|955.38 to 3,229.10|12.99%|0.2579|
|Women's email|4,244.12|1,697.65|1,000.00|697.65|-323.86 to 1,723.82|23.56%|0.1198|

Control is the zero incremental baseline. Net return on cost is net contribution / incremental campaign costs, undefined at zero costs. It is a scenario ratio, not realized ROI.

## Decision and limitations
Both emails have evidence of a positive primary conversion effect in this historical experiment. The supplied scenario can be changed to favorable or unfavorable by changing margin, delivery costs or setup costs. No subgroup targeting policy is validated by the adjusted interaction tests.
Use a contemporary randomized replication with measured costs, contribution margin, unsubscribe/complaint and deliverability guardrails. Set a business-approved economic threshold before the replication. Do not treat statistical significance as a rollout decision.
Conditional intervals transform the existing pointwise revenue interval by fixed nonnegative audience × multiplier × margin and subtract fixed costs. They exclude commercial-input uncertainty, treatment effects on margin, audience mix changes, future realized campaign variation and market drift. They are not calibrated future-profit prediction intervals. No joint coverage across treatment choices is claimed.
All source rows and zero-spend customers remain. Original IDs, logs and timestamps are unavailable. Dataset redistribution rights remain unclear; only aggregate tables are included.

## Reproduction and handoff
`python -m src.business_pipeline` regenerates these scenarios, Power BI aggregates, workbook input JSON and the report from canonical Session 2 exports. Excel formulas provide editable calculations. See docs/ECONOMICS.md, docs/EXCEL.md and powerbi/README.md for formulas, build and verification boundaries.
