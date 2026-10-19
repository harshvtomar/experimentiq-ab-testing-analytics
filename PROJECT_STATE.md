# ExperimentIQ — Session 1 checkpoint
Repository: https://github.com/harshvtomar/experimentiq-ab-testing-analytics (main)

## Data and architecture
Original Hillstrom CSV acquired: 64,000 rows, 12 source columns, checksum in reports/provenance.json. Source values retained; derived fields separately named. No missing/invalid categories or numeric values; 6,562 repeated rows retained. Raw and normalized customer-level data excluded from Git due to unconfirmed redistribution permission.

Modular Python pipeline, constrained SQLite database, KPI view, 12 SQL analyses, aggregate exports, baseline balance and preliminary SRM diagnostics implemented. Four Streamlit pages use the same canonical metrics. Conversion primary, visit/spend secondary. No formal outcome inference or rollout decision yet.

## Verification
Pipeline completed; all eight numeric arm KPI columns independently reconcile. Latest local suite: 23 passed, 0 failed, 0 skipped, including authentic integration and four-page AppTest. Initial caption syntax issue fixed. See docs/QA.md.

## Delivery state
Repository created. Implementation publication, hosted CI, visual screenshots and live deployment are in progress at this checkpoint. No live URL is claimed here yet.

## Remaining work
Finish publication/deployment verification and update this state. Session 2: formal inference, confidence intervals, multiplicity and cautious segment analysis. Sessions 3–4: economics/reporting and final case study. Dataset redistribution permission remains unconfirmed; keep row-level files ignored.
