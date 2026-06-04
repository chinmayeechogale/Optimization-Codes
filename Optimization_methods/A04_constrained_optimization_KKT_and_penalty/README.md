# Constrained Optimization: KKT Conditions & Penalty Methods

## Problem Statement

Solve constrained optimization problems using KKT conditions, reduced-variable formulations, and penalty/barrier methods. Problems include a geometry-based design problem reduced to 1D, derivative approximation comparison, and a multi-case KKT active-set analysis.

## Methods Used

- **Variable reduction** — Eliminate equality constraints algebraically to convert a constrained multi-variable problem into a 1D unconstrained problem; solve with `fminbnd`.
- **Penalty method** — Apply external quadratic penalty for inequality constraints; compare penalty-method solution to reduced-variable solution using `fminsearch`.
- **Derivative approximation** — Compare forward difference, central difference, and complex-step methods for numerical gradient accuracy.
- **KKT case analysis** — Enumerate all possible active-set combinations for a 2-variable problem with 3 constraints; analytically solve each case and verify KKT conditions (stationarity, primal feasibility, dual feasibility, complementary slackness).
- **Reduced KKT system** — Use `fsolve` to solve the nonlinear KKT system directly for a constrained optimization problem.

## Key Skills Demonstrated

- Formulating and solving constrained optimization using KKT necessary conditions.
- Distinguishing between active and inactive constraints and verifying valid Lagrange multipliers.
- Comparing numerical differentiation methods in terms of accuracy and computational cost.
- Penalty-method convergence behavior as penalty parameter μ increases.

## Files

| File | Description |
|------|-------------|
| `A04_P1_reduced_unconstrained_geometry.m` | Reduce geometry problem to 1D, solve with fminbnd and penalty + fminsearch |
| `A04_P2_derivative_approximation.m` | Compare forward, central, and complex-step finite differences |
| `A04_P3_KKT_case_analysis.m` | Enumerate and verify KKT conditions across all active-set cases |
| `A04_P4_KKT_fsolve.m` | Solve KKT system numerically using fsolve |

## How to Run

Open any `.m` file in MATLAB and press **Run**. No additional toolboxes required.
