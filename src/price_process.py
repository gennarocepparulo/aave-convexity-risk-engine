import numpy as np

def simulate_gbm(S0, mu, sigma, T, N, n_paths, seed=42):
    np.random.seed(seed)

    dt = T / N
    time_grid = np.linspace(0, T, N + 1)

    Z = np.random.normal(size=(n_paths, N))
    log_returns = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z

    log_S = np.cumsum(log_returns, axis=1)
    log_S = np.hstack([np.zeros((n_paths, 1)), log_S])

    S_paths = S0 * np.exp(log_S)

    return S_paths, time_grid