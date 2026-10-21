# ExperimentIQ — Statistical analysis report

## Executive decision summary
This is a retrospective analysis of the 2008 Hillstrom randomized email experiment, not a preregistered study. All 64,000 assignments and zero-spend outcomes are retained. Causal interpretation relies on the source-reported randomization and independent customers; original logs and IDs cannot be audited.

### 1. Is there evidence of an effect?
- Men's email minus Control: primary conversion Fisher p=1.16743e-13, Holm p=2.33485e-13; reject equal conversion rates within the primary family.
- Women's email minus Control: primary conversion Fisher p=0.000164999, Holm p=0.000164999; reject equal conversion rates within the primary family.

### 2. How large is the effect?
|Outcome / contrast|Estimate|95% pointwise CI|Raw p|Holm p|Family|
|---|---:|---|---:|---:|---|
|conversion: Men's email minus Control|0.6805 pp|[0.5014, 0.8641]|1.16743e-13|2.33485e-13|primary_conversion|
|conversion: Women's email minus Control|0.3111 pp|[0.1502, 0.4745]|0.000164999|0.000164999|primary_conversion|
|conversion: Men's email minus Women's email|0.3694 pp|[0.1746, 0.5663]|0.000232732|0.000465464|exploratory_email_comparison|
|visit: Men's email minus Control|7.6590 pp|[6.9953, 8.3227]|5.43736e-113|1.08747e-112|secondary_visit|
|visit: Women's email minus Control|4.5233 pp|[3.8894, 5.1574]|2.30099e-44|2.30099e-44|secondary_visit|
|visit: Men's email minus Women's email|3.1356 pp|[2.4284, 3.8428]|3.79405e-18|1.13822e-17|exploratory_email_comparison|
|spend: Men's email minus Control|0.7698 $/customer|[0.4888, 1.0573]|1.16381e-07|2.32763e-07|secondary_revenue|
|spend: Women's email minus Control|0.4244 $/customer|[0.1690, 0.6810]|0.0011294|0.0011294|secondary_revenue|
|spend: Men's email minus Women's email|0.3454 $/customer|[0.0291, 0.6569]|0.0304687|0.0304687|exploratory_email_comparison|

Conversion effects expressed per 1,000 assigned customers:
- Men's email minus Control: 6.81 additional conversions per 1,000 (pointwise 95% CI 5.01 to 8.64); relative uplift 118.84% (approximate continuity-adjusted log-RR interval 76.47% to 170.19%).
- Women's email minus Control: 3.11 additional conversions per 1,000 (pointwise 95% CI 1.50 to 4.75); relative uplift 54.33% (approximate continuity-adjusted log-RR interval 22.88% to 93.27%).

### 3. Is it economically meaningful?
Economic value is undetermined. Revenue is not profit. No delivery costs, contribution margin, capacity constraints or business-approved minimum effect are supplied. The estimated revenue difference is per assigned customer over two weeks, not a forecast for future customers.

## Conditional recommendation
Use the primary family evidence and effect intervals to prioritize a contemporary replication. Consider an email treatment only with costs, margins, unsubscribe/complaint guardrails and deliverability measured. Do not declare a profitable rollout or a validated segment targeting policy from this analysis. The men’s merchandise label describes message content, not customer gender.

## Design, methods and multiple testing
Primary conversion contrasts: two separate emails versus no-email control (Holm family size 2). Secondary visit and revenue contrasts each have separate size-2 families. Email-versus-email is an exploratory three-outcome family. No global family-wise guarantee is asserted across families. All planned results are shown.
Binary tests use two-sided Fisher exact p-values, Newcombe/Wilson risk-difference intervals and approximate continuity-adjusted log-RR intervals. CIs are pointwise, not Holm-adjusted or exact inversions of Fisher tests. A p-value is not the probability that the null is true. See docs/STATISTICAL_ANALYSIS_PLAN.md for the plan committed before Session 2 calculations.

## Revenue uncertainty and Monte Carlo checks
10,000 empirical customer bootstrap replications per arm; seed 20261020. Identical values are compressed into frequencies, with multinomial probabilities proportional to counts. This exactly preserves the empirical n-customer bootstrap distribution for means, including zeros. No equal-weight unique-value sampling occurs.
Percentile 95% intervals are accompanied by separate Welch approximate mean-test p-values; bootstrap tail fractions are not presented as null p-values.
|Contrast|Bootstrap SE|Analytic SE|Half-run endpoint drift / CI width|Warning|
|---|---:|---:|---:|---|
|Men's email minus Control|0.14609|0.14525|0.282%|False|
|Women's email minus Control|0.13134|0.13033|0.619%|False|
|Men's email minus Women's email|0.16093|0.15962|1.185%|False|

Inference calculation time in this run: 1.136 seconds. Monte Carlo stability does not establish nominal coverage under every heavy-tailed population.

## Segment exploration
Fixed pre-treatment partitions: channel, recency bands, history <=$200/>$200, newbie and two historical merchandise indicators. Segment effects are exploratory with Holm across 28 tests. All 12 planned interaction tests share a separate Holm family. Interaction is evaluated on the additive risk-difference scale with sparse-cell safeguards; it is not inferred from a difference in subgroup significance.
|Variable|Treatment|Interaction raw p|Holm p|Status|
|---|---|---:|---:|---|
|channel|Men's email|0.313086|1|approximate additive interaction evaluated|
|channel|Women's email|0.18376|1|approximate additive interaction evaluated|
|recency_band|Men's email|0.555722|1|approximate additive interaction evaluated|
|recency_band|Women's email|0.795986|1|approximate additive interaction evaluated|
|historical_spend_band|Men's email|0.0221543|0.221543|approximate additive interaction evaluated|
|historical_spend_band|Women's email|0.361752|1|approximate additive interaction evaluated|
|newbie|Men's email|0.518689|1|approximate additive interaction evaluated|
|newbie|Women's email|0.00835951|0.0919546|approximate additive interaction evaluated|
|mens|Men's email|0.281774|1|approximate additive interaction evaluated|
|mens|Women's email|0.0283998|0.255598|approximate additive interaction evaluated|
|womens|Men's email|0.433848|1|approximate additive interaction evaluated|
|womens|Women's email|0.00551841|0.0662209|approximate additive interaction evaluated|

Full sample sizes, rates, pointwise intervals and warnings are in segments.csv. Overlapping partitions, retrospective examination and approximate interaction tests prohibit confident subgroup-winner claims.

## Integrity and limitations
SRM diagnostic p=0.903693; this does not verify original assignment logs. Maximum absolute measured baseline SMD=0.01690.
Source provenance is checksum verified. Missing or invalid outcomes stop ingestion; trace-ID duplication stops inference. Exact repeated source rows remain because no original identity supports deduplication. There are no timestamps, long-term outcomes, campaign costs or margins. This historical sample does not establish modern-market transferability. Distributional assumptions, unobserved data errors and individual independence remain limitations.

## Reproduction
`python -m src.pipeline` then `python -m src.statistical_pipeline`; run `EXPERIMENTIQ_REQUIRE_DATA=1 python -m pytest -q`. See metadata.json for source/plan hashes, package versions, seed and replications. Row-level files are not redistributed. Session 3 adds explicit economics scenarios and reporting; no invented costs enter this report.
