# ExperimentIQ: resume and interview guide

harshvtomar | Independent analytics portfolio project

Repository: https://github.com/harshvtomar/experimentiq-ab-testing-analytics
Live application: https://experimentiq-ab-testing-analytics.streamlit.app/

## Data Analyst resume entry
**ExperimentIQ - A/B Testing Analytics | Python, SQL, SQLite, Streamlit, Excel**
- Analyzed 64,000 customers from an authentic three-arm randomized email experiment using Python and 12 SQL analyses; reconciled eight KPI fields and preserved all source observations.
- Applied Fisher exact tests, Newcombe confidence intervals, Holm correction and 10,000-replication bootstrapping; estimated a 0.6805-percentage-point conversion increase for men's email versus control in the historical experiment.
- Built a nine-page Streamlit dashboard and seven-sheet formula-based Excel report; validated data, statistical outputs and scenario calculations with 75 automated tests and GitHub Actions.

## Business Analyst resume entry
**ExperimentIQ - Marketing Experiment Decision Support | SQL, Python, Streamlit, Excel**
- Evaluated two email treatments against a no-email control across 64,000 randomized customers, translating conversion, engagement and revenue evidence into conditional business recommendations.
- Built editable audience, margin and campaign-cost scenarios with break-even thresholds and sensitivity analysis; reconciled 11 economic outputs between Python and SQL without treating modeled contribution as realized profit.
- Delivered a nine-page decision-support dashboard, seven-sheet Excel workbook and executive case study linking effect size, uncertainty and commercial assumptions to a contemporary replication plan.

Use the actual current test count when updating these bullets. Do not claim Power BI dashboard development, corporate employment, client delivery, achieved savings, or a realized revenue increase. The Power BI deliverable is an import package and unexecuted measure specification.

## A natural 90-second explanation
I built ExperimentIQ to answer a retailer's practical question: should it send a men's merchandise email, a women's merchandise email, or no email? I used Kevin Hillstrom's original randomized experiment with 64,000 customer records and two-week outcomes.

I first built a reproducible Python pipeline that verifies the file checksum, validates the schema and preserves repeated observations. I used SQLite to independently check the main KPIs. Conversion was the primary outcome, with website visits and spend per assigned customer as secondary outcomes.

Both emails showed evidence of a positive conversion effect versus control in this historical experiment. For men's email, the estimated difference was about 0.68 percentage points, or 6.8 additional conversions per 1,000 assignments. I reported uncertainty and Holm-adjusted p-values, and used 10,000 customer bootstrap replications for spending.

The business challenge was that the dataset contains no campaign costs or margins. I therefore built a clearly hypothetical economics simulator, rather than claiming a profitable campaign. Users can change audience, margin and costs and see break-even thresholds and sensitivity.

The final delivery includes a nine-page Streamlit app, an editable Excel workbook, a case study and automated regression tests. My recommendation is a contemporary randomized replication with measured costs and operational guardrails before rollout.

## Technical interview questions and answers

### 1. Why did you choose this project?
It connects data engineering, SQL, statistics and business decisions using authentic randomized data. It also forces a useful distinction between a positive measured effect and a profitable intervention.

### 2. What was randomized?
The source describes random assignment to men's merchandise email, women's merchandise email or no email. These labels identify message content, not customer gender. Original assignment logs are unavailable, so the design claim cannot be independently audited.

### 3. Why does randomization matter?
Random assignment makes treatment independent of baseline customer characteristics in expectation. Under consistency, independence and no interference, group differences can estimate assignment effects. It does not guarantee exactly equal sample sizes or transport to a modern audience.

### 4. What does the control group provide?
It estimates purchasing and visits without the campaign during the same reporting window. Treatment revenue alone includes sales that may have occurred anyway. Incremental effects require comparison with control.

### 5. What was your primary outcome?
Conversion: customers who purchased divided by all customers assigned to an arm. Visits and two-week spend were secondary. The analysis plan was frozen before new inference, but after descriptive results were seen; it was retrospective, not preregistered.

### 6. What is the difference between percentage points and percent change?
Men's email conversion was about 1.2531% versus 0.5726% in control. Subtraction gives 0.6805 percentage points. Dividing the difference by the control rate gives about 118.84% relative change. The large relative number reflects the low baseline rate.

### 7. What does a p-value mean?
Assuming the null hypothesis and test assumptions, it quantifies how unusual an outcome at least as extreme as the observed one would be. It is not the probability that the null is true, the probability the decision is wrong, or the size of the business benefit.

### 8. Why use Fisher's exact test?
Conversion is binary and purchases are relatively rare. Fisher's two-sided test provides a consistent count-based comparison, including small-cell fixtures. I report effect sizes and intervals alongside p-values.

### 9. What does a 95% confidence interval mean?
Under the method's assumptions, a procedure repeated over comparable samples would cover the fixed estimand about 95% of the time. The observed interval is not a 95% probability distribution over that fixed parameter. These intervals are pointwise, not simultaneous across all comparisons.

### 10. Why Holm correction?
Testing several hypotheses creates more opportunities for false rejection. Holm adjusts the ordered p-values to control family-wise error within a declared family without requiring independent tests. The two conversion-versus-control tests form the primary family; secondary and exploratory families are separate. There is no global guarantee across all families.

### 11. Why can a confidence interval and adjusted p-value disagree?
The pointwise Newcombe interval is not multiplicity-adjusted and is not an exact inversion of Fisher's test. Family-specific rejection uses the Holm-adjusted p-value. I disclose these different constructions rather than making all displays imply the same decision rule.

### 12. Why bootstrap spending?
Spending has many zeros and a small number of large values. Within-arm customer resampling estimates uncertainty for mean spend differences without assuming normal individual spend. Percentile bootstrap intervals still have finite-sample and tail limitations.

### 13. How did you make the bootstrap efficient and reproducible?
I fixed the seed and used independent random streams for each arm. Repeated spend values were compressed into frequencies, then multinomial counts were drawn with probabilities proportional to their original frequencies. This preserves the empirical customer bootstrap distribution for the mean. It does not give each unique value equal weight.

### 14. Where do revenue p-values come from?
A separate approximate Welch unequal-variance test. A fraction of ordinary bootstrap draws above or below zero is not automatically a valid null-hypothesis p-value. Bootstrap intervals and Welch tests are explicitly distinguished.

### 15. Why revenue per assigned customer rather than per purchaser?
Purchasing is itself affected by treatment. Restricting the denominator to purchasers selects a post-treatment group and answers a different question. Including all randomized customers, including zeros, preserves the assignment-effect comparison.

### 16. How did you validate the data and SQL?
The pipeline verifies the original SHA-256, 64,000 rows, 12 columns, categories, missingness and numeric constraints. SQLite independently aggregates eight KPI fields and runs 12 analyses using CTEs, CASE, grouping, null-safe division and windows. SQL also independently reconciles 11 economic outputs.

### 17. Why retain repeated rows?
Identical attributes and outcomes do not prove duplicate customers. There are no original customer IDs. Dropping the 6,562 repeated rows after first occurrence would alter the randomized sample without evidence. Generated row IDs trace file positions only.

### 18. What did the integrity checks establish?
The preliminary equal-probability allocation check gave p about 0.904 and baseline standardized differences were small. These diagnostics did not flag an obvious imbalance; they do not prove correct randomization or rule out unseen data errors.

### 19. Did you identify a profitable customer segment?
No. Segments use pre-treatment attributes, but they are exploratory. None of the 12 planned additive-scale interaction tests rejected after Holm. Different subgroup significance labels are not evidence that the subgroup effects differ. Overlapping partitions must not be summed as distinct customers.

### 20. How do you calculate contribution and break-even delivery cost?
For audience N, historical revenue effect d, multiplier k, margin m, delivery cost c and fixed setup F: net contribution = N*k*d*m - N*c - F. The maximum delivery cost per customer is k*d*m - F/N for N greater than zero. A negative threshold means even free delivery cannot cover setup under those assumptions.

### 21. How do you handle zero or missing inputs?
Zero audience still incurs the assumed setup cost. Zero campaign cost makes net return on cost undefined. Missing required assumptions produce unavailable outputs, not zeros. Invalid input ranges are rejected. A zero affine coefficient collapses the statistical interval mechanically, not because future business outcomes are certain.

### 22. Why doesn't statistical significance guarantee profitability?
A treatment may increase purchasing but cost more to run than its incremental contribution. Costs and margins were not measured here. The commercial model is conditional on user inputs and the historical effect transferring; it is not observed profit or a future-profit prediction interval.

### 23. What were your most important QA discoveries?
Small positive p-values could round to zero during JSON serialization, so I introduced precision-preserving strict JSON. SQL reconciliation could fail on all-undefined numeric columns, so I made null conversion explicit. Regression tests cover both. The validated statistical estimates and decisions did not change.

### 24. How do the Streamlit, Excel and Power BI deliverables differ?
Streamlit is a live interactive application tested in a browser. Excel contains seven sheets, 113 formulas and three bound charts; its builder, input recalculation and export/reopen were tested with Artifact Tool and LibreOffice. Native Microsoft Excel was not tested. Power BI has validated aggregate CSVs, relationships, Power Query and DAX specifications, but no verified PBIX, executed DAX or rendered native report.

### 25. What would you do with contemporary data?
Define the primary outcome, economic threshold, sample size and multiplicity plan before the experiment. Capture assignment IDs, delivery/compliance, costs, margins, returns and unsubscribe/complaint guardrails. Run a new randomized experiment, audit missingness and interference, and use measured unit economics to support a rollout decision. Long-term outcomes require longer follow-up, not relabeling two-week spend as lifetime value.
