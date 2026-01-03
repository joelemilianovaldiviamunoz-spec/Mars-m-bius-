# MÖBIUS-JARVIS v1.0

Repositorio base para MÖBIUS-JARVIS — asistente/visualizador de coherencia Möbiusiana y herramientas astrobiológicas.

Estructura del proyecto:
- app.py: Streamlit app principal con pestañas: Exoplanetas (NASA), Navegación Marte (Folium), Cosmología retrocausal.
- celda_0_trmh_core.py: Núcleo TRMH (módulo principal de análisis de coherencia).
- celda_1_nasa_feeds.py: Integración con APIs de la NASA / MAVEN (placeholders).
- celda_2_mac_anomalies.py: Módulo MAC Anomalies (con CSV privado para 144+20 zonas secretas).
- celda_3_memss_mobius.py: Möbius Entanglement Memory System (MEMS) stub.
- celda_5_quantum_retro.py: Módulo Quantum-Retrocausal (funciones cosmológicas).
- celda_6_biosig_detector.py: Biosignature Detector v4.0 (implementado).
- data/top20_mars_sites.csv: CSV público de ejemplo con los 20 sitios en Marte.
- maps/initial_map.html: mapa folium exportado de ejemplo.
- voice/: carpeta para scripts de voz basados en Grok (opcional).

Celdas / Módulos (0..13) — breve descripción
- Celda 0 — Inicialización / utilidades compartidas (params, logging, helpers).
- Celda 1 — TRMH: núcleo de análisis de coherencia (funciones R_full, muestreo).
- Celda 2 — Integración NASA / Exoplanetas: fetch y preprocesado de exoplanetas (TAB/CSV).
- Celda 3 — Preprocesado de datos astronómicos / filtros / transformaciones.
- Celda 4 — Visualización genérica (matplotlib/plotly wrappers).
- Celda 5 — Módulo MEME: simulaciones multi-escala (generadores de periodos, Qs, fases).
- Celda 6 — Biosignature detector (ejemplo implementado: `celda_6_biosig_detector.py`).
- Celda 7 — Módulo CRCT / Reconfiguración temporal (clase CRCT).
- Celda 8 — Mapas de navegación Mars (folium helpers, top sites, HiRISE links).
- Celda 9 — Cosmología retrocausal: funciones para w(z) y análisis con datasets.
- Celda 10 — RAG / búsqueda de literatura (vector DB glue-code placeholder).
- Celda 11 — Export / Save session / logging científico.
- Celda 12 — Tests / demos / notebooks.
- Celda 13 — Interfaz final / UI helpers para Streamlit.

Cómo empezar
1. Clona el repo y navega a la carpeta mobius-jarvis-v1.
2. Crea un virtualenv e instala dependencias:
   pip install -r requirements.txt
3. Ejecuta la app:
   streamlit run app.py

Notas
- Muchos endpoints (p. ej. NASA, DESI) requieren revisar APIs y cuotas — las llamadas actuales son ilustrativas.
- No incluir claves en el frontend; use variables de entorno en producción.
