
import numpy as np

# Bounds
lb = np.array([65,   1,  0,  695_000, 225, 815], dtype=float)
ub = np.array([95,   5,  4,  725_000, 245, 855], dtype=float)

# Starting point (midpoint of bounds) 
X = np.array([80.0, 3.0, 2.0, 710_000.0, 235.0, 835.0])

# Objective (x4 has zero emission coefficient at Mcal/h scale) 
# J = 1e-3 * (-0.0686*X1 + 0.2146*X2 - 0.3432*X3 + 0.0*X4 + 0.4996*X5 + 0.4639*X6)
c_J = 1e-3 * np.array([-0.0686, 0.2146, -0.3432, 0.0, 0.4996, 0.4639])

def J_fun(X):
    return c_J @ X

# Pre-multiplied by 1000 for Mcal/h: 0.001727, 0.001635, 0.002731
def G1(X):
#NPHR(x) - 2750 <= 0
    return (0.2598*X[0] + 0.3361*X[1] + 0.2394*X[2]
            + 0.001727*X[3] + 1.1498*X[4] + 1.4238*X[5] - 2750)

def G2(X):
#NTHR(x) - 2600 <= 0
    return (0.2379*X[0] + 0.2909*X[1] + 0.3460*X[2]
            + 0.001635*X[3] + 1.0487*X[4] + 1.3266*X[5] - 2600)

def G3(X):
#4240 - HHV(x) <= 0
    return 4240 - (0.3817*X[0] + 0.3432*X[1] + 0.2709*X[2]
                   + 0.002731*X[3] + 1.7837*X[4] + 2.2291*X[5])

# Penalty formula 
R = 100

def pen(G):
    return 0.5 * (G + abs(G)) ** 2

def PHI(X):
    return J_fun(X) + R * (pen(G1(X)) + pen(G2(X)) + pen(G3(X)))

# Gradient of PHI (central finite difference)
def grad_PHI(X, h=1e-6):
    g = np.zeros(len(X))
    for i in range(len(X)):
        Xp = X.copy(); Xp[i] += h
        Xm = X.copy(); Xm[i] -= h
        g[i] = (PHI(Xp) - PHI(Xm)) / (2 * h)
    return g

# Optimization parameters 
ITERMAX = 50
TOL     = 1e-6
alpha0  = 1e-2   # NOTE: too small for gradient scale ~1e-3 -> converges at x0
beta    = 0.5
c       = 1e-4



for K in range(1, ITERMAX + 1):
    PHI_curr    = PHI(X)
    J_curr      = J_fun(X)
    DELPHI_curr = grad_PHI(X)

    d = -DELPHI_curr   # steepest descent direction

    # Armijo backtracking
    alpha = alpha0
    while True:
        X_trial = np.clip(X + alpha * d, lb, ub)
        if PHI(X_trial) <= PHI_curr + c * alpha * (DELPHI_curr @ d):
            break
        alpha *= beta
        if alpha < 1e-10:
            break

    X_new = X_trial
    ERR   = np.linalg.norm(X_new - X) ** 2

    if ERR <= TOL:
        X = X_new
        break

    X = X_new

# Results
X1, X2, X3, X4, X5, X6 = X
J_opt  = J_fun(X)
NPHR   = G1(X) + 2750
NTHR   = G2(X) + 2600
HHV    = 4240 - G3(X)
g1, g2, g3 = G1(X), G2(X), G3(X)
feasible = (g1 <= 0) and (g2 <= 0) and (g3 <= 0)


print("SD Result:")
print("\n")
print(f"X1  SH spray flow    (t/h)    = {X1:.4f}")
print(f"X2  RH spray flow    (t/h)    = {X2:.4f}")
print(f"X3  APH leakage      (%)      = {X3:.4f}")
print(f"X4  Boiler energy    (Mcal/h) = {X4:.2f}")
print(f"X5  Feedwater temp   (F)      = {X5:.4f}")
print(f"X6  Feedwater flow   (t/h)    = {X6:.4f}")
print(f"\nJ(x*) = {J_opt:.8f}")
print(f"\nNPHR = {NPHR:.4f}  (limit <= 2750)  {'FEASIBLE' if g1 <= 0 else 'VIOLATED'}")
print(f"NTHR = {NTHR:.4f}  (limit <= 2600)  {'FEASIBLE' if g2 <= 0 else 'VIOLATED'}")
print(f"HHV  = {HHV:.4f}  (limit >= 4240)  {'FEASIBLE' if g3 <= 0 else 'VIOLATED'}")
print(f"\nFeasible? {'Yes' if feasible else 'No'}")

# Individual emission predictions at optimum - Coefficient for X4 is 0
SO2  =  0.0781*X1 - 0.0227*X2 + 0.0558*X3 + 0.2032*X5 + 0.2227*X6
NOx  =  0.0200*X1 - 0.2224*X2 + 0.1160*X3 + 0.0468*X5 + 0.0995*X6
CO   = -0.1304*X1 + 0.5578*X2 - 0.4485*X3 + 0.2450*X5 + 0.1042*X6
CO2  =  9.6570*X1 + 10.2390*X2 + 6.3627*X3 + 39.7455*X5 + 50.9580*X6
Dust = -0.0042*X1 - 0.0052*X2 - 0.0151*X3 + 0.0040*X5 + 0.0044*X6

print("\nEmissions at optimal point:")
print(f"  SO2  = {SO2:.4f}  mg/m3")
print(f"  NOx  = {NOx:.4f}  mg/m3")
print(f"  CO   = {CO:.4f}  mg/m3")
print(f"  CO2  = {CO2:.4f}  ppm")
print(f"  Dust = {Dust:.4f}  mg/m3")
