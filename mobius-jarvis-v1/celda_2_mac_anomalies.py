# Celda 2 — MAC anomalies (stub). NOTE: private CSV with 144+20 zones must remain private.

import pandas as pd
from pathlib import Path

DATA_PRIV = Path(__file__).parent / 'data' / 'mac_anomalies_private.csv'


def load_mac_anomalies():
    if DATA_PRIV.exists():
        return pd.read_csv(DATA_PRIV)
    else:
        raise FileNotFoundError('Private MAC anomalies CSV not found. Place it in data/mac_anomalies_private.csv')
