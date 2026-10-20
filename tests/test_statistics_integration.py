import json
import os
import numpy as np
import pandas as pd
import pytest
from src.config import ROOT
from src.download import load_raw
from src.preprocess import normalize
from src.inference import (binary_results,revenue_results,adjust_families,segment_results,assert_analysis_population)
from src.metrics import aggregate
from src.statistical_pipeline import calculate,run

pytestmark=pytest.mark.integration
@pytest.fixture(scope='module')
def actual():
    path=ROOT/'data/raw/hillstrom.csv'
    if not path.exists():
        if os.getenv('EXPERIMENTIQ_REQUIRE_DATA')=='1':pytest.fail('Authentic dataset absent')
        pytest.skip('Real-data inference not verified: source absent')
    return normalize(load_raw(path))

@pytest.fixture(scope='module')
def calculated(actual):return calculate(actual)[0]

def test_real_population_and_kpis(actual,calculated):
    assert_analysis_population(actual)
    assert len(actual)==actual.row_id.nunique()==64000
    summary=aggregate(actual).set_index('arm')
    for x in calculated['binary'].itertuples():
        metric='conversion_rate' if x.outcome=='conversion' else 'visit_rate'
        assert x.rate_t==pytest.approx(summary.loc[x.treatment,metric])
        assert x.effect==pytest.approx(summary.loc[x.treatment,metric]-summary.loc[x.reference,metric])
        assert x.p_adjusted>=x.p_raw
    for x in calculated['revenue'].itertuples():
        assert x.effect==pytest.approx(summary.loc[x.treatment,'spend_per_customer']-summary.loc[x.reference,'spend_per_customer'])
        assert x.bootstrap_se==pytest.approx(x.analytic_se,rel=.05)
        assert x.bootstrap_reps==10000
    assert calculated['bootstrap_histogram'].groupby('comparison')['count'].sum().eq(10000).all()
    assert len(calculated['segments'])==28 and len(calculated['interactions'])==12
    assert calculated['segments'].family_size.eq(28).all()
    assert calculated['interactions'].family_size.eq(12).all()
    for _,rows in calculated['segments'].groupby(['variable','treatment']):
        assert rows.n_t.sum()==summary.loc[rows.treatment.iloc[0],'n']
        assert rows.n_c.sum()==summary.loc['Control','n']

def test_bootstrap_real_reproducible(actual,calculated):
    r,h,d=revenue_results(actual)
    pd.testing.assert_frame_equal(h,calculated['bootstrap_histogram'])
    np.testing.assert_array_equal(r.ci_low,calculated['revenue'].ci_low)

def test_machine_exports(actual):
    tables,meta=run()
    payload=json.loads((ROOT/'reports/session2/inferential_results.json').read_text(),parse_constant=lambda x:pytest.fail('Nonstandard JSON constant'))
    assert payload['metadata']['checks']['n']==64000
    assert len(payload['results']['binary'])==6
    assert 'Economic value is undetermined' in (ROOT/'reports/session2/STATISTICAL_REPORT.md').read_text()

def test_new_pages_use_canonical_calculations(actual,calculated):
    from streamlit.testing.v1 import AppTest
    app=AppTest.from_file(str(ROOT/'app.py'),default_timeout=45).run()
    for page in ['Statistical Significance','Revenue Uplift Analysis','Segment Effect Explorer','Business Recommendations']:
        app.sidebar.radio[0].set_value(page).run();assert not app.exception
        assert len(app.dataframe)>0
    app.sidebar.radio[0].set_value('Statistical Significance').run()
    table=app.dataframe[0].value
    expected=calculated['binary'].query("outcome=='conversion'")[table.columns]
    pd.testing.assert_frame_equal(table,expected)
    app.selectbox[0].set_value('visit').run();assert not app.exception
    table=app.dataframe[0].value
    pd.testing.assert_frame_equal(table,calculated['binary'].query("outcome=='visit'")[table.columns])
    app.sidebar.radio[0].set_value('Segment Effect Explorer').run()
    app.selectbox[0].set_value('newbie').run()
    app.selectbox[1].set_value("Women's email").run();assert not app.exception
    table=app.dataframe[0].value
    expected=calculated['segments'].query('variable=="newbie" and treatment=="Women\'s email"')[table.columns]
    pd.testing.assert_frame_equal(table,expected)
