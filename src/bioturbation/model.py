import numpy as np
import pandas as pd
import plotly.express as px
from bioturbation.soil import SoilProfile


def run(n_soil_layers, soil_layer_depth, initial_conc, earthworm_density, beta,
                 dt=86400, steady_state_tol=1e-12, max_iter=10000):
    """Perform the bioturabtion calculations"""

    # Set up the soil profile
    soil_profile = SoilProfile(n_soil_layers,
                               soil_layer_depth,        # Depth of the soil layers in the profile [m]
                               initial_conc,            # Initial concentration in each layer [kg/m3]
                               earthworm_density,       # Earthworm density for each layer [earthworms/m2]
                               beta)                    # Empirical parameter relating earthworm density to depth to mix [m3/s]

    # Fill data fill the initial concentrations (specified as input)
    data = [[layer.conc] for layer in soil_profile.soil_layers]
    data_t = [layer.conc for layer in soil_profile.soil_layers]
    t = 0

    # Perform bioturbation until concentration equal across the soil layers
    while t < max_iter + 1 and not equal(data_t, tol=steady_state_tol):
        soil_profile.bioturbation(dt)
        for l, layer in enumerate(soil_profile.soil_layers):
            data[l].append(layer.conc)
            data_t = [layer.conc for layer in soil_profile.soil_layers]
        t += 1
        # If not converged after 10000 time steps, exit and set values as None
        if t > max_iter:
            print(f'Steady state not reached after {max_iter} days.')

    return np.array(data)


def as_df(data):
    df = pd.DataFrame(np.swapaxes(data,0,1),
                      columns=[f'soil_layer_{i+1}' for i in np.arange(0,data.shape[0])])
    return df


def plot(data):
    fig = px.line(as_df(data), labels={'value': 'concentration', 'index': 'time'})
    fig.show()


def equal(lst, tol=1e-12):
    """Check if list (lst) is equal within the specified tolerance (tol)"""
    diff = abs(max(lst) - min(lst))
    return diff < tol