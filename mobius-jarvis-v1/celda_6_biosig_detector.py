"""Celda 6 — Biosignature detector (ejemplo).
Provee utilidades para:
- generar espectros sintéticos (con/without biosignature)
- entrenar un clasificador simple
- predecir score de biosignature en espectros
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import joblib
import os

MODEL_PATH = "models"
os.makedirs(MODEL_PATH, exist_ok=True)

def generate_synthetic_spectra(n_samples=1000, n_wl=200, biosig_rate=0.3, random_state=42):
    rng = np.random.RandomState(random_state)
    X = rng.normal(loc=0.0, scale=1.0, size=(n_samples, n_wl))
    y = rng.rand(n_samples) < biosig_rate
    bands = [int(n_wl*0.2), int(n_wl*0.5), int(n_wl*0.75)]
    for i in range(n_samples):
        if y[i]:
            for b in bands:
                X[i, b:b+3] += rng.uniform(1.5, 3.0)
    cols = [f"wl_{i}" for i in range(n_wl)]
    df = pd.DataFrame(X, columns=cols)
    df["biosig"] = y.astype(int)
    return df

def train_detector(df, n_estimators=100, random_state=0):
    X = df.drop(columns=["biosig"]).values
    y = df["biosig"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state, stratify=y)
    clf = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1, random_state=random_state)
    clf.fit(X_train, y_train)
    y_prob = clf.predict_proba(X_test)[:,1]
    auc = roc_auc_score(y_test, y_prob)
    model_file = os.path.join(MODEL_PATH, "biosig_rf.joblib")
    joblib.dump(clf, model_file)
    return {"auc": float(auc), "model_path": model_file}

def load_detector():
    model_file = os.path.join(MODEL_PATH, "biosig_rf.joblib")
    if os.path.exists(model_file):
        return joblib.load(model_file)
    return None

def predict_spectrum(model, spectrum):
    x = np.asarray(spectrum).reshape(1, -1)
    p = model.predict_proba(x)[0,1]
    return float(p)

def launch_ui(st=None):
    if st is None:
        raise RuntimeError("launch_ui requiere parámetro st (streamlit).")
    st.subheader("Celda 6 — Biosignature detector (demo)")
    if st.button("Generar dataset sintético y entrenar modelo"):
        with st.spinner("Generando y entrenando..."):
            df = generate_synthetic_spectra(n_samples=800, n_wl=200, biosig_rate=0.3)
            metrics = train_detector(df)
        st.success(f"Entrenado. AUC: {metrics['auc']:.3f}")
        st.info(f"Modelo guardado en: {metrics['model_path']}")

    model = load_detector()
    if model is not None:
        st.write("Modelo cargado.")
        df_test = generate_synthetic_spectra(n_samples=1, n_wl=200, biosig_rate=0.5, random_state=np.random.randint(0,10000))
        spec = df_test.drop(columns=["biosig"]).iloc[0].values
        score = predict_spectrum(model, spec)
        st.write(f"Score demo de biosignature (probabilidad): {score:.3f}")
    else:
        st.warning("No se encontró modelo. Entrena uno con el botón superior.")
