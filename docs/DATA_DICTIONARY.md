# Data dictionary

Missing original fields are not imputed. Validation rejects incomplete data so denominators cannot silently drift. Raw column order is checked.

|Field|Values/type|Role|Definition|
|---|---|---|---|
|recency|Integer 1–12|Baseline|Months since last purchase|
|history_segment|Seven original labels|Baseline|Historical dollar spending band; retained as provided|
|history|Nonnegative number|Baseline|Dollars spent in preceding year|
|mens|Binary 0/1|Baseline|Purchased men’s merchandise in preceding year; not customer gender|
|womens|Binary 0/1|Baseline|Purchased women’s merchandise in preceding year; not customer gender|
|zip_code|Urban / Rural / Surburban|Baseline|Geographic category, not an actual postal code|
|newbie|Binary 0/1|Baseline|New customer during preceding twelve months; not a non-purchaser|
|channel|Phone / Web / Multichannel|Baseline|Historical purchase channel|
|segment|Mens E-Mail / Womens E-Mail / No E-Mail|Assignment|Randomized email arm|
|visit|Binary 0/1|Outcome|Visited website during two-week follow-up|
|conversion|Binary 0/1|Primary outcome|Purchased during two-week follow-up|
|spend|Nonnegative number|Outcome|Dollars spent during two-week follow-up|
|row_id|Text|Derived trace|Checksum prefix plus one-based original record position; not a customer ID or timestamp|
|arm|Control / Men’s email / Women’s email|Derived assignment|Readable treatment mapping from segment|
|geography|Urban / Rural / Suburban|Derived baseline|Surburban spelling normalized separately|
|history_band_order|Integer 1–7|Derived baseline|Original history band prefix for sorting|
|spend_cents|Nonnegative integer|Derived outcome|Spend × 100 rounded to cents for exact sums; source monetary precision is checked|
