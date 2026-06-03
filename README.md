# Optimization Codes

MATLAB implementations of gradient-based, heuristic, and multi-objective optimization methods — plus a surrogate-based power plant emission minimization project.

---

## Highlights

- **Classical methods:** Gradient & Hessian computation, conjugate directions, KKT conditions, penalty & barrier methods.
- **Heuristics:** Simulated annealing and Particle Swarm Optimization (PSO) with bounded variables and penalty-based constraint handling.
- **Engineering application:** Surrogate-based optimization for emission reduction in a coal-fired power plant, including sensitivity analysis and Pareto-front generation via Normal Boundary Intersection (NBI).

---

## Repository Structure

```
Optimization-Codes/
|
|-- assignments/                          # Coursework assignments (MATLAB)
|   |-- A02_gradient_hessian_conjugate_directions/   # Gradient, Hessian, conjugate directions, penalty methods
|   |-- A03_simulated_annealing_and_PSO/             # Simulated annealing & PSO for constrained design
|   |-- A04_constrained_optimization_KKT_and_penalty/ # KKT conditions, reduced systems, penalty methods
|
|-- power-plant-emission-optimization/    # Capstone project: coal plant emission minimization
    |-- data/                             # Dataset instructions (Kaggle source)
    |-- surrogate_models/                 # Regression-based surrogate model scripts
    |-- single_objective/                 # SD, CG, PSO, SQP implementations
    |-- multi_objective/                  # NBI Pareto-front generation
    |-- plots/                            # Convergence histories, Pareto front, sensitivity plots
    |-- report/                           # Final project report (PDF)
```

---

## Tech Stack

- **MATLAB** — Core algorithm implementations, plotting, and surrogate model fitting
- **Python** — PSO implementation (NumPy-based) and NBI multi-objective optimization

---

## Industry Relevance

The methods implemented here are directly applicable to real-world engineering design and energy systems problems. The PSO-based speed reducer design problem (Assignment 03) mirrors industrial mechanical design optimization, while the power plant emission project demonstrates end-to-end applied optimization: data-driven surrogate modeling, multi-variable constrained minimization, sensitivity analysis, and multi-objective trade-off analysis. These are core skills sought in roles involving simulation-based design, process optimization, and sustainable energy systems.

---

## How to Run

- **MATLAB assignments:** Open the `.m` file in MATLAB and run directly. No additional toolboxes required unless noted in the folder README.
- **Python scripts (power plant project):** Requires Python 3.x with `numpy` and `scipy`. Run `pip install numpy scipy` if needed.
- See the `README.md` inside each folder for problem-specific instructions.

---

## Author

**Chinmayee Chogale**  
Graduate Student — Optimization & Engineering Design  
[GitHub](https://github.com/chinmayeechogale)
