"""Original-source retrieval with byte identity and immutable local storage."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen
import pandas as pd
from src.config import SOURCE_URL, EXPECTED_SHA256

def checksum(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def verify_source(path):
    actual = checksum(path)
    if actual != EXPECTED_SHA256:
        raise ValueError(f'Source checksum mismatch: {actual}; do not silently accept changed bytes')
    return actual

def retrieve(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / 'hillstrom.csv'
    if path.exists():
        verify_source(path)
        if not path.with_suffix('.provenance.json').exists():
            raise ValueError('Cached source lacks provenance; restore its manifest')
        return path
    with urlopen(SOURCE_URL, timeout=60) as response:
        payload = response.read()
        resolved = response.geturl()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError('Downloaded bytes do not match verified original dataset')
    # Exclusive creation prevents overwriting an existing original.
    with path.open('xb') as stream:
        stream.write(payload)
    manifest = {'source_url':SOURCE_URL, 'resolved_url':resolved,
                'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),
                'sha256':digest,'bytes':len(payload)}
    path.with_suffix('.provenance.json').write_text(json.dumps(manifest,indent=2))
    return path

def load_raw(path, verify=True):
    if verify:
        verify_source(path)
    return pd.read_csv(path)
