"""Retrospective inference. See the separately committed statistical analysis plan."""
from itertools import combinations
import numpy as np
import pandas as pd
from scipy import stats
from src.config import ARMS

ALPHA = .05
SEED = 20261020
REPLICATIONS = 10000
CONTRASTS = [(ARMS[1], ARMS[0]), (ARMS[2], ARMS[0]), (ARMS[1], ARMS[2])]

def holm(p_values):
    """Holm step-down; undefined hypotheses retain their place in planned family."""
    p=np.asarray(p_values,dtype=float)
    if np.any((p[np.isfinite(p)]<0)|(p[np.isfinite(p)]>1)) or np.isinf(p).any():
        raise ValueError('p-values must be in [0,1] or NaN')
    valid=np.isfinite(p); safe=np.where(valid,p,1.)
    order=np.argsort(safe,kind='stable');m=len(p)
    adjusted=np.empty(m)
    adjusted[order]=np.minimum(1,np.maximum.accumulate(safe[order]*(m-np.arange(m))))
    return np.where(valid,adjusted,np.nan)

def wilson(events,n,alpha=ALPHA):
    if not 0<alpha<1: raise ValueError('alpha must be between zero and one')
    if n<=0 or int(n)!=n or int(events)!=events or not 0<=events<=n: raise ValueError('Invalid binomial counts')
    z=stats.norm.ppf(1-alpha/2);p=events/n;den=1+z*z/n
    center=(p+z*z/(2*n))/den
    half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return max(0.,center-half), min(1.,center+half)

def binary_effect(events_t,n_t,events_c,n_c,alpha=ALPHA):
    for e,n in [(events_t,n_t),(events_c,n_c)]:
        if not np.isfinite(e) or not np.isfinite(n) or int(e)!=e or int(n)!=n or n<0 or not 0<=e<=n:
            raise ValueError('Invalid binomial counts')
    if not 0<alpha<1: raise ValueError('Invalid alpha')
    out={'n_t':int(n_t),'n_c':int(n_c),'events_t':int(events_t),'events_c':int(events_c),
         'method':'two-sided Fisher exact; Newcombe Wilson RD interval',
         'ci_scope':'pointwise 95%; not multiplicity adjusted',
         'relative_ci_method':'approximate log RR with +0.5 events and +1 denominators',
         'status':'estimable' if n_t and n_c else 'empty arm'}
    names=['rate_t','rate_c','effect','ci_low','ci_high','risk_ratio','relative_effect',
           'rr_ci_low','rr_ci_high','relative_ci_low','relative_ci_high','p_raw']
    if not n_t or not n_c:
        out.update(dict.fromkeys(names,np.nan)); return out
    pt,pc=events_t/n_t,events_c/n_c;effect=pt-pc
    lt,ut=wilson(events_t,n_t,alpha);lc,uc=wilson(events_c,n_c,alpha)
    lo=effect-np.sqrt((pt-lt)**2+(uc-pc)**2)
    hi=effect+np.sqrt((ut-pt)**2+(pc-lc)**2)
    rr=pt/pc if pc>0 else np.nan
    adj_rr=((events_t+.5)/(n_t+1))/((events_c+.5)/(n_c+1))
    se=np.sqrt(1/(events_t+.5)-1/(n_t+1)+1/(events_c+.5)-1/(n_c+1))
    z=stats.norm.ppf(1-alpha/2)
    rl,rh=np.exp(np.log(adj_rr)+np.array([-1,1])*z*se)
    p=stats.fisher_exact([[events_t,n_t-events_t],[events_c,n_c-events_c]],alternative='two-sided').pvalue
    out.update(dict(zip(names,[pt,pc,effect,max(-1.,lo),min(1.,hi),rr,rr-1,rl,rh,rl-1,rh-1,float(p)])))
    return out

def assert_analysis_population(df):
    required=['row_id','arm','conversion','visit','spend_cents']
    if any(c not in df for c in required):raise ValueError('Missing analytical fields')
    if df[required].isna().any().any():raise ValueError('Missing assignment or outcomes')
    if not df.row_id.is_unique:raise ValueError('Repeated trace IDs: computational double counting')
    if not df.arm.isin(ARMS).all():raise ValueError('Unknown arm')
    for c in ['conversion','visit']:
        if not df[c].isin([0,1]).all():raise ValueError('Invalid binary outcomes')
    if not np.isfinite(df.spend_cents).all() or (df.spend_cents<0).any():raise ValueError('Invalid spend')

def binary_results(df):
    assert_analysis_population(df)
    rows=[]
    for outcome in ['conversion','visit']:
        for a,b in CONTRASTS:
            x=df.loc[df.arm==a,outcome]; y=df.loc[df.arm==b,outcome]
            row=binary_effect(int(x.sum()),len(x),int(y.sum()),len(y))
            family=('primary_conversion' if outcome=='conversion' else 'secondary_visit') if b==ARMS[0] else 'exploratory_email_comparison'
            row.update(outcome=outcome,treatment=a,reference=b,comparison=f'{a} minus {b}',family=family)
            rows.append(row)
    return pd.DataFrame(rows)

def bootstrap_means(values,reps=REPLICATIONS,seed=SEED):
    """Exact empirical n-out-of-n bootstrap for means, compressed by value frequency."""
    x=np.asarray(values,dtype=float)
    if x.ndim!=1 or not len(x) or not np.isfinite(x).all() or (x<0).any():raise ValueError('Require finite nonnegative spending')
    if not isinstance(reps,(int,np.integer)) or reps<2:raise ValueError('Require >=2 replications')
    unique,counts=np.unique(x,return_counts=True)
    probabilities=counts/len(x); rng=np.random.default_rng(seed)
    result=np.empty(reps)
    for start in range(0,reps,256):
        weights=rng.multinomial(len(x),probabilities,size=min(256,reps-start))
        result[start:start+len(weights)]=weights@unique/len(x)
    return result

def welch_p(x,y):
    if len(x)<2 or len(y)<2:return np.nan
    if np.var(x)==0 and np.var(y)==0:return 1. if np.mean(x)==np.mean(y) else np.nan
    vx,vy=np.var(x,ddof=1)/len(x),np.var(y,ddof=1)/len(y)
    se2=vx+vy
    dof=se2**2/(vx**2/(len(x)-1)+vy**2/(len(y)-1))
    return float(2*stats.t.sf(abs(np.mean(x)-np.mean(y))/np.sqrt(se2),dof))

def revenue_results(df,reps=REPLICATIONS,seed=SEED):
    assert_analysis_population(df)
    streams=np.random.SeedSequence(seed).spawn(len(ARMS))
    raw={a:df.loc[df.arm==a,'spend_cents'].to_numpy(dtype=float)/100 for a in ARMS}
    if any(len(v)<2 for v in raw.values()):raise ValueError('Revenue requires >=2 observations in every arm')
    boot={a:bootstrap_means(raw[a],reps,streams[i]) for i,a in enumerate(ARMS)}
    rows=[];histograms=[];diagnostics=[]
    for arm,x in raw.items():
        total=x.sum();top=max(1,int(np.ceil(len(x)*.01)))
        diagnostics.append({'arm':arm,'n':len(x),'positive_spend_count':int((x>0).sum()),'zero_share':float((x==0).mean()),
                            'mean':float(x.mean()),'p95':float(np.quantile(x,.95)),'p99':float(np.quantile(x,.99)),
                            'max':float(x.max()),'top_1pct_spend_share':float(np.sort(x)[-top:].sum()/total) if total else np.nan})
    for a,b in CONTRASTS:
        x,y=raw[a],raw[b];draws=boot[a]-boot[b];lo,hi=np.quantile(draws,[.025,.975])
        halves=[np.quantile(d,[.025,.975]) for d in np.array_split(draws,2)]
        drift=float(np.max(np.abs(np.asarray(halves)-[lo,hi])))
        width=hi-lo
        analytical_se=np.sqrt(x.var(ddof=1)/len(x)+y.var(ddof=1)/len(y))
        rows.append({'outcome':'spend','treatment':a,'reference':b,'comparison':f'{a} minus {b}',
                     'family':'secondary_revenue' if b==ARMS[0] else 'exploratory_email_comparison',
                     'n_t':len(x),'n_c':len(y),'mean_t':x.mean(),'mean_c':y.mean(),'effect':x.mean()-y.mean(),
                     'ci_low':lo,'ci_high':hi,'p_raw':welch_p(x,y),'bootstrap_reps':reps,'seed':seed,
                     'bootstrap_se':draws.std(ddof=1),'analytic_se':analytical_se,
                     'half_run_endpoint_drift':drift,'drift_fraction_width':drift/width if width>0 else np.nan,
                     'convergence_warning':bool(width<=0 or drift/width>.1),
                     'bootstrap_method':'empirical customer bootstrap; percentile interval',
                     'p_method':'Welch two-sided approximate mean test', 'ci_scope':'pointwise 95%; not multiplicity adjusted'})
        counts,edges=np.histogram(draws,bins=100)
        histograms.extend({'comparison':f'{a} minus {b}','left':l,'right':r,'count':int(n)} for l,r,n in zip(edges[:-1],edges[1:],counts))
    return pd.DataFrame(rows),pd.DataFrame(histograms),pd.DataFrame(diagnostics)

def adjust_families(binary,revenue):
    both=pd.concat([binary,revenue],ignore_index=True)
    for family,idx in both.groupby('family').groups.items():
        both.loc[idx,'p_adjusted']=holm(both.loc[idx,'p_raw'])
        both.loc[idx,'family_size']=len(idx)
    both['reject_holm_005']=both.p_adjusted<ALPHA
    return both[both.outcome!='spend'].reset_index(drop=True),both[both.outcome=='spend'].reset_index(drop=True)

SEGMENTS=['channel','recency_band','historical_spend_band','newbie','mens','womens']
def segment_fields(df):
    result=df.copy()
    result['recency_band']=pd.cut(result.recency,[0,3,6,12],labels=['1–3 months','4–6 months','7–12 months']).astype(str)
    result['historical_spend_band']=np.where(result.history<=200,'<= $200','> $200')
    return result

def interaction_test(rows):
    """Approximate additive-scale heterogeneity across disjoint baseline categories."""
    d=pd.DataFrame(rows)
    eligible=((d.n_t>=100)&(d.n_c>=100)&(d.events_t>=5)&(d.events_c>=5)&((d.n_t-d.events_t)>=5)&((d.n_c-d.events_c)>=5))
    if len(d)<2 or not eligible.all():
        return {'statistic':np.nan,'df':max(0,len(d)-1),'p_raw':np.nan,'status':'not evaluated: sparse or absent categories'}
    var=d.rate_t*(1-d.rate_t)/d.n_t+d.rate_c*(1-d.rate_c)/d.n_c
    weights=1/var;common=np.average(d.effect,weights=weights)
    q=float(np.sum(weights*(d.effect-common)**2))
    return {'statistic':q,'df':len(d)-1,'p_raw':float(stats.chi2.sf(q,len(d)-1)),'status':'approximate additive interaction evaluated'}

def segment_results(df):
    assert_analysis_population(df);data=segment_fields(df);rows=[];interactions=[]
    for variable in SEGMENTS:
        for treatment in ARMS[1:]:
            group=[]
            for level in sorted(data[variable].unique()):
                cell=data[data[variable]==level]
                x=cell.loc[cell.arm==treatment,'conversion'];y=cell.loc[cell.arm==ARMS[0],'conversion']
                row=binary_effect(int(x.sum()),len(x),int(y.sum()),len(y))
                row.update(variable=variable,level=str(level),treatment=treatment,reference=ARMS[0],
                           sparse_warning=bool(min(len(x),len(y))<100 or min(x.sum(),y.sum())<5))
                rows.append(row);group.append(row)
            interaction=interaction_test(group)
            interaction.update(variable=variable,treatment=treatment,reference=ARMS[0],method='inverse-variance additive risk-difference heterogeneity; exploratory')
            interactions.append(interaction)
    cells=pd.DataFrame(rows);ints=pd.DataFrame(interactions)
    cells['p_adjusted']=holm(cells.p_raw);ints['p_adjusted']=holm(ints.p_raw)
    cells['family_size']=len(cells);ints['family_size']=len(ints)
    return cells,ints
