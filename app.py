"""Streamlit MVP. Every chart uses the same validated, checksum-pinned source."""
import json
import pandas as pd
import plotly.express as px
import streamlit as st
from src.config import ROOT, FILTERS, EXPECTED_ROWS
from src.download import retrieve,load_raw
from src.validate import validate
from src.preprocess import normalize,filter_customers
from src.metrics import aggregate,comparisons,integrity,balance

st.set_page_config(page_title='ExperimentIQ | Experiment Performance Intelligence',page_icon='🧪',layout='wide')
st.markdown('<style>.block-container{max-width:1300px;padding-top:2rem}h1{letter-spacing:-1px}div[data-testid="stMetric"]{background:#f0f5fa;border-radius:12px;padding:16px}div[data-testid="stMetricValue"]{font-size:1.65rem}</style>',unsafe_allow_html=True)
@st.cache_data(show_spinner='Verifying original experiment data…')
def load_data():
    path=retrieve(ROOT/'data/raw')
    raw=load_raw(path); quality=validate(raw,EXPECTED_ROWS)
    return normalize(raw),quality,json.loads(path.with_suffix('.provenance.json').read_text())

st.sidebar.title('ExperimentIQ')
st.sidebar.caption('A/B Testing & Incremental Revenue Optimization')
page=st.sidebar.radio('Workspace',['Executive Overview','Treatment Comparison','Customer Segment Explorer','Data Quality & Methodology','Statistical Significance','Revenue Uplift Analysis','Segment Effect Explorer','Business Recommendations','Business Economics & ROI Simulator'])
st.sidebar.divider()
st.sidebar.caption('SESSION 3 · BUSINESS ECONOMICS — Authentic 2008 experiment. Two-week outcomes; commercial scenarios are hypothetical.')
st.title('Experiment Performance Intelligence')
st.caption('ExperimentIQ  /  '+page)
st.info('Descriptive pages show observed outcomes. Statistical pages add uncertainty and family-specific Holm adjustments. Revenue is not profit; modern rollout needs cost evidence and replication.')
try:
    df,quality,provenance=load_data()
except Exception as exc:
    st.error(f'Authentic data unavailable or invalid: {exc}')
    st.code('python -m src.pipeline')
    st.stop()
summary=aggregate(df)
colors={'Control':'#61758a',"Men's email":'#176bba',"Women's email":'#16a394'}
def chart(table,metric,title,percent=False):
    fig=px.bar(table,x='arm',y=metric,color='arm',color_discrete_map=colors,
               hover_data=['n'],text_auto='.2%' if percent else (',d' if metric=='n' else '.3f'),title=title,
               labels={'arm':'Randomized arm',metric:title,'n':'Assigned customers'})
    fig.update_layout(title_font_size=14,showlegend=False,height=340,margin=dict(l=12,r=12,t=55,b=20),paper_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes(title=None)
    if percent: fig.update_yaxes(tickformat='.1%')
    st.plotly_chart(fig,width='stretch')
def export(table,label,key):
    st.download_button(label,table.to_csv(index=False).encode(),key+'.csv','text/csv',key=key)

if page=='Executive Overview':
    a,b,c=st.columns(3)
    a.metric('Customers',f'{len(df):,}');b.metric('Experiment arms','3');c.metric('Observed spend ($)',f'${summary.total_spend.sum():,.2f}')
    st.caption('All customers assigned to each arm form the denominator, including zero spend and non-converters. Outcomes cover the two weeks following the campaign.')
    left,right=st.columns(2)
    with left: chart(summary,'conversion_rate','Conversion rate (primary)',True)
    with right: chart(summary,'visit_rate','Website visit rate',True)
    with left: chart(summary,'spend_per_customer','Spend per customer ($)')
    with right: chart(summary,'n','Assignment counts')
    st.dataframe(summary,width='stretch',hide_index=True)
    export(summary,'Download arm KPI summary','arm_kpis')
elif page=='Treatment Comparison':
    st.subheader('Three comparisons, shared definitions')
    st.caption('First arm minus second arm. Rate differences use percentage points (pp); relative differences use the second arm as denominator. Spend differences are dollars per assigned customer.')
    table=comparisons(summary)
    st.dataframe(table,width='stretch',hide_index=True)
    for metric,title in [('conversion_rate_difference_pp','Conversion difference (percentage points)'),('visit_rate_difference_pp','Visit difference (percentage points)'),('spend_per_customer_difference_dollars','Spend difference ($ per customer)')]:
        fig=px.bar(table,x=metric,y='comparison',orientation='h',title=title,hover_data=['n_a','n_b'],text_auto='.3f',color_discrete_sequence=['#176bba'])
        fig.add_vline(x=0,line_color='#61758a');st.plotly_chart(fig,width='stretch')
    export(table,'Download descriptive comparisons','comparisons')
elif page=='Customer Segment Explorer':
    st.subheader('Explore pre-treatment audiences')
    st.caption('All filters intersect. Selecting no values produces an empty slice. Segment differences are exploratory, not confirmed heterogeneous effects.')
    filters={}
    columns=st.columns(3)
    for i,column in enumerate(FILTERS):
        with columns[i%3]:
            options=sorted(df[column].unique().tolist())
            filters[column]=st.multiselect(column.replace('_',' ').title(),options,default=options,key='filter_'+column)
    subset=filter_customers(df,filters)
    st.metric('Selected customers',f'{len(subset):,}')
    if subset.empty:
        st.warning('No customers match these filters. Restore one or more values to continue.')
    else:
        table=aggregate(subset)
        if (table.n<100).any(): st.warning('At least one arm has fewer than 100 customers. Descriptive estimates may be unstable; this is not a statistical threshold.')
        chart(table,'conversion_rate','Selected audience conversion rate',True)
        st.dataframe(table,width='stretch',hide_index=True)
        st.dataframe(comparisons(table),width='stretch',hide_index=True)
        export(table,'Download filtered aggregate KPIs','filtered_kpis')
elif page=='Data Quality & Methodology':
    st.subheader('Source, integrity and interpretation')
    st.markdown('[Original challenge](https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html) · Kevin Hillstrom, MineThatData, March 2008')
    st.json(provenance)
    st.write('Validated records:',len(df),' • Original columns: 12')
    st.json(quality)
    st.json(integrity(df))
    st.markdown("""**Arm definitions:** Men's merchandise email, women's merchandise email, and no-email control. Product categories do not identify customer gender.

**KPI formulas:** conversion rate = conversions / assigned customers; visit rate = visitors / assigned customers; average spend = total observed spend / assigned customers. Absolute rate difference = 100 × (rate A − rate B), in percentage points. Relative change = 100 × (A/B − 1), undefined when B = 0.

**Data treatment:** original columns retained; `Surburban` maps to `Suburban` only in a new field. Repeated rows are retained. Row IDs identify source-file positions, not original customers. Missing or invalid data stops analysis.

**Limits:** no original IDs, dates, assignment logs, campaign costs, margins or long-term outcomes. Two-week spend is neither profit nor lifetime value. This historical experiment cannot establish present-day commercial impact. Only conditional recommendations are supported; see Business Recommendations.""")
    with st.expander('Descriptive baseline balance'):
        table=balance(df);st.dataframe(table,width='stretch',hide_index=True)
        export(table,'Download baseline balance','baseline_balance')
    st.download_button('Download quality report',json.dumps(quality,indent=2),'quality.json','application/json')

elif page=='Business Economics & ROI Simulator':
    from src.economics_ui import render
    render(df)
else:
    from src.statistical_ui import render
    render(page,df)
