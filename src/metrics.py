"""All denominators are randomized customers within the selected arm and slice."""
from itertools import combinations
import math
import numpy as np
import pandas as pd
from src.config import ARMS, BASELINE

def aggregate(df, by=None):
    keys = list(by or []) + ['arm']
    out = df.groupby(keys,observed=True,dropna=False).agg(
        n=('row_id','size'), conversions=('conversion','sum'), visits=('visit','sum'),
        spend_cents=('spend_cents','sum')).reset_index()
    if not by:
        out = out.set_index('arm').reindex(ARMS).reset_index()
        out[['n','conversions','visits','spend_cents']] = out[['n','conversions','visits','spend_cents']].fillna(0).astype('int64')
    denominator = out.n.replace(0,np.nan)
    out['conversion_rate'] = out.conversions / denominator
    out['visit_rate'] = out.visits / denominator
    out['total_spend'] = out.spend_cents / 100
    out['spend_per_customer'] = out.total_spend / denominator
    return out

def comparisons(summary):
    indexed = summary.set_index('arm')
    rows = []
    for a,b in [(ARMS[1],ARMS[0]),(ARMS[2],ARMS[0]),(ARMS[1],ARMS[2])]:
        row={'comparison':f'{a} minus {b}','n_a':int(indexed.loc[a,'n']),'n_b':int(indexed.loc[b,'n'])}
        for metric in ['conversion_rate','visit_rate','spend_per_customer']:
            av,bv=indexed.loc[a,metric],indexed.loc[b,metric]
            row[metric+'_difference'+('_pp' if metric.endswith('rate') else '_dollars')] = (av-bv)*(100 if metric.endswith('rate') else 1)
            row[metric+'_relative_pct'] = (av/bv-1)*100 if pd.notna(bv) and bv!=0 else np.nan
        rows.append(row)
    return pd.DataFrame(rows)

def integrity(df):
    counts = df.arm.value_counts().reindex(ARMS,fill_value=0)
    # Source describes 1/3 assignment probabilities, not exact realized counts.
    n=len(df)
    statistic = float((((counts-n/3)**2)/(n/3)).sum()) if n else None
    # Chi-square survival function at df=2 is exactly exp(-x/2).
    return {'counts':{k:int(v) for k,v in counts.items()},'expected_probabilities':[1/3]*3,
            'allocation_basis':'Original challenge states one third randomly selected for each arm',
            'srm_chi_square':statistic,'srm_df':2,
            'srm_p_value':math.exp(-statistic/2) if n else None,
            'srm_flag_at_0_001':bool(statistic is not None and math.exp(-statistic/2)<.001),
            'interpretation':'Preliminary allocation diagnostic only; no outcome significance test'}

def balance(df):
    """Descriptive pairwise standardized differences; no significance labels."""
    encoded = df[BASELINE].astype(float).copy()
    for c in ['channel','geography','history_segment']:
        encoded = pd.concat([encoded,pd.get_dummies(df[c],prefix=c,dtype=float)],axis=1)
    encoded['arm']=df.arm
    rows=[]
    for a,b in combinations(ARMS,2):
        for c in encoded.columns.drop('arm'):
            x=encoded.loc[encoded.arm==a,c]; y=encoded.loc[encoded.arm==b,c]
            pooled=np.sqrt((x.var(ddof=1)+y.var(ddof=1))/2)
            rows.append({'arm_a':a,'arm_b':b,'covariate':c,'mean_a':x.mean(),'mean_b':y.mean(),
                         'standardized_difference':(x.mean()-y.mean())/pooled if pooled>0 else np.nan})
    return pd.DataFrame(rows)
