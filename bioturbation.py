# import plotly.offline as py
# import plotly.graph_objs as go


class SoilLayer:

    def __init__(self, depth, initial_conc, earthworm_density, alpha):
        """Initialise this soil layer with given depth, concentration and earthworm density"""
        self.depth = depth                                  # m
        self.conc = initial_conc                            # any sensible unit (e.g. kg/m3)
        self.earthworm_density = earthworm_density          # worms/m3
        self.alpha = alpha                                  # m4/s

    def get_bioturbation_rate(self):
        """Calculate the bioturbation rate [/s] for this soil layer and the layer below"""
        bioturbation_rate = (self.earthworm_density * self.alpha) / self.depth
        return bioturbation_rate


class SoilProfile:

    def __init__(self, n_soil_layers, soil_layer_depth, initial_conc, earthworm_density, alpha=1e-8):
        """Initialise the soil profile with given number of soil layers and parameters for those layers"""
        # Create the soil layers in this profile
        self.soil_layers = []
        for i in range(0, n_soil_layers):
            self.soil_layers.append(SoilLayer(soil_layer_depth,
                                              initial_conc[i],
                                              earthworm_density[i],
                                              alpha))

    def bioturbation(self, dt):
        """Perform bioturbation for the length of time t by mixing calculated depth of two layers together"""
        for l, layer in enumerate(self.soil_layers):
            fraction_of_layer_to_mix = layer.get_bioturbation_rate() * dt
            # Don't do for the final layer
            if l < len(self.soil_layers) - 1:
                layer.conc = layer.conc + fraction_of_layer_to_mix * (self.soil_layers[l+1].conc - layer.conc)
                self.soil_layers[l+1].conc = self.soil_layers[l+1].conc \
                                             + fraction_of_layer_to_mix * (layer.conc - self.soil_layers[l+1].conc)


def equal(lst, tol=1e-12):
    """Check if list (lst) is equal within the specified tolerance (tol)"""
    diff = abs(max(lst) - min(lst))
    return diff < tol


def bioturbation(config, max_iter=10000):
    soil_profile = SoilProfile(config['n_soil_layers'],
                               config['soil_layer_depth'],      # Depth of the soil layers in the profile [m]
                               config['initial_conc'],          # Initial concentration in each layer [kg/m3]
                               config['earthworm_density'],     # Earthworm density for each layer [earthworms/m2]
                               config['beta'])  # Empirical parameter relating earthworm density to depth to mix [m3/s]

    # Fill data fill the initial concentrations (specified as input)
    data = [[layer.conc] for layer in soil_profile.soil_layers]
    data_t = [layer.conc for layer in soil_profile.soil_layers]
    t = 0

    # Perform bioturbation until concentration equal across the soil layers
    while t < max_iter + 1 and not equal(data_t, tol=config['steady_state_tol']):
        soil_profile.bioturbation(86400)
        for l, layer in enumerate(soil_profile.soil_layers):
            data[l].append(layer.conc)
            data_t = [layer.conc for layer in soil_profile.soil_layers]
        t += 1
        # If not converged after 10000 time steps, exit and set values as None
        if t > max_iter:
            print("Warning: Steady state not reached after {0} days.".format(max_iter))

    return data


def __main__():
    data = bioturbation({
        'n_soil_layers': 4,
        'soil_layer_depth': 0.1,
        'initial_conc': [4e-9, 0, 0, 0],
        'earthworm_density': [20, 20, 20, 20],
        'beta': 1e-8
    })
    py_data = [go.Scatter(y=data_l,
                          name='Layer {0}'.format(l+1)) for l, data_l in enumerate(data)]

    py.plot(go.Figure(data=py_data,
                      layout=go.Layout(xaxis={'title': 'Time (days)'},
                                       yaxis={'title': 'Concentration (kg/m3)'})))