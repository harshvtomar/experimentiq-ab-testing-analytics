# EXPERIMENTIQ — WORK SESSION 2
## Formal inference and defensible experiment recommendations

Continue https://github.com/harshvtomar/experimentiq-ab-testing-analytics on main. Preferred model: GPT-6 Astra — Medium Reasoning if available. One focused five-hour Work session. Do not restart or modify unrelated repositories.

First inspect remote main and read README.md, PROJECT_STATE.md, SESSION_LOG.md, docs/QA.md, docs/METHODOLOGY.md, docs/KPI_DEFINITIONS.md and this prompt. Use the latest remote state as authoritative; deployment and CI may have been updated after this prompt was drafted. Preserve working components and rerun the pipeline and existing tests before edits.

## Established foundation
Authentic original Hillstrom 64,000-row, 12-column CSV, SHA-256 0e5893329d8b93cefecc571777672028290ab69865718020c78c7284f291aece. Three arms retained separately. Raw/row-level processed files are not committed; download with python -m src.pipeline. No missing values observed; repeated observations retained. Normalized geography is separate from original Surburban labels. Source row-position IDs are not customer IDs.

Python modules cover retrieval, validation, normalization, KPIs, filters, baseline balance, SRM, SQLite and exports. SQL schema and 12 queries independently reconcile all eight numeric arm KPI fields. Four Streamlit pages work with canonical functions. Latest initial local checkpoint: 23 tests passed including authentic integration and dashboard AppTest; consult QA for subsequent results. No formal outcome testing, confidence intervals or validated rollout decision was implemented in Session 1.

## Session 2 objectives
1. Define a retrospective analysis plan before computing inferential results: conversion primary; visit/spend secondary; each email versus control as primary treatment contrasts; explicitly classify email-versus-email. Define correction families and practical decision thresholds without claiming preregistration.
2. Implement tested binary-outcome inference and absolute/relative effect estimates with appropriate confidence intervals and documented small/zero-cell behavior. Report n and event counts. Do not label p-values as probability the null is true.
3. Handle multiple comparisons transparently (e.g. Holm within declared families); show raw and adjusted p-values with methods. Avoid fishing across endpoints and subgroups.
4. Analyze zero-heavy, skewed revenue using reproducible customer-level bootstrap within randomized arms; record seeds, resample counts, method, performance and convergence considerations. Do not substitute revenue among converters for revenue per assigned customer.
5. Extend integrity checks carefully; randomization is described by the source but cannot be audited from logs. Baseline attributes must never include visit, conversion or spend.
6. Segment exploration must emphasize interaction evidence, sample size, uncertainty, multiple comparisons and instability; avoid causal subgroup conclusions from separate significance tests. Respect project scope—no unnecessary ML.
7. Integrate estimates/uncertainty into dashboard and exports while preserving descriptive metrics. Explicitly label inference methods and assumptions. Distinguish statistical evidence, practical importance and business uncertainty; costs/margins are still absent.
8. Add meaningful unit/integration tests for hand-calculated examples, zero-event cases, symmetry, reproducibility, multiplicity, extreme revenue and dashboard correctness. Run existing suite and GitHub CI; record exact results and skips.
9. Publish meaningful commits, verify remote SHA and hosted CI. Inspect any existing deployed app and update it without creating unnecessary duplicate deployments.
10. Update PROJECT_STATE.md, SESSION_LOG.md, docs/QA.md and NEXT_SESSION_PROMPT.md for Session 3.

Keep raw customer data out of Git until redistribution rights are confirmed. Never fabricate results, timestamps, significance, profits, tests or deployment success. If original acquisition fails, report it; do not silently switch datasets. Session 3 economics/Excel and Session 4 portfolio completion are deferred.

Final report: verified commit/repository, completed inference methods, actual results with uncertainty and multiplicity context, tests/CI, actual deployment status, unresolved limitations and next-session checkpoint.
