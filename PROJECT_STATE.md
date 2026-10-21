# ExperimentIQ - final portfolio checkpoint

Repository: https://github.com/harshvtomar/experimentiq-ab-testing-analytics (main)
Live application: https://experimentiq-ab-testing-analytics.streamlit.app/

## Architecture and preserved evidence
Original Hillstrom CSV -> checksum/schema/quality validation -> preserved observations with separate normalized fields -> Python KPIs and constrained SQLite -> statistical inference -> conditional economics -> Streamlit, Excel and aggregate Power BI import assets.

64,000 rows, 12 original fields; SHA-256 `0e5893329d8b93cefecc571777672028290ab69865718020c78c7284f291aece`. All 6,562 repeated rows retained. No missing/invalid values found. Raw/customer-level files and SQLite remain excluded from Git because redistribution permission is unconfirmed. No original IDs, timestamps or assignment logs exist in the supplied file.

All 12 SQL analyses and eight KPI fields reconcile. Fisher/Newcombe binary inference, declared Holm families, 10,000-replication empirical customer bootstrap (seed 20261020), 28 subgroup comparisons and 12 interaction hypotheses remain intact. No Holm-adjusted interaction rejects. Statistical CSV results did not change during Session 4.

## Final features
- Nine-page Streamlit dashboard with live baseline filters, descriptive comparisons, inference, bootstrap diagnostics, subgroup exploration, recommendations and conditional economics.
- Canonical economics: explicit assumptions, break-even calculations, sensitivity, conditional uncertainty, 11-field SQL reconciliation and scenario exports.
- Seven-sheet Excel workbook, 113 formulas, three charts; Artifact Tool builder and verification evidence; unchanged delivered workbook SHA `5dbea525acb18d0d3d62ba6ef9279a53ec6f17c4900c95159ad4962b9eef32f4`.
- Power BI import package, grains/relationships, Power Query function and DAX specifications. No native PBIX or DAX execution.
- Six-page final PDF in `reports/session4/ExperimentIQ_Final_Case_Study.pdf`; reproducible ReportLab builder in `scripts/build_case_study.py`. All rendered pages visually inspected.
- Recruiter README; `docs/RESUME_AND_INTERVIEW.md` with two role-specific entries, 25 questions/answers and a 90-second explanation.

## Session 4 corrections
Published application commit `0eb68f4c7b807fa1b1a335cfa509188272061334`:
1. Preserve tiny p-values in strict JSON instead of decimal-place rounding to zero; scientific notation in inference tables.
2. Convert all-null SQL economic outputs to numeric missing values before reconciliation; zero-input scenarios now compare safely.
3. Clarify continuity-adjusted relative intervals versus multiplicity adjustment; label money as source dollars.
4. Refine title, responsive typography, wrapped metric labels and sidebar wording.

## Verification
Baseline: 70 passed. Expanded final local regression: **75 passed in 13.71s**, zero failures/skips, after regenerating all three pipelines. Committed logs and JUnit evidence: `reports/session4/verification/`. Hosted code CI run 39601927562 succeeded: 64 unit tests and 11 authentic integration tests; original acquisition and inference/economics regeneration succeeded. See `docs/QA.md` for final publication CI evidence.

All nine live pages opened in Chrome; changed filters/outcomes/treatments, empty channel selection, disabled assumptions, zero audience and 14 custom download events verified. Desktop 1440x1000 and representative narrow 390x844 layouts checked. Browser download bytes were not reread; canonical outputs are tested locally.

Workbook fully regenerated in a disposable directory; changed-input/reopen evidence matched existing delivery. LibreOffice headless recalculation matched Python, no formula errors. Native Microsoft Excel was not available. Power BI source tables independently match canonical exports; Windows Desktop, native PBIX and DAX rendering remain unverified.

## Maintenance, not another mandatory development session
`NEXT_SESSION_PROMPT.md` now describes maintenance and optional improvements. Preserve this repository and existing app. Remaining optional verification requires a native Excel session and a Windows Power BI Desktop session. Contemporary business recommendations require a new experiment with observed costs/margins and operational guardrails. Raw redistribution requires explicit rights clarification. No achieved commercial benefits are claimed.
