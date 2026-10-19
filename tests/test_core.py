import json
import sqlite3
import numpy as np
import pandas as pd
import pytest
from src.config import ARMS
from src.validate import validate,quality_report
from src.preprocess import normalize,filter_customers
from src.metrics import aggregate,comparisons,integrity,balance
from src.database import load_sqlite,run_queries,reconcile
from src.download import verify_source,retrieve

def test_schema_and_row_count(raw):
    assert validate(raw,4)['valid']
    with pytest.raises(ValueError): validate(raw,5)
    with pytest.raises(ValueError): validate(raw.drop(columns='spend'))

@pytest.mark.parametrize('column,value',[('conversion',2),('visit',None),('segment','Other'),('spend',-1),('history',np.inf),('recency',1.5),('recency',13),('channel','SMS'),('zip_code','Unknown'),('newbie',-1)])
def test_bad_data_rejected(raw,column,value):
    raw[column]=raw[column].astype(object);raw.loc[0,column]=value
    assert not quality_report(raw)['valid']
    with pytest.raises(ValueError): normalize(raw)

def test_normalization_preserves_raw_and_duplicates(raw):
    original=raw.copy();raw=pd.concat([raw,raw.iloc[[0]]],ignore_index=True)
    c=normalize(raw)
    pd.testing.assert_frame_equal(c[original.columns],raw)
    assert len(c)==5 and c.row_id.is_unique
    assert c.geography.iloc[0]=='Suburban' and c.zip_code.iloc[0]=='Surburban'
    assert c.arm.tolist()==['Control','Control',"Men's email","Women's email",'Control']
    assert quality_report(raw)['repeated_rows_after_first']==1
    pd.testing.assert_frame_equal(c,normalize(raw))

def test_metrics(clean):
    s=aggregate(clean).set_index('arm')
    assert s.loc['Control','conversion_rate']==.5
    assert s.loc['Control','spend_cents']==1234
    assert s.loc['Control','spend_per_customer']==6.17
    assert s.loc["Women's email",'total_spend']==20
    c=comparisons(s.reset_index()).iloc[0]
    assert c.conversion_rate_difference_pp==-50
    assert c.conversion_rate_relative_pct==-100

def test_empty_and_missing_arm(clean):
    s=aggregate(clean.iloc[:0]);assert s.n.sum()==0 and s.conversion_rate.isna().all()
    assert comparisons(s).conversion_rate_relative_pct.isna().all()
    s=aggregate(clean[clean.arm!="Women's email"])
    assert s.set_index('arm').loc["Women's email",'n']==0

def test_zero_reference(clean):
    clean['conversion']=0
    assert comparisons(aggregate(clean)).conversion_rate_relative_pct.isna().all()

def test_filters(clean):
    assert len(filter_customers(clean,{'channel':['Web'],'mens':[1]}))==2
    assert filter_customers(clean,{'channel':[]}).empty
    assert filter_customers(clean,{'channel':['Invalid']}).empty
    with pytest.raises(ValueError): filter_customers(clean,{'conversion':[1]})
    with pytest.raises(ValueError): filter_customers(clean,{'channel':'Web'})

def test_weighted_segments(clean):
    segments=aggregate(clean,['channel'])
    assert segments.n.sum()==len(clean)
    assert segments.conversions.sum()/segments.n.sum()==clean.conversion.mean()

def test_sql_independent_calculations(clean,tmp_path):
    db=load_sqlite(clean,tmp_path/'test.sqlite')
    assert reconcile(db,aggregate(clean))['status']=='passed'
    queries=run_queries(db);assert len(queries)==12
    assert queries['01_assignment_counts'].assigned_pct.sum()==pytest.approx(100)
    with sqlite3.connect(db) as c:
        with pytest.raises(sqlite3.IntegrityError): c.execute('UPDATE customers SET conversion=2')

def test_integrity_and_balance(clean):
    assert integrity(clean)['counts']['Control']==2
    assert integrity(clean.iloc[:0])['srm_p_value'] is None
    b=balance(clean);assert not b.covariate.str.contains('conversion|visit|spend').any()

def test_checksum_rejects_corruption(tmp_path):
    p=tmp_path/'hillstrom.csv';p.write_text('bad source')
    with pytest.raises(ValueError): verify_source(p)
    with pytest.raises(ValueError): retrieve(tmp_path)
