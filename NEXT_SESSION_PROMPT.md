# ExperimentIQ - maintenance and optional improvements

Continue the existing repository and Streamlit deployment; do not restart or create replacements.
Repository: https://github.com/harshvtomar/experimentiq-ab-testing-analytics
Live: https://experimentiq-ab-testing-analytics.streamlit.app/

Read remote main, README.md, PROJECT_STATE.md, SESSION_LOG.md, docs/QA.md and docs/RELEASE_NOTES.md first. Remote main is authoritative. Application QA fixes were published as 0eb68f4c7b807fa1b1a335cfa509188272061334; later commits contain final portfolio deliverables and evidence. Fetch the latest SHA rather than assuming this code checkpoint is the latest commit.

The four-session portfolio scope is delivered. This is maintenance guidance, not a required fifth development session. Current suite: 75 tests; 64 fixture-only and 11 authentic integration. Full final local regeneration passed; hosted code CI run 39601927562 passed. Final publication evidence is in docs/QA.md and the repository Actions history.

For any code/dependency change, restore pinned Python 3.12 requirements and run:
```
python -m src.pipeline
python -m src.statistical_pipeline
python -m src.business_pipeline
EXPERIMENTIQ_REQUIRE_DATA=1 python -m pytest -q
```
Preserve all 64,000 source rows, pinned checksum, 12 SQL analyses, statistical methods and families, 10,000 bootstrap replications/seed, conditional economics, seven-sheet workbook and nine dashboard pages. Keep row-level data outside Git until redistribution rights are established. Never replace authentic results with synthetic data. Tests may use synthetic fixtures.

Optional work, only when requested or supported:
1. Open/recalculate the existing workbook in native Microsoft Excel; record version, boundary cases and actual results. Current verification is Artifact Tool and LibreOffice, not Excel native.
2. Use Windows Power BI Desktop to import the existing package, execute/validate DAX, reconcile measures and create a native PBIX. Current package is not a rendered Power BI report.
3. With contemporary randomized data, preregister new hypotheses, allocation and sample-size design, add observed costs/margins and guardrails, then evaluate rollout thresholds. Do not change historical findings for presentation.
4. Clarify raw-data redistribution rights and maintain a legally permitted source/cache strategy.
5. Review dependencies and live-app availability periodically; validate changes with the full suite and a real browser. Streamlit may sleep; a successful GitHub push alone is not deployment verification.

PDF regeneration: install reportlab==4.4.9, ensure DejaVuSans.ttf and DejaVuSans-Bold.ttf are available (EXPERIMENTIQ_FONT_DIR can override the default Linux font folder), then run python scripts/build_case_study.py. Use the committed genuine screenshots. Render and inspect every page after edits. Excel builder requirements are in docs/EXCEL.md.

Update QA, project state and session log with actual commands/results. Publish meaningful commits, verify remote SHA and hosted CI. Distinguish historical evidence, hypothetical economics and unverified native-tool claims. No commercial savings, employment/client engagement or present-day performance is implied by this independent project.
