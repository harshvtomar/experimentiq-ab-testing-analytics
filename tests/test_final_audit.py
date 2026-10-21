"""Independent final audit of authentic exports and financial boundary behavior."""
import os
from dataclasses import replace
import numpy as np
import pandas as pd
import pytest
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import confint_proportions_2indep
from src.config import ROOT
from src.economics import DEMO,compare,sensitivity
from src.business_pipeline import reconcile_economics

@pytest.mark.integration
def test_authentic_inference_against_independent_references():
    if not (ROOT/'data/raw/hillstrom.csv').exists():
        if os.getenv('EXPERIMENTIQ_REQUIRE_DATA')=='1':pytest.fail('Authentic data absent')
        pytest.skip('Authentic audit not run')
    raw=pd.read_csv(ROOT/'data/raw/hillstrom.csv')
    b=pd.read_csv(ROOT/'reports/session2/binary.csv')
    r=pd.read_csv(ROOT/'reports/session2/revenue.csv')
    mapping={'Control':'No E-Mail',"Men's email":'Mens E-Mail',"Women's email":'Womens E-Mail'}
    for x in b.itertuples():
        a=raw.loc[raw.segment==mapping[x.treatment],x.outcome]
        c=raw.loc[raw.segment==mapping[x.reference],x.outcome]
        assert (x.n_t,x.n_c,x.events_t,x.events_c)==(len(a),len(c),a.sum(),c.sum())
        np.testing.assert_allclose([x.ci_low,x.ci_high],confint_proportions_2indep(int(a.sum()),len(a),int(c.sum()),len(c),method='newcomb',compare='diff'),rtol=1e-12)
        p=stats.fisher_exact([[a.sum(),len(a)-a.sum()],[c.sum(),len(c)-c.sum()]]).pvalue
        assert x.p_raw==pytest.approx(p,rel=1e-12,abs=0)
    for x in r.itertuples():
        a=raw.loc[raw.segment==mapping[x.treatment],'spend'];c=raw.loc[raw.segment==mapping[x.reference],'spend']
        assert x.effect==pytest.approx(a.mean()-c.mean(),rel=1e-12)
        assert x.p_raw==pytest.approx(stats.ttest_ind(a,c,equal_var=False).pvalue,rel=1e-10,abs=0)
    for _,group in pd.concat([b,r]).groupby('family'):
        np.testing.assert_allclose(group.p_adjusted,multipletests(group.p_raw,method='holm')[1],rtol=1e-12,atol=0)
    ints=pd.read_csv(ROOT/'reports/session2/interactions.csv')
    assert len(ints)==12 and not (ints.p_adjusted<.05).any()


def test_sql_boundary_scenarios_and_sensitivity_slopes():
    rev=pd.DataFrame({'treatment':["Men's email","Women's email"],'reference':['Control']*2,
                      'effect':[2.,-1.],'ci_low':[1.,-2.],'ci_high':[3.,0.]})
    for updates in [{'audience':0},{'margin':0},{'delivery_cost':0,'fixed_cost':0},
                    {'audience':10**12},{'audience':1000,'margin':.5,'delivery_cost':.5,'fixed_cost':500}]:
        assert reconcile_economics(compare(rev,replace(DEMO,**updates)))['status']=='passed'
    grid=sensitivity(rev,DEMO)
    for (driver,arm),g in grid[grid.treatment!='Control'].groupby(['driver','treatment']):
        g=g.sort_values('driver_value');d=2 if arm=="Men's email" else -1
        slope={'margin':DEMO.audience*d*DEMO.multiplier,'delivery_cost':-DEMO.audience,
               'audience':d*DEMO.multiplier*DEMO.margin-DEMO.delivery_cost}[driver]
        np.testing.assert_allclose(np.diff(g.net_value),np.diff(g.driver_value)*slope,rtol=1e-12,atol=1e-9)


def test_all_powerbi_fact_exports_equal_canonical_tables():
    pairs={'arm_performance':'arm_kpis.csv','descriptive_comparisons':'comparisons.csv',
           'binary_inference':'session2/binary.csv','revenue_inference':'session2/revenue.csv',
           'segment_effects':'session2/segments.csv','interactions':'session2/interactions.csv',
           'scenario_snapshot':'session3/demonstration_scenarios.csv','sensitivity_snapshot':'session3/sensitivity.csv'}
    for dest,source in pairs.items():
        pd.testing.assert_frame_equal(pd.read_csv(ROOT/'powerbi/data'/f'{dest}.csv'),pd.read_csv(ROOT/'reports'/source))
