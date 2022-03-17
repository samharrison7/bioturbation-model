from bioturbation import bioturbation
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

# Mesocosms
#   Volume of soil: 1.46e-3 m3
#   Earthworms: 5
#   Earthworm density: 3411 worms/m3

# Importing the experimental data
df = pd.read_excel('/home/sharrison/nf/data/interim/soil/mesocosms/mesocosms.xlsx')
df_init = df.iloc[0]                    # Get the measurements at t=0
# Loop over columns and get values for initial concs
initial_conc = []
for name, val in df_init[1:].iteritems():
    if "error" not in name:
        initial_conc.append(val)

# Array of experimental layers for use in plotting data
#   experimental layer => [model layer(s)]
experimental_layers = {
    'Layer 1': [1, 2],
    'Layer 2': [3],
    'Middle layer': [4, 5],
    'Layer 3': [6],
    'Layer 4': [7, 8]
}
colors = {
    'Layer 1': 'blue',
    'Layer 2': 'green',
    'Middle layer': 'red',
    'Layer 3': 'orange',
    'Layer 4': 'cyan'
}

# Set up the config
config = {
    'n_soil_layers': 8,
    'soil_layer_depth': 0.02,                   # m
    'initial_conc': initial_conc,               # mg/kg dry weight
    'earthworm_density': [3411] * 8,            # worms/m3
    'beta': 4.4229119627116475e-12
}

y_calc = bioturbation(config)
x_calc = range(0, len(y_calc[0]))
print("Time to steady state: {0}".format(len(y_calc[0])))

# Loop through the experimental layers and plot the calculated concentrations,
# averaging over the model layers, followed by the experimental concentrations
for experimental_layer, model_layers in experimental_layers.items():
    model_data_array = np.zeros([len(model_layers), len(x_calc)])
    experimental_data_array = np.zeros([len(model_layers), df.shape[0]])
    experimental_error_array = np.zeros([len(model_layers), df.shape[0]])
    for l, model_layer in enumerate(model_layers):
        model_data_array[l] = y_calc[model_layer - 1]
        experimental_data_array[l] = df['Layer {0}'.format(model_layer)]
        experimental_error_array[l] = df['Layer {0} error'.format(model_layer)]

    # Get average for these model layers
    model_data = np.mean(model_data_array, axis=0)
    experimental_data = np.mean(experimental_data_array, axis=0)
    experimental_error = np.mean(experimental_error_array, axis=0)

    # Plot this model output for this experimental layer
    plt.plot(x_calc, model_data, label=experimental_layer, color=colors[experimental_layer])
    plt.errorbar(df['Time'].tolist(),
                 experimental_data,
                 yerr=experimental_error,
                 fmt='o',
                 label=experimental_layer,
                 color=colors[experimental_layer])

plt.xlabel('Time (days)')
plt.ylabel('Concentration (mg/kg dry weight)')
plt.yscale('log')
plt.xlim(xmin=-5, xmax=500)
plt.legend()
plt.show()
