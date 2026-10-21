# Session 1 verification record
Environment: Python 3.12. Dependencies pinned in requirements.txt to the installed versions used for validation.

- `python -m src.pipeline`: completed on authentic original data; 64,000 records, 12 original fields, all 12 SQL queries executed; eight numeric arm KPI columns reconciled at 1e-12 tolerance.
- Initial `python -m pytest -q --junitxml=reports/test-results.xml`: 22 passed, 1 failed. The dashboard had an unterminated sidebar caption string. Fixed the string before delivery.
- Same command after correction: **23 passed in 6.43s**, 0 failures, 0 skips. Includes real-data reproducibility, all four dashboard pages, canonical KPI equality, channel filter and empty selection through Streamlit AppTest.
- Browser localhost attempt reached the user's separate existing local app, not the execution container. That tab was closed without interaction; this does not count as visual verification of ExperimentIQ.
- GitHub Actions on foundation commit `9f3f98db4c9fc74279bb7479710baad09b98204c`: both jobs passed. Run https://github.com/harshvtomar/experimentiq-ab-testing-analytics/actions/runs/39308327718 . Logs confirm 20 unit tests passed (3 integration deselected) and 3 authentic integration tests passed (20 unit deselected); no skips.
- Streamlit deployment initiated. Setup-form selection did not persist; hosted settings showed Python 3.14. Changed the settings control to Python 3.12 with keyboard selection, verified Selected 3.12, and saved. Browser verification pending build completion.

Synthetic rows exist only in tests/conftest.py and never feed project findings. Integration requires the original pinned file; CI sets EXPERIMENTIQ_REQUIRE_DATA=1 so missing real data fails.

## Completed delivery verification
- Final application-code commit: `cd20f34cba6e035faf28225fd79e5f4d303c80b0`. Local suite after narrow-screen label fixes: **23 passed in 7.27s**, 0 failures, 0 skips (`python -m pytest -q --junitxml=reports/test-results.xml`).
- Hosted CI for that commit: run 39309754651 completed successfully; https://github.com/harshvtomar/experimentiq-ab-testing-analytics/actions/runs/39309754651 . Earlier detailed logs verify the 20-unit/3-integration split; test sources did not change in the UI commit.
- Live app: https://experimentiq-ab-testing-analytics.streamlit.app/ . Hosted settings saved as Python 3.12. All four pages opened in the connected Chrome browser and genuine Plotly charts rendered. The app downloaded original bytes matching the source pin; hosted provenance was visible on the methodology page.
- Executive Overview displayed 64,000 customers, 3 arms and $67,258.13 observed spend. Screenshot captured after fixing narrow-screen clipped metric values/titles and recaptured on continuation (2026-10-20).
- Treatment Comparison rendered three comparisons and charts.
- Customer Segment Explorer: removed Multichannel and Phone; Web-only count was 28,217, matching an independent pandas calculation. Removed Web as well; count became 0 with the intended explanatory warning. No exception was displayed.
- Data Quality & Methodology rendered source manifest, completeness, validity, SRM and explanatory limits; expanded baseline balance successfully.
- All five custom downloads completed in the browser: arm_kpis CSV, comparisons CSV, filtered_kpis CSV, baseline_balance CSV and quality JSON. Filenames were returned by download events. Local downloaded bytes were not read back; corresponding numerical payloads are tested through canonical tables and pipeline exports.
- An initial download wait timed out; reconnected and used paired event/click operations to confirm completion. This was a browser automation recovery, not an application-code defect.
- A standalone urllib request encountered Streamlit redirects; do not cite that request as HTTP-200 validation. Deployment acceptance is based on actual interactive browser rendering.
- Final checkpoint adds docs/screenshots only; verify its own Actions run from the repository after publication. No additional application tests are claimed beyond the runs above.

# Session 2 verification
- Inspected remote main at `e3fb36be94ff74660525fbed9567a692ee0392ed`, all checkpoint documents and existing modules/SQL/tests before edits.
- Runtime dependencies required reinstallation; first pytest invocation could not start (pytest absent). Restored pinned requirements. Existing pipeline completed and baseline suite passed: **23 passed in 6.35s**.
- Retrospective plan committed separately before inferential calculations: `2397f9dfb0f227dbfda728b5a11b89b03b9c3b59`.
- Initial inference unit suite: 18 passed; one precision warning from scipy Welch on a small constant synthetic arm. Implemented the algebraically equivalent Welch statistic/df directly and tested against scipy on a nondegenerate example; no change to the analysis plan.
- `python -m src.statistical_pipeline`: completed on 64,000 authentic rows with 10,000 replications/arm. All three bootstrap endpoint drift ratios below 1.2% of CI width; bootstrap and analytic SEs agree within the tested 5% tolerance. Exact runtime/package/plan/source hashes in reports/session2/metadata.json.
- `python -m pytest -q --junitxml=reports/test-results.xml`: **46 passed in 12.32s**, 0 failed, 0 skipped, no warnings. Includes prior tests; independent statsmodels CI/Holm references; known Fisher example; seed/empirical-bootstrap moment tests; heavy tails; all eight pages through AppTest; canonical table equality and real-data exports.
- Published implementation to main as `c582909b345d29e0ca1ed79ba478f4b26f2187b9`; fetched remote and synchronized local main.
- Hosted run https://github.com/harshvtomar/experimentiq-ab-testing-analytics/actions/runs/39378714645 succeeded. Actual job logs: **39 passed, 7 deselected in 1.23s** (unit); **7 passed, 39 deselected in 15.02s** (authentic integration). No skips/failures. Authentic acquisition and the full inference pipeline both succeeded as explicit preceding steps.
- Same live app verified in connected Chrome on 2026-10-20. All eight pages rendered. Overview retained 64,000 customers and $67,258.13 spend; source page displayed matching pinned checksum and 64,000 valid records. The original comparison and customer explorer pages also opened without an exception.
- New controls: changed Outcome from conversion to visit; changed bootstrap comparison to women's email versus control and observed updated histogram; changed segment partition to newbie and treatment to women's email and observed two corresponding effects and sample-size table.
- All six new downloads completed, with browser event filenames: binary_inference.csv, revenue_inference.csv, all_segment_effects.csv, all_interactions.csv, ExperimentIQ_Statistical_Report.md and inferential_results.json. Browser-downloaded bytes were not reread; canonical local payloads and page table equality are tested.
- Saved actual browser screenshot as screenshots/statistical-significance.png. Visual inspection identified numeric intermediate ticks for binary subgroup levels; set forest y-axis to categorical. This is a presentation change only, with no altered calculations.

- Final local verification after categorical-axis fix: `EXPERIMENTIQ_REQUIRE_DATA=1 python -m pytest -q --junitxml=reports/test-results.xml` — **46 passed in 11.55s**, zero failures/skips.

# Session 3 — 2026-10-21
- Inspected remote main at 4afa95e77d4ead1275b696a566b6d350d91f8f8f and read prior checkpoints, methods, source modules, tests and analytical outputs.
- Original pipeline passed. Statistical pipeline initially could not find statsmodels package metadata after runtime restoration; restored the existing pinned requirements, then inference completed. Baseline: **46 passed in 12.24s**. No source/statistical methods changed.
- Added canonical economics, independent SQL arithmetic, sensitivity, ninth dashboard page and business exports. First targeted economics/UI run: **20 passed in 4.07s**, with six pandas concat deprecation warnings. Changed sensitivity assembly to records, resolving the warnings.
- First complete workbook suite: 66 passed, 2 failed. One test assumed a chart ZIP path; corrected it to the actual valid OOXML chart location. Boundary recalculation exposed an authoring-engine zero/blank comparison issue; replaced blank equality with ISNUMBER to preserve zero. Both workbook tests passed after correction.
- Final local command `EXPERIMENTIQ_REQUIRE_DATA=1 python -m pytest -q --junitxml=reports/test-results.xml`: **70 passed in 15.20s**, zero failures/skips/warnings. All original eight pages and the ninth simulator are covered through AppTest.
- Workbook: seven sheets/three bound charts; actual changed-input, zero/missing/invalid cases recalculated; exported/reopened; all seven rendered previews inspected. Source p-values retain full float serialization. Hash manifest binds builder, input JSON, workbook and recalculation evidence.
- LibreOfficeDev 26.8 headless opened/recalculated a disposable workbook copy. Net/interval values matched and worksheet error-cell scan found zero errors. Native Microsoft Excel was not run.
- Power BI data grains/keys and source-value equivalence tested. Linux environment has no Power BI Desktop; no .pbix or executed DAX claim.
- Session 3 implementation publication and hosted verification follow this checkpoint.

### Session 3 hosted acceptance — 2026-10-21
- Implementation commit c64133e894e136fa4daecf9e564c1da8dcc57410 reached remote main. Actions run 39562622600 succeeded: unit job 119097224402 **60 passed, 10 deselected in 1.44s**; authentic job 119097224143 **10 passed, 60 deselected in 15.27s**. Acquisition, statistical regeneration and economics SQL reconciliation succeeded before integration tests. No skips/failures.
- Existing Streamlit app was asleep; woke it using its public control and verified Executive Overview (64,000 participants; $67,258.13 observed spend) and the ninth economics page in connected Chrome.
- Opt-in disabled state correctly withheld an economic conclusion. Demonstration men's net $2,079.31; increasing audience to 20,000 gave $4,658.62; zero audience gave −$500.00. Restoring 10,000 and selecting women's email gave $697.65 with conditional range −$323.86 to $1,723.82. Results match the canonical arithmetic.
- All three download events completed: ExperimentIQ_Current_Scenario.csv, ExperimentIQ_Sensitivity.csv and ExperimentIQ_Business_Analytics_Report.xlsx. Browser-downloaded bytes were not reread; local payloads/workbook are separately tested.
- Browser review exposed Markdown interpretation of paired currency symbols in the interval caption. Changed its labels to USD without changing calculations. All original eight pages remain covered by AppTest; this acceptance did not repeat a full live traversal of those pages.

- Final caption-only correction: after restoring runtime dependencies (pytest initially absent), full local regression passed **70 tests in 14.65s**, no skips/failures. Commit 7b999dec7efad0d79e60ce4333f4085df1c3c6a1 reached remote; hosted run 39600063982 succeeded in both jobs. Live reload confirmed plain USD interval labels and unchanged values. Actual screenshot: screenshots/economics-simulator.png. Subsequent checkpoint changes only documentation/screenshots.

# Session 4 - final regression and portfolio QA

## Baseline and corrections
Inspected remote main at `eece6c9b32d31b4458de4573d9cf283fffa0d785`, the required checkpoint/method/report documents, Python/SQL/dashboard/economics/workbook code and tests. Ran all three pipelines and the authentic-data suite: **70 passed in 13.42s**, no failures/skips.

Found and corrected two numerical reporting defects:
- pandas JSON decimal-place serialization rounded sufficiently small nonzero p-values to zero. Shared strict serialization now preserves native floating-point precision and maps missing values to JSON null; infinite values fail. Dashboard p-value columns use scientific notation. Existing statistical estimates, CSV outputs and decisions remain unchanged.
- SQL reconciliation received object-typed all-null columns for undefined economics ratios at zero inputs. Explicit numeric conversion preserves missingness and permits correct comparison. The new boundary test initially produced **1 failed, 74 passed in 14.54s**; corrected run: **75 passed in 14.41s**.

Also clarified continuity adjustment versus multiplicity adjustment, replaced an unsupported USD label with source dollars, and refined title/spacing/responsive metric labels. Published application commit: `0eb68f4c7b807fa1b1a335cfa509188272061334`.

## Final reproducibility run
After continuation reset the runtime packages, restored `requirements.txt` (pytest was initially absent). Executed:
```
python -m src.pipeline
python -m src.statistical_pipeline
python -m src.business_pipeline
EXPERIMENTIQ_REQUIRE_DATA=1 python -m pytest -q --junitxml=reports/session4/verification/tests.xml
```
All commands completed. **75 passed in 13.71s; 0 failed, 0 skipped.** Logs and JUnit are committed under `reports/session4/verification/`. Only elapsed-runtime metadata changed on regeneration; restored that nondeterministic metadata to the published checkpoint. Statistical CSVs, business exports, data checksum and delivered workbook remained unchanged.

New independent checks compare authentic Fisher tests, Newcombe intervals, Welch p-values and all Holm families with reference implementations; verify SQL economics at zero audience/margin/costs, very large audience and break-even; exercise negative uplift and sensitivity slopes; reconcile all eight Power BI fact exports. Existing tests cover missing/invalid inputs, filtered/empty data, dashboard tables, bootstrap reproducibility and workbook formulas/caches. Synthetic fixtures never feed reported experimental findings.

## Hosted code CI
[Run 39601927562](https://github.com/harshvtomar/experimentiq-ab-testing-analytics/actions/runs/39601927562), commit `0eb68f4c7b807fa1b1a335cfa509188272061334`, completed successfully.
- Unit job 119228304809: **64 passed, 11 deselected in 1.18s**.
- Authentic integration job 119228304335: **11 passed, 64 deselected in 16.71s**.
- Original data acquisition, inference reproduction and economic SQL reconciliation succeeded before integration testing. Deselection is intentional suite separation, not skipping real-data validation.

## Live browser QA
Existing public app: https://experimentiq-ab-testing-analytics.streamlit.app/ . Connected Chrome opened the actual deployed app after the code push and showed the new title/sidebar/currency caption. No deployment conclusion was inferred from Git alone.

| Page | Actual browser check |
|---|---|
| Executive Overview | 64,000 customers, three arms, 67,258.13 observed spend; Plotly charts and table rendered. |
| Treatment Comparison | Three comparisons, absolute/relative rate differences and spend comparisons rendered. |
| Customer Segment Explorer | Web-only filter returned 28,217, independently matching Python; clearing all channels returned zero with the intended no-match state. |
| Data Quality & Methodology | Pinned SHA, 64,000 valid rows, completeness and 6,562 repeats visible; baseline balance expanded. |
| Statistical Significance | Conversion forest rendered; changing Outcome to visit updated estimates/intervals. |
| Revenue Uplift Analysis | Revenue forest, diagnostics and histogram rendered; changing bootstrap comparison to women's email versus control updated the histogram. |
| Segment Effect Explorer | Changed partition to newbie and treatment to women's email; two level-specific estimates rendered with sample-size table and interaction caution. |
| Business Recommendations | Correct primary effect magnitudes/Holm p-values, unknown profitability and contemporary replication recommendation visible. |
| Business Economics & ROI Simulator | Disabled assumptions withheld conclusions. Enabled demo men's net 2,079.31; zero audience net -500; restored 10,000 and switched to women's net 697.65, interval -323.86 to 1,723.82. Inputs and conditional labels matched canonical Python. |

All **14 custom download events completed**: arm KPIs, comparisons, filtered KPIs, baseline balance, quality report, binary inference (visit), revenue inference, all subgroup effects, all interactions, statistical report, inference JSON, current scenario, sensitivity analysis and Excel workbook. Downloaded bytes on the user's computer were not reread. Payload correctness is independently covered by canonical outputs/tests. Built-in Plotly toolbar exports were not exhaustively tested.

Representative desktop viewport 1440x1000 and narrow 390x844 checks: overview metrics/charts and economics controls/metrics/interval text rendered legibly; navigation expanded/collapsed and pages changed. Wide data tables remain horizontally scrollable rather than squeezing numerical columns. This is not exhaustive device certification. Viewport override was reset after QA. Genuine captures are in `screenshots/session4/`.

One checkbox automation `check()` did not change state; DOM inspection confirmed it remained unchecked, and clicking the visible label enabled it. This was an automation recovery, not a verified app defect.

## Excel, Power BI and PDF
- Full unchanged workbook builder ran in a disposable directory; regenerated recalculation/reopen evidence matched delivery exactly. Seven sheets, 113 formulas, three bound charts and no broken/error formulas were checked. Original workbook SHA remained `5dbea525acb18d0d3d62ba6ef9279a53ec6f17c4900c95159ad4962b9eef32f4`.
- Fresh LibreOffice headless open/recalculation of a disposable copy matched Python for net/interval cells E22:F24; no formula error cells. See Session 4 JSON evidence. Prior seven-sheet visual review remains recorded in Session 3; no workbook layout change was made. Native Microsoft Excel was not run.
- Power BI grains/keys/source values and integration instructions reviewed; eight fact exports reconciled by authentic-data tests. No Windows Power BI Desktop, native PBIX, executed DAX or rendering claim.
- Six-page ReportLab case study uses canonical aggregate CSVs and genuine browser screenshots. Rendered every page with Poppler and visually inspected all six. Embedded DejaVu fonts corrected an initial standard-font rendering issue; no final clipping/overlap found. The PDF is not a replacement for interactive dashboard QA.

## Remaining limits
No known unresolved regression failure. Native Microsoft Excel and native Power BI verification require their supported application environments. Raw redistribution permission remains unresolved. Economics remains hypothetical; modern rollout needs a contemporary experiment and measured commercial inputs.
