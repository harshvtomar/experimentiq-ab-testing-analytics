import pandas as pd
from src.validate import validate
from src.config import TREATMENTS, EXPECTED_SHA256, FILTERS

def normalize(df):
    validate(df)
    result = df.copy(deep=True)
    result.insert(0,'row_id',[f'{EXPECTED_SHA256[:12]}:{i:05d}' for i in range(1,len(df)+1)])
    result['arm'] = result.segment.map(TREATMENTS)
    result['geography'] = result.zip_code.replace({'Surburban':'Suburban'})
    result['history_band_order'] = result.history_segment.str[0].astype(int)
    result['spend_cents'] = (result.spend * 100).round().astype('int64')
    return result

def filter_customers(df, filters=None):
    result = df
    for column, values in (filters or {}).items():
        if column not in FILTERS: raise ValueError(f'Not a baseline filter: {column}')
        if not isinstance(values,(list,tuple,set)): raise ValueError('Filter values must be a collection')
        result = result.loc[result[column].isin(values)]
    return result.copy()
