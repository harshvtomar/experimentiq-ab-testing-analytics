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
- Session 2 publication, hosted CI and real-browser verification pending at implementation checkpoint; append verified results after deployment. No claim of public success yet.
