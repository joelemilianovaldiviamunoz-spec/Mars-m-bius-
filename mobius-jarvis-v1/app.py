# MÖBIUS-JARVIS v1.0 - Streamlit app
# - Sidebar: seleccionar celda/módulo
# - Pestañas: Exoplanetas (NASA), Navegación Marte, Cosmología retrocausal

import streamlit as st
import importlib
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import folium
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent

st.set_page_config(page_title="MÖBIUS-JARVIS v1.0", layout="wide")

st.sidebar.title("MÖBIUS-JARVIS")
st.sidebar.markdown("Selecciona celda / módulo o navega por pestañas principales.")

mod_choice = st.sidebar.selectbox(
    "Seleccionar módulo (celda) o vista rápida:",
    options=["Pestañas principales"] + [f"celda_{i}" for i in range(14)]
)

# Helper: intentar importar módulo dinámicamente si existe
def load_module(name: str):
    try:
        spec = importlib.import_module(name)
        importlib.reload(spec)
        return spec
    except Exception as e:
        st.warning(f"No se pudo cargar el módulo '{name}': {e}")
        return None

if mod_choice != "Pestañas principales":
    st.header(f"Módulo seleccionado: {mod_choice}")
    mod = load_module(mod_choice)
    if mod:
        doc = getattr(mod, "__doc__", "")
        if doc:
            st.markdown(f"**Descripción:**\n\n{doc}")
        callables = [n for n in dir(mod) if not n.startswith("_")]
        st.write("Objetos públicos en el módulo:")
        st.write(callables)
        if hasattr(mod, "launch_ui"):
            try:
                mod.launch_ui(st=st)
            except Exception as e:
                st.error(f"Error al ejecutar launch_ui(): {e}")
    st.stop()

# -------------------------
# PESTAÑAS PRINCIPALES
# -------------------------
tab1, tab2, tab3 = st.tabs(["TRMH - Exoplanetas (NASA)", "Navegación Marte", "Cosmología retrocausal"])

with tab1:
    st.header("TRMH — Exoplanetas (integración NASA)")
    st.markdown(
        """
        Esta pestaña demuestra integración con catálogos astronómicos (p. ej. NASA Exoplanet Archive).
        En producción revisa cuotas, endpoints oficiales y caching.
        """
    )
    col1, col2 = st.columns([2, 1])
    with col2:
        nrows = st.number_input("Número de filas a mostrar", min_value=10, max_value=200, value=50)
        refresh = st.button("Refrescar datos (fetch)")

    @st.cache_data(ttl=3600)
    def fetch_exoplanet_archive(limit=200):
        query = ("select pl_name, hostname, disc_year, pl_bmassj, pl_orbper, pl_radj "
                 "from pscomppars order by disc_year desc")
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
        params = {"query": query, "format": "csv", "rows": limit}
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        df = pd.read_csv(pd.compat.StringIO(r.text))
        return df

    try:
        if refresh:
            st.cache_data.clear()
        df = fetch_exoplanet_archive(limit=nrows)
        st.write(f"Mostrando {len(df)} filas (última actualización: {datetime.utcnow().isoformat()} UTC)")
        st.dataframe(df)
        if not df.empty:
            fig, ax = plt.subplots(figsize=(6,4))
            ax.scatter(df["pl_orbper"].replace([np.nan], [0]), df["pl_bmassj"].replace([np.nan], [0]), alpha=0.7)
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_xlabel("Periodo orbital (d)")
            ax.set_ylabel("Masa (M_jup)")
            ax.set_title("Periodo vs Masa — Exoplanetas (muestreo)")
            st.pyplot(fig)
    except Exception as e:
        st.error(f"Error al obtener datos del Exoplanet Archive: {e}")
        st.info("Si el endpoint está inaccesible, prueba más tarde o usa datos locales / cached.")

with tab2:
    st.header("Navegación Marte — Mapa de Sitios (Top 20)")
    st.markdown("Mapa interactivo con marcadores, score estimado y enlaces a imágenes HiRISE (ejemplos).")

    # Load CSV from data folder if exists
    data_csv = BASE / 'data' / 'top20_mars_sites.csv'
    if data_csv.exists():
        df_sites = pd.read_csv(data_csv)
    else:
        df_sites = pd.DataFrame([])

    if df_sites.empty:
        st.warning("No se encontró data/top20_mars_sites.csv. Se usarán sitios sintéticos de ejemplo.")
        top_sites = [
            {"name": "Gale Crater (MSL)", "lat": -5.4, "lon": 137.8, "score": 0.92, "hirise": "https://hirise.lpl.arizona.edu/"},
            {"name": "Jezero Crater (Perseverance)", "lat": 18.4, "lon": 77.5, "score": 0.95, "hirise": "https://hirise.lpl.arizona.edu/"},
            {"name": "Elysium Planitia (InSight)", "lat": 4.5, "lon": 135.9, "score": 0.76, "hirise": "https://hirise.lpl.arizona.edu/"},
        ]
        for i in range(3,20):
            top_sites.append({
                "name": f"Site {i+1}",
                "lat": np.random.uniform(-30, 30),
                "lon": np.random.uniform(-180, 180),
                "score": float(np.round(np.random.uniform(0.4, 0.98), 2)),
                "hirise": "https://hirise.lpl.arizona.edu/"
            })
    else:
        top_sites = df_sites.to_dict(orient='records')

    center = [np.mean([s["lat"] for s in top_sites]), np.mean([s["lon"] for s in top_sites])]
    m = folium.Map(location=center, zoom_start=3, tiles="Stamen Terrain")
    for s in top_sites:
        popup_html = (f"<b>{s['name']}</b><br/>Score: {s['score']}<br/>"
                      f"<a target='_blank' href='{s['hirise']}'>HiRISE</a>")
        folium.CircleMarker(
            location=(s["lat"], s["lon"]),
            radius=8,
            color="crimson",
            fill=True,
            fill_color="crimson",
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(m)

    st_map = st_folium(m, width=900, height=500)

    with st.expander("Tabla de sitios"):
        st.table(pd.DataFrame(top_sites))

with tab3:
    st.header("Cosmología retrocausal — levantando gráficos demo")
    st.markdown("Gráficos demostrativos: w(z) (ecuación de estado) vs z y C_t vs z (índice de coherencia sintético).")

    z = np.linspace(0, 3, 200)
    w0 = st.sidebar.slider("w0", -1.5, -0.5, -1.0)
    wa = st.sidebar.slider("wa", -1.0, 1.0, 0.2)
    w_z = w0 + wa * z / (1 + z)

    fig1, ax1 = plt.subplots(figsize=(6,4))
    ax1.plot(z, w_z, label=f"CPL: w0={w0}, wa={wa}")
    ax1.axhline(-1.0, color="k", ls="--", alpha=0.6)
    ax1.set_xlabel("Redshift z")
    ax1.set_ylabel("w(z)")
    ax1.set_title("w(z) vs z — parametrización CPL (demo)")
    ax1.legend()
    st.pyplot(fig1)

    Ct = 50 + 50 * np.exp(-z/1.2) * np.cos(2.0 * z + 0.3)
    fig2, ax2 = plt.subplots(figsize=(6,4))
    ax2.plot(z, Ct, color="tab:purple")
    ax2.set_xlabel("Redshift z")
    ax2.set_ylabel("C_t (índice sintético)")
    ax2.set_title("C_t vs z (synthetic demonstration)")
    st.pyplot(fig2)

    st.markdown("Si dispones de DESI DR2 o datasets reales, agrega un uploader o conexión aquí para análisis directo.")
