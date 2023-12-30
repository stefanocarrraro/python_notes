# Resolve the following optimization problem

# max x + 2y - 3z

# s.t. 2x + y <= a              |  2 1 0        1
#      x - 3y + z >= b          |  1 -3 1       -1
#      x + 2y + 2z <= c         |  1 2 2        1
#      3x - y - z <= d          |  3 -1 -1      1
#      x + y + z >= e           |  1 1 1        -1

#Parameters: a = 5, b = 3, c = 7, d = 10, e = 4

{(1,1): 2, (1,3): 0, (2,2): -3, (3,2): 2, (3,3): 2, (4,1): 3, (4,2): -1, (4,3): -1}

# ----------------------------------------------------------------------
print("\n\n")
import pyomo.environ as pyo

# create a model
model = pyo.AbstractModel()

model.I = pyo.RangeSet(3)
model.I.display()
model.J = pyo.RangeSet(5)
model.x = pyo.Var(model.I)
#model.x.display()
model.c = pyo.Param(model.J, mutable=True)
model.b = pyo.Param(model.J, model.I, mutable=True)
model.d = pyo.Param(model.J, mutable=True)
#model.con = pyo.ConstraintList()

def Obj(model):
    return model.x[1] + 2*model.x[2] - 3*model.x[3]

model.OBJ = pyo.Objective(rule=Obj, sense=pyo.maximize)

def Constr(model, j):
    return ((model.d[j]*(sum(model.x[i]*model.b[j,i]) <= model.c[j])) for i in model.I)

#for j in model.J:
#    model.con.add(expr=Constr(model, 5))
model.con = pyo.Constraint(rule=Constr)
model.con.display()

#def Const1(model):
#    return 2*model.x[1] + model.x[2] <= model.coef[1]

#def Const2(model):
#    return model.x[1] - 3*model.x[2] + model.x[3] >= model.coef[2]

#def Const3(model):
#    return model.x[1] + 2*model.x[2] +2*model.x[3] <= model.coef[3]

#def Const4(model):
#    return 3*model.x[1] - model.x[2] - model.x[3] <= model.coef[4]

#def Const5(model):
#    return sum(model.x[i] for i in model.I) >= model.coef[5]



#model.display()

# Initializing the parameters
DATA = {None: {
    'I': {None: [1,2,3]},
    'J': {None: [1,2,3,4,5]},
    'c': {1:5, 2:3, 3:7, 4:10, 5:4},
    'b': {(1,1): 2, (1,3): 0, (2,2): -3, (3,2): 2, (3,3): 2, (4,1): 3, (4,2): -1, (4,3): -1},
    'd': {1:1, 2:-1, 3:1, 4:1, 5:-1}
}}

inst = model.create_instance(DATA)
inst.pprint()

#solver = pyo.SolverFactory('glpk')

#results = solver.solve(model)
#print(results)


print("\n\n")






