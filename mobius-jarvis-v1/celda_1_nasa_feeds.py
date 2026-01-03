# Celda 1 — Integración con feeds NASA / MAVEN (placeholders)

import requests
import pandas as pd

NASA_EXOARCHIVE_TAP = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"


def fetch_exoplanets(limit=200, timeout=30):
    query = ("select pl_name, hostname, disc_year, pl_bmassj, pl_orbper, pl_radj "
             "from pscomppars order by disc_year desc")
    params = {"query": query, "format": "csv", "rows": limit}
    r = requests.get(NASA_EXOARCHIVE_TAP, params=params, timeout=timeout)
    r.raise_for_status()
    df = pd.read_csv(pd.compat.StringIO(r.text))
    return df


def fetch_maven_data(endpoint_url, params=None):
    """Placeholder for MAVEN or other NASA mission data endpoints."""
    r = requests.get(endpoint_url, params=params, timeout=30)
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return r.text
