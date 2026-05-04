import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def run_cascade_simulation(
    params,
    n_agents=1000,
    seed=42,
):
    """
    Minimal cascade engine with probabilistic, agent-specific liquidation.

    Liquidation occurs as a Bernoulli event with probability π_{i,t},
    conditional on:
      - Health Factor < 1
      - oracle availability
      - economic profitability
      - agent-specific urgency (distance to boundary)

    This model introduces ONE feedback loop:
      liquidation -> selling -> price impact -> HF deterioration -> more liquidation
    """

    rng = np.random.default_rng(seed)

    # ------------------------------------------------------------------
    # Parameters
    # ------------------------------------------------------------------
    S0 = params["S0"]
    mu = params["mu"]
    sigma = params["sigma"]
    T = params["T"]
    N = params["N"]

    Q = params["Q"]
    LT = params["LT"]

    beta = params["beta"]                 # liquidation bonus
    impact_lambda = params["impact_lambda"]  # price impact
    eps = params["eps"]                   # smoothness of profitability
    delta = params["delta"]               # smoothness of urgency
    oracle_step = params["oracle_step"]

    dt = T / N

    # ------------------------------------------------------------------
    # Agent initialization (heterogeneous solvency)
    # ------------------------------------------------------------------
    HF0 = rng.uniform(1.2, 2.5, size=n_agents)
    B0 = (Q * S0 * LT) / HF0

    liquidated = np.zeros(n_agents, dtype=bool)

    # ------------------------------------------------------------------
    # Market state
    # ------------------------------------------------------------------
    S = np.zeros(N)
    S[0] = S0

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------
    cascade_count = np.zeros(N)
    toxic_fraction = np.zeros(N)

    # ------------------------------------------------------------------
    # Main time loop
    # ------------------------------------------------------------------
    for t_idx in range(1, N):

        # --- exogenous price evolution (GBM) ---
        dW = rng.normal(scale=np.sqrt(dt))
        S[t_idx] = S[t_idx - 1] * np.exp(
            (mu - 0.5 * sigma**2) * dt + sigma * dW
        )

        # --- endogenous price impact from previous liquidations ---
        if cascade_count[t_idx - 1] > 0:
            S[t_idx] *= np.exp(
                -impact_lambda * cascade_count[t_idx - 1] * Q
            )

        # --- compute Health Factors ---
        HF = (Q * S[t_idx] * LT) / B0

        # --- oracle availability (hard gate) ---
        oracle_active = (t_idx % oracle_step == 0)

        newly_liquidated = np.zeros(n_agents, dtype=bool)

        if oracle_active:

            # ----------------------------------------------------------
            # Liquidation probability π_{i,t}
            # ----------------------------------------------------------

            # Global collateral value
            V_t = Q * S[t_idx]

            # (1) Economic profitability (global)
            profitability = sigmoid(
                (beta - impact_lambda * V_t) / eps
            )

            # (2) Urgency: distance to boundary (agent-specific)
            urgency = sigmoid(
                (1.0 - HF) / delta
            )

            # (3) Final liquidation probability
            
            liquidity_factor = params.get("liquidity_factor", 1.0)

            p_liq = liquidity_factor * profitability * urgency


            # ----------------------------------------------------------
            # Liquidation execution (Bernoulli)
            # ----------------------------------------------------------
            candidates = (HF < 1.0) & (~liquidated)

            draws = rng.uniform(size=n_agents)
            execute = candidates & (draws < p_liq)

            newly_liquidated[execute] = True
            liquidated[execute] = True

        # ------------------------------------------------------------------
        # Diagnostics update
        # ------------------------------------------------------------------
        cascade_count[t_idx] = newly_liquidated.sum()

        toxic = (HF < 1.0) & (~liquidated)
        toxic_fraction[t_idx] = toxic.mean()

    return {
        "price": S,
        "cascade_count": cascade_count,
        "toxic_fraction": toxic_fraction,
        "final_liquidation_fraction": liquidated.mean(),
    }