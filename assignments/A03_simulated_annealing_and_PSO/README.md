# Simulated Annealing & Particle Swarm Optimization

## Problem Statement

Minimize nonconvex functions with bound constraints using simulated annealing; then solve a 7-variable constrained speed reducer design problem using Particle Swarm Optimization (PSO) with a quadratic penalty for 11 nonlinear constraints.

## Methods Used

- **Simulated Annealing (SA)**
  - Temperature initialized from sampled uphill moves to set acceptance probability.
  - Probabilistic acceptance of worse solutions to escape local minima.
  - Bound-constrained variable handling via reflection/rejection.
  - Convergence monitored over iterations with objective history plots.

- **Particle Swarm Optimization (PSO)**
  - Swarm size: 50 particles, 10 iterations.
  - Each particle updates velocity and position using personal best and global best.
  - Quadratic penalty term added to objective to handle 11 nonlinear constraints.
  - Applied to the classic 7-variable speed reducer design benchmark.

## Key Skills Demonstrated

- Implementation of population-based and trajectory-based metaheuristics from scratch.
- Understanding of exploration vs. exploitation trade-off in SA and PSO.
- Constraint handling via external penalty method in heuristic optimization.
- Convergence analysis and discussion of sensitivity to algorithm parameters.

## Files

| File | Description |
|------|-------------|
| `A03_P1_simulated_annealing_quadratic.m` | SA applied to a quadratic function with bound constraints |
| `A03_P2_simulated_annealing_nonconvex.m` | SA on a nonconvex trigonometric/polynomial function |
| `A03_P3_PSO_speed_reducer.m` | PSO for 7-variable speed reducer design with 11 constraints |

## How to Run

Open any `.m` file in MATLAB and press **Run**. No additional toolboxes required.
