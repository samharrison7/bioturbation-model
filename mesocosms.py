from bioturbation import bioturbation
import matplotlib.pyplot as plt

# Mesocosms
#   Volume of soil: 1.46e-3 m3
#   Earthworms: 5
#   Earthworm density: 3425 worms/m3

config = {
    'n_soil_layers': 6,
    'soil_layer_depth': 0.02,                                               # m
    'initial_conc': [1e8, 0, 0, 0, 0, 0],                             # mg/kg dry weight
    'earthworm_density': [0.01e8, 0.01e8, 0.01e8, 0.01e8, 0.01e8, 0.01e8],  # worms/m3
    'beta': 1e-14
}

data = bioturbation(config)
plt.plot(data)
