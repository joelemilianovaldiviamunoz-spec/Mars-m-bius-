# Celda 0 — Núcleo TRMH (implementación mínima)

import numpy as np

class TRMHParameters:
    """Contenedor de parámetros para TRMH."""
    def __init__(self):
        self.ALPHA = 8.0
        self.Q_MEAN = 0.8
        self.Q_SIGMA = 0.12
        self.CYCLES = {
            "rotacion_planetaria": 1.0,
            "lunacion": 29.53,
            "traslacion_planetaria": 365.25,
            "rotacion_estelar": 25.0,
            "periodo_galactico": 230e6 * 365.0
        }

params = TRMHParameters()


def sample_periods(P_ref, scale_factor=1.0):
    out = {}
    for k, v in P_ref.items():
        factor = np.random.lognormal(mean=0.0, sigma=0.3 * scale_factor)
        out[k] = float(v * factor)
    return out


def R_full(periods, freqs_ref, weights, Qs, phases, alpha=None):
    if alpha is None:
        alpha = params.ALPHA
    terms = []
    for k in freqs_ref.keys():
        P = periods.get(k, 1.0)
        f = 1.0 / P if P > 1e-12 else 0.0
        f_ref = 1.0 / freqs_ref[k] if freqs_ref[k] > 1e-12 else 0.0
        rel_error = (f - f_ref)**2 / (f_ref**2) if f_ref > 1e-12 else 0.0
        q = Qs.get(k, 1.0)
        w = weights.get(k, 0.0)
        term = w * q * np.exp(-alpha * rel_error)
        terms.append(term)
    raw = float(np.sum(terms))
    max_possible = float(np.sum([abs(weights.get(k,0.0)) for k in freqs_ref.keys()]))
    Ct = 100.0 * raw / max_possible if max_possible > 0 else 0.0
    return Ct
