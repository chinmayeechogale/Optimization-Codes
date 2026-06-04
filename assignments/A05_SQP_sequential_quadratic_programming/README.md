# Assignment 05 – Sequential Quadratic Programming (SQP)

## Problem Statement

Apply Sequential Quadratic Programming (SQP) via MATLAB's `fmincon` to minimize three benchmark functions: the Rosenbrock function (unimodal), the Eggcrate function (highly multimodal), and the Golinski speed reducer design problem (7-variable, 11 nonlinear constraints). Ten random starting points are used per problem to assess robustness.

## Methods Used

- **SQP via `fmincon`** (MATLAB) with `Algorithm = 'sqp'`
- **Multi-start strategy** — 10 random starting points per problem using `rng(683)` for reproducibility
- **Constraint handling** — bound constraints for P1/P2; nonlinear inequality constraints for P3 speed reducer
- **Convergence tracking** — custom `OutputFcn` to record iteration history and path

## Problems Solved

| File | Problem | Result |
|------|---------|--------|
| `A05_P1_SQP_rosenbrock.m` | Minimize Rosenbrock f(x) = 100(x2-x1²)² + (1-x1)², bounds [-5,5]² | Robust: all 10 runs converge to (1,1) |
| `A05_P2_SQP_eggcrate.m` | Minimize f(x) = x1²+x2²+25(sin²x1+sin²x2), bounds [-2π,2π]² | Not robust: multimodal, multiple local minima found |
| `A05_P3_SQP_speed_reducer.m` | 7-variable speed reducer with 11 nonlinear constraints | Highly robust: all 10 runs → (3.5, 0.7, 17, 7.3, 7.72, 3.35, 5.29), f≈2994.5 |

## Key Skills Demonstrated

- Understanding of SQP as a gradient-based constrained optimizer.
- Multi-start robustness analysis: SQP is robust for convex/well-conditioned problems but sensitive to starting points for nonconvex multimodal functions.
- Comparison of SQP (Assignment 05) vs PSO (Assignment 03) on the same speed reducer benchmark: SQP converges in 4–5 iterations vs PSO's 10 iterations.

## How to Run

Open any `.m` file in MATLAB and press **Run**. Requires the Optimization Toolbox (`fmincon`).
