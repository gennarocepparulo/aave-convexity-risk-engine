import numpy as np

def compute_debt(B0, r_b, time_grid):
    return B0 * np.exp(r_b * time_grid)