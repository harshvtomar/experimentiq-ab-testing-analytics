# Five-page report specification

Apply a restrained navy/blue/green palette, white background, readable units and a persistent label: historical two-week experiment; commercial scenarios hypothetical. These are build specifications, not screenshots of an implemented Power BI report.

1. **Experiment Performance:** assigned-customer and observed-spend cards from arm_performance; arm bars for weighted conversion, visit rate and spend/customer; table with arm counts. No invented date axis.
2. **Statistical Evidence:** one outcome and one contrast slicer; interval table showing point estimate, lower/upper bounds, raw/Holm p and family. Use binary percentage points versus revenue dollars/customer. Avoid a single pooled significance badge.
3. **Customer Segment Analysis:** one baseline variable slicer and treatment slicer; category effect table with n_t/n_c, events and pointwise intervals; separate adjusted interaction statistic. Show exploratory warning. Never sum samples across overlapping variables.
4. **Incremental Revenue Economics:** explicit hypothetical assumption table; treatment comparison net-contribution bars; driver slicer plus driver_value axis and treatment legend for sensitivity. Control baseline zero. Show conditional lower/upper values and break-even thresholds; state these are exported snapshots.
5. **Executive Decision Summary:** three questions—evidence, effect size, economics under assumptions. Show conditional replication recommendation and operational guardrails. Explain missing commercial evidence and historical transfer limitations. Link the Markdown executive report and Excel workbook.

Validation before publication: test single versus multiple contrast selections, no-data filters, undefined ratios, factor units, signed effects, source totals and no double counting. Save screenshots and native .pbix only after actual Desktop checks.
