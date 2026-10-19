# KPI contract
For each assigned arm (or arm within a baseline-filtered slice):

|Metric|Formula|Unit|
|---|---|---|
|n|COUNT(all assigned rows)|customers|
|conversions|SUM(conversion)|customers who purchased|
|visits|SUM(visit)|customers who visited, not sessions|
|conversion_rate|conversions / n|fraction; multiply by 100 to display percent|
|visit_rate|visits / n|fraction|
|total_spend|SUM(spend_cents) / 100|source dollars|
|spend_per_customer|total_spend / n|dollars per randomized customer|
|Rate difference|100 × (rate A − rate B)|percentage points (pp)|
|Relative difference|100 × (metric A / metric B − 1)|percent; undefined when B=0|
|Spend difference|spend/customer A − spend/customer B|dollars/customer|

Use all assigned customers, including zero outcomes. Never average subgroup percentages without weighting by subgroup denominators. Filtered summaries are recomputed from rows. Empty or absent arms have n=0, sums=0, and undefined means/rates (`NaN`, shown as blank), not fabricated zero rates. Missing treatment or outcomes stop ingestion rather than excluding rows. No purchaser-only average is labeled revenue per customer.

The three comparisons are men's email minus control, women's email minus control, and men's email minus women's email. Current values are observed descriptive contrasts, not significance decisions. Total spend is observed revenue, not incremental profit. Currency is described by the author as dollars; no exchange-rate conversion is made.
