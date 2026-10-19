# Session 1 verification record
Environment: Python 3.12. Dependencies pinned in requirements.txt to the installed versions used for validation.

- `python -m src.pipeline`: completed on authentic original data; 64,000 records, 12 original fields, all 12 SQL queries executed; eight numeric arm KPI columns reconciled at 1e-12 tolerance.
- Initial `python -m pytest -q --junitxml=reports/test-results.xml`: 22 passed, 1 failed. The dashboard had an unterminated sidebar caption string. Fixed the string before delivery.
- Same command after correction: **23 passed in 6.43s**, 0 failures, 0 skips. Includes real-data reproducibility, all four dashboard pages, canonical KPI equality, channel filter and empty selection through Streamlit AppTest.
- Browser localhost attempt reached the user's separate existing local app, not the execution container. That tab was closed without interaction; this does not count as visual verification of ExperimentIQ.
- CI and live browser deployment verification: pending at this checkpoint; will be updated after publication.

Synthetic rows exist only in tests/conftest.py and never feed project findings. Integration requires the original pinned file; CI sets EXPERIMENTIQ_REQUIRE_DATA=1 so missing real data fails.
