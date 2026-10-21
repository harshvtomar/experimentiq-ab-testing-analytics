# Final portfolio release notes

## Session 4
Application fixes: `0eb68f4c7b807fa1b1a335cfa509188272061334`.

- Full-precision strict JSON prevents tiny p-values from becoming zero; tables use scientific notation.
- SQL/Python economic reconciliation accepts all-null ratio columns at boundary inputs.
- Clarified relative-interval wording and source-dollar units; refined responsive dashboard headings and labels.
- Added independent authentic Fisher/Newcombe/Welch/Holm comparisons, economics boundaries and Power BI source reconciliation. Final suite: 75 passed, no failures/skips.
- Completed all-nine-page browser traversal, all 14 custom downloads and representative narrow/desktop checks.
- Rebuilt workbook in a disposable directory and repeated LibreOffice recalculation without changing the delivered XLSX.
- Added final PDF, recruiter README, role-specific resume bullets, 25 interview questions, screenshot evidence and maintenance guidance.

No statistical CSV estimates, declared hypothesis families, bootstrap seed/replications, original data observations or workbook business assumptions were changed for presentation. JSON serialization preserves existing values more accurately.

## Verification boundaries
CI checks Python outputs, canonical data and delivered workbook structure/caches; it does not run native Excel or Power BI. Browser download events completed, but downloaded bytes on the user device were not independently reread. Representative responsive checks are not exhaustive device/browser certification. Power BI remains an import package. Source rights and modern-market transfer remain limitations, not implementation defects.

No release tag is required for use. Use an immutable commit SHA for a reproducible checkpoint; see Actions and docs/QA.md for publication verification.
