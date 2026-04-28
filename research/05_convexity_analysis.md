
## Liquidation Risk as Boundary‑Driven Convexity

### 5.1 From Volatility to Distance‑to‑Boundary

Results from Day 4 showed that, for positions with moderate leverage, liquidation probability increases smoothly with volatility. In isolation, volatility does not generate dramatic nonlinear behavior. This observation motivates a more precise question:

> Where does convexity in Aave liquidation risk actually originate?

The answer lies not primarily in volatility, but in **distance to the liquidation boundary**, as measured by the initial Health Factor \( HF_0 \).

In Aave, solvency is enforced through a hard threshold:
\[
HF_t < 1 \quad \Rightarrow \quad \text{position becomes liquidatable}.
\]
This creates a **state‑dependent nonlinearity**: far from the boundary, shocks have limited effect; near the boundary, the same shocks produce disproportionately large changes in liquidation risk.

---

### 5.2 Sensitivity of Liquidation Probability to Initial Health Factor

To make this mechanism explicit, we study the sensitivity of liquidation probability with respect to the initial Health Factor:
\[
\frac{\partial}{\partial HF_0} \; P(\tau \le T \mid \sigma).
\]

Figure *Sensitivity dP/dHF₀* reports this derivative across a range of \( HF_0 \) values and volatility regimes.

**Key observations:**

- **Far from the boundary (high \( HF_0 \))**  
  The sensitivity is close to zero across all volatility levels. Well‑collateralized positions are largely insensitive to marginal changes in leverage.

- **Approaching the boundary**  
  As \( HF_0 \) decreases toward 1, the sensitivity becomes increasingly negative. Small reductions in initial Health Factor produce increasingly large increases in liquidation probability.

- **Near the boundary ( \( HF_0 \approx 1 \) )**  
  As HF0→1, the sensitivity of liquidation probability increases sharply in magnitude, indicating a boundary-driven amplification of risk. This behavior reflects the first-passage nature of liquidation: near the boundary, small changes in initial conditions dramatically alter the probability of crossing the threshold.

This behavior is consistent across volatility regimes, though volatility determines how early this convex region becomes active.

---

### 5.3 Role of Volatility: Activation, Not Origin, of Convexity

Volatility modulates the activation region of this nonlinearity rather than its structural origin. In low-volatility regimes, liquidation risk is tightly concentrated near the boundary, leading to a sharp transition in sensitivity. In high-volatility regimes, stochastic fluctuations dominate, smoothing the transition and reducing the apparent steepness of the response.

- **Low volatility regimes**  
  Risk is concentrated very close to the boundary. Positions appear safe until they approach \( HF = 1 \), at which point liquidation sensitivity increases abruptly.

- **High volatility regimes**  
  Risk is distributed over a wider range of \( HF_0 \). Sensitivity is negative even far from the boundary, but the relative acceleration near \( HF = 1 \) is less extreme.

This implies that volatility determines **where** convexity becomes relevant, while leverage determines **how strong** convexity is.

---

### 5.4 Interpretation: Convexity as a Credit‑Risk Phenomenon

The convexity observed here is fundamentally different from payoff convexity in derivative markets.

In Aave:
- Convexity does not arise from nonlinear payoffs,
- but from **threshold‑based solvency enforcement**.

Liquidation is a **discrete event**, triggered by a continuous stochastic process crossing a boundary. As a result:
- risk is negligible far from the boundary,
- but increases nonlinearly as the boundary is approached.

This is characteristic of **credit‑risk convexity**, where default probability responds sharply to changes in leverage near solvency limits.

---

### 5.5 Connection to AMM Convexity

This framework provides a clean conceptual bridge to previous work on AMM liquidity provision:

| AMM Liquidity Provision | Aave Lending |
|------------------------|-------------|
| Convexity in payoff function | Convexity in event probability |
| Continuous losses via price moves | Discrete liquidation events |
| Short gamma everywhere | Short gamma near solvency boundary |
| Volatility drives curvature | Distance‑to‑boundary drives curvature |

In both systems, nonlinear risk arises not from volatility alone, but from **mechanism design**: invariants in AMMs and thresholds in lending protocols.

---

### 5.6 Implications for Protocol Design and Risk Management

These results highlight why Aave’s risk framework focuses on:
- conservative liquidation thresholds,
- caps on leverage,
- strong discouragement of positions near \( HF = 1 \).

From a risk‑management perspective, controlling **distance to boundary** is more effective than reacting to volatility ex post. Small parameter changes near the threshold can have outsized effects on system stability.

---

### 5.7 Summary

This analysis demonstrates that:
- liquidation risk in Aave is **convex in leverage**, not in volatility alone;
- the dominant nonlinear driver is proximity to the liquidation boundary;
- volatility acts as an amplifier, but not the source, of convexity.

Liquidation in Aave is therefore best understood as a **boundary‑driven, path‑dependent credit‑risk process**, rather than a linear accumulation of market risk.

This completes the convexity analysis layer of the project.