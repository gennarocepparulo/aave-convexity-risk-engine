# Mathematical Framework: Health Factor Dynamics and Liquidation Risk

## 1. Objective of the Model

This document formalizes a **minimal mathematical model** of liquidation risk in Aave v3, with the goal of isolating the **nonlinear (convex) relationship** between collateral price uncertainty, leverage, and liquidation events.

The model focuses on **user-level liquidation risk** and treats liquidation as a **first‑passage problem** of a stochastic process. Protocol-level feedback mechanisms (interest-rate endogeneity, cascading liquidations, bad-debt absorption) are explicitly deferred to later phases.

---

## 2. State Variables

We consider a single borrower position characterized by the following variables.

### 2.1 Collateral Price

Let  
\[
S_t
\]
denote the market price of the collateral asset at time \( t \).

### 2.2 Collateral Value

Let  
\[
C_t = q \cdot S_t
\]
denote the total collateral value, where \( q \) is the fixed quantity of collateral supplied.

### 2.3 Debt Value

Let  
\[
D_t
\]
denote the outstanding debt, including accrued interest.

In the baseline model, debt dynamics are treated as **deterministic or slowly varying** relative to collateral price movements.

### 2.4 Liquidation Threshold

Let  
\[
LT \in (0,1]
\]
denote the liquidation threshold parameter set by governance for the collateral asset.

### 2.5 Health Factor

The **Health Factor** is the central solvency metric and is defined as:
\[
HF_t = \frac{C_t \cdot LT}{D_t}
\]

A position becomes **eligible for liquidation** when:
\[
HF_t < 1
\]

---

## 3. Collateral Price Dynamics

### 3.1 Baseline Assumption

In Phase 1, collateral prices are modeled as a **geometric Brownian motion (GBM)**:
\[
dS_t = \mu S_t \, dt + \sigma S_t \, dW_t
\]

where:
- \( \mu \) is the drift,
- \( \sigma \) is the volatility,
- \( W_t \) is a standard Brownian motion.

In discrete time, this can be written as:
\[
S_{t+\Delta t} = S_t \exp\left((\mu - \tfrac12\sigma^2)\Delta t + \sigma \sqrt{\Delta t} Z_t\right),
\quad Z_t \sim \mathcal{N}(0,1)
\]

### 3.2 Rationale

GBM is chosen because:
- it is tractable and well understood,
- it isolates liquidation convexity from price‑process complexity,
- it provides a clean baseline extensible to jumps or stochastic volatility.

---

## 4. Debt Dynamics

### 4.1 Phase‑1 Assumption

In the baseline specification, debt is modeled as either:
\[
D_t = D_0
\]
or
\[
D_t = D_0 e^{r t}
\]

where \( r \) is a constant effective borrow rate.

### 4.2 Justification

Liquidation convexity exists even under **fixed debt**. Allowing endogenous interest-rate dynamics is unnecessary for identifying the core nonlinear effects and is deferred to later phases.

---

## 5. Liquidation as a Stopping Time

Liquidation is modeled as a **first‑passage event**.

Define the liquidation time:
\[
\tau = \inf \{ t \ge 0 : HF_t < 1 \}
\]

This formulation treats liquidation as:
- a boundary‑crossing event,
- not a continuous loss function,
- sensitive to both volatility and leverage.

---

## 6. Control Parameters

The following parameters are treated as **fixed inputs** that define a scenario:

- Initial loan‑to‑value (LTV)
- Initial Health Factor \( HF_0 \)
- Liquidation threshold \( LT \)
- Volatility \( \sigma \)
- Drift \( \mu \)
- Debt growth rate \( r \)

These parameters are varied across scenarios but are not stochastic.

---

## 7. Modeling Scope and Exclusions

To maintain clarity, the following elements are **excluded from Phase 1**:

- endogenous interest-rate feedback via utilization,
- strategic liquidator behavior,
- market impact during liquidation,
- oracle manipulation or latency,
- correlated multi‑asset positions,
- protocol‑level bad debt or safety modules.

The purpose of this phase is to establish a **clean baseline** for liquidation convexity.

---

## 8. Interpretation: Convexity in Aave

Convexity in this framework arises from the **threshold structure** of solvency.

When a position is well collateralized, small price fluctuations have limited effect on liquidation risk. As leverage increases and the Health Factor approaches 1, **marginal price shocks generate disproportionately large increases in liquidation probability**.

This produces:
- nonlinear liquidation probabilities,
- asymmetric outcome distributions,
- tail‑dominated risk profiles.

This mechanism is the **credit‑risk analogue** of convexity previously observed in AMM liquidity provision, where nonlinear payoffs arise from inventory exposure.

---

## 9. Link to Simulation

This framework directly motivates the Monte Carlo engine implemented in Phase 1:

- simulate collateral price paths,
- compute Health Factor paths,
- record first‑passage liquidation events,
- analyze the distribution of \( \tau \) across scenarios.

All subsequent numerical results are interpretations of this mathematical structure.