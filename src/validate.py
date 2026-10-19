"""Fail closed on missing, invalid, or unexpected analytical input; never drop rows."""
import numpy as np
import pandas as pd
from src.config import COLUMNS, CATEGORIES

def quality_report(df, expected_rows=None):
    errors = []
    if list(df.columns) != COLUMNS:
        errors.append('Schema mismatch (names or order)')
    if expected_rows is not None and len(df) != expected_rows:
        errors.append(f'Expected {expected_rows} records, observed {len(df)}')
    missing = {c:int(n) for c,n in df.isna().sum().items()}
    if any(missing.values()): errors.append('Missing values; pipeline refuses to change denominators')
    unexpected = {}
    for c, allowed in CATEGORIES.items():
        if c in df:
            unexpected[c] = sorted(set(df[c].dropna().astype(str)) - set(allowed))
            if unexpected[c]: errors.append(f'Unexpected {c} categories')
    numeric_invalid = {}
    for c in ['recency','history','mens','womens','newbie','visit','conversion','spend']:
        if c not in df: continue
        s = pd.to_numeric(df[c], errors='coerce')
        bad = ~np.isfinite(s)
        if c in ['mens','womens','newbie','visit','conversion']:
            bad |= ~s.isin([0,1])
        elif c == 'recency': bad |= ~s.between(1,12) | (s % 1 != 0)
        else:
            bad |= s < 0
            if c == 'spend': bad |= ~np.isclose(s * 100, (s * 100).round(), atol=1e-7, rtol=0)
        numeric_invalid[c] = int(bad.sum())
        if bad.any(): errors.append(f'Invalid numeric values: {c}')
    anomalies = {}
    if {'conversion','visit','spend'}.issubset(df.columns) and not any(numeric_invalid.values()):
        anomalies = {'conversion_without_visit':int(((df.conversion==1)&(df.visit==0)).sum()),
                     'positive_spend_without_conversion':int(((df.spend>0)&(df.conversion==0)).sum()),
                     'conversion_without_positive_spend':int(((df.conversion==1)&(df.spend==0)).sum())}
    return {'rows':len(df), 'columns':list(df.columns), 'missing':missing,
            'unexpected_categories':unexpected,'invalid_numeric_counts':numeric_invalid,
            'repeated_rows_after_first':int(df.duplicated().sum()),
            'duplicate_policy':'Retain all rows; no original customer identifier exists',
            'cross_outcome_anomalies':anomalies,'errors':errors,'valid':not errors}

def validate(df, expected_rows=None):
    report = quality_report(df, expected_rows)
    if not report['valid']:
        raise ValueError('; '.join(report['errors']))
    return report
