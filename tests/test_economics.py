import math
from dataclasses import replace
import numpy as np
import pandas as pd
import pytest
from src.economics import Assumptions, evaluate, compare, sensitivity, DEMO
from src.business_pipeline import reconcile_economics

def test_hand_calculated_financial_bridge():
    r=evaluate(2,1,3,Assumptions(1000,.4,.1,200, .5))
    assert (r['revenue'],r['gross_contribution'],r['variable_cost'],r['total_cost'],r['net_value'])==(1000,400,100,300,100)
    assert (r['net_low'],r['net_high'])==(-100,300)
    assert r['break_even_uplift']==.75
    assert r['break_even_margin']==.3
    assert r['max_delivery_cost']==pytest.approx(.2)
    assert r['net_return_on_cost']==pytest.approx(1/3)

def test_zero_audience_costs_remain():
    r=evaluate(2,1,3,Assumptions(0,.4,.1,200,1))
    assert r['net_value']==r['net_low']==r['net_high']==-200
    assert r['max_delivery_cost'] is None and r['break_even_uplift'] is None

def test_zero_margin_and_zero_cost():
    r=evaluate(2,1,3,Assumptions(1000,0,0,0,1))
    assert r['net_value']==0 and r['classification']=='break-even'
    assert r['break_even_uplift'] is None and r['net_return_on_cost'] is None
    r=evaluate(2,1,3,Assumptions(1000,.4,0,0,1))
    assert r['net_value']==800 and r['break_even_margin']==0

def test_missing_is_not_zero():
    r=evaluate(2,1,3,Assumptions(1000,None,.1,200,1))
    assert r['net_value'] is None and r['classification']=='missing assumptions' and r['missing']=='margin'

def test_negative_uplift_and_control_baseline():
    r=evaluate(-2,-3,-1,Assumptions(1000,.4,.1,200,1))
    assert r['net_value']==-1100 and r['break_even_margin'] is None
    assert r['max_delivery_cost']<0 and r['net_low']<=r['net_value']<=r['net_high']
    control=evaluate(0,0,0,Assumptions(),'Control')
    assert control['net_value']==0 and control['net_return_on_cost'] is None

@pytest.mark.parametrize('changes',[{'audience':1.5},{'audience':-1},{'margin':1.01},{'margin':-.01},
 {'delivery_cost':-1},{'fixed_cost':float('nan')},{'multiplier':1.1},{'audience':True},{'delivery_cost':float('inf')}])
def test_invalid_assumptions(changes):
    with pytest.raises(ValueError):evaluate(2,1,3,replace(DEMO,**changes))

def test_break_even_boundaries_and_large_audience():
    a=Assumptions(1000,.5,.5,500,1)
    assert evaluate(2,1,3,a)['classification']=='break-even'
    assert evaluate(2,1,3,replace(a,delivery_cost=.51))['classification']=='unfavorable'
    assert evaluate(2,1,3,replace(a,delivery_cost=.49))['classification']=='favorable'
    r=evaluate(2,1,3,replace(a,audience=10**12))
    assert math.isfinite(r['net_value']) and r['net_value']==5e11-500

def test_monotonic_interval_and_multiplier():
    a=Assumptions(25000,.3,.04,500,.75)
    draws=np.array([-1.,0.,.4,1.,2.])
    lo,hi=np.quantile(draws,[.025,.975])
    r=evaluate(.4,lo,hi,a)
    transformed=draws*a.audience*a.margin*a.multiplier-a.audience*a.delivery_cost-a.fixed_cost
    np.testing.assert_allclose([r['net_low'],r['net_high']],np.quantile(transformed,[.025,.975]))
    z=evaluate(.4,lo,hi,replace(a,multiplier=0))
    assert z['net_low']==z['net_high']==z['net_value']==-1500

def test_compare_sensitivity_and_sql_do_not_mutate():
    rev=pd.DataFrame({'treatment':["Men's email","Women's email"],'reference':['Control']*2,'effect':[2.,1.], 'ci_low':[1.,.5], 'ci_high':[3.,1.5]})
    original=rev.copy(deep=True)
    table=compare(rev,DEMO);grid=sensitivity(rev,DEMO)
    assert reconcile_economics(table)['status']=='passed'
    assert grid.query('treatment=="Control"').net_value.eq(0).all()
    assert set(grid.driver)=={'margin','delivery_cost','audience'}
    pd.testing.assert_frame_equal(rev,original)
    assert sensitivity(rev,Assumptions()).empty

def test_invalid_effects_and_missing_contrasts():
    for args in [(float('nan'),0,1),(1,2,1)]:
        with pytest.raises(ValueError):evaluate(*args,DEMO)
    with pytest.raises(ValueError):evaluate(1,0,2,DEMO,'unknown')
