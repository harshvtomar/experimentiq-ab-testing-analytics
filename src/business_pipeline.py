"""Generate aggregate business reporting assets: python -m src.business_pipeline."""
import hashlib
import json
import shutil
import sqlite3
from dataclasses import asdict
from pathlib import Path
import numpy as np
import pandas as pd
from src.config import ROOT, EXPECTED_SHA256
from src.economics import DEMO, compare, sensitivity

def reconcile_economics(table):
    inputs=table.loc[table.treatment!='Control',['treatment','audience','margin','delivery_cost','fixed_cost','multiplier','source_effect','source_low','source_high']]
    with sqlite3.connect(':memory:') as con:
        inputs.to_sql('scenario_inputs',con,index=False)
        sql=pd.read_sql_query((ROOT/'sql/economics.sql').read_text(),con)
    py=table.set_index('treatment');sql=sql.set_index('treatment')
    for col in sql:
        np.testing.assert_allclose(sql[col],py.loc[sql.index,col],rtol=1e-12,atol=1e-9,equal_nan=True)
    return {'status':'passed','fields':list(sql.columns),'absolute_tolerance':1e-9}

def run(root=ROOT):
    root=Path(root);out=root/'reports/session3';out.mkdir(parents=True,exist_ok=True)
    rev=pd.read_csv(root/'reports/session2/revenue.csv')
    binary=pd.read_csv(root/'reports/session2/binary.csv')
    arms=pd.read_csv(root/'reports/arm_kpis.csv')
    scenario=compare(rev,DEMO);grid=sensitivity(rev,DEMO)
    check=reconcile_economics(scenario)
    scenario.to_csv(out/'demonstration_scenarios.csv',index=False)
    grid.to_csv(out/'sensitivity.csv',index=False)
    meta={'assumption_basis':'hypothetical demonstration, not actual commercial inputs',
          'assumptions':asdict(DEMO),'source_sha256':EXPECTED_SHA256,
          'revenue_export_sha256':hashlib.sha256((root/'reports/session2/revenue.csv').read_bytes()).hexdigest(),
          'sql_reconciliation':check}
    (out/'metadata.json').write_text(json.dumps(meta,indent=2,allow_nan=False))
    def records(frame):
        return [{k:None if pd.isna(v) else v for k,v in row.items()} for row in frame.to_dict('records')]
    workbook={'arms':records(arms),
              'binary':records(binary),
              'revenue':records(rev),
              'scenario':records(scenario),
              'assumptions':asdict(DEMO),'metadata':meta}
    (out/'workbook_inputs.json').write_text(json.dumps(workbook,indent=2,allow_nan=False))
    power=root/'powerbi/data';power.mkdir(parents=True,exist_ok=True)
    mapping={'arm_performance':'arm_kpis.csv','descriptive_comparisons':'comparisons.csv',
             'binary_inference':'session2/binary.csv','revenue_inference':'session2/revenue.csv',
             'segment_effects':'session2/segments.csv','interactions':'session2/interactions.csv'}
    for name,source in mapping.items():shutil.copyfile(root/'reports'/source,power/(name+'.csv'))
    scenario.to_csv(power/'scenario_snapshot.csv',index=False)
    grid.to_csv(power/'sensitivity_snapshot.csv',index=False)
    pd.DataFrame({'arm':['Control',"Men's email","Women's email"],'arm_order':[0,1,2]}).to_csv(power/'dim_arm.csv',index=False)
    lines=['# ExperimentIQ — Executive business report','',
      '## Objective and evidence',
      'Determine which explicit campaign assumptions could make historical email effects economically attractive. Hillstrom randomized 64,000 customers across two merchandise emails and no-email control. Outcomes span two weeks. Conversion is primary; visits and spending are secondary.',
      '', '### 1. Is there statistical evidence of an effect?']
    for r in binary[binary.family=='primary_conversion'].itertuples():
        lines.append(f'- {r.treatment}: conversion difference {100*r.effect:.4f} pp; 95% pointwise CI [{100*r.ci_low:.4f}, {100*r.ci_high:.4f}]; primary Holm p={r.p_adjusted:.6g}.')
    lines+=['','### 2. How large is the effect?']
    for r in rev[rev.reference=='Control'].itertuples():
        lines.append(f'- {r.treatment}: ${r.effect:.4f} additional revenue per assigned customer, 95% percentile bootstrap CI [${r.ci_low:.4f}, ${r.ci_high:.4f}].')
    lines+=['','### 3. Under which assumptions is it attractive?',
      'Illustration only: 10,000 eligible customers; 40% contribution margin on incremental sales; $0.05 incremental delivery cost per customer; $500 fixed incremental setup; multiplier 1. All commercial assumptions are invented demonstration inputs, not measured facts.',
      '|Intervention|Revenue ($)|Gross contribution ($)|Total costs ($)|Net contribution ($)|Conditional lower–upper ($)|Break-even margin|Maximum delivery cost ($)|',
      '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in scenario[scenario.treatment!='Control'].itertuples():
        lines.append(f'|{r.treatment}|{r.revenue:,.2f}|{r.gross_contribution:,.2f}|{r.total_cost:,.2f}|{r.net_value:,.2f}|{r.net_low:,.2f} to {r.net_high:,.2f}|{r.break_even_margin:.2%}|{r.max_delivery_cost:.4f}|')
    lines+=['','Control is the zero incremental baseline. Net return on cost is net contribution / incremental campaign costs, undefined at zero costs. It is a scenario ratio, not realized ROI.',
      '', '## Decision and limitations',
      'Both emails have evidence of a positive primary conversion effect in this historical experiment. The supplied scenario can be changed to favorable or unfavorable by changing margin, delivery costs or setup costs. No subgroup targeting policy is validated by the adjusted interaction tests.',
      'Use a contemporary randomized replication with measured costs, contribution margin, unsubscribe/complaint and deliverability guardrails. Set a business-approved economic threshold before the replication. Do not treat statistical significance as a rollout decision.',
      'Conditional intervals transform the existing pointwise revenue interval by fixed nonnegative audience × multiplier × margin and subtract fixed costs. They exclude commercial-input uncertainty, treatment effects on margin, audience mix changes, future realized campaign variation and market drift. They are not calibrated future-profit prediction intervals. No joint coverage across treatment choices is claimed.',
      'All source rows and zero-spend customers remain. Original IDs, logs and timestamps are unavailable. Dataset redistribution rights remain unclear; only aggregate tables are included.',
      '', '## Reproduction and handoff',
      '`python -m src.business_pipeline` regenerates these scenarios, Power BI aggregates, workbook input JSON and the report from canonical Session 2 exports. Excel formulas provide editable calculations. See docs/ECONOMICS.md, docs/EXCEL.md and powerbi/README.md for formulas, build and verification boundaries.']
    (out/'EXECUTIVE_BUSINESS_REPORT.md').write_text('\n'.join(lines)+'\n')
    return scenario,check

if __name__=='__main__':
    table,check=run();print(table[['treatment','revenue','net_value','net_low','net_high']].to_string(index=False));print(json.dumps(check))
