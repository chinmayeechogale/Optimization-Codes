import numpy as np
import pandas as pd
from scipy.optimize import minimize


x0 = np.array([80, 3, 2, 710000, 235, 835], dtype=float)

lb = np.array([65, 1, 0, 695000, 225, 815], dtype=float)
ub = np.array([95, 5, 4, 725000, 245, 855], dtype=float)
w = np.array([0.25, 0.25, 0.25, 0.15, 0.10])

_T = pd.read_excel('Objective_reg.xlsx')
_T = _T.dropna(subset=['SO2 (mg/m3)', 'Nox (mg/m3)', 'CO (mg/m3)', 'CO2 (ppm)', 'Dust (mg/m3)'])
ref = {
    'SO2':  _T['SO2 (mg/m3)'].mean(),
    'NOx':  _T['Nox (mg/m3)'].mean(),
    'CO':   _T['CO (mg/m3)'].mean(),
    'CO2':  _T['CO2 (ppm)'].mean(),
    'Dust': _T['Dust (mg/m3)'].mean(),
}
print('Normalization means (dataset):')
for k, v in ref.items():
    print(f'  avg_{k:<4} = {v:.4f}')


def make_model(c, b, sq, cross):
    return {'c': c, 'b': np.array(b), 'sq': np.array(sq), 'cross': np.array(cross)}


def build_quadratic_model():
    model = {}

    model['SO2'] = make_model(
        437.4490683267,
        [0.8198071934, -0.2157032002, 0.1899610630, 0.3943522819, 0.4170693660, 0.3042813313],
        [0.2800335340, -0.3704128535, 0.2326841547, -0.1423787796, 0.1268093964, -0.5024168585],
        [0.4389000893, -0.6214677162, -1.3381744613, 0.8507549512, 1.5235530595,
         0.9671483406, -0.4793229660, 0.3306230614, 1.5161544900,
         1.1947708753, -0.1445169529, 1.4276883615,
         -0.4541595326, -0.5495792644, -0.2388311974])

    model['NOx'] = make_model(
        194.0914575255,
        [-0.2520304783, -0.3962410114, 0.1775274359, 0.4744275999, -0.3468190989, -0.1291232140],
        [1.1090162001, -0.3928987032, 0.4243436342, -0.3789914821, 0.1124077541, -0.7960375759],
        [-1.4502615336, -0.5706169108, -0.4362945619, 0.9572205440, 1.5007746721,
         -0.2300368131, -0.1762756059, 0.5852698019, 0.2369786769,
         -0.1314940048, 0.0025574156, 0.1622174629,
         0.0386389659, 0.4245761989, -0.8309524724])

    model['CO'] = make_model(
        260.7171622052,
        [-2.9744476857, -0.1776771322, -2.2573886607, -0.1515925532, 1.4849384441, -1.1744675297],
        [3.7840635663, -1.7696489594, 2.2545211773, -2.1188607142, 0.1190834916, 2.4568450709],
        [4.0103204334, 6.5029985959, -5.9397427414, -2.4876903117, -2.9293447643,
         1.6164156971, 0.9759918217, -1.8167364615, -4.2385019652,
         2.7640216839, -2.4636260054, -5.3871961524,
         -0.6046304745, -3.6341061229, 5.4811772610])

    model['CO2'] = make_model(
        97831.5521938283,
        [2.4166250702, 10.4332860859, -11.1020770135, 6.2236091860, -8.0257514612, -1.6408025452],
        [20.9376256822, 15.1196067924, 9.6139025579, 35.6849823758, -0.0457765272, -5.7277227968],
        [15.7356081117, 20.1200812589, -33.4323605086, -2.9834984288, -9.0272238260,
         -20.1380632252, -16.1274816119, -25.7752895379, -21.7492048044,
         4.9126108382, -29.6721120362, 0.4414593950,
         12.5651493575, 6.1692617394, 8.2851307827])

    model['Dust'] = make_model(
        14.5231464791,
        [-0.0843694819, -0.0552850402, -0.0390187808, 0.0683057933, 0.0271530900, -0.0881746398],
        [-0.0642464048, -0.0354693173, -0.0554667699, 0.0116716724, 0.0247562385, -0.1530821795],
        [0.1398263715, 0.1702192857, 0.1855621323, -0.1092083856, -0.1633132482,
         0.1042575963, 0.1207120588, -0.0117436505, -0.0345341129,
         0.1697849996, -0.1023654252, -0.0180330035,
         0.0826657505, 0.1088193992, 0.6068773348])

    model['NPHR'] = make_model(
        2711.3882635105,
        [0.1176942038, 0.0747818799, 0.3796105223, 0.1976023396, 0.1298649673, 0.4365408587],
        [-0.2247566470, -0.3698233290, -0.7404783559, -0.7103917012, 0.8531532713, -0.4944574920],
        [-0.3138964528, -1.3377552864, -0.3576361104, 0.1193616588, -0.5667915983,
         1.0301166599, 0.2668688101, 1.0467268271, 0.4606186485,
         -0.7816367713, 1.4195708528, 0.0627402609,
         -0.1767079365, 0.3367746764, -2.4040381760])

    model['NTHR'] = make_model(
        2540.2088800770,
        [0.2071108665, 0.1855092078, 0.0892043560, 0.2905621187, -0.1818812411, 0.1722213115],
        [-0.8600977671, -0.4707669747, 0.0848872859, -1.6336196960, 0.2347090437, 0.2315376786],
        [-0.0040346202, -0.5311967522, -1.1831699935, 0.0994261682, 0.3298600729,
         -0.1522436819, -0.5177171800, 0.3170852729, 1.2403679728,
         -0.1072117633, 0.7153241881, -1.9476862753,
         -0.0233302582, 0.4292856390, -0.3863382716])

    model['HHV'] = make_model(
        4253.5160275007,
        [-0.5906631904, 0.1279392326, -0.2958610834, -0.1449239333, 0.1503174813, 0.3073814931],
        [0.3253746447, 0.2584512830, 0.0379219520, 0.2453036806, -0.0834785973, -0.0342238496],
        [-0.2815950687, 0.3449310340, 0.4155800435, -0.6114107117, -0.5337900820,
         0.2633000261, 0.1963441632, -0.4775084871, 0.4672474325,
         -0.3766223092, 0.3266581789, -0.7103974272,
         0.3331980917, 0.3244190385, 0.4248897323])

    return model


def code_vars(x):
    center = np.array([80, 3, 2, 710000, 235, 835], dtype=float)
    half   = np.array([15, 2, 2, 15000, 10, 20],    dtype=float)
    return (x - center) / half


def eval_quad(z, m):
    cr = m['cross']
    return (m['c']
            + m['b'][0]*z[0] + m['b'][1]*z[1] + m['b'][2]*z[2]
            + m['b'][3]*z[3] + m['b'][4]*z[4] + m['b'][5]*z[5]
            + m['sq'][0]*z[0]**2 + m['sq'][1]*z[1]**2 + m['sq'][2]*z[2]**2
            + m['sq'][3]*z[3]**2 + m['sq'][4]*z[4]**2 + m['sq'][5]*z[5]**2
            + cr[0]*z[0]*z[1]  + cr[1]*z[0]*z[2]  + cr[2]*z[0]*z[3]
            + cr[3]*z[0]*z[4]  + cr[4]*z[0]*z[5]
            + cr[5]*z[1]*z[2]  + cr[6]*z[1]*z[3]  + cr[7]*z[1]*z[4]  + cr[8]*z[1]*z[5]
            + cr[9]*z[2]*z[3]  + cr[10]*z[2]*z[4] + cr[11]*z[2]*z[5]
            + cr[12]*z[3]*z[4] + cr[13]*z[3]*z[5]
            + cr[14]*z[4]*z[5])


def predict_objective_outputs(x, model):
    z = code_vars(x)
    SO2  = eval_quad(z, model['SO2'])
    NOx  = eval_quad(z, model['NOx'])
    CO   = eval_quad(z, model['CO'])
    CO2  = eval_quad(z, model['CO2'])
    Dust = eval_quad(z, model['Dust'])
    return SO2, NOx, CO, CO2, Dust


def predict_all_quad(x, model):
    z = code_vars(x)
    SO2  = eval_quad(z, model['SO2'])
    NOx  = eval_quad(z, model['NOx'])
    CO   = eval_quad(z, model['CO'])
    CO2  = eval_quad(z, model['CO2'])
    Dust = eval_quad(z, model['Dust'])
    NPHR = eval_quad(z, model['NPHR'])
    NTHR = eval_quad(z, model['NTHR'])
    HHV  = eval_quad(z, model['HHV'])
    return SO2, NOx, CO, CO2, Dust, NPHR, NTHR, HHV


def objective_fun(x, model):
    SO2, NOx, CO, CO2, Dust = predict_objective_outputs(x, model)
    SO2_n  = SO2  / ref['SO2']
    NOx_n  = NOx  / ref['NOx']
    CO_n   = CO   / ref['CO']
    CO2_n  = CO2  / ref['CO2']
    Dust_n = Dust / ref['Dust']
    return w[0]*SO2_n + w[1]*NOx_n + w[2]*CO_n + w[3]*CO2_n + w[4]*Dust_n


def constraint_fun(x, model):
    z = code_vars(x)
    NPHR = eval_quad(z, model['NPHR'])
    NTHR = eval_quad(z, model['NTHR'])
    HHV  = eval_quad(z, model['HHV'])
    # c <= 0 form: NPHR-2750, NTHR-2600, 4240-HHV
    return np.array([NPHR - 2750, NTHR - 2600, 4240 - HHV])


if __name__ == '__main__':
    model = build_quadratic_model()

    obj    = lambda x: objective_fun(x, model)
    constr = {'type': 'ineq', 'fun': lambda x: -constraint_fun(x, model)}  # scipy: ineq means >= 0

    bounds = list(zip(lb, ub))

    result = minimize(
        fun=obj,
        x0=x0,
        method='SLSQP',
        bounds=bounds,
        constraints=constr,
        options={
            'maxiter': 500,
            'ftol': 1e-10,
            'iprint': 1,
            'disp': True,
        }
    )

    x_opt = result.x
    f_opt = result.fun

    print('\nOptimal x =')
    print(x_opt)
    print(f'\nOptimal weighted objective = {f_opt}')

    SO2, NOx, CO, CO2, Dust, NPHR, NTHR, HHV = predict_all_quad(x_opt, model)

    print('\nPredicted outputs at optimum:')
    print(f'SO2  = {SO2:.6f}')
    print(f'NOx  = {NOx:.6f}')
    print(f'CO   = {CO:.6f}')
    print(f'CO2  = {CO2:.6f}')
    print(f'Dust = {Dust:.6f}')
    print(f'NPHR = {NPHR:.6f}')
    print(f'NTHR = {NTHR:.6f}')
    print(f'HHV  = {HHV:.6f}')
    print(f'exitflag = {result.status}')
    print(result)
