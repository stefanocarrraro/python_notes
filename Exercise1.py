# Resolve the following optimization problem

# max x + 2y - 3z

# s.t. 2x + y <= a
#      x - 3y + z >= b
#      x + 2y + 2z <= c
#      3x - y - z <= d
#      x, y, z >= e

#Parameters: a = 5, b = 3, c = 7, d = 10, e = 4

# ----------------------------------------------------------------------

import pyomo.environ as pyo

# create a model
model = pyo.ConcreteModel()

model.I = pyo.Set()
model.J = pyo.Set()
model.x = pyo.Var(model.I)
model.coef = pyo.Param(model.J, mutable=True)

# Initializing the parameters
DATA = {None: {
    'I': {None: [1,2,3]},
    'J': {None: [1,2,3,4,5]},
    'coef': {None: [5, 3, 7, 10, 4]},
}}

def Obj(model):
    return model.x[1] + 2*model.x[2] - 3*model.x[3]

model.OBJ = pyo.Objective(rule=Obj, sense=max)

def Const(model):
    return {
        2*model.x[1] + model.x[2] <= model.coef[1], 
        model.x[1] - 3*model.x[2] + model.x[3] >= model.coef[2],
        model.x[1] + 2*model.x[2] +2*model.x[3] <= model.coef[3],
        3*model.x[1] - model.x[2] - model.x[3] <= model.coef[4],
        sum(model.x[i] for i in model.I) >= model.coef[5]
    }

model.con = pyo.Constraint(rule=Const)

inst = model.create_instance(DATA)
inst.display()







