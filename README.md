# Aave Convexity & Liquidation Risk Engine

## A. Motivation
From AMM convexity to credit risk convexity.
Why Aave is a natural next step in DeFi mechanism research.

## B. Core Question
Is Aave’s lending system structurally exposed to nonlinear liquidation risk under volatility and leverage?

## C. Overcollateralized lending
- Health Factor as the key state variable
- Liquidation thresholds
- Utilization-based borrow dynamics
- Risk controls: E-Mode, Isolation Mode, caps

## D. Key Contributions
- stochastic model of Health Factor dynamics
- Monte Carlo liquidation engine
- distributional analysis of liquidation timing and severity
- convexity interpretation of leverage and liquidation thresholds

## E. Methodology
- collateral price process
- debt process
- simulation design
- assumptions and simplifications
- first-passage liquidation detection

## F. Early Results
- liquidation probability vs volatility
- time-to-liquidation distribution
- tail behavior under stressed regimes

## G. Connection to Previous Work
This project extends the "DeFi Convexity Risk Engine":
- Uniswap → convexity via impermanent loss / inventory exposure
- Aave → convexity via leverage and liquidation thresholds

## H. Roadmap
- baseline HF simulation
- distributional analysis
- stress scenarios
- protocol-level extensions

## I. Future Work
- GHO module
- endogenous liquidations
- liquidation cascades
- market impact
- protocol-level bad debt / Umbrella layer

# Aave Convexity & Liquidation Risk Engine

> **Key takeaway.** Liquidation risk in Aave is governed by a **nonlinear, boundary‑driven risk surface**. Leverage (distance to the Health Factor threshold) is the primary source of convexity; volatility acts as an **accelerator** that activates and front‑loads risk near the boundary.

---

## Abstract
This project studies liquidation risk in the Aave lending protocol through the lens of **convexity and threshold effects**. Using a Monte Carlo simulation framework, we show that liquidation risk is not linear in volatility or leverage. Instead, it emerges from a **state‑conditioned risk surface** driven by proximity to the liquidation boundary (Health Factor = 1). Volatility amplifies and accelerates this boundary‑driven convexity. The analysis unifies baseline dynamics, sensitivity measures, and stress scenarios into a single, interpretable risk surface.

---

## 1. Motivation
In AMM liquidity provision, convexity arises from payoff geometry (impermanent loss, short gamma). In DeFi credit protocols like Aave, convexity arises from **threshold‑based solvency rules**. Liquidation is a discrete event triggered when the Health Factor crosses a boundary, making risk **state‑dependent and nonlinear**.

**Research question.** *Where does convexity in Aave liquidation risk live, and how is it activated under market stress?*

---

## 2. System Model
A borrower position is characterized by stochastic collateral value and deterministic debt accumulation. The Health Factor is

$$HF_t = \frac{Q \cdot S_t \cdot LT}{B_t},$$

and liquidation occurs at the first time $HF_t < 1$. This formulation turns liquidation into a **first‑passage (stopping‑time) problem** rather than a linear loss process.

---

## 3. Methodology

### Simulation Engine
- Monte Carlo simulation of collateral price paths
- Deterministic debt evolution
- Pathwise computation of Health Factor
- Detection of first liquidation time

### Core Outputs
- Liquidation probability
- Time‑to‑liquidation distribution
- Survival curve $P(\tau > t)$
- Sensitivity of liquidation probability to initial Health Factor

All experiments vary **one dimension at a time** to isolate mechanisms.

---

## 4. Baseline Dynamics (Day 4)

### Figure 1 — Liquidation Probability vs Volatility
![Figure 1 — Liquidation Probability vs Volatility](figures/fig1_liquidation_probability_vs_volatility.png)

Liquidation probability increases with volatility, but the response is smooth away from the boundary. Volatility alone does not generate strong convexity.

---

### Figure 2 — Time‑to‑Liquidation Distribution
![Figure 2 — Time‑to‑Liquidation Distribution](figures/fig2_time_to_liquidation_distribution.png)

Conditional distribution of liquidation times shows **diffusion‑driven erosion**: failures are neither immediate nor purely terminal, indicating path dependence.

---

## 5. Convexity Insight Layer (Day 5)

### Figure 4 — Liquidation Probability vs Initial Health Factor
![Figure 4 — Liquidation Probability vs Initial Health Factor](figures/fig4_liquidation_probability_vs_HF0.png)


Holding volatility fixed, liquidation probability increases **convexly** as $HF_0$ approaches the boundary. Far from the boundary, leverage changes matter little; near it, small changes have large effects.

---

### Figure 6 — Sensitivity $dP/dHF_0$
![Figure 6 — Sensitivity vs Distance to Boundary](figures/fig6_sensitivity_vs_distance.png)

Local sensitivity reveals that convexity is **sharply concentrated near $HF=1$**. Volatility shifts where convexity activates but does not create it.

---

## 6. Stress Scenarios (Day 6)

### Scenario 1 — Volatility Spike
![Figure 7 — Volatility Spike Distribution Shift](figures/fig7_volatility_spike_distribution.png)

A volatility shock ($\sigma: 0.4 \rightarrow 1.0$) increases liquidation probability and **front‑loads failures**, shifting liquidation times earlier. Volatility acts as an **accelerator**.

---

### Scenario 2 — Health Factor Compression
![Figure 8 — Health Factor Compression Convexity](figures/fig8_hf_compression.png)

Compressing $HF_0$ ($2.0 \rightarrow 1.2$) at fixed volatility produces a **convex explosion** in liquidation probability, isolating boundary‑driven risk.

---

### Figure 5 — Liquidation Risk Surface (Core Result)
![Figure 5 — Liquidation Risk Surface](figures/fig5_liquidation_risk_surface.png)

**Axes:** x = initial Health Factor $HF_0$; y = volatility $\sigma$; color = liquidation probability.

This heatmap is the **core contribution**. Risk remains low in safe regimes, then increases sharply along a narrow transition band as leverage and volatility interact. The diagonal cliff visualizes **boundary‑driven convexity** and unifies all stress scenarios.

---

## 7. Interpretation

The results reveal that Aave liquidation risk is structurally analogous to a **distance-to-default problem**:

- The Health Factor acts as a **state variable measuring distance to the liquidation boundary**.
- Liquidation occurs as a **first-passage event**, not as a gradual loss process.
- Convexity emerges because the probability of boundary crossing is a **nonlinear function of distance**, not because of payoff curvature.

Volatility does not create convexity. Instead, it determines the **rate at which trajectories explore the state space**, thereby controlling how quickly positions approach the boundary.

This explains why:
- Risk appears negligible in well-collateralized regimes  
- Risk increases smoothly in intermediate regimes  
- Risk becomes highly sensitive near the boundary  

The system therefore exhibits a **phase-transition–like behavior**, where small changes in leverage or volatility can shift positions from a stable to a fragile regime.

---

## 8. Connection to Previous Work

| AMM Liquidity Provision | Aave Lending |
|---|---|
| Payoff convexity | Event‑probability convexity |
| Short gamma everywhere | Short gamma near boundary |
| Continuous losses | Discrete liquidation |

This project extends prior AMM convexity analysis to **DeFi credit risk**.

---

## 9. Supporting Diagnostics (Appendix)

### Figure 9 — Time‑Conditioned Hazard (Appendix)
![Figure 9 — Time‑Conditioned Hazard](figures/fig9_hazard_rate_time.png)

The time‑conditioned hazard confirms non‑memoryless behavior but is dominated by boundary effects. State‑conditioned measures provide clearer economic insight.

---

## 10. Reproducibility
Run the notebooks in order:
1. `01_system_model.ipynb`
2. `02_baseline_distributions.ipynb`
3. `03_convexity_analysis.ipynb`
4. `05_stress_scenarios.ipynb`

All figures are saved programmatically to `figures/`.

---
## 11. Implications for Protocol Design

The boundary-driven structure of liquidation risk has direct implications:

- **Risk is concentrated near the liquidation threshold**  
  → monitoring should focus on positions close to the boundary rather than system-wide averages

- **Volatility shocks are most dangerous when leverage is already high**  
  → systemic risk emerges from the interaction of market stress and user positioning

- **Liquidation thresholds implicitly define system fragility**  
  → small changes in parameters (LT, LTV) can significantly shift the fragility frontier

- **Static risk metrics are insufficient**  
  → risk must be evaluated conditionally on state (Health Factor), not only on exogenous variables
---

## Conclusion
Aave liquidation risk is governed by a **nonlinear, boundary‑driven risk surface**. Understanding this geometry is essential for protocol design, risk management, and governance. This project provides a compact simulation framework to visualize and reason about that surface.
# Systemic Liquidation Risk in Aave

> **TL;DR**  
> Liquidation risk in Aave is a *phase phenomenon*. Volatility shifts the regime boundary between efficient liquidation and systemic cascades, while liquidity constraints primarily alter *how* stress propagates rather than *where* regimes change. Protocol stability is therefore **state‑dependent**: parameters calibrated in calm markets may become insufficient under stress.

---

## 1. Motivation

Liquidations in DeFi lending protocols are often analyzed at the level of individual positions. However, protocol‑level failures emerge from *interactions*: execution frictions, price impact, and feedback loops that couple many positions through a shared market.

This project asks a focused question:

> **When do local liquidations turn into systemic cascades?**

We answer this by moving progressively from single‑position convexity to a minimal system‑level cascade model and by mapping the resulting **phase structure** under stress.

---

## 2. Core Mechanism

### 2.1 Boundary‑Driven Risk

Aave enforces solvency through a Health Factor (HF) threshold. Liquidation risk is therefore a **boundary‑crossing problem**, not a smooth loss process. This generates convexity: small price moves near the boundary produce large changes in liquidation risk.

---

### 2.2 Probabilistic Liquidation Execution

Instead of assuming mechanical execution when \(HF < 1\), liquidation is modeled as a **stochastic execution process**:

\[
\pi_{i,t}
=
\mathbf{1}_{\text{oracle active}}
\cdot
\sigma\!\left(\frac{\beta - \lambda Q S_t}{\varepsilon}\right)
\cdot
\sigma\!\left(\frac{1 - HF_{i,t}}{\delta}\right)
\]

where:
- \(\beta\) is the liquidation bonus,
- \(\lambda\) captures market impact,
- the first sigmoid models *economic profitability*,
- the second sigmoid models *agent‑specific urgency* (distance to the boundary).

Liquidation becomes a **Bernoulli event** conditioned on system state. This avoids degenerate hard constraints and allows execution frictions to matter.

---

## 3. From Single Positions to Cascades

A minimal feedback loop is introduced:

1. Some positions liquidate (probabilistically).
2. Liquidations sell collateral.
3. Selling depresses the market price.
4. Lower prices push other positions toward the HF boundary.

This loop is sufficient to generate **nonlinear amplification** and **system‑wide cascades**.

---

## 4. Phase Diagram: Existence of Cascades (Day 4)

We map the average cascade size as a function of:
- **x‑axis:** price impact \(\lambda\),
- **y‑axis:** liquidation bonus \(\beta\).

The result is a clear phase structure with three regimes:
- **Stable:** isolated liquidations, no propagation,
- **Fragile:** path‑dependent outcomes, large variance,
- **Collapse:** system‑wide liquidation cascades.

![Cascade Phase Diagram](figures/cascade.png)

**Figure 1 —** Cascade phase diagram showing the transition from stable to collapse regimes as a function of liquidation incentives and price impact.

---

## 5. Stress Testing the Phase Boundary (Day 5)

### 5.1 Volatility Stress

Increasing price volatility does **not** merely increase liquidation activity. It **shifts the critical phase boundary**:

- For a given \(\beta\), cascades occur at *lower* \(\lambda\).
- The entire instability region expands.

This shows that **protocol stability is state‑dependent**: parameters safe in calm markets may fail under volatility stress.

---

### 5.2 Liquidity Thinning

Liquidity constraints reduce execution probability. In this minimal model, liquidity stress:

- increases latent vulnerability (toxic positions linger),
- but dampens immediate propagation by suppressing execution.

As a result, liquidity stress mainly affects *dynamics and variance*, not the mean phase boundary.

---

### 5.3 Combined Stress: Non‑Additivity

Overlaying baseline, volatility stress, and combined volatility + liquidity stress yields a subtle but important result:

![Cascade Phase Boundary Under Stress](figures/overlay_test.png)

**Figure 2 —** Phase boundary under stress.  
White: baseline.  
Red: volatility stress.  
Orange: volatility + liquidity stress.

**Key observation:**
- Volatility alone shifts the boundary.
- Adding liquidity stress does *not* further shift it significantly.

This demonstrates **non‑additive stress interactions**: different stressors act on different components of the liquidation mechanism and can partially offset at the regime level, even though internal dynamics change substantially.

---

## 6. Interpretation and Design Implications

1. **Volatility is the dominant regime‑shifting stressor.**  
   It determines whether the system enters a fragile or collapse regime.

2. **Liquidity constraints are propagation modifiers.**  
   They affect timing, persistence, and uncertainty, rather than the location of regime boundaries.

3. **Boundary stability does not imply dynamic similarity.**  
   Similar phase boundaries can mask very different internal dynamics (fast cascades vs slow‑burn stress).

4. **Static calibration is insufficient.**  
   Liquidation parameters calibrated under normal conditions may be inadequate during stressed states.

---

## 7. Limitations and Extensions

This is a deliberately minimal model. It abstracts from:
- close‑factor mechanics (partial liquidation),
- credit constraints of flash‑loan‑based liquidators,
- protocol‑level feedbacks such as stablecoin (GHO) dynamics.

These features are important and can be layered on top, but the results here already show that **systemic risk emerges before full realism is added**.

---

## 8. Main Takeaway

> **Systemic liquidation risk in Aave is a phase phenomenon driven by boundary convexity and feedback. Volatility shifts regime boundaries, while liquidity shapes propagation. Protocol safety is therefore inherently state‑dependent.**

This framework provides a foundation for stress‑aware parameter design and for extending analysis to protocol‑level feedbacks.
``