#!/usr/bin/env python3
from bioturbation import bioturbation, as_df
import plotly.express as px


data = bioturbation(
    n_soil_layers=4,
    soil_layer_depth=0.1,
    initial_conc=[4e-9, 0, 0, 0],
    earthworm_density=[20, 20, 20, 20],
    steady_state_tol=1e-12,
    beta=1e-8
)

fig = px.line(as_df(data))
fig.show()