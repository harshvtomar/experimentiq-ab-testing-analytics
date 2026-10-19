import sqlite3
import re
import numpy as np
import pandas as pd
from src.config import ROOT

def load_sqlite(df, path):
    with sqlite3.connect(path) as connection:
        connection.executescript((ROOT/'sql/schema.sql').read_text())
        columns=','.join('"'+c+'"' for c in df.columns)
        placeholders=','.join('?' for _ in df.columns)
        connection.executemany(f'INSERT INTO customers ({columns}) VALUES ({placeholders})',df.itertuples(index=False,name=None))
        connection.commit()
    return path

def run_queries(path):
    chunks=re.split(r'-- query: ',(ROOT/'sql/analysis.sql').read_text())[1:]
    with sqlite3.connect(path) as connection:
        return {part.split('\n',1)[0]:pd.read_sql_query(part.split('\n',1)[1],connection) for part in chunks}

def reconcile(path, python_summary):
    with sqlite3.connect(path) as connection:
        sql=pd.read_sql_query('SELECT * FROM arm_kpis',connection).set_index('arm').sort_index()
    py=python_summary.set_index('arm').sort_index()
    if list(sql.index)!=list(py.index): raise AssertionError('Arm mismatch')
    for column in sql.columns:
        np.testing.assert_allclose(sql[column],py[column],rtol=1e-12,atol=1e-12,equal_nan=True)
    return {'status':'passed','metrics':list(sql.columns),'tolerance':1e-12}
