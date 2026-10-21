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
