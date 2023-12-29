# First simple optimization problem:

# OF:       min (2*x1 + 3*x2)
# subject to:  3*x1 +   4*x2 >= 1
#              x1, x2 >= 0

# ----------------------------------------------------------------------------

import pyomo.environ as pyo

modelA = pyo.AbstractModel()

modelA.I = pyo.RangeSet()
modelA.x = pyo.Var(modelA.I, domain=pyo.NonNegativeReals)
modelA.c = pyo.Param(modelA.I)
modelA.b = pyo.Param(modelA.I)

dAta = {None: {
    'I': {None: [1, 2]},
    'c': {1: 2, 2: 3},
    'b': {1: 3, 2: 4},
}}

def OBJ_FCN(m):
    return sum(m.c[i] * m.x[i] for i in m.I)

modelA.OF = pyo.Objective(rule=OBJ_FCN)

def CONST(m):
    return sum(m.b[i] * m.x[i] for i in m.I) >= 1

modelA.const = pyo.Constraint(modelA.I, rule=CONST)

# Create an instance and initialize it with the data
instanceA = modelA.create_instance(data=dAta)

# Accessing and displaying the initialized data
print("Index set (I):", instanceA.I.display())
print("Objective function coefficients (c):", instanceA.c.display())
print("Constraint coefficients (b):", instanceA.b.display())
