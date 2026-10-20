# ExperimentIQ
### A/B Testing & Incremental Revenue Optimization

A reproducible retail experimentation analytics case study built on Kevin Hillstrom's authentic 64,000-customer randomized email experiment. **Session 1 foundation**: descriptive results, data integrity, SQL verification and an interactive Streamlit MVP. Formal inference is reserved for Session 2.

## Business question
Which merchandise email, if any, should a retailer consider deploying to improve purchasing and revenue? Conversion is primary; website visits and two-week spend per assigned customer are secondary. All three experimental arms remain distinct.

## Computed findings
|Arm|Assigned customers|Conversions|Conversion rate|Visit rate|Spend/customer|
|---|---:|---:|---:|---:|---:|
|Control|21,306|122|0.5726%|10.6167%|$0.6528|
|Men's email|21,307|267|1.2531%|18.2757%|$1.4226|
|Women's email|21,387|189|0.8837%|15.1400%|$1.0772|

Observed total spend: **$67,258.13**. Men's email minus control conversion difference: **0.6805 percentage points**; women's email minus control: **0.3111 percentage points**. These are descriptive differences, **not statistically established improvements or rollout recommendations**. Outcomes span two weeks following the campaign; this is historical evidence, not a present-day revenue forecast.

## Reproduce (Python 3.12)
```bash
git clone https://github.com/harshvtomar/experimentiq-ab-testing-analytics.git
cd experimentiq-ab-testing-analytics
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.pipeline
EXPERIMENTIQ_REQUIRE_DATA=1 python -m pytest -q
python -m streamlit run app.py
```
Windows PowerShell activation: `.venv\Scripts\Activate.ps1`; set `$env:EXPERIMENTIQ_REQUIRE_DATA="1"` before running pytest. Network access to the author's dataset is required on first run. Subsequent runs verify the local checksum. A download or checksum failure stops processing rather than using synthetic data.

## Architecture
Original CSV → checksum verification → schema/quality validation → separate normalized fields → canonical Python KPIs and independent constrained SQLite analytics → aggregate reports and Streamlit.

- `src/`: retrieval, validation, preprocessing, metrics, SQLite and pipeline orchestration.
- `sql/`: constrained schema, KPI view and 12 meaningful analyses.
- `app.py`: Executive Overview, Treatment Comparison, Customer Segment Explorer, Data Quality & Methodology.
- `reports/`: computed aggregate KPIs, quality/provenance/SRM diagnostics, baseline balance and query exports.
- `tests/`: deterministic synthetic unit fixtures and explicitly real-data integration/AppTest coverage.
- `docs/`: business brief, source/license review, data dictionary, KPI contract, methodology and SQL guide.
- `PROJECT_STATE.md`, `SESSION_LOG.md`, `NEXT_SESSION_PROMPT.md`: continuation checkpoint.

## Verified foundation
64,000 rows and 12 original fields. No missing values, unexpected categories or invalid numeric values observed. The 6,562 repeated rows after first occurrence are retained. Original `Surburban` spelling remains; a separate geography field uses `Suburban`. No fabricated customer IDs or timestamps.

All eight numeric arm KPI fields reconcile between SQL and Python. Dashboard calculations reuse canonical functions; filters only use baseline fields, sample sizes accompany comparisons, and empty selections show an explanatory state. Downloads are labeled aggregate CSV/diagnostic JSON exports.

## Data provenance and licensing
[Original challenge](https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html) · [TFDS corroborating catalog](https://www.tensorflow.org/datasets/catalog/hillstrom). Retrieved from the original CSV URL; checksum and timestamp are in `reports/provenance.json`. No explicit dataset redistribution license was found. Raw/customer-level data and SQLite are excluded from Git. See [source review](docs/DATA_SOURCE.md).

## Testing and CI
`python -m pytest -m 'not integration' -q` runs fixture-only tests. Real-data tests skip explicitly if data is absent, unless `EXPERIMENTIQ_REQUIRE_DATA=1`, which makes absence fail. GitHub Actions has separate unit and authentic-integration jobs. The latter downloads and verifies the dataset before testing and cannot pass by silently skipping data acquisition. See `docs/QA.md` for actual run results and deployment status.

## Limits and roadmap
No original customer IDs, timestamps, assignment logs, costs, margins or lifetime outcomes. No claim that unadjusted raw means prove efficacy. Segment comparisons are exploratory.

1. **Session 1:** authentic data, Python/SQL foundation, integrity diagnostics and dashboard MVP.
2. **Session 2:** inference, confidence intervals, multiplicity, robust revenue uncertainty and segment interactions.
3. **Session 3:** explicit economics scenarios, Excel executive reporting and Power BI integration where available.
4. **Session 4:** final QA, deployment refinement and portfolio case study.

## Live dashboard and verification
[Open ExperimentIQ](https://experimentiq-ab-testing-analytics.streamlit.app/) — deployed to Streamlit Community Cloud, Python 3.12, branch `main`, entry point `app.py`.

All four pages were opened in a real browser. The Web-only filter returned 28,217 customers, independently matching Python. Clearing all channels produced the expected no-data state. All five custom download controls completed: arm KPIs, comparisons, filtered KPIs, baseline balance and quality report. The numerical tables are additionally verified through AppTest and SQL reconciliation. Browser downloads were observed completing; downloaded bytes on the user's computer were not re-read.

![Verified live executive overview](screenshots/executive-overview.png)

Local tests: **23 passed, 0 failed, 0 skipped**. [Verified CI on the latest application-code commit](https://github.com/harshvtomar/experimentiq-ab-testing-analytics/actions/runs/39309754651): both jobs passed. The final checkpoint changes documentation/screenshots only. See [QA evidence](docs/QA.md) and [Session 2 prompt](NEXT_SESSION_PROMPT.md).
