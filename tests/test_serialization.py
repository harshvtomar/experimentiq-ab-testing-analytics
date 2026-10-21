import json
import numpy as np
import pandas as pd
import pytest
from src.serialization import table_bundle


def test_strict_json_preserves_small_probabilities_and_missing():
    p=5.437358977013792e-113
    frame=pd.DataFrame({'p_raw':[p, np.nan], 'n':[100,0]})
    result=json.loads(json.dumps(table_bundle({'binary':frame}),allow_nan=False))
    assert result['binary'][0]['p_raw']==p
    assert result['binary'][1]['p_raw'] is None
    assert result['binary'][0]['n']==100


def test_infinite_exports_fail_closed():
    with pytest.raises(ValueError):
        table_bundle({'bad':pd.DataFrame({'effect':[float('inf')]})})
