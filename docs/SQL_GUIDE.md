# SQL analytics guide
`sql/schema.sql` creates a constrained customer table, useful indexes and the `arm_kpis` view. Integer cents avoid floating-sum currency drift; rates use REAL division and NULLIF guards. Python uses its own groupby implementation; `reconcile()` compares all eight numeric arm KPI columns to SQLite at tolerance 1e-12.

`sql/analysis.sql` contains 12 named queries executed by `run_queries()` and exported to `reports/sql/`:

1. Assignment counts and share (window total).
2. Conversion counts and rates.
3. Website visit counts and rates.
4. Observed total spend and mean spend per assigned customer.
5. Treatment-versus-control contrasts (CTE and meaningful single-control cross join).
6. Recency by arm (GROUP BY and HAVING).
7. Historical spending bands by arm, sorted by original band order.
8. Geographic categories by arm.
9. Historical channels by arm.
10. New-customer flag by arm (CASE label).
11. Historical merchandise purchasing composition (conditional aggregation).
12. Historical channel composition within each arm (partitioned window denominator).

All query results are descriptive. No query filters customers based on outcomes. Sample sizes accompany rates. Geographic categories are not locations; new customers already purchased within the source eligibility window. SQL table values preserve original source fields alongside normalized fields. Schema constraints enforce treatment mapping, numeric/binary validity and non-null fields; the Python validator additionally verifies full source schema and category coverage.

Run independently after the pipeline: `sqlite3 data/processed/experimentiq.sqlite < sql/analysis.sql` (if SQLite CLI is installed), or use `src.database.run_queries` from Python.
