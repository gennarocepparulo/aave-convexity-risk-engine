import numpy as np

def should_liquidate(volume, bonus, impact_lambda):
    """
    Economic liquidation condition.

    Liquidation is executed only if liquidation bonus
    exceeds estimated price impact cost.

    Parameters
    ----------
    volume : float
        Liquidated collateral value.
    bonus : float
        Liquidation bonus (fraction).
    impact_lambda : float
        Linear price impact coefficient.

    Returns
    -------
    bool
        True if liquidation is profitable.
    """
    impact_cost = impact_lambda * volume
    liquidation_gain = bonus * volume
    return liquidation_gain > impact_cost


def compute_liquidation_times(
    HF_paths,
    time_grid,
    oracle_step=1,
    bonus=None,
    impact_lambda=None,
    Q=None,
    S_paths=None,
):
    """
    Compute liquidation times with optional oracle discretization
    and incentive-based liquidation filtering.

    Baseline behavior (Week 1):
    - oracle_step = 1
    - bonus = None
    - impact_lambda = None
    -> instant mechanical liquidation

    Extensions (Week 2):
    - oracle_step > 1: delayed boundary detection
    - bonus & impact_lambda: endogenous liquidation
    """

    n_paths, n_steps = HF_paths.shape
    tau = np.full(n_paths, np.nan)
    liquidated = np.zeros(n_paths, dtype=bool)

    for t_idx in range(0, n_steps, oracle_step):

        HF_t = HF_paths[:, t_idx]
        breached = (HF_t < 1.0) & (~liquidated)

        if not np.any(breached):
            continue

        # === Mechanical liquidation (baseline) ===
        if bonus is None or impact_lambda is None:
            liquidated[breached] = True
            tau[breached] = time_grid[t_idx]
            continue

        # === Incentive-filtered liquidation ===
        # Minimal volume approximation
        S_t = S_paths[t_idx]
        volume = Q * S_t

        for i in np.where(breached)[0]:
            if should_liquidate(volume, bonus, impact_lambda):
                liquidated[i] = True
                tau[i] = time_grid[t_idx]

    return tau, liquidated