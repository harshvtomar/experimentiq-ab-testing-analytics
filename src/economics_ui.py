"""Scenario inputs never mutate source observations or inferential tables."""
import json
import plotly.express as px
import streamlit as st
from src.config import ROOT, ARMS
from src.economics import Assumptions, compare, sensitivity
from src.statistical_ui import canonical_results

PAGE='Business Economics & ROI Simulator'

def render(df):
    st.subheader('Campaign economics under explicit assumptions')
    st.warning('Commercial inputs are hypothetical. Historical two-week revenue effects do not establish current-market profit.')
    ready=st.checkbox('Enable hypothetical assumptions',value=False)
    treatment=st.selectbox('Treatment',ARMS[1:],key='econ_treatment')
    a,b,c=st.columns(3)
    n=a.number_input('Eligible audience',0,1000000000000,10000,1000,key='econ_audience',disabled=not ready)
    m=b.number_input('Contribution margin (%)',0.,100.,40.,5.,key='econ_margin',disabled=not ready)
    cost=c.number_input('Incremental delivery cost ($/customer)',0.,1000000.,.05,.01,format='%.4f',key='econ_delivery',disabled=not ready)
    fixed=a.number_input('Fixed incremental cost ($)',0.,1000000000000.,500.,100.,key='econ_fixed',disabled=not ready)
    k=b.number_input('Effect multiplier',0.,1.,1.,.05,key='econ_multiplier',disabled=not ready)
    st.caption('Multiplier scales the historical effect and interval. Shrinking a negative effect toward zero is not conservative. Fixed setup cost is incurred even with zero audience.')
    if not ready:
        st.info('No economic conclusion yet. Enable assumptions and review each input to calculate a scenario.')
        return
    assumptions=Assumptions(n,m/100,cost,fixed,k)
    revenue=canonical_results(df)[0]['revenue']
    try:
        table=compare(revenue,assumptions); grid=sensitivity(revenue,assumptions)
    except ValueError as exc:
        st.error(str(exc));return
    selected=table.loc[table.treatment==treatment].iloc[0]
    a,b,c=st.columns(3)
    a.metric('Incremental revenue',f'${selected.revenue:,.2f}')
    b.metric('Net campaign contribution',f'${selected.net_value:,.2f}')
    c.metric('Scenario',selected.classification.title())
    st.caption(f'Conditional transformed pointwise interval: {selected.net_low:,.2f} to {selected.net_high:,.2f} (source dollars). This is not a prediction interval for a future campaign.')
    st.dataframe(table,hide_index=True,width='stretch')
    st.caption('Control is an incremental zero baseline with no campaign costs. Negative maximum affordable delivery cost means even free delivery cannot cover setup at the assumed margin. Break-even margin above 100% is infeasible. Undefined ratios remain blank.')
    fig=px.bar(table,x='treatment',y='net_value',color='treatment',title='Hypothetical net contribution by intervention',labels={'net_value':'Net contribution ($)','treatment':'Intervention'})
    st.plotly_chart(fig,width='stretch')
    for driver,label in [('margin','Contribution margin (fraction)'),('delivery_cost','Delivery cost ($/customer)'),('audience','Eligible audience')]:
        plot=grid[grid.driver==driver]
        fig=px.line(plot,x='driver_value',y='net_value',color='treatment',markers=True,labels={'driver_value':label,'net_value':'Net contribution ($)'},title='Sensitivity to '+label.lower())
        fig.add_hline(y=0,line_dash='dash');st.plotly_chart(fig,width='stretch')
    st.markdown('**Uncertainty:** fixed nonnegative audience, multiplier and margin give a monotone affine transformation of the existing revenue interval. Coverage remains pointwise for that transformed historical estimand, conditional on those assumptions. Commercial uncertainty and transfer to new customers are not included. At zero margin, audience or multiplier, statistical variation collapses mechanically; this does not establish business certainty.')
    st.download_button('Download current scenario',table.to_csv(index=False),'ExperimentIQ_Current_Scenario.csv','text/csv')
    st.download_button('Download sensitivity analysis',grid.to_csv(index=False),'ExperimentIQ_Sensitivity.csv','text/csv')
    workbook=ROOT/'reports/session3/ExperimentIQ_Business_Analytics_Report.xlsx'
    if workbook.exists():
        st.download_button('Download Excel business report',workbook.read_bytes(),workbook.name,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        st.caption('Excel starts with the labeled demonstration assumptions. It does not inherit your current browser inputs; use the current-scenario CSV for those.')
