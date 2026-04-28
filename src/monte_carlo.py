from src.price_process import simulate_gbm
from src.debt_model import compute_debt
from src.health_factor import compute_health_factor
from src.liquidation_engine import compute_liquidation_times
from src.analytics import liquidation_probability


def run_simulation(params):
    S_paths, time_grid = simulate_gbm(
        params["S0"],
        params["mu"],
        params["sigma"],
        params["T"],
        params["N"],
        params["n_paths"]
    )

    B_t = compute_debt(params["B0"], params["r_b"], time_grid)

    HF_paths = compute_health_factor(
        S_paths,
        B_t,
        params["Q"],
        params["LT"]
    )

    tau, liquidated = compute_liquidation_times(HF_paths, time_grid)

    return {
        "S_paths": S_paths,
        "HF_paths": HF_paths,
        "time_grid": time_grid,
        "liquidation_times": tau,
        "liquidated": liquidated,
        "liquidation_prob": liquidation_probability(liquidated),
    }