## 1-Page System Map
Project framing
This project studies Aave as a threshold-based credit system: users supply collateral, borrow against it, and are kept solvent through a Health Factor mechanism that determines when positions become eligible for liquidation. In Aave v3, risk is managed through overcollateralization, reserve-specific risk parameters, and utilization-based interest-rate dynamics. [raw.github...ontent.com], [aave.com], [aave.com]

## 1) Actors
Suppliers / Liquidity Providers
Suppliers deposit assets into Aave and receive aTokens, whose balances grow over time from borrowing activity in the pool. Their role is to provide the liquidity that borrowers draw from. [raw.github...ontent.com]
Borrowers
Borrowers post collateral and take out loans against it. Their positions are always intended to remain overcollateralized, and their solvency is monitored through the Health Factor. [raw.github...ontent.com], [aave.com]
Liquidators
When a borrower’s Health Factor falls below 1, external liquidators can repay part of the borrower’s debt and receive collateral at a discount via the liquidation bonus. This is the core stabilization mechanism that keeps the protocol solvent at the user-position level. [raw.github...ontent.com], [aave.com]
Governance / Risk Stewards
Aave Governance and its delegated stewards set or adjust key parameters such as LTVs, liquidation thresholds, reserve factors, supply caps, borrow caps, and asset-specific risk configurations. Governance also defines frameworks for asset onboarding and rapid cap updates. [docs.gho.xyz], [aave.com]
Oracle Layer
Aave relies on oracle inputs to value collateral and debt. Because Health Factor depends on these valuations, oracle integrity is part of the protocol’s risk architecture. [github.com], [aave.com]

## 2) State Variables
Collateral Value CtC_tCt​
The market value of the borrower’s posted collateral changes over time as the underlying asset price moves. This is the key stochastic driver in the Week 1 model. [raw.github...ontent.com], [aave.com]
Debt Value DtD_tDt​
The borrower’s outstanding debt evolves through the borrowed amount and accrued interest. In the simplest first model, debt can be treated as deterministic or slowly growing; later versions can make it rate-dependent. [raw.github...ontent.com]
Liquidation Threshold LTLTLT
Each collateral asset has a governance-defined liquidation threshold that determines how much of the collateral value counts toward solvency before liquidation becomes possible. [aave.com], [aave.com]
Health Factor HFtHF_tHFt​
The Health Factor is the core solvency state variable. In Aave, positions become eligible for liquidation when HF < 1. A stylized representation is:
HFt=Ct⋅LTDtHF_t = \frac{C_t \cdot LT}{D_t}HFt​=Dt​Ct​⋅LT​
This is the central object of the simulation engine. [raw.github...ontent.com], [aave.com]
Utilization UtU_tUt​
At the reserve level, utilization measures how much liquidity is borrowed relative to available liquidity. Borrow rates rise as utilization increases, with Aave v3 using a two-slope interest-rate model around an optimal utilization point. [raw.github...ontent.com]
Volatility σt\sigma_tσt​
For this project, volatility is the main driver of collateral-path uncertainty. It is not itself an on-chain Aave parameter, but it is the key stochastic input in the liquidation-risk model.
First Liquidation Time τ\tauτ
The first time at which the simulated Health Factor falls below 1 defines the liquidation event timing:
τ=inf⁡{t≥0:HFt<1}\tau = \inf \{ t \ge 0 : HF_t < 1 \}τ=inf{t≥0:HFt​<1}
This turns liquidation into a first-passage problem, which is the right probabilistic lens for Week 1.

## 3) Control Parameters
Loan-to-Value (LTV)
LTV determines how much a user can initially borrow against posted collateral. It affects how levered the position is at entry. [aave.com], [aave.com]
Liquidation Threshold
The liquidation threshold determines when a position becomes unsafe enough to be liquidated. It is closely related to, but distinct from, the initial LTV. [aave.com], [aave.com]
Liquidation Bonus
The liquidation bonus is the discount granted to liquidators on collateral when they repay debt. It is designed to incentivize timely liquidation. [raw.github...ontent.com], [aave.com]
Reserve Factor
The reserve factor diverts a portion of borrower interest away from suppliers and toward the protocol treasury. It matters more for protocol economics than for the Week 1 user-level liquidation model, but it is part of the system map. [raw.github...ontent.com], [deepwiki.com]
Supply Caps / Borrow Caps
Aave v3 uses supply caps and borrow caps to limit exposure to specific assets and reduce the system-wide impact of risky or thin-liquidity reserves. [aave.com], [raw.github...ontent.com]
E-Mode
Efficiency Mode increases capital efficiency for correlated assets by allowing higher borrowing power in tightly related asset categories, such as stablecoins. [raw.github...ontent.com]
Isolation Mode / Siloed Borrowing
These mechanisms allow riskier assets to be onboarded while containing their systemic impact through debt ceilings and tighter borrowing constraints. [raw.github...ontent.com], [aave.com]
Interest-Rate Curve Parameters
Aave v3 borrow rates respond to utilization through a piecewise structure with a base rate and two slopes around an optimal usage point. For Week 1, these dynamics can be simplified or frozen. [raw.github...ontent.com]

## 4) Failure Modes
User-Level Liquidation
The most direct failure mode is the borrower crossing the liquidation boundary: if collateral value falls or debt grows enough that HF < 1, the position becomes liquidatable. [raw.github...ontent.com], [aave.com]
Gap / Volatility Risk
A large or sudden move in collateral price can push a position rapidly toward liquidation, especially when initial Health Factor is already low. In the project lens, this is where liquidation risk becomes strongly nonlinear.
Oracle Risk
If the oracle price is delayed, incorrect, or manipulated, collateral valuation can become distorted, affecting Health Factor and liquidation decisions. Oracle risk is explicitly identified as a protocol risk category. [github.com]
Collateral Liquidity Risk
If collateral loses liquidity or becomes hard to liquidate in stressed conditions, liquidation may become less effective, raising the risk of shortfall. Aave’s broader risk framework explicitly treats collateral quality and market liquidity as core concerns. [github.com], [aave.com]
Protocol Shortfall / Deficit
If liquidations are not sufficient to fully absorb debt during extreme conditions, deficits can emerge. Aave’s newer Umbrella system is specifically designed to automate bad-debt coverage through staked aTokens and GHO. [bkrem.github.io]
Network / Bridge Risk
Because Aave operates across multiple chains and infrastructures, network and bridge failures are also recognized as part of the broader protocol risk surface. [github.com], [docs.gho.xyz]

## 5) Core System Flow

Collateral is supplied into the protocol and valued through oracle-based pricing. [raw.github...ontent.com], [github.com]
Debt is borrowed against that collateral subject to governance-defined risk parameters. [raw.github...ontent.com], [aave.com]
Health Factor evolves as collateral prices move and debt accrues. [raw.github...ontent.com], [aave.com]
If HF remains above 1, the position survives; if HF falls below 1, the position becomes eligible for liquidation. [raw.github...ontent.com], [aave.com]
Liquidators intervene by repaying debt and seizing collateral with a bonus, restoring solvency if the liquidation process is effective. [raw.github...ontent.com], [aave.com]
Governance adjusts parameters over time to reduce systemic risk and maintain protocol resilience. [docs.gho.xyz], [aave.com]


## 6) Week 1 Modeling Scope
For Week 1, the project will focus on user-level liquidation risk, not full protocol insolvency. That means the baseline engine will treat:

collateral price as the main stochastic driver,
debt as deterministic or slowly accruing,
parameters as fixed,
and liquidation as the first time HF crosses below 1