"""
Assumptions (Baseline):
- Instant liquidation at HF < 1
- Deterministic debt growth
- Continuous price observation (no oracle delay)
- No market impact

Extensions (Week 2):
- Oracle discretization (oracle_step)
- Incentive-filtered liquidation (bonus, impact_lambda)
"""


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

    tau, liquidated = compute_liquidation_times(
        HF_paths,
        time_grid,
        oracle_step=params.get("oracle_step", 1),
        bonus=params.get("bonus", None),
        impact_lambda=params.get("impact_lambda", None),
        Q=params.get("Q", None),
        S_paths=S_paths,
    )