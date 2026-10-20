import itertools
import numpy as np
import pandas as pd
import pytest
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from statsmodels.stats.multitest import multipletests
from src.inference import (binary_effect,holm,bootstrap_means,binary_results,revenue_results,
                           adjust_families,assert_analysis_population,interaction_test,segment_fields)

@pytest.mark.parametrize('counts',[(12,100,5,100),(0,10,0,10),(1,5,0,7),(100,100,95,100),(3,1000,1,900)])
def test_binary_reference_intervals(counts):
    result=binary_effect(*counts)
    lo,hi=confint_proportions_2indep(*counts,method='newcomb',compare='diff')
    assert result['ci_low']==pytest.approx(lo)
    assert result['ci_high']==pytest.approx(hi)
    assert -1<=result['ci_low']<=result['effect']<=result['ci_high']<=1

def test_known_fisher_and_effect():
    r=binary_effect(6,8,1,4)
    assert r['p_raw']==pytest.approx(0.2222222222222222)
    assert r['effect']==.5 and r['risk_ratio']==3 and r['relative_effect']==2
    reverse=binary_effect(1,4,6,8)
    assert reverse['effect']==-r['effect']
    assert reverse['ci_low']==pytest.approx(-r['ci_high'])
    assert reverse['p_raw']==pytest.approx(r['p_raw'])

def test_zero_events_and_empty():
    r=binary_effect(0,10,0,10)
    assert r['p_raw']==1 and r['ci_low']<0<r['ci_high']
    assert np.isnan(r['risk_ratio']) and np.isfinite(r['rr_ci_high'])
    r=binary_effect(1,10,0,10);assert np.isnan(r['relative_effect'])
    assert binary_effect(0,0,1,10)['status']=='empty arm'
    assert np.isnan(binary_effect(0,0,1,10)['p_raw'])

@pytest.mark.parametrize('args',[(2,1,0,1),(-1,5,0,5),(1.2,5,1,5),(1,5,0,-1)])
def test_invalid_counts(args):
    with pytest.raises(ValueError):binary_effect(*args)

def test_holm_hand_and_reference():
    p=[.01,.04,.03];np.testing.assert_allclose(holm(p),[.03,.06,.06])
    np.testing.assert_allclose(holm(p),multipletests(p,method='holm')[1])
    assert np.isnan(holm([.01,np.nan])[1])
    assert holm([.01,np.nan])[0]==.02
    with pytest.raises(ValueError):holm([1.1])

def test_null_fixture():
    r=binary_effect(20,200,20,200)
    assert r['effect']==0 and r['p_raw']==1 and r['ci_low']<0<r['ci_high']

def test_bootstrap_reproducibility_and_weighting():
    x=np.array([0]*9+[100])
    a=bootstrap_means(x,20000,12);b=bootstrap_means(x,20000,12)
    np.testing.assert_array_equal(a,b)
    assert a.mean()==pytest.approx(10,abs=.3) # Equal unique-value weights would yield 50.
    assert a.std()==pytest.approx(np.sqrt(np.var(x)/len(x)),rel=.025)

def test_exact_bootstrap_small_distribution():
    exact=np.array([np.mean(x) for x in itertools.product([0.,0.,3.],repeat=3)])
    sampled=bootstrap_means([0,0,3],30000,4)
    assert sampled.mean()==pytest.approx(exact.mean(),abs=.025)
    assert sampled.var()==pytest.approx(exact.var(),rel=.025)

def test_heavy_tail_and_degenerate():
    draws=bootstrap_means([0]*99+[1e9],5000,42)
    assert np.isfinite(draws).all() and np.quantile(draws,.975)>0
    np.testing.assert_array_equal(bootstrap_means([0]*20,20,5),np.zeros(20))
    for invalid in [[],[np.nan],[np.inf],[-1]]:
        with pytest.raises(ValueError):bootstrap_means(invalid,100)

def test_integrity_and_families(clean):
    assert_analysis_population(clean)
    with pytest.raises(ValueError):assert_analysis_population(pd.concat([clean,clean.iloc[[0]]]))
    b=binary_results(clean);r,_,_=revenue_results(pd.concat([clean.assign(row_id=clean.row_id+'a'),clean.assign(row_id=clean.row_id+'b')]),100,3)
    b,r=adjust_families(b,r)
    assert sorted(b.family_size.unique())==[2,3]
    assert sorted(r.family_size.unique())==[2,3]
    assert (b[b.family=='primary_conversion'].family_size==2).all()
    fields=segment_fields(clean)
    assert fields.recency_band.iloc[0]=='1–3 months'
    assert fields.historical_spend_band.iloc[0]=='<= $200'

def test_interaction_uses_difference_not_subgroup_significance():
    equal=[binary_effect(20,1000,10,1000),binary_effect(20,1000,10,1000)]
    assert interaction_test(equal)['p_raw']==1
    changed=[binary_effect(90,1000,10,1000),binary_effect(10,1000,90,1000)]
    assert interaction_test(changed)['p_raw']<.001
    assert np.isnan(interaction_test([binary_effect(0,1000,5,1000),equal[0]])['p_raw'])

def test_welch_matches_scipy():
    from src.inference import welch_p
    x=np.array([0.,0.,1.,40.,100.]);y=np.array([0.,2.,3.,4.])
    assert welch_p(x,y)==pytest.approx(stats.ttest_ind(x,y,equal_var=False).pvalue)
