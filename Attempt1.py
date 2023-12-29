# First simple optimization problem:

# OF:       min (2*x1 + 3*x2)
# subject to:  3*x1 +   4*x2 >= 1
#              x1, x2 >= 0

# ------------------------------------------------------

# concrete model: 

import pyomo.environ as pyo

model = pyo.ConcreteModel()

#model.D = pyo.Set(dimen=2)
model.x = pyo.Var([0, 1], domain=pyo.NonNegativeReals)

def obj_fcn(model):
    return 2 * model.x[0] + 3 * model.x[1]

model.OBJ = pyo.Objective(rule=obj_fcn)

def constr (model):
    return 3*model.x[0] + 4*model.x[1] >= 1

model.CON = pyo.Constraint(rule=constr)

print("\nThe model is defined as follows: \n")

# solving the model

optimal = pyo.SolverFactory('glpk')
optimal.solve(model)
model.display()
print("\n\n\n\n\n\n")









