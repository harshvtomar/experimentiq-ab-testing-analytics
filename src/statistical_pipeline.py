"""Canonical inference exports; invoke python -m src.statistical_pipeline."""
import json
import hashlib
import time
import platform
import importlib.metadata
from pathlib import Path
import pandas as pd
from src.config import ROOT,EXPECTED_ROWS,EXPECTED_SHA256
from src.serialization import table_bundle
from src.download import retrieve,load_raw
from src.validate import validate
from src.preprocess import normalize
from src.metrics import integrity,balance
from src.inference import (binary_results,revenue_results,adjust_families,segment_results,
                           assert_analysis_population,SEED,REPLICATIONS)

def calculate(df,reps=REPLICATIONS,seed=SEED):
    started=time.perf_counter(); assert_analysis_population(df)
    binary=binary_results(df)
    revenue,histogram,diagnostics=revenue_results(df,reps,seed)
    binary,revenue=adjust_families(binary,revenue)
    segments,interactions=segment_results(df)
    tables={'binary':binary,'revenue':revenue,'bootstrap_histogram':histogram,
            'revenue_diagnostics':diagnostics,'segments':segments,'interactions':interactions}
    checks={'n':len(df),'unique_trace_ids':int(df.row_id.nunique()),'assignment_counts':integrity(df)['counts'],
            'srm':integrity(df),'max_absolute_baseline_smd':float(balance(df).standardized_difference.abs().max()),
            'no_outcome_segmentation':True,'original_randomization_logs_available':False}
    return tables,checks,round(time.perf_counter()-started,3)

def markdown_report(tables,meta):
    b=tables['binary'];r=tables['revenue'];i=tables['interactions']
    lines=['# ExperimentIQ — Statistical analysis report','',
           '## Executive decision summary',
           'This is a retrospective analysis of the 2008 Hillstrom randomized email experiment, not a preregistered study. All 64,000 assignments and zero-spend outcomes are retained. Causal interpretation relies on the source-reported randomization and independent customers; original logs and IDs cannot be audited.',
           '', '### 1. Is there evidence of an effect?']
    for row in b[b.family=='primary_conversion'].itertuples():
        lines.append(f'- {row.comparison}: primary conversion Fisher p={row.p_raw:.6g}, Holm p={row.p_adjusted:.6g}; '+('reject equal conversion rates within the primary family.' if row.reject_holm_005 else 'insufficient evidence within the primary family.'))
    lines += ['', '### 2. How large is the effect?', '|Outcome / contrast|Estimate|95% pointwise CI|Raw p|Holm p|Family|','|---|---:|---|---:|---:|---|']
    for table,mult,unit in [(b,100,'pp'),(r,1,'$/customer')]:
        for x in table.itertuples():
            lines.append(f'|{x.outcome}: {x.comparison}|{x.effect*mult:.4f} {unit}|[{x.ci_low*mult:.4f}, {x.ci_high*mult:.4f}]|{x.p_raw:.6g}|{x.p_adjusted:.6g}|{x.family}|')
    lines += ['','Conversion effects expressed per 1,000 assigned customers:']
    for x in b[b.family=='primary_conversion'].itertuples():
        lines.append(f'- {x.comparison}: {x.effect*1000:.2f} additional conversions per 1,000 (pointwise 95% CI {x.ci_low*1000:.2f} to {x.ci_high*1000:.2f}); relative uplift {x.relative_effect*100:.2f}% (approximate continuity-adjusted log-RR interval {x.relative_ci_low*100:.2f}% to {x.relative_ci_high*100:.2f}%).')
    lines += ['','### 3. Is it economically meaningful?',
              'Economic value is undetermined. Revenue is not profit. No delivery costs, contribution margin, capacity constraints or business-approved minimum effect are supplied. The estimated revenue difference is per assigned customer over two weeks, not a forecast for future customers.',
              '', '## Conditional recommendation',
              'Use the primary family evidence and effect intervals to prioritize a contemporary replication. Consider an email treatment only with costs, margins, unsubscribe/complaint guardrails and deliverability measured. Do not declare a profitable rollout or a validated segment targeting policy from this analysis. The men’s merchandise label describes message content, not customer gender.',
              '', '## Design, methods and multiple testing',
              'Primary conversion contrasts: two separate emails versus no-email control (Holm family size 2). Secondary visit and revenue contrasts each have separate size-2 families. Email-versus-email is an exploratory three-outcome family. No global family-wise guarantee is asserted across families. All planned results are shown.',
              'Binary tests use two-sided Fisher exact p-values, Newcombe/Wilson risk-difference intervals and approximate continuity-adjusted log-RR intervals. CIs are pointwise, not Holm-adjusted or exact inversions of Fisher tests. A p-value is not the probability that the null is true. See docs/STATISTICAL_ANALYSIS_PLAN.md for the plan committed before Session 2 calculations.',
              '', '## Revenue uncertainty and Monte Carlo checks',
              f"{meta['bootstrap_reps']:,} empirical customer bootstrap replications per arm; seed {meta['seed']}. Identical values are compressed into frequencies, with multinomial probabilities proportional to counts. This exactly preserves the empirical n-customer bootstrap distribution for means, including zeros. No equal-weight unique-value sampling occurs.",
              'Percentile 95% intervals are accompanied by separate Welch approximate mean-test p-values; bootstrap tail fractions are not presented as null p-values.',
              '|Contrast|Bootstrap SE|Analytic SE|Half-run endpoint drift / CI width|Warning|','|---|---:|---:|---:|---|']
    for x in r.itertuples():lines.append(f'|{x.comparison}|{x.bootstrap_se:.5f}|{x.analytic_se:.5f}|{x.drift_fraction_width:.3%}|{x.convergence_warning}|')
    lines += ['',f"Inference calculation time in this run: {meta['runtime_seconds']:.3f} seconds. Monte Carlo stability does not establish nominal coverage under every heavy-tailed population.",
              '', '## Segment exploration',
              'Fixed pre-treatment partitions: channel, recency bands, history <=$200/>$200, newbie and two historical merchandise indicators. Segment effects are exploratory with Holm across 28 tests. All 12 planned interaction tests share a separate Holm family. Interaction is evaluated on the additive risk-difference scale with sparse-cell safeguards; it is not inferred from a difference in subgroup significance.',
              '|Variable|Treatment|Interaction raw p|Holm p|Status|','|---|---|---:|---:|---|']
    for x in i.itertuples():lines.append(f'|{x.variable}|{x.treatment}|{x.p_raw:.6g}|{x.p_adjusted:.6g}|{x.status}|')
    lines += ['', 'Full sample sizes, rates, pointwise intervals and warnings are in segments.csv. Overlapping partitions, retrospective examination and approximate interaction tests prohibit confident subgroup-winner claims.',
              '', '## Integrity and limitations',
              f"SRM diagnostic p={meta['checks']['srm']['srm_p_value']:.6f}; this does not verify original assignment logs. Maximum absolute measured baseline SMD={meta['checks']['max_absolute_baseline_smd']:.5f}.",
              'Source provenance is checksum verified. Missing or invalid outcomes stop ingestion; trace-ID duplication stops inference. Exact repeated source rows remain because no original identity supports deduplication. There are no timestamps, long-term outcomes, campaign costs or margins. This historical sample does not establish modern-market transferability. Distributional assumptions, unobserved data errors and individual independence remain limitations.',
              '', '## Reproduction',
              '`python -m src.pipeline` then `python -m src.statistical_pipeline`; run `EXPERIMENTIQ_REQUIRE_DATA=1 python -m pytest -q`. See metadata.json for source/plan hashes, package versions, seed and replications. Row-level files are not redistributed. Session 3 adds explicit economics scenarios and reporting; no invented costs enter this report.']
    return '\n'.join(lines)+'\n'

def run(root=ROOT,reps=REPLICATIONS,seed=SEED):
    root=Path(root);raw=load_raw(retrieve(root/'data/raw'));validate(raw,EXPECTED_ROWS)
    df=normalize(raw);tables,checks,elapsed=calculate(df,reps,seed)
    meta={'source_sha256':EXPECTED_SHA256,'plan_sha256':hashlib.sha256((ROOT/'docs/STATISTICAL_ANALYSIS_PLAN.md').read_bytes()).hexdigest(),
          'bootstrap_reps':reps,'seed':seed,'runtime_seconds':elapsed,'python':platform.python_version(),
          'packages':{x:importlib.metadata.version(x) for x in ['numpy','pandas','scipy','statsmodels']},'checks':checks}
    out=root/'reports/session2';out.mkdir(parents=True,exist_ok=True)
    for name,table in tables.items():table.to_csv(out/f'{name}.csv',index=False)
    (out/'metadata.json').write_text(json.dumps(meta,indent=2,allow_nan=False))
    # Preserve tiny p-values; map unavailable values to strict JSON null.
    payload=table_bundle(tables)
    (out/'inferential_results.json').write_text(json.dumps({'metadata':meta,'results':payload},indent=2,allow_nan=False))
    (out/'STATISTICAL_REPORT.md').write_text(markdown_report(tables,meta))
    return tables,meta

if __name__=='__main__':
    tables,meta=run();print(json.dumps(meta,indent=2));print(tables['binary'][['outcome','comparison','effect','ci_low','ci_high','p_raw','p_adjusted']].to_string(index=False));print(tables['revenue'][['comparison','effect','ci_low','ci_high','p_raw','p_adjusted','drift_fraction_width']].to_string(index=False))
