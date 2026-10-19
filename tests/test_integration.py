import os
import json
import pandas as pd
import pytest
from src.config import ROOT,EXPECTED_ROWS
from src.download import load_raw,checksum,retrieve
from src.validate import validate
from src.preprocess import normalize
from src.pipeline import run
from src.metrics import aggregate

pytestmark=pytest.mark.integration
@pytest.fixture
def authentic():
    path=ROOT/'data/raw/hillstrom.csv'
    if not path.exists():
        if os.getenv('EXPERIMENTIQ_REQUIRE_DATA')=='1': pytest.fail('Authentic data required but missing')
        pytest.skip('Authentic data not acquired; integration NOT verified')
    return path

def test_authentic_source(authentic):
    d=load_raw(authentic)
    assert validate(d,EXPECTED_ROWS)['valid']
    assert len(d)==64000
    assert retrieve(authentic.parent)==authentic
    pd.testing.assert_frame_equal(load_raw(authentic),d)

def test_reproducible_pipeline(authentic,tmp_path):
    import shutil
    raw=tmp_path/'data/raw';raw.mkdir(parents=True)
    shutil.copy2(authentic,raw/authentic.name)
    shutil.copy2(authentic.with_suffix('.provenance.json'),raw/'hillstrom.provenance.json')
    before=checksum(raw/'hillstrom.csv')
    result=run(tmp_path)
    first=(tmp_path/'data/processed/customers.csv').read_bytes()
    run(tmp_path)
    assert first==(tmp_path/'data/processed/customers.csv').read_bytes()
    assert before==checksum(raw/'hillstrom.csv')
    assert result['reconciliation']['status']=='passed'
    assert pd.read_csv(tmp_path/'reports/arm_kpis.csv').n.sum()==64000

def test_dashboard_pages_and_filters(authentic):
    from streamlit.testing.v1 import AppTest
    app=AppTest.from_file(str(ROOT/'app.py'),default_timeout=30).run()
    assert not app.exception
    assert app.metric[0].value=='64,000'
    canonical=aggregate(normalize(load_raw(authentic)))
    pd.testing.assert_frame_equal(app.dataframe[0].value,canonical)
    for page in ['Treatment Comparison','Customer Segment Explorer','Data Quality & Methodology']:
        app.sidebar.radio[0].set_value(page).run()
        assert not app.exception
    app.sidebar.radio[0].set_value('Customer Segment Explorer').run()
    app.multiselect[0].set_value([]).run()
    assert not app.exception and 'No customers' in app.warning[0].value
    app.multiselect[0].set_value(['Web']).run()
    assert not app.exception
    expected=aggregate(normalize(load_raw(authentic)).query("channel == 'Web'"))
    pd.testing.assert_frame_equal(app.dataframe[0].value,expected)
