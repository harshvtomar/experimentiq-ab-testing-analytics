# Conditional campaign economics

The original experiment measures revenue, not campaign costs, margins or profit. All commercial inputs are hypothetical/user-supplied. The application starts with economics disabled; the workbook and exported demonstration explicitly label their example assumptions.

Let N be a nonnegative whole eligible audience, d the canonical historical revenue effect per assigned customer, k a fixed multiplier in [0,1], m a fixed contribution margin in [0,1], c nonnegative incremental delivery cost/customer, and F nonnegative fixed incremental setup cost. Source dollars are used without FX conversion.

|Output|Formula|Boundary behavior|
|---|---|---|
|Effective revenue uplift|k × d|Negative values remain negative|
|Projected incremental revenue|N × k × d|Zero audience gives zero revenue|
|Incremental gross contribution|N × k × d × m|Margin is assumed, not experimentally estimated|
|Variable delivery costs|N × c|Costs are per assigned, not converted customer|
|Total incremental costs|N × c + F|Setup is incurred even if N=0|
|Net campaign contribution|N × k × d × m − N × c − F|Not observed profit|
|Break-even effective uplift|(N × c + F)/(N × m)|Undefined when N × m=0; threshold is after multiplier|
|Break-even margin|(N × c + F)/(N × k × d)|Defined only for positive projected revenue; >1 is infeasible|
|Maximum delivery cost|k × d × m − F/N|Undefined at N=0; negative means no nonnegative delivery cost is affordable|
|Net return on cost|Net contribution/(N × c + F)|Undefined at zero costs, not infinite ROI|

No-email control is an incremental baseline: zero incremental revenue, contribution and campaign costs; break-even/return ratios are not applicable. Scenario comparisons apply the same assumptions to both interventions, not a fabricated budget allocation. Alternative cost differences may be represented directly as c/F only if nonnegative; cost-saving interventions are outside this implementation's stated domain.

Missing required assumptions produce unavailable outputs, not zeros. Invalid, nonfinite, negative costs, fractional audiences and out-of-domain margins/multipliers are rejected. Audience and cost inputs are bounded at 10^12 to avoid nonsensical numeric overflow. Break-even classification uses an absolute numerical tolerance of 10^-9 dollars. Zero multiplier suppresses measured effects; it is not evidence of no treatment effect. For a negative d, multiplying by less than one moves toward zero and is not conservative.

## Uncertainty
For pointwise interval [L,U], transform to [NkmL−Nc−F, NkmU−Nc−F]. The nonnegative affine coefficient makes endpoint order valid. For positive coefficient, coverage is inherited for this transformed historical estimand conditional on fixed assumptions, subject to the original bootstrap limitations. At zero coefficient, the interval collapses algebraically. Neither case establishes certain current-market profit.

This is not a prediction interval for realized future campaign totals. It excludes cost/margin uncertainty, audience changes, treatment effects on margin, interference, campaign execution risk and historical-to-modern transport uncertainty. There is no simultaneous coverage guarantee across selected interventions or scenarios. No p-value for business profitability is manufactured. One-at-a-time sensitivity explores assumptions; it is not a probability model for them.

## Implementation and reproduction
`src/economics.py` owns formulas and input validation. `src/economics_ui.py` adds the ninth page. `python -m src.business_pipeline` reads unrounded canonical Session 2 CSVs and exports demonstration/sensitivity tables, workbook inputs, Power BI tables and the executive report. `sql/economics.sql` independently checks 11 numerical outputs. The original 12 customer analytics queries remain intact.

The workbook holds live formulas and one editable input set for both treatments. Demo defaults: N=10,000; m=40%; c=$0.05; F=$500; k=1. These are not actual retailer economics. Raw/customer-level records remain excluded from Git.
