# NOTES ABOUT THE PYOMO LIBRARY

# ABSTRACT MODELS: "AbstractModel". An abstract model is a template or a blueprint for a mathematical programming problem.
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

def obj_expression(m):                                  # Defining the function for the OF: (sum of c_j*x_j) to be minimized 
    return pyo.summation(m.c, m.x)

model.OBJ = pyo.Objective(rule=obj_expression)          # Defining the OF as the function obj_expression defined above
# The default sense is minimization. For maximization, the sense=pyo.maximize argument must be used

def ax_constraint_rule(m, i):                           # Defining the constraints: sum of a_ij*x_j >= b_i for all i in I
    # return the expression for the constraint for i
    return sum(m.a[i,j] * m.x[j] for j in m.J) >= m.b[i]

# the next line creates one constraint for each member of the set model.I
model.AxbConstraint = pyo.Constraint(model.I, rule=ax_constraint_rule)  # Defining the constraints as the function ax_constraint_rule defined above

# To define the parameters of the model, we need to create a data file (data.dat) with the following format:
#param m := 1 ;
#param n := 2 ;
#param a :=
#1 1 3
#1 2 4
#;
#param c:=
#1 2
#2 3
#;
#param b := 1 1 ;

# then the model is run by typing the following command in the terminal:
# pyomo solve --solver=glpk AbsModel.py Data.dat

# IN THE RESULTS: Number in [] represent the time the model required for each step

# ----------------------------------------------------------------------------------------------------------------

# Concrete models "ConcreteModel" are used to define concrete optimization models in Pyomo. Is used when all the 
# parameters of the optimization problem are known at the time the model is defined.

model = pyo.ConcreteModel()    # defining "model" as a Concrete model
model.x = pyo.Var([1,2], domain=pyo.NonNegativeReals)  # Variables x[1] and x[2] as non-negative real numbers
model.OBJ = pyo.Objective(expr = 2*model.x[1] + 3*model.x[2])  # Objective function 2*x[1] + 3*x[2] to be minimized
model.Constraint1 = pyo.Constraint(expr = 3*model.x[1] + 4*model.x[2] >= 1)    # Constraint 3*x[1] + 4*x[2] >= 1 

# ----------------------------------------------------------------------------------------------------------------

# SETs and RANGESETs: Sets are used to define the index sets for variables, parameters, and constraints.
# https://pyomo.readthedocs.io/en/stable/pyomo_modeling_components/Sets.html

model.A = pyo.Set() 
model.D = pyo.RangeSet(5, 10)   # Set B is the set of integers from 5 to 10
model.A.pprint()
model.D.pprint()

model.I = model.A | model.D # union
model.J = model.A & model.D # intersection
model.K = model.A - model.D # difference
model.L = model.A ^ model.D # exclusive-or
model.M = model.A * model.D # cross-product

# Pyomo provies some prefedined sets. Useful are:
model.A = pyo.PositiveReals     # Valid also negative
model.B = pyo.PositiveIntegers  # Valid also negative
model.C = pyo.NonPositiveReals  # Valid also NonNegative and with Integers
