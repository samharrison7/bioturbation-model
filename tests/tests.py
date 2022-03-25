#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bioturbation.model import run

# Create an arbitrary model run
data = run(
    n_soil_layers=4,
    soil_layer_depth=0.1,
    initial_conc=[4e-9, 0, 0, 0],
    earthworm_density=[20, 20, 20, 20],
    beta=1e-8
)
# This should result in 4 soil layers and 78 time steps (until steady state)
assert data.shape == (4, 73) 

# Another model run that takes longer to solve
data = run(
    n_soil_layers=10,
    soil_layer_depth=0.05,
    initial_conc=[10e-9, 5e-9, 3e-9, 1e-9, 0, 0, 0, 0, 0, 0],
    earthworm_density=[20, 20, 20, 10, 10, 10, 5, 5, 5, 5],
    beta=1e-8
)
# This should result in 10 soil layers and 400 time steps (until steady state)
assert data.shape == (10, 400)

print("Tests passed successfully!")