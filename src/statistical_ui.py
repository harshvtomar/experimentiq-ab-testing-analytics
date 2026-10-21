"""Four additional pages; canonical computations are shared with batch exports."""
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from src.inference import REPLICATIONS,SEED
from src.serialization import table_bundle
from src.statistical_pipeline import calculate,markdown_report

PAGES=['Statistical Significance','Revenue Uplift Analysis','Segment Effect Explorer','Business Recommendations']

@st.cache_data(show_spinner='Calculating reproducible inference and 10,000 bootstrap replications…')
def canonical_results(df):
    return calculate(df)

def forest(table,multiplier=1,unit='dollars per assigned customer',label='comparison'):
    fig=go.Figure(go.Scatter(x=table.effect*multiplier,y=table[label],mode='markers',
        marker=dict(size=11,color='#176bba'),error_x=dict(type='data',symmetric=False,
        array=(table.ci_high-table.effect)*multiplier,arrayminus=(table.effect-table.ci_low)*multiplier),
        hovertemplate='%{y}<br>Effect: %{x:.4f}<extra></extra>'))
    fig.add_vline(x=0,line_dash='dash',line_color='#61758a')
    fig.update_layout(xaxis_title=f'Effect ({unit}) · 95% pointwise interval',yaxis_title=None,yaxis_type='category',
                      height=max(320,75*len(table)),margin=dict(l=10,r=25,t=20,b=50))
    st.plotly_chart(fig,width='stretch')

def evidence_table(table, **kwargs):
    """Scientific notation avoids displaying tiny positive p-values as zero."""
    config={c:st.column_config.NumberColumn(c,format='%.3e')
            for c in ['p_raw','p_adjusted'] if c in table}
    st.dataframe(table,column_config=config,**kwargs)

def download(table,name):
    st.download_button('Download '+name.replace('_',' '),table.to_csv(index=False).encode(),name+'.csv','text/csv',key='s2_'+name)

def render(page,df):
    tables,checks,elapsed=canonical_results(df)
    b=tables['binary'];r=tables['revenue']
    st.caption('Retrospective plan • Two-sided tests • α = 0.05 • Pointwise 95% intervals • Holm adjustment within declared families')
    if page=='Statistical Significance':
        st.subheader('Effect size and uncertainty')
        outcome=st.selectbox('Outcome',['conversion','visit'])
        selected=b[b.outcome==outcome].copy()
        forest(selected,100,'percentage points')
        evidence_table(selected[['comparison','n_t','n_c','events_t','events_c','rate_t','rate_c','effect','ci_low','ci_high','relative_effect','relative_ci_low','relative_ci_high','p_raw','p_adjusted','family','family_size','reject_holm_005']],hide_index=True,width='stretch')
        st.markdown('**Primary family:** the two conversion contrasts versus control. Visits form a separate secondary family. Email-versus-email comparisons across three outcomes form one exploratory family. There is no global error-control claim across these families.')
        st.caption('Table effects/rates are fractions; the forest uses percentage points. Fisher exact p-values and Newcombe/Wilson intervals use different constructions. CIs are not Holm-adjusted. Relative intervals are approximate continuity-adjusted log-RR intervals; raw relative effects are undefined with a zero reference rate.')
        download(selected,'binary_inference')
    elif page=='Revenue Uplift Analysis':
        st.subheader('Incremental observed revenue, including zero spend')
        forest(r)
        evidence_table(r[['comparison','n_t','n_c','mean_t','mean_c','effect','ci_low','ci_high','p_raw','p_adjusted','family']],hide_index=True,width='stretch')
        st.info('Revenue is not profit. Campaign costs and margins are unavailable. These are two-week historical assignment effects, not forecasts.')
        comparison=st.selectbox('Bootstrap comparison',r.comparison.tolist())
        hist=tables['bootstrap_histogram'].query('comparison == @comparison').copy()
        hist['midpoint']=(hist.left+hist.right)/2
        fig=px.bar(hist,x='midpoint',y='count',labels={'midpoint':'Bootstrap mean difference ($/assigned customer)','count':'Replications'},color_discrete_sequence=['#176bba'])
        fig.add_vline(x=0,line_dash='dash');st.plotly_chart(fig,width='stretch')
        st.caption('10,000 within-arm customer bootstrap replications; seed 20261020. Multinomial empirical frequencies preserve each original row’s sampling weight, including zeros. The percentile CI is pointwise; p-values use a separate approximate Welch test.')
        evidence_table(tables['revenue_diagnostics'],hide_index=True,width='stretch')
        evidence_table(r[['comparison','bootstrap_reps','seed','bootstrap_se','analytic_se','drift_fraction_width','convergence_warning']],hide_index=True,width='stretch')
        st.caption('Monte Carlo check: endpoint drift in either 5,000-replication half relative to the full CI width; flag above 10% or a degenerate interval. Stability does not guarantee population coverage.')
        download(r,'revenue_inference')
    elif page=='Segment Effect Explorer':
        st.subheader('Exploratory subgroup effects')
        st.warning('These are retrospective exploratory comparisons. A significant result in one subgroup and a non-significant result in another does not establish an interaction.')
        cells=tables['segments'];ints=tables['interactions']
        variable=st.selectbox('Baseline partition',cells.variable.unique().tolist())
        treatment=st.selectbox('Email treatment',cells.treatment.unique().tolist())
        subset=cells[(cells.variable==variable)&(cells.treatment==treatment)].copy()
        forest(subset,100,'percentage points',label='level')
        evidence_table(subset[['level','n_t','n_c','events_t','events_c','rate_t','rate_c','effect','ci_low','ci_high','p_raw','p_adjusted','sparse_warning']],hide_index=True,width='stretch')
        st.caption('Subgroup p-values use Holm over all 28 planned comparisons, not just the selected view. Pointwise intervals are not adjusted.')
        selected=ints[(ints.variable==variable)&(ints.treatment==treatment)]
        st.subheader('Interaction evidence on the additive scale')
        evidence_table(selected,hide_index=True,width='stretch')
        st.caption('Approximate omnibus heterogeneity of category-specific risk differences. All categories require >=100 customers and >=5 events/non-events per arm. Sparse partitions are not tested. Holm covers all 12 planned interaction hypotheses; no validated targeting rule is implied.')
        download(cells,'all_segment_effects');download(ints,'all_interactions')
    else:
        st.subheader('Evidence, effect size and economic uncertainty')
        primary=b[b.family=='primary_conversion']
        for x in primary.itertuples():
            evidence='Evidence of a conversion difference within the primary family' if x.reject_holm_005 else 'Insufficient evidence within the primary family'
            st.markdown(f'**{x.comparison}: {evidence}.** Estimated {x.effect*1000:.2f} additional conversions per 1,000 assignments (95% pointwise CI {x.ci_low*1000:.2f} to {x.ci_high*1000:.2f}); Holm p = {x.p_adjusted:.3g}.')
        st.markdown('**Economic meaningfulness is undetermined.** We have no measured campaign costs, contribution margins or business-approved minimum effect. Estimated revenue differences must not be presented as profit or guaranteed future returns.')
        st.markdown('**Conditional next step:** use the historical evidence to design a contemporary replication with cost, margin, deliverability and unsubscribe/complaint guardrails. Choose a rollout threshold with the business before that new experiment. Do not deploy a subgroup targeting policy based only on these exploratory cuts.')
        evidence_table(r[['comparison','effect','ci_low','ci_high','p_adjusted','family']],hide_index=True,width='stretch')
        st.caption('Causal interpretation depends on source-reported randomization, consistent treatment and independent customers. No original assignment logs or customer IDs can be audited. Historical two-week outcomes do not establish current-market effects or lifetime value.')
        meta={'bootstrap_reps':REPLICATIONS,'seed':SEED,'checks':checks,'runtime_seconds':elapsed}
        report=markdown_report(tables,meta)
        st.download_button('Download statistical report',report,'ExperimentIQ_Statistical_Report.md','text/markdown')
        bundle=table_bundle(tables)
        st.download_button('Download all inference results',json.dumps(bundle,indent=2,allow_nan=False),'inferential_results.json','application/json')
