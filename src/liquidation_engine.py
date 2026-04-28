import numpy as np

def compute_liquidation_times(HF_paths, time_grid):
    below_threshold = HF_paths < 1.0

    first_hit_idx = np.argmax(below_threshold, axis=1)
    has_liquidation = below_threshold.any(axis=1)

    liquidation_times = np.full(HF_paths.shape[0], np.nan)
    liquidation_times[has_liquidation] = time_grid[first_hit_idx[has_liquidation]]

    return liquidation_times, has_liquidation