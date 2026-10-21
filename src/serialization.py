"""Strict JSON records that retain float precision, including very small p-values."""
import math
import pandas as pd


def records(frame):
    result = []
    for row in frame.to_dict('records'):
        clean = {}
        for key, value in row.items():
            if pd.isna(value):
                clean[key] = None
            elif isinstance(value, float) and not math.isfinite(value):
                raise ValueError('Nonfinite analytical output')
            else:
                clean[key] = value
        result.append(clean)
    return result


def table_bundle(tables):
    return {name: records(table) for name, table in tables.items()}
