import numpy as np

lb = np.array([65,  1,  0,  695000, 225, 815], dtype=float)
ub = np.array([95,  5,  4,  725000, 245, 855], dtype=float)
x0 = np.array([80,  3,  2,  710000, 235, 835], dtype=float)

RHO = 1e6  # penalty factor

# Regression coefficients for x4 in Kcal/h (from linear regression on dataset)
# multiplied by 1000 inside constraints() to convert Mcal/h → Kcal/h.
_C_NPHR_x4 = 0.0000017270   # × 1000 → 0.001727 per Mcal/h
_C_NTHR_x4 = 0.0000016350   # × 1000 → 0.001635 per Mcal/h
_C_HHV_x4  = 0.0000027310   # × 1000 → 0.002731 per Mcal/h


def objective(x):
    x1, x2, x3, x4, x5, x6 = x
    return 1e-3 * (-0.0686*x1 + 0.2146*x2 - 0.3432*x3 + 0.4996*x5 + 0.4639*x6)


def constraints(x):
    x1, x2, x3, x4, x5, x6 = x
    x4_kcal = x4 * 1000  # convert Mcal/h → Kcal/h for regression coefficients
    G1 = 0.2598*x1 + 0.3361*x2 + 0.2394*x3 + _C_NPHR_x4*x4_kcal + 1.1498*x5 + 1.4238*x6 - 2750
    G2 = 0.2379*x1 + 0.2909*x2 + 0.3460*x3 + _C_NTHR_x4*x4_kcal + 1.0487*x5 + 1.3266*x6 - 2600
    G3 = 4240 - (0.3817*x1 + 0.3432*x2 + 0.2709*x3 + _C_HHV_x4*x4_kcal + 1.7837*x5 + 2.2291*x6)
    return G1, G2, G3


def penalized_objective(x):
    J = objective(x)
    G1, G2, G3 = constraints(x)
    # bound violations
    g_lb = np.maximum(0, lb - x)
    g_ub = np.maximum(0, x - ub)
    penalty = RHO * (max(0, G1)**2 + max(0, G2)**2 + max(0, G3)**2
                     + np.sum(g_lb**2) + np.sum(g_ub**2))
    return J + penalty


#PSO
def run_pso(n_particles=120, max_iter=300, tol=1e-8,
            w=0.7, c1=1.5, c2=1.5, seed=42):
    rng = np.random.default_rng(seed)
    n_var = len(lb)

    # initialise swarm: seed 12 particles from x0, rest random
    pos = rng.uniform(lb, ub, size=(n_particles, n_var))
    pos[:12] = x0

    vel = rng.uniform(-(ub - lb), (ub - lb), size=(n_particles, n_var))

    pbest_pos = pos.copy()
    pbest_val = np.array([penalized_objective(p) for p in pos])

    gbest_idx = np.argmin(pbest_val)
    gbest_pos = pbest_pos[gbest_idx].copy()
    gbest_val = pbest_val[gbest_idx]

    print(f"\nRunning PSO — {n_particles} particles, {max_iter} max iterations\n")

    prev_best = np.inf
    for it in range(1, max_iter + 1):
        r1 = rng.random((n_particles, n_var))
        r2 = rng.random((n_particles, n_var))

        vel = (w * vel
               + c1 * r1 * (pbest_pos - pos)
               + c2 * r2 * (gbest_pos - pos))

        pos = np.clip(pos + vel, lb, ub)

        vals = np.array([penalized_objective(p) for p in pos])

        improved = vals < pbest_val
        pbest_pos[improved] = pos[improved]
        pbest_val[improved] = vals[improved]

        new_best_idx = np.argmin(pbest_val)
        if pbest_val[new_best_idx] < gbest_val:
            gbest_val = pbest_val[new_best_idx]
            gbest_pos = pbest_pos[new_best_idx].copy()
        if abs(prev_best - gbest_val) < tol and it > 10:
            print(f"\nConverged at iteration {it} (delta < {tol})")
            break
        prev_best = gbest_val

    return gbest_pos, gbest_val

if __name__ == "__main__":
    xbest, fbest = run_pso()

    x1, x2, x3, x4, x5, x6 = xbest
    J = objective(xbest)
    G1, G2, G3 = constraints(xbest)
    penalty = fbest - J

    NPHR = G1 + 2750
    NTHR = G2 + 2600
    HHV  = 4240 - G3

    is_feasible = (G1 <= 0) and (G2 <= 0) and (G3 <= 0)

    print("Results:")
    print(f"x1  (SH spray flow)        = {x1:.6f}  t/h")
    print(f"x2  (RH spray flow)        = {x2:.6f}  t/h")
    print(f"x3  (APH leakage)          = {x3:.6f}  %")
    print(f"x4  (Boiler energy input)  = {x4:.2f}  Mcal/h  ({x4*1000:.0f} Kcal/h)")
    print(f"x5  (Feedwater temp)       = {x5:.6f}  °C")
    print(f"x6  (Feedwater flow)       = {x6:.6f}  t/h")
    print(f"\nObjective  J(x)            = {J:.8f}")
    print(f"Penalty term               = {penalty:.8f}")
    print(f"Penalized objective        = {fbest:.8f}")
    print("\n")
    print("Constraint Values")
    print("\n")
    print(f"G1 = {G1:.8f}   (must be <= 0)")
    print(f"G2 = {G2:.8f}   (must be <= 0)")
    print(f"G3 = {G3:.8f}   (must be <= 0)")

    print(f"NPHR = {NPHR:.6f}   (must be <= 2750 kcal/kWh)")
    print(f"NTHR = {NTHR:.6f}   (must be <= 2600 kcal/kWh)")
    print(f"HHV  = {HHV:.6f}   (must be >= 4240 kcal/kg)")
    print(f"\nFeasible solution? {'Yes' if is_feasible else 'No'}")
