#!/usr/bin/env python3
from model import run, as_df
from model import as_df

data = run(
    n_soil_layers=4,
    soil_layer_depth=0.1,
    initial_conc=[4e-9, 0, 0, 0],
    earthworm_density=[20, 20, 20, 20],
    beta=1e-8
)
print(data)