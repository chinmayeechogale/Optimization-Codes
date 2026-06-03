# Gradient, Hessian & Conjugate Directions

## Problem Statement

Implement and apply gradient and Hessian computations to analyze quadratic and nonlinear functions, verify orthogonality of conjugate directions, and explore penalty methods for single-constraint problems.

## Methods Used

- **Gradient & Hessian computation** — Analytical and numerical (finite difference) derivation for quadratic and nonlinear functions.
- **Conjugate directions** — Construction and verification that search directions are mutually conjugate (A-orthogonal) with respect to the Hessian matrix.
- **Penalty method** — Conversion of a constrained single-variable problem to an unconstrained one using an external quadratic penalty term; study of penalty parameter effect on convergence.

## Key Skills Demonstrated

- Computing and interpreting gradients and Hessians for optimization landscapes.
- Verifying that conjugate directions satisfy d_i^T * A * d_j = 0 (i ≠ j), which guarantees minimization of a quadratic in at most n steps.
- Understanding how the penalty parameter μ affects feasibility and objective trade-off.

## Files

| File | Description |
|------|-------------|
| `A02_P1_conjugate_directions_quadratic.m` | Gradient, Hessian, and conjugate direction verification for a quadratic function |
| `A02_P2_penalty_single_constraint.m` | Penalty method applied to a single-constraint 1D optimization problem |

## How to Run

Open any `.m` file in MATLAB and press **Run**. No additional toolboxes required.
