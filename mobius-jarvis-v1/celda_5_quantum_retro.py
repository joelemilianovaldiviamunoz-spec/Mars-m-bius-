# Celda 5 — Quantum-Retrocausal module (stubs for cosmology functions)

import numpy as np


def w_cpl(z, w0=-1.0, wa=0.2):
    return w0 + wa * z / (1 + z)


def synthetic_Ct_vs_z(z):
    return 50 + 50 * np.exp(-z/1.2) * np.cos(2.0 * z + 0.3)
