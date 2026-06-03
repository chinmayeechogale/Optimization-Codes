# Power Plant Emission Optimization

## Project Overview

This project applies surrogate-based optimization to minimize emissions from a coal-fired power plant. Using 2022 historical operating data, regression models are built for five emission outputs and three process constraints. Multiple single-objective and multi-objective optimization methods are implemented and compared.

---

## Problem Formulation

**Objective:** Minimize a weighted sum of normalized emissions: SO₂, NOx, CO, CO₂, and dust.

**Design Variables (6):**
| Variable | Description |
|----------|-------------|
| x1 | Desuperheating water flow 1 |
| x2 | Desuperheating water flow 2 |
| x3 | APH leakage |
| x4 | Boiler energy |
| x5 | Feedwater temperature |
| x6 | Feedwater flow |

**Constraints:** NPHR ≤ upper bound, NTHR ≤ upper bound, HHV ≥ lower bound, plus variable bounds.

---

## Methods Implemented

### Surrogate Modeling
- Linear and quadratic regression models fitted from 2022 plant data.
- Models map design variables to: SO₂, NOx, CO, CO₂, dust, NPHR, NTHR, HHV.

### Single-Objective Optimization
| Method | Notes |
|--------|-------|
| Steepest Descent (SD) | Gradient-based, with line search |
| Conjugate Gradient (CG) | Normalized variables for better conditioning |
| Particle Swarm Optimization (PSO) | Python/MATLAB, swarm-based global search |
| Sequential Quadratic Programming (SQP) | MATLAB `fmincon` with analytical gradients |

- Constraints handled via external quadratic penalty and bound penalties.
- Starting point selected via one-factor-at-a-time DOE (3 levels per variable).

### Multi-Objective Optimization
- Objective 1: Normalized emissions (minimize)
- Objective 2: NPHR — plant heat rate efficiency (minimize)
- **Normal Boundary Intersection (NBI)** method used to generate a well-distributed Pareto front.

### Sensitivity Analysis
- Analytical and central-difference derivatives of objective and constraints w.r.t. each design variable.
- Identifies most influential variables and active constraints at optimum.

---

## Key Results

- **PSO** found the best single-objective solution: normalized emission ≈ **0.4839**, at a boundary point with active HHV constraint.
- **CG** (normalized variables) reached ≈ **0.4855**, with good feasibility.
- **Feedwater flow (x6) and feedwater temperature (x5)** are the most influential variables for the emission objective.
- **Boiler energy (x4)** primarily affects feasibility (HHV constraint) rather than emissions directly.
- **Multi-objective Pareto front** shows a clear trade-off between minimizing emissions and minimizing NPHR (improving plant efficiency).

---

## Repository Structure

```
power-plant-emission-optimization/
|-- data/                    # Dataset instructions (Kaggle source link)
|-- surrogate_models/        # Scripts to fit regression surrogate models
|-- single_objective/        # SD, CG, PSO, SQP optimization scripts
|-- multi_objective/         # NBI Pareto-front generation
|-- plots/                   # Convergence plots, Pareto front, sensitivity figures
|-- report/                  # Final project report PDF
```

---

## Tech Stack

- **MATLAB** — Surrogate modeling, SD, CG, SQP, NBI
- **Python** — PSO implementation using NumPy

---

## How to Run

1. Download data per instructions in `data/DATA_README.md`.
2. Run scripts in `surrogate_models/` to build regression models.
3. Run optimization scripts in `single_objective/` or `multi_objective/`.
4. Plots are saved to `plots/`.

---

## Why This Project Matters for Industry

This project demonstrates a complete optimization pipeline on a real engineering system:
- Data preprocessing and surrogate model building from historical plant data.
- Multi-variable constrained optimization using both gradient-based and heuristic methods.
- Multi-objective trade-off analysis relevant to sustainability and energy efficiency goals.
- Sensitivity analysis to identify critical design levers — directly applicable to process optimization roles in energy, chemical, and manufacturing industries.
