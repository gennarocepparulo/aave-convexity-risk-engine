# Aave Convexity & Liquidation Risk Engine

## 1. Motivation
From AMM convexity to credit risk convexity.
Why Aave is a natural next step in DeFi mechanism research.

## 2. Core Question
Is Aave’s lending system structurally exposed to nonlinear liquidation risk under volatility and leverage?

## 3. Why Aave?
- Overcollateralized lending
- Health Factor as the key state variable
- Liquidation thresholds
- Utilization-based borrow dynamics
- Risk controls: E-Mode, Isolation Mode, caps

## 4. Key Contributions
- stochastic model of Health Factor dynamics
- Monte Carlo liquidation engine
- distributional analysis of liquidation timing and severity
- convexity interpretation of leverage and liquidation thresholds

## 5. Methodology
- collateral price process
- debt process
- simulation design
- assumptions and simplifications
- first-passage liquidation detection

## 6. Early Results
- liquidation probability vs volatility
- time-to-liquidation distribution
- tail behavior under stressed regimes

## 7. Connection to Previous Work
This project extends the "DeFi Convexity Risk Engine":
- Uniswap → convexity via impermanent loss / inventory exposure
- Aave → convexity via leverage and liquidation thresholds

## 8. Roadmap
- baseline HF simulation
- distributional analysis
- stress scenarios
- protocol-level extensions

## 9. Future Work
- GHO module
- endogenous liquidations
- liquidation cascades
- market impact
- protocol-level bad debt / Umbrella layer
