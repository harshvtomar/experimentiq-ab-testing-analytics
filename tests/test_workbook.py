"""Validate exported OOXML and recorded Artifact Tool recalculation against Python.

CI inspects the delivered workbook; it does not claim to run native Excel.
"""
import json
import hashlib
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
import pytest
from src.config import ROOT
from src.economics import Assumptions,compare

OUT=ROOT/'reports/session3'
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def test_exported_workbook_structure_and_formula_caches():
    with zipfile.ZipFile(OUT/'ExperimentIQ_Business_Analytics_Report.xlsx') as z:
        book=ET.fromstring(z.read('xl/workbook.xml'))
        names=[x.attrib['name'] for x in book.findall('s:sheets/s:sheet',NS)]
        assert len(names)==7 and 'Scenario Inputs' in names
        sheets=[x for x in z.namelist() if x.startswith('xl/worksheets/sheet') and x.endswith('.xml')]
        formula_cells=[]
        for name in sheets:
            tree=ET.fromstring(z.read(name))
            assert not [c for c in tree.findall('.//s:c',NS) if c.attrib.get('t')=='e']
            formula_cells.extend(c for c in tree.findall('.//s:c',NS) if c.find('s:f',NS) is not None)
        assert formula_cells and all('#REF!' not in c.find('s:f',NS).text for c in formula_cells)
        charts=[x for x in z.namelist() if '/charts/chart' in x and x.endswith('.xml')]
        assert len(charts)==3
        assert all(b'<c:f>' in z.read(c) or b'<f>' in z.read(c) for c in charts)

def test_recorded_excel_recalculation_matches_python():
    checks=json.loads((OUT/'excel_recalculation_checks.json').read_text())
    rev=pd.read_csv(ROOT/'reports/session2/revenue.csv')
    row_to_key={16:'effective_uplift',17:'revenue',18:'gross_contribution',19:'variable_cost',20:'fixed_cost',21:'total_cost',22:'net_value',23:'net_low',24:'net_high',26:'break_even_uplift',27:'break_even_margin',28:'max_delivery_cost',29:'net_return_on_cost',30:'classification'}
    assert {c['label'] for c in checks}=={'demo','changed','zero audience','zero costs','zero margin','missing margin','invalid margin'}
    for case in checks:
        if case['label'] in ['missing margin','invalid margin']:
            assert case['model'][6]==['n.a.','n.a.']
            continue
        expected=compare(rev,Assumptions(*case['inputs'])).iloc[1:]
        for row,key in row_to_key.items():
            for i in range(2):
                actual=case['model'][row-16][i];want=expected.iloc[i][key]
                if isinstance(want,str):assert actual==want
                elif want is None or pd.isna(want):assert actual=='n.a.'
                else:assert actual==pytest.approx(want,rel=1e-12,abs=1e-8)
    saved=json.loads((OUT/'excel_reopen_values.json').read_text())
    assert saved==checks[0]['model'][6:9]

def test_verification_manifest_and_exported_cached_values():
    manifest=json.loads((OUT/'excel_verification_manifest.json').read_text())
    for file,digest in manifest['hashes'].items():
        target=(ROOT/file) if file.startswith('scripts/') else OUT/file
        assert hashlib.sha256(target.read_bytes()).hexdigest()==digest
    with zipfile.ZipFile(OUT/'ExperimentIQ_Business_Analytics_Report.xlsx') as z:
        model=ET.fromstring(z.read('xl/worksheets/sheet3.xml'))
        cells={c.attrib['r']:c for c in model.findall('.//s:c',NS)}
        values=json.loads((OUT/'excel_reopen_values.json').read_text())
        for i,row in enumerate([22,23,24]):
            for j,col in enumerate(['E','F']):
                assert float(cells[f'{col}{row}'].find('s:v',NS).text)==pytest.approx(values[i][j],rel=1e-12)
