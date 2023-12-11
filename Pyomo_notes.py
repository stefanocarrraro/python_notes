# NOTES ABOUT THE PYOMO LIBRARY

# Abstract models "AbstractModel". An abstract model is a template or a blueprint for a mathematical programming problem.
# It defines the structure of the problem without specifying numerical values. It is useful when the problem structure is known, 
# but the actual data values are not fixed at the time of model creation. Data is added later, after the abstract model is defined, 
# and the model is then instantiated

# Explanation here: https://pyomo.readthedocs.io/en/stable/pyomo_overview/simple_examples.html

import pyomo.environ as pyo         # Import the Pyomo library

model = pyo.AbstractModel()         # Defining "model"as an Abstract model

model.m = pyo.Param(within=pyo.NonNegativeIntegers)     # number of rows (non-negative integer parameter m)
model.n = pyo.Param(within=pyo.NonNegativeIntegers)     # number of columns (non-negative integer parameter n)

model.I = pyo.RangeSet(1, model.m)                      # Set I is the set of rows (1, 2, ..., m)
model.J = pyo.RangeSet(1, model.n)                      # Set J is the set of columns (1, 2, ..., n)  

model.a = pyo.Param(model.I, model.J)                   # a is a 2D array indexed by sets I and J [a_ij] (coefficient matrix)
model.b = pyo.Param(model.I)                            # b is a 1D array indexed by set I [b_i] (right-hand side coefficients)
model.c = pyo.Param(model.J)                            # c is a 1D array indexed by set J [c_j] (objective function coefficients)

# the next line declares a variable indexed by the set J
model.x = pyo.Var(model.J, domain=pyo.NonNegativeReals)

def obj_expression(m):
    return pyo.summation(m.c, m.x)

model.OBJ = pyo.Objective(rule=obj_expression)

def ax_constraint_rule(m, i):
    # return the expression for the constraint for i
    return sum(m.a[i,j] * m.x[j] for j in m.J) >= m.b[i]

# the next line creates one constraint for each member of the set model.I
model.AxbConstraint = pyo.Constraint(model.I, rule=ax_constraint_rule)

# ----------------------------------------------------------------------------------------------------------------

# Concrete models "ConcreteModel" are used to define concrete optimization models in Pyomo. Is used when all the 
# parameters of the optimization problem are known at the time the model is defined.

model = pyo.ConcreteModel()    # defining "model" as a Concrete model
model.x = pyo.Var([1,2], domain=pyo.NonNegativeReals)  # Variables x[1] and x[2] as non-negative real numbers
model.OBJ = pyo.Objective(expr = 2*model.x[1] + 3*model.x[2])  # Objective function 2*x[1] + 3*x[2] to be minimized
model.Constraint1 = pyo.Constraint(expr = 3*model.x[1] + 4*model.x[2] >= 1)    # Constraint 3*x[1] + 4*x[2] >= 1 



import sys
print(sys.path)
