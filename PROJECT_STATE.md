# ExperimentIQ — Session 1 completed checkpoint
Repository: https://github.com/harshvtomar/experimentiq-ab-testing-analytics (main)
Live: https://experimentiq-ab-testing-analytics.streamlit.app/

## Architecture and authentic data
Original Hillstrom CSV → checksum verification → strict schema/quality validation → added normalized fields → canonical pandas KPIs and constrained SQLite verification → aggregate reports and four-page Streamlit dashboard.
64,000 records, 12 original columns; SHA-256 `0e5893329d8b93cefecc571777672028290ab69865718020c78c7284f291aece`. No observed missing/invalid values or cross-outcome inconsistencies. All 6,562 repeated rows after first occurrence retained. Raw spelling preserved with separate normalized geography; source-position IDs are not original customer IDs. Row-level data and SQLite remain excluded from Git.

## Completed Session 1 scope
- Source/license inspection and timestamped checksum manifest.
- Modular reproducible Python pipeline; validation, normalization, all requested KPIs/segments and exports.
- Constrained SQLite schema, arm KPI view, 12 working analyses; eight numeric KPI fields reconcile independently at 1e-12 tolerance.
- Assignment counts, missingness/outcome checks, preliminary SRM and descriptive covariate balance.
- Executive Overview, Treatment Comparison, Customer Segment Explorer, Data Quality & Methodology.
- Working live charts, baseline filters, empty selection behavior and five aggregate/diagnostic downloads.
- Documentation, computed descriptive observations, meaningful tests, CI and GitHub delivery.
- Live Streamlit deployment and real-browser verification, including saved screenshot.

## Verification and delivery
Latest application-code commit: `cd20f34cba6e035faf28225fd79e5f4d303c80b0` (final checkpoint adds only docs/screenshots). Local suite: 23 passed, 0 failed, 0 skipped. Hosted CI run 39309754651 passed; earlier run 39308327718 logs confirm 20 unit + 3 authentic integration tests. See docs/QA.md for commands, initial fixed failure and browser evidence.
Streamlit: Python 3.12, branch main, app.py. Web-only audience count 28,217 matched Python; empty-channel state verified; all five custom downloads completed. Desktop screenshot: screenshots/executive-overview.png.

## Blockers and limitations
No unresolved mandatory Session 1 implementation blocker. Raw dataset redistribution permission remains unconfirmed: continue excluding row-level files; obtain author permission before publicly bundling them. Fresh setup depends on the original host; cached bytes are verified and preserved. If host access fails, restore a known verified CSV plus manifest or investigate and document an authentic alternative without silently changing the checksum.

## Deferred intentionally
Session 2: hypothesis tests, confidence intervals, multiplicity correction, robust revenue uncertainty, segment interaction analysis and defensible recommendations. No statistical-significance or rollout claims yet.
Session 3: economics scenarios, Excel reporting and Power BI where available.
Session 4: final QA, dashboard polish and portfolio case study.
Continue using NEXT_SESSION_PROMPT.md; inspect latest main before editing. Do not restart.
