import numpy as np
from scipy.optimize import minimize
# BOUNDS
lb = np.array([65,  1,  0,  695_000, 225, 815], dtype=float)
ub = np.array([95,  5,  4,  725_000, 245, 855], dtype=float)

# STARTING POINT
x0 = np.array([80,  3,  2,  710_000, 235, 835], dtype=float)

def normalize(x):
    return (x - lb) / (ub - lb)

def unnormalize(x_norm):
    return lb + x_norm * (ub - lb)

x0_norm = normalize(x0)

# J = 1e-3 * (-0.0686*X1 + 0.2146*X2 - 0.3432*X3 + 0*X4 + 0.4996*X5 + 0.4639*X6)
c_J = 1e-3 * np.array([-0.0686, 0.2146, -0.3432, 0.0, 0.4996, 0.4639])

def objective(x_norm):
    x = unnormalize(x_norm)
    return c_J @ x

def g1(x_norm):
#NPHR(x) - 2750 <= 0
    x = unnormalize(x_norm)
    return (0.2598*x[0] + 0.3361*x[1] + 0.2394*x[2] + 0.001727*x[3]
            + 1.1498*x[4] + 1.4238*x[5] - 2750)

def g2(x_norm):
#NTHR(x) - 2600 <= 
    x = unnormalize(x_norm)
    return (0.2379*x[0] + 0.2909*x[1] + 0.3460*x[2] + 0.001635*x[3]
            + 1.0487*x[4] + 1.3266*x[5] - 2600)

def g3(x_norm):
#4240 - HHV(x) <= 0
    x = unnormalize(x_norm)
    return 4240 - (0.3817*x[0] + 0.3432*x[1] + 0.2709*x[2] + 0.002731*x[3]
                   + 1.7837*x[4] + 2.2291*x[5])

#Penalty formula: R * (1/2)*(G + |G|)^2
R = 100    
RHO_BOUNDS = 1e6   
def pen(G):
    return 0.5 * (G + abs(G)) ** 2

def penalized_objective(x_norm):
    J  = objective(x_norm)
    cp = R * (pen(g1(x_norm)) + pen(g2(x_norm)) + pen(g3(x_norm)))
    bp = 0.5 * RHO_BOUNDS * (np.sum(np.maximum(0, -x_norm) ** 2)
                            + np.sum(np.maximum(0, x_norm - 1) ** 2))
    return J + cp + bp

# RUN CG
result = minimize(
    fun    = penalized_objective,
    x0     = x0_norm,
    method = 'CG',
    options= {'maxiter': 10000, 'gtol': 1e-6}
)

x_opt = unnormalize(result.x)
X1, X2, X3, X4, X5, X6 = x_opt

#Emissions at optimal point
SO2  =  0.0781*X1 - 0.0227*X2 + 0.0558*X3 + 0.2032*X5 + 0.2227*X6
NOx  =  0.0200*X1 - 0.2224*X2 + 0.1160*X3 + 0.0468*X5 + 0.0995*X6
CO   = -0.1304*X1 + 0.5578*X2 - 0.4485*X3 + 0.2450*X5 + 0.1042*X6
CO2  =  9.6570*X1 + 10.2390*X2 + 6.3627*X3 + 39.7455*X5 + 50.9580*X6
Dust = -0.0042*X1 - 0.0052*X2 - 0.0151*X3 + 0.0040*X5 + 0.0044*X6

print("Results:")
print(f"X1  SH spray flow    (t/h)    = {X1:.4f}")
print(f"X2  RH spray flow    (t/h)    = {X2:.4f}")
print(f"X3  APH leakage      (%)      = {X3:.4f}")
print(f"X4  Boiler energy    (Mcal/h) = {X4:.2f}")
print(f"X5  Feedwater temp   (F)      = {X5:.4f}")
print(f"X6  Feedwater flow   (t/h)    = {X6:.4f}")

print(f"\nJ(x0)  = {objective(x0_norm):.8f}")
print(f"J(x*)  = {objective(result.x):.8f}")

NPHR = g1(result.x) + 2750
NTHR = g2(result.x) + 2600
HHV  = 4240 - g3(result.x)
print(f"\nNPHR = {NPHR:.4f} kcal/kWh  (limit <= 2750)  {'FEASIBLE' if g1(result.x) <= 0 else 'VIOLATED'}")
print(f"NTHR = {NTHR:.4f} kcal/kWh  (limit <= 2600)  {'FEASIBLE' if g2(result.x) <= 0 else 'VIOLATED'}")
print(f"HHV  = {HHV:.4f} kcal/kg   (limit >= 4240)  {'FEASIBLE' if g3(result.x) <= 0 else 'VIOLATED'}")

print("\nSO2, NOx, CO, CO2, Dust at optimal x:")
print(f"  SO2  = {SO2:.4f}  mg/m3")
print(f"  NOx  = {NOx:.4f}  mg/m3")
print(f"  CO   = {CO:.4f}   mg/m3")
print(f"  CO2  = {CO2:.4f}  ppm")
print(f"  Dust = {Dust:.4f}  mg/m3")

print(f"\nConverged : {result.success}")
print(f"Message   : {result.message}")
print(f"Iterations: {result.nit}")
