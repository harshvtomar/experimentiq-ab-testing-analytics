import os
import hashlib
import pandas as pd
import pytest
from src.config import ROOT
from src.economics import Assumptions, DEMO, compare
from src.business_pipeline import run

pytestmark=pytest.mark.integration

@pytest.fixture(autouse=True)
def require_data():
    if not (ROOT/'data/raw/hillstrom.csv').exists():
        if os.getenv('EXPERIMENTIQ_REQUIRE_DATA')=='1':pytest.fail('Authentic data required')
        pytest.skip('Real-data economics not verified')

def test_canonical_business_export_preserves_statistics():
    paths=list((ROOT/'reports/session2').glob('*.csv'))
    before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    table,check=run()
    assert check['status']=='passed'
    rev=pd.read_csv(ROOT/'reports/session2/revenue.csv')
    pd.testing.assert_frame_equal(table,compare(rev,DEMO))
    assert all(hashlib.sha256(p.read_bytes()).hexdigest()==before[p] for p in paths)

def test_powerbi_aggregate_grains_and_source_values():
    run();folder=ROOT/'powerbi/data'
    keys={'dim_arm':['arm'],'arm_performance':['arm'],'binary_inference':['outcome','treatment','reference'],
          'revenue_inference':['treatment','reference'],'segment_effects':['variable','level','treatment'],
          'interactions':['variable','treatment'],'scenario_snapshot':['treatment'],
          'sensitivity_snapshot':['driver','driver_value','treatment']}
    arms=set(pd.read_csv(folder/'dim_arm.csv').arm)
    for name,key in keys.items():
        table=pd.read_csv(folder/(name+'.csv'))
        assert not table.duplicated(key).any()
        col='arm' if 'arm' in table else 'treatment'
        assert set(table[col])<=arms
    pd.testing.assert_frame_equal(pd.read_csv(folder/'arm_performance.csv'),pd.read_csv(ROOT/'reports/arm_kpis.csv'))

def test_dashboard_assumption_changes_and_missing_state():
    from streamlit.testing.v1 import AppTest
    app=AppTest.from_file(str(ROOT/'app.py'),default_timeout=45).run()
    app.sidebar.radio[0].set_value('Business Economics & ROI Simulator').run()
    assert not app.exception and not app.dataframe
    app.checkbox[0].set_value(True).run()
    assert not app.exception
    rev=pd.read_csv(ROOT/'reports/session2/revenue.csv')
    pd.testing.assert_frame_equal(app.dataframe[0].value,compare(rev,DEMO),check_exact=False,atol=1e-10,rtol=1e-10)
    app.number_input(key='econ_audience').set_value(20000)
    app.number_input(key='econ_margin').set_value(20.)
    app.number_input(key='econ_fixed').set_value(1000.)
    app.number_input(key='econ_multiplier').set_value(.5)
    app.number_input(key='econ_delivery').set_value(.1).run()
    expected=compare(rev,Assumptions(20000,.2,.1,1000.,.5))
    pd.testing.assert_frame_equal(app.dataframe[0].value,expected,check_exact=False,atol=1e-10,rtol=1e-10)
    app.selectbox(key='econ_treatment').set_value("Women's email").run()
    assert not app.exception
    app.number_input(key='econ_audience').set_value(0).run()
    assert app.dataframe[0].value.iloc[1].net_value==-1000
    app.checkbox[0].set_value(False).run()
    assert not app.exception and not app.dataframe
