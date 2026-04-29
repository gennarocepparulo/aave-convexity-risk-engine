# Model Limitations & Reality Gap

This document formalizes the **assumptions and scope** of the baseline liquidation model used in this project. The purpose is not to weaken the core results, but to **clarify which findings are structural** (driven by protocol design) and which depend on simplifying approximations. All extensions introduced in Week 2 should be interpreted as **layered perturbations** of this baseline.

---

## 1. Baseline Model Assumptions

The baseline Monte Carlo engine studies liquidation risk under the following assumptions:

### 1.1 Instantaneous Liquidation at the Boundary
Liquidation is triggered mechanically and immediately when the Health Factor crosses the threshold:

$$HF_t < 1.$$

There is no delay between boundary crossing and liquidation execution. Liquidation is treated as a deterministic stopping event.

---

### 1.2 Deterministic Debt Evolution
Debt evolves deterministically according to a fixed rule (e.g., constant or smoothly compounding growth). There is no feedback from utilization, liquidity stress, or market conditions into the debt process.

---

### 1.3 Continuous Price Observation
Collateral prices are assumed to be observed continuously and without delay. The model implicitly assumes:

- perfect price feeds,
- no oracle heartbeat or deviation thresholds,
- no latency between market price changes and protocol observation.

As a result, liquidation decisions are based on the true underlying price process.

---

### 1.4 Mechanical Liquidation (No Incentives)
Liquidation is treated as a purely mechanical rule. If the liquidation condition is met, liquidation always occurs. There is no modeling of:

- liquidation bonuses,
- slippage,
- gas costs,
- or liquidator profitability constraints.

---

### 1.5 No Market Impact
Liquidations do not affect prices. Each position is treated in isolation, and collateral sales do not generate price impact or feedback into other positions.

---

## 2. Implications of the Assumptions

These assumptions deliberately isolate a **clean structural mechanism**: liquidation as a first‑passage event of a stochastic Health Factor process. Under these conditions:

- Liquidation convexity arises solely from the **threshold structure** of the protocol.
- Nonlinearity is localized near the liquidation boundary.
- Volatility acts as an accelerator but does not generate convexity by itself.

These results are therefore **structural** with respect to Aave’s liquidation rule and do not rely on detailed microstructure modeling.

---

## 3. What the Baseline Model Does *Not* Capture

The baseline model does not aim to represent the full operational reality of the Aave protocol. In particular, it omits:

- oracle discretization and delayed boundary detection,
- endogenous liquidation decisions driven by incentives,
- liquidity constraints and market impact,
- multi‑agent interactions and cascades,
- protocol‑level state variables such as stablecoin supply.

As a result, baseline liquidation probabilities should not be interpreted as **point forecasts**, but as **mechanism‑level diagnostics**.

---

## 4. Structural vs Approximation‑Dependent Results

A key distinction throughout this project is between:

- **Structural results**, which arise from protocol design and persist under perturbations, and
- **Approximation‑dependent results**, which may change once frictions are introduced.

The following findings are expected to be **structural**:

- boundary‑driven convexity in liquidation risk,
- nonlinear sensitivity to distance from the liquidation threshold,
- activation of risk under volatility stress.

The following aspects are **approximation‑dependent**:

- exact liquidation timing,
- magnitude of liquidation probabilities,
- shape of hazard rates and time profiles.

---

## 5. Extension Strategy

Rather than replacing the baseline model, Week 2 introduces **incremental layers** that relax specific assumptions:

- Day 2: discrete oracle observation and delayed boundary detection,
- Day 3: incentive‑filtered liquidation rules,
- Day 4: multi‑agent cascades and market impact,
- Day 6: protocol‑level aggregation via GHO dynamics.

Each extension is designed to test whether the **structural convexity result survives contact with reality**, and to identify the conditions under which it amplifies into systemic risk.

---

## 6. Interpretation Guidance

Results from the baseline model should be interpreted as answers to the question:

> *What does the liquidation rule itself imply, before frictions are introduced?*

Subsequent extensions answer:

> *How does this structural risk interact with real‑world delays, incentives, and feedback loops?*

This layered approach ensures that conclusions about systemic risk are grounded in **mechanism design**, not in over‑fitted simulations.

---

## 7. Summary

The baseline model is intentionally stylized. Its value lies in isolating the **geometric and probabilistic structure** of Aave’s liquidation mechanism. By making its limitations explicit, we establish a clean reference point against which all subsequent frictions and extensions can be meaningfully evaluated.