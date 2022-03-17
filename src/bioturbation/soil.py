class SoilLayer:
    """Class representing a soil layer"""

    def __init__(self, depth, initial_conc, earthworm_density, beta):
        """Initialise this soil layer with given depth, concentration and earthworm density"""
        self.depth = depth                                  # m
        self.conc = initial_conc                            # kg/m3
        self.earthworm_density = earthworm_density          # individuals/m3
        self.beta = beta                                    # m4/s
        self.bioturbation_rate = (self.earthworm_density * self.beta) / self.depth


class SoilProfile:
    """Class representing a soil profile, consisting of a number of soil layers"""

    def __init__(self, n_soil_layers, soil_layer_depth, initial_conc, earthworm_density, beta):
        """Initialise the soil profile with given number of soil layers and parameters for those layers
            soil_layer_depth: [m]
            initial_conc: [kg/m3]
            earthworm_density: [individuals/m3]
            beta: Empirical fitting parameter [m4/s]"""
        # Create the soil layers in this profile
        self.soil_layers = []
        for i in range(0, n_soil_layers):
            self.soil_layers.append(SoilLayer(soil_layer_depth,
                                              initial_conc[i],
                                              earthworm_density[i],
                                              beta))

    def bioturbation(self, dt):
        """Perform bioturbation for the length of time t by mixing calculated depth of two layers together"""
        for l, layer in enumerate(self.soil_layers):
            fraction_of_layer_to_mix = layer.bioturbation_rate * dt
            # Don't do for the final layer
            if l < len(self.soil_layers) - 1:
                layer.conc = layer.conc + fraction_of_layer_to_mix * (self.soil_layers[l+1].conc - layer.conc)
                self.soil_layers[l+1].conc = self.soil_layers[l+1].conc \
                                             + fraction_of_layer_to_mix * (layer.conc - self.soil_layers[l+1].conc)
