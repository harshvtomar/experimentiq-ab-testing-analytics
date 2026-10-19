# Experiment methodology and statistical handoff
The source describes random selection with intended one-third probability for each of three arms. Actual counts need not be identical. We retain the complete supplied assignment population. Randomization logs, eligibility exclusions, deliverability and noncompliance data are unavailable; randomization cannot be independently audited.

## Integrity diagnostics
- Count assignments by arm; reject missing assignment or outcome data, unexpected labels and invalid numeric/binary outcomes.
- Check cross-outcome anomalies descriptively without dropping rows.
- Preliminary sample-ratio check against the source's stated probabilities: Pearson chi-square, 2 degrees of freedom, p=exp(-statistic/2). A diagnostic flag uses p<0.001. This threshold is an engineering diagnostic, not a test of effectiveness; no flag is not proof of correct randomization.
- Baseline comparisons use pre-treatment recency, history, merchandise indicators, newbie, historical channel, geography and spending bands. Categorical levels are one-hot encoded. Pairwise standardized mean differences divide mean difference by sqrt((sample variance A + sample variance B)/2). Undefined zero-variance or insufficient-data comparisons remain undefined. This is descriptive balance, without post-treatment variables or automatic causal conclusions.

## Missingness and repeated observations
No missing values were observed in this acquisition. Future missingness is a hard validation failure, requiring explicit remediation rather than imputation or changing denominators. The 6,562 repeated records after first occurrence are preserved. Without customer IDs, identical attributes and outcomes do not demonstrate duplicated people. Row position is only a stable trace key for this exact byte-pinned source.

## Limits and next inference contract
Primary estimand: difference in mean binary conversion per assigned customer for each email versus control. Secondary: visit probability and mean spend including zeros. Keep email-versus-email as a separately declared contrast. Session 2 must declare outcome/contrast families before testing, use an appropriate multiple-testing strategy and clearly distinguish confirmatory intentions from this retrospective analysis.

Prepare inference functions consuming normalized row data and explicit arm/outcome/seed parameters. Return effect estimate, uncertainty interval, raw and adjusted p-values, sample sizes, method and assumptions; do not use UI-formatted numbers. Implement zero-event, small-cell and heavy-tail safeguards. Bootstrap randomized customers within arms, not aggregate rows. Segment interaction evidence requires careful multiplicity handling; no rankings based only on noisy raw lifts.

No customer IDs, timestamps or chronological event stream are available. No long-term value, ROI, campaign profit, modern-market extrapolation or forecasting is claimed. No ML is needed for Session 1. Proposed future economics require user-editable assumptions clearly separated from observed data.
