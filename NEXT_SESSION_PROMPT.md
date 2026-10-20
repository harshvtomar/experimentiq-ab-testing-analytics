# EXPERIMENTIQ — WORK SESSION 3
## Incremental Revenue Economics, Business Scenario Modeling, Excel Reporting and Power BI Integration

Continue https://github.com/harshvtomar/experimentiq-ab-testing-analytics on main. Live app: https://experimentiq-ab-testing-analytics.streamlit.app/ . Preferred model GPT-6 Astra — Medium Reasoning if available. One focused five-hour Work session. Do not restart, create another repository or deploy a duplicate app.

First inspect current remote main; read README.md, PROJECT_STATE.md, SESSION_LOG.md, docs/QA.md, docs/STATISTICAL_ANALYSIS_PLAN.md, docs/METHODOLOGY.md, docs/KPI_DEFINITIONS.md and reports/session2/STATISTICAL_REPORT.md. Re-run python -m src.pipeline, python -m src.statistical_pipeline and EXPERIMENTIQ_REQUIRE_DATA=1 python -m pytest -q. Inspect deployment/CI evidence from the latest checkpoint rather than assuming it.

Established: authentic 64,000-row Hillstrom experiment (checksum pinned); 12 SQL queries; eight KPI fields reconciled independently; eight dashboard pages; 46 passing local tests; hosted CI run 39378714645 passed 39 unit and 7 authentic integration tests on implementation commit c582909b345d29e0ca1ed79ba478f4b26f2187b9. All eight live pages and six new downloads were browser-verified. Source records retained, repeated rows not removed, raw/processed customer-level bytes excluded from Git. Retrospective SAP committed before inference as 2397f9dfb0f227dbfda728b5a11b89b03b9c3b59.

Session 2: Fisher tests, Newcombe/Wilson absolute CIs, approximate log-RR CIs, separate declared Holm families; 10,000 within-arm customer bootstrap replications at seed 20261020 with frequency-preserving multinomial resampling, percentile revenue CIs and separate Welch p-values. Fixed 28 subgroup contrasts and 12 additive interaction tests. All planned results exported as CSV and strict JSON with source/plan hashes. No adjusted interaction rejection supports targeting claims.

Observed effects versus control: men's conversion +0.6805 pp (95% pointwise CI 0.5014–0.8641), women's +0.3111 pp (0.1502–0.4745). Revenue/customer +$0.7698 (0.4888–1.0573) and +$0.4244 (0.1690–0.6810). These are historical two-week estimates, not profit or guaranteed future performance. Costs/margins are missing.

Session 3 tasks:
1. Build a clearly hypothetical economics layer: user-entered audience size, contribution margin, delivery cost, fixed campaign costs and optional conservative effect assumption. Never describe default assumptions as observed business facts. Label dollars consistently; do not invent currency conversions.
2. Calculate projected incremental revenue, contribution and net campaign value with explicit formulas and break-even thresholds. Propagate statistical uncertainty transparently with valid assumptions; do not multiply unrelated CI endpoints and call the result a calibrated joint interval. Maintain a no-assumptions state when costs/margin are missing.
3. Keep statistical evidence separate from economic scenarios. Retain three arms and pointwise-versus-adjusted distinctions. Do not turn exploratory subgroups into validated targeting policies.
4. Add usable dashboard scenario controls and exports without breaking the eight existing pages. Match all calculations to a tested canonical module and reconcile applicable formulas through SQL/Excel.
5. Create a professional Excel report with formulas, scenario inputs, provenance, statistical results and executive charts. Use the spreadsheet skill and validate formulas/recalculation. Do not fabricate real commercial profit.
6. Provide Power BI integration only where technically supported: clean aggregate tables, relationship/measure documentation and a usable supported artifact. Do not label documentation or CSVs as a verified .pbix dashboard. Explain any desktop/sign-in blocker precisely.
7. Update statistical/executive report with three separate judgments: evidence of effect, magnitude/uncertainty, and economics conditional on specified assumptions. Preserve all existing results and methodology.
8. Add meaningful tests for break-even calculations, edge cases, missing inputs, large audiences, uncertainty handling, Excel checks and regressions. Run complete suite and hosted CI, verify existing live app and key controls in a browser.
9. Commit meaningful checkpoints, verify remote SHA and CI; update PROJECT_STATE.md, SESSION_LOG.md, docs/QA.md and NEXT_SESSION_PROMPT.md for Session 4 final QA and portfolio case study.

No raw-data redistribution unless permission is established. No fabricated tests, deployment, Power BI outputs or model performance. Preserve original source and use documented acquisition if host is unavailable. Finish with actual deliverables, source/commit, tests/CI/deployment status, assumptions, limitations and remaining Session 4 tasks.
