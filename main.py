import plotly.offline as py
import plotly.graph_objs as go


class SoilLayer:

    def __init__(self, depth, initial_conc, earthworm_density):
        """Initialise this soil layer with given depth, concentration and earthworm density"""
        self.depth = depth
        self.conc = initial_conc
        self.earthworm_density = earthworm_density

    def get_bioturbation_rate(self):
        """Calculate the bioturbation rate for this soil layer and the layer below"""
        bioturbation_rate = (self.earthworm_density * 1e-8) / self.depth
        return bioturbation_rate


class SoilProfile:

    def __init__(self, n_soil_layers, soil_layer_depth, initial_conc, earthworm_density):
        """Initialise the soil profile with given number of soil layers and parameters for those layers"""
        # Create the soil layers in this profile
        self.soil_layers = []
        for i in range(0, n_soil_layers):
            self.soil_layers.append(SoilLayer(soil_layer_depth[i],
                                              initial_conc[i],
                                              earthworm_density[i]))

    def bioturbation(self, t):
        """Perform bioturbation for the length of time t by mixing calculated depth of two layers together"""
        for l, layer in enumerate(self.soil_layers):
            fraction_of_layer_to_mix = layer.get_bioturbation_rate() * t
            # Don't do for the final layer
            if l < len(self.soil_layers) - 1:
                layer.conc = layer.conc + fraction_of_layer_to_mix * (self.soil_layers[l+1].conc - layer.conc)
                self.soil_layers[l+1].conc = self.soil_layers[l+1].conc + \
                                             fraction_of_layer_to_mix * (layer.conc - self.soil_layers[l+1].conc)


def equal(list):
    """Check if list is (almost) equal"""
    diff = abs(max(list) - min(list))
    return diff < 1e-12


# Config
n_soil_layers = 4
soil_layer_depth = [0.1, 0.1, 0.1, 0.1]                       # Depth of each soil layer in the profile [m]
initial_conc = [4e-9, 0, 0, 0]                                # Initial concentration in each layer [kg/m3]
earthworm_density = [20, 20, 20, 20]                          # Earthworm density for each layer [earthworms/m2]

soil_profile = SoilProfile(n_soil_layers,
                           soil_layer_depth,
                           initial_conc,
                           earthworm_density)

# Fill data fill the initial concentrations (specified as input)
data = [[layer.conc] for layer in soil_profile.soil_layers]
data_t = [layer.conc for layer in soil_profile.soil_layers]
t = 0

# Perform bioturbation until concentration equal across the soil layers
while not equal(data_t):
    soil_profile.bioturbation(86400)
    for l, layer in enumerate(soil_profile.soil_layers):
        data[l].append(layer.conc)
        data_t = [layer.conc for layer in soil_profile.soil_layers]
    t += 1

py_data = [go.Scatter(y=data_l,
                      name='Layer {0}'.format(l+1)) for l, data_l in enumerate(data)]

py.plot(go.Figure(data=py_data,
                  layout=go.Layout(xaxis={'title': 'Time (days)'},
                                   yaxis={'title': 'Concentration (kg/m3)'})))
