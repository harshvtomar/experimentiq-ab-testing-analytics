import pandas as pd
import pytest
from src.config import COLUMNS
from src.preprocess import normalize

@pytest.fixture
def raw():
    # Synthetic unit-test fixtures only; never used for project findings.
    return pd.DataFrame([
      [1,'1) $0 - $100',50.,1,0,'Surburban',0,'Web','No E-Mail',1,1,12.34],
      [2,'1) $0 - $100',40.,0,1,'Rural',1,'Phone','No E-Mail',0,0,0.],
      [3,'2) $100 - $200',150.,1,1,'Urban',0,'Web','Mens E-Mail',1,0,0.],
      [4,'2) $100 - $200',180.,1,0,'Urban',1,'Multichannel','Womens E-Mail',1,1,20.]
    ],columns=COLUMNS)
@pytest.fixture
def clean(raw): return normalize(raw)
