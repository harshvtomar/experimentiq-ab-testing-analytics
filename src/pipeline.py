import argparse
import json
from pathlib import Path
from src.config import ROOT, EXPECTED_ROWS, FILTERS
from src.download import retrieve, load_raw
from src.validate import validate
from src.preprocess import normalize
from src.metrics import aggregate, comparisons, integrity, balance
from src.database import load_sqlite, run_queries, reconcile

def run(root=ROOT):
    root=Path(root)
    raw=retrieve(root/'data/raw')
    df=load_raw(raw)
    quality=validate(df,EXPECTED_ROWS)
    clean=normalize(df)
    processed=root/'data/processed'; processed.mkdir(parents=True,exist_ok=True)
    reports=root/'reports'; reports.mkdir(parents=True,exist_ok=True)
    clean.to_csv(processed/'customers.csv',index=False)
    summary=aggregate(clean)
    summary.to_csv(reports/'arm_kpis.csv',index=False)
    comparisons(summary).to_csv(reports/'comparisons.csv',index=False)
    balance(clean).to_csv(reports/'baseline_balance.csv',index=False)
    for column in FILTERS: aggregate(clean,[column]).to_csv(reports/f'segments_{column}.csv',index=False)
    database=load_sqlite(clean,processed/'experimentiq.sqlite')
    sql_reports=reports/'sql';sql_reports.mkdir(exist_ok=True)
    for name,table in run_queries(database).items(): table.to_csv(sql_reports/f'{name}.csv',index=False)
    outputs={'quality':quality,'integrity':integrity(clean),'reconciliation':reconcile(database,summary),
             'provenance':json.loads(raw.with_suffix('.provenance.json').read_text())}
    for name,value in outputs.items(): (reports/f'{name}.json').write_text(json.dumps(value,indent=2))
    return outputs

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=ROOT)
    args=parser.parse_args(); print(json.dumps(run(args.root),indent=2))
