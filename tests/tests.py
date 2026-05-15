#!/usr/bin/env python3
import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bioturbation.model import run
from bioturbation.soil import SoilProfile


# --- Shape tests (default tri-diagonal K) -----------------------------------

data = run(
    n_soil_layers=4,
    soil_layer_depth=0.1,
    initial_conc=[4e-9, 0, 0, 0],
    earthworm_density=[20, 20, 20, 20],
    beta=1e-8,
)
assert data.shape == (4, 78), f"expected (4, 78), got {data.shape}"

data10 = run(
    n_soil_layers=10,
    soil_layer_depth=0.05,
    initial_conc=[10e-9, 5e-9, 3e-9, 1e-9, 0, 0, 0, 0, 0, 0],
    earthworm_density=[20, 20, 20, 10, 10, 10, 5, 5, 5, 5],
    beta=1e-8,
)
assert data10.shape == (10, 594), f"expected (10, 594), got {data10.shape}"


# --- Mass conservation (default tri-diagonal K) -----------------------------

# Equal-depth layers, so conservation reduces to constancy of the column sum.
totals = data.sum(axis=0)
assert np.allclose(totals, totals[0], rtol=0, atol=1e-20), "mass not conserved (default)"

totals10 = data10.sum(axis=0)
assert np.allclose(totals10, totals10[0], rtol=0, atol=1e-20), "mass not conserved (default, 10-layer)"


# --- Steady-state value -----------------------------------------------------

assert np.allclose(data[:, -1], data[:, 0].mean()), "steady state != initial mean (default)"
assert np.allclose(data10[:, -1], data10[:, 0].mean()), "steady state != initial mean (10-layer)"


# --- Mass conservation (explicit symmetric K) -------------------------------

rng = np.random.default_rng(0)
N = 6
A = rng.uniform(0, 1e-7, size=(N, N))
K = (A + A.T) / 2
np.fill_diagonal(K, 0)
data_K = run(
    n_soil_layers=N,
    soil_layer_depth=0.1,
    initial_conc=[1.0, 0.5, 0.25, 0.1, 0.0, 0.0],
    earthworm_density=[0, 0, 0, 0, 0, 0],
    beta=0.0,
    transport_matrix=K,
)
totals_K = data_K.sum(axis=0)
assert np.allclose(totals_K, totals_K[0], rtol=0, atol=1e-12), "mass not conserved (explicit K)"


# --- Non-adjacent smoke test ------------------------------------------------

# Only layers 0 and 3 are coupled; layers 1 and 2 are disconnected and must stay put.
K_na = np.zeros((4, 4))
K_na[0, 3] = K_na[3, 0] = 1e-7
data_na = run(
    n_soil_layers=4,
    soil_layer_depth=0.1,
    initial_conc=[1.0, 0.2, 0.3, 0.0],
    earthworm_density=[0, 0, 0, 0],
    beta=0.0,
    transport_matrix=K_na,
)
assert np.isclose(data_na[0, -1], 0.5), f"layer 0 -> {data_na[0, -1]}, expected 0.5"
assert np.isclose(data_na[3, -1], 0.5), f"layer 3 -> {data_na[3, -1]}, expected 0.5"
assert np.isclose(data_na[1, -1], 0.2), "layer 1 should be unchanged"
assert np.isclose(data_na[2, -1], 0.3), "layer 2 should be unchanged"


# --- Validation -------------------------------------------------------------

def _expect_value_error(K_bad, label):
    try:
        SoilProfile(
            n_soil_layers=K_bad.shape[0] if K_bad.ndim == 2 else 4,
            soil_layer_depth=0.1,
            initial_conc=[0.0] * (K_bad.shape[0] if K_bad.ndim == 2 else 4),
            earthworm_density=[0] * (K_bad.shape[0] if K_bad.ndim == 2 else 4),
            beta=0.0,
            transport_matrix=K_bad,
        )
    except ValueError:
        return
    raise AssertionError(f"expected ValueError for {label}")


_expect_value_error(np.array([[0.0, 1e-7], [2e-7, 0.0]]), "non-symmetric")  # also wrong shape for N=4

K_asym = np.zeros((4, 4))
K_asym[0, 1] = 1e-7  # K[1,0] left at 0
_expect_value_error(K_asym, "non-symmetric (4x4)")

K_diag = np.zeros((4, 4))
K_diag[2, 2] = 1e-7
_expect_value_error(K_diag, "non-zero diagonal")

K_neg = np.zeros((4, 4))
K_neg[0, 1] = K_neg[1, 0] = -1e-7
_expect_value_error(K_neg, "negative entry")


print("Tests passed successfully!")
