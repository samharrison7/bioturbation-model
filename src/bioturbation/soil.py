import warnings

import numpy as np


class SoilLayer:
    """Class representing a soil layer"""

    def __init__(self, depth, initial_conc, earthworm_density, beta):
        """Initialise this soil layer with given depth, concentration and earthworm density"""
        self.depth = depth                                  # m
        self.conc = initial_conc                            # kg/m3
        self.earthworm_density = earthworm_density          # individuals/m3
        self.beta = beta                                    # m4/s


class SoilProfile:
    """Class representing a soil profile, consisting of a number of soil layers"""

    def __init__(self, n_soil_layers, soil_layer_depth, initial_conc, earthworm_density, beta,
                 transport_matrix=None):
        """Initialise the soil profile with given number of soil layers and parameters for those layers
            soil_layer_depth: [m]
            initial_conc: [kg/m3]
            earthworm_density: [individuals/m3]
            beta: Empirical fitting parameter [m4/s]
            transport_matrix: Optional N x N symmetric matrix of pairwise transport rates [1/s]
                between any two soil layers. When omitted, a tri-diagonal matrix is built from
                beta and earthworm_density, reproducing adjacent-only mixing."""
        # Create the soil layers in this profile
        self.soil_layers = []
        for i in range(0, n_soil_layers):
            self.soil_layers.append(SoilLayer(soil_layer_depth,
                                              initial_conc[i],
                                              earthworm_density[i],
                                              beta))

        # Build or validate the pairwise transport-rate matrix K [1/s].
        # Mass is conserved exactly when K is symmetric (equal-depth case). For
        # unequal layer depths, conservation requires d_i * K[i,j] == d_j * K[j,i];
        # current model uses equal depths so simple symmetry is enforced.
        if transport_matrix is None:
            K = np.zeros((n_soil_layers, n_soil_layers))
            for l in range(n_soil_layers - 1):
                rate = beta * earthworm_density[l] / soil_layer_depth
                K[l, l + 1] = rate
                K[l + 1, l] = rate
        else:
            K = np.asarray(transport_matrix, dtype=float)
            if K.shape != (n_soil_layers, n_soil_layers):
                raise ValueError(
                    f"transport_matrix must have shape ({n_soil_layers}, {n_soil_layers}), "
                    f"got {K.shape}"
                )
            if not np.allclose(K, K.T):
                raise ValueError("transport_matrix must be symmetric")
            if not np.allclose(np.diag(K), 0):
                raise ValueError("transport_matrix must have zero diagonal")
            if (K < 0).any():
                raise ValueError("transport_matrix must be non-negative")
        self.K = K

    def bioturbation(self, dt):
        """Advance the soil profile by one time step of length dt [s].

        Computes all pairwise fluxes from the old state in a single sweep, so total
        mass is conserved exactly (modulo floating-point) for any symmetric K."""
        c_old = np.array([layer.conc for layer in self.soil_layers])
        delta = (self.K * (c_old[np.newaxis, :] - c_old[:, np.newaxis])).sum(axis=1)
        c_new = c_old + dt * delta
        for layer, c in zip(self.soil_layers, c_new):
            layer.conc = c
        if dt * self.K.sum(axis=1).max() > 1:
            warnings.warn(
                "dt * max_row_sum(K) > 1: forward-Euler stability bound violated",
                RuntimeWarning,
            )
