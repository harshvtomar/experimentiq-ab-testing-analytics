# Session 1 verification record
Environment: Python 3.12. Dependencies pinned in requirements.txt to the installed versions used for validation.

- `python -m src.pipeline`: completed on authentic original data; 64,000 records, 12 original fields, all 12 SQL queries executed; eight numeric arm KPI columns reconciled at 1e-12 tolerance.
- Initial `python -m pytest -q --junitxml=reports/test-results.xml`: 22 passed, 1 failed. The dashboard had an unterminated sidebar caption string. Fixed the string before delivery.
- Same command after correction: **23 passed in 6.43s**, 0 failures, 0 skips. Includes real-data reproducibility, all four dashboard pages, canonical KPI equality, channel filter and empty selection through Streamlit AppTest.
- Browser localhost attempt reached the user's separate existing local app, not the execution container. That tab was closed without interaction; this does not count as visual verification of ExperimentIQ.
- GitHub Actions on foundation commit `9f3f98db4c9fc74279bb7479710baad09b98204c`: both jobs passed. Run https://github.com/harshvtomar/experimentiq-ab-testing-analytics/actions/runs/39308327718 . Logs confirm 20 unit tests passed (3 integration deselected) and 3 authentic integration tests passed (20 unit deselected); no skips.
- Streamlit deployment initiated. Setup-form selection did not persist; hosted settings showed Python 3.14. Changed the settings control to Python 3.12 with keyboard selection, verified Selected 3.12, and saved. Browser verification pending build completion.

Synthetic rows exist only in tests/conftest.py and never feed project findings. Integration requires the original pinned file; CI sets EXPERIMENTIQ_REQUIRE_DATA=1 so missing real data fails.
