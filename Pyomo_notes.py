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
# model.A = pyo.PositiveReals     # Valid also negative
# model.B = pyo.PositiveIntegers  # Valid also negative
# model.C = pyo.NonPositiveReals  # Valid also NonNegative and with Integers


# PARAMETERS: Parameters are used to define the coefficients of the objective function and constraints. they have a similar
# concept of the stes. https://pyomo.readthedocs.io/en/stable/pyomo_modeling_components/Parameters.html

# create a parameter that represents a square matrix with 9, 16, 25 on the main diagonal and zeros elsewhere
model.A = pyo.RangeSet(1,3)
v={}        
v[1,1] = 9    
v[2,2] = 16
v[3,3] = 25
model.S1 = pyo.Param(model.A, model.A, initialize=v, default=0) # default=0 is used to set the default value of the parameter
model.S1.pprint() 

# VARIABLES: Variables are used to define the decision variables of the optimization problem. They are indexed by sets.
# https://pyomo.readthedocs.io/en/stable/pyomo_modeling_components/Variables.html

model.LumberJack = pyo.Var(within=pyo.NonNegativeReals, bounds=(0, 6), initialize=1.5)

# bounds = A function (or Python object) that gives a (lower,upper) bound pair for the variable
# domain = A set that is a super-set of the values the variable can take on.
# initialize = A function (or Python object) that gives a starting value for the variable; this is particularly important for non-linear models
# It's also possible to do:
model.LumberJack = 1.5
# within = (synonym for domain)

# OBJECTIVE FUNCTION: The objective function is used to define the objective function of the optimization problem.
# https://pyomo.readthedocs.io/en/stable/pyomo_modeling_components/Objective.html

#def ObjRule(model):
#    return 2*model.x[1] + 3*model.x[2]
#model.obj1 = pyo.Objective(rule=ObjRule)

# or
#def ObjRule(model):
#    return pyo.summation(model.p, model.x) + model.y
#model.obj2 = pyo.Objective(rule=ObjRule, sense=pyo.maximize)


# CONSTRAINTS: Constraints are used to define the constraints of the optimization problem. They are indexed by sets.
# https://pyomo.readthedocs.io/en/stable/pyomo_modeling_components/Constraints.html

def ConstraintRule(model, i):
    return sum(model.A[i,j]*model.x[j] for j in model.J) >= 0  # sum of a_ij*x_j >= 0 for all i in I

ciao = pyo.Constraint(model.I, rule=ConstraintRule) # Defining the constraints as the function ax_constraint_rule defined above


model.A = pyo.RangeSet(1, 10)
model.c = pyo.Param(model.A)        # c is a 1D array indexed by set A [c_i] (objective function coefficients)
model.d = pyo.Param()               # d is a 1D array 
model.x = pyo.Var(model.A, domain=pyo.Boolean) # x is a 1D array indexed by set A [x_i] (decision variables)
model.A.pprint()
model.c.pprint()
model.d.pprint()
model.x.pprint()

# It's also possible to do : 
model.c = pyo.ConstraintList()      # Empty constraint list and then add the constraints one by one with the following code line:
# model.c.add(expr = sum(model.A[i,j]*model.x[j] for j in model.J) >= 0)

# There are some keywords for piecewise linear expressions:

# pw_pts ={},[],()       A list of points that define the piecewise linear function

# pw_repn = <option>     The representation of the piecewise linear function. Valid values are:
#                           'INC' - incremental (delta) method
#                           'DEC' - decremental (lambda) method
#                           'CC' - convex combination model
#                           'LINEAR' - the function is linear

# pw_constr_type = <option>  The type of constraints used to define the piecewise linear function. Valid values are:
#                               'EQ' - equality constraints
#                               'LN' - lower boudary constraints
#                               'UB' - upper boundary constraints

# f_rule=f(model,i,i,...,x),[],{}   An object that returns a numeric value that is the range value corresponding to each piecewise domain point

# warn_tol = <float>    A tolerance used to check for errors in the piecewise linear function definition. Default is 1e-6 (i.e. 6.4)

# ESPRESSION OBJECTS: similar to the Param component but the underlying values can be numeric constants or Pyomo extressions:

model = pyo.ConcreteModel()
model.x = pyo.Var(initialize=1.0)
def _e(m, i):
    return m.x * i
model.e = pyo.Expression([1, 2, 4], rule=_e)
model.e.pprint()

# or using defined expressions for other expressions:

model = pyo.ConcreteModel()
model.x = pyo.Var()
# create a Pyomo expression
e1 = model.x + 5
# create another Pyomo expression
# e1 is copied when generating e2
e2 = e1 + model.x

# ----------------------------------------------------------------------------------------------------------------

# https://pyomo.readthedocs.io/en/stable/working_models.html

# SOLVERS: Pyomo provides a common interface to many solvers. The following solvers are supported:
# For CONCRETE models use the following code lines:

opt = pyo.SolverFactory('glpk')     # Selecting the solver (glpk) - GLPK (GNU Linear Programming Kit) is a free, open source software library written in C  
opt.solve(model)                    # Solving the model with the selected solver 

# For ABSTRACT models use the following code lines:

instance = model.create_instance()  # Creating an instance of the model, "intance"means "model with data attached to it (parameters, variables, constraints)"
#                                     the model is instantiated with specific values for the parameters
opt = pyo.SolverFactory('glpk')  
opt.solve(instance)                 # Solving the model with the selected solver
instance.display()                  # Displaying the results
# in the terminal use: pyomo solve --solver=glpk AbsModel.py Data.dat

# the models we define can be changed and re-solved without having to re-instantiate the model. It is sufficient to change parameters, constraints, or variables.
# for abstact models, it is needed to change the instance and re-solve instance before re-solving the model

# it is also possible to:
 
# fix variables:                                instance.x[2].fix(1)
#                       or alternatively        instance.x.value = 1
#                                               instance.x.fixed = True
# unfix them:                                   instance.x[2].unfix()
#
# Extend OBJ FCN:                               model.obj.expr += 10 * model.y    
#
# Activate/disactivate BOJ FCN:                 model.obj.deactivate()

# ----------------------------------------------------------------------------------------------------------------

# ACCESSING STUFF: https://pyomo.readthedocs.io/en/stable/working_models.html

# VARIABLES
# To print all the values of the variables in the terminal:
# for v in instance.component_data_objects(pyo.Var, active=True):
#     print(v, pyo.value(v))  

# PARAMETERS VALUES: 
# DUALS
# SLACKS
# SOLUTION STATUS
# OBJECTIVE VALUE
# SOLVER TIME

# DISPLAY OF SOLVER OUTPUT: results = opt.solve(instance, tee=True)


# ----------------------------------------------------------------------------------------------------------------



# WORKING WITH ABSTRACT MODELS: Construction occurs in two phases. When you first declare and attach components to 
# the model, those components are empty containers and not fully constructed, even if you explicitly provide data.
# https://pyomo.readthedocs.io/en/stable/working_abstractmodels/instantiating_models.html

# Create a concrete instance of the abstract model:
instance = model.create_instance()

model = pyo.AbstractModel()

model.p = pyo.Param(initialize=5)

model.I = pyo.Set(initialize=[1,2,3])
model.x = pyo.Var(model.I)

# OBS: it's possible to decleare some updates in the concrete_instance() which will overwrite the values in the abstract model. Example:
instance2 = model.create_instance({None: {'I': {None: [4,5]}}})


# ----------------------------------------------------------------------------------------------------------------

# INITIALIZING DATA FOR AN ABSTRACT MODEL: https://pyomo.readthedocs.io/en/stable/working_abstractmodels/data/raw_dicts.html
print("\n\n Instance \n\n")
m = pyo.AbstractModel()
m.I = pyo.Set()                             # Set I is the set of rows (1, 2, ..., m)
m.p = pyo.Param()                           # p is a 1D array (1 element)
m.q = pyo.Param(m.I)                        # q is a 1D array indexed by set I [q_i] - 1 element for each i in I
m.r = pyo.Param(m.I, m.I, default=0)        # r is a matrix indexed by sets I and I [r_ij] - 1 element for each i,j in I
data = {None: {
    'I': {None: [1,2,3]},                   # Set I is of indeces 1,2,3
    'p': {None: 100},                       # p is 1 element = 100
    'q': {1: 10, 2:20, 3:30},               # q is a 1D array with 3 elements = 10,20,30
    'r': {(1,1): 110, (1,2): 120, (2,3): 230},  # r is a 2D matrix that looks like this: [ 110 120 0 , 0 0 230 , 0 0 0]
}}
i = m.create_instance(data)
i.pprint()
print("\n\n")

# IMPORT DATA FROM OUTSIDE FILE: https://pyomo.readthedocs.io/en/stable/working_abstractmodels/data/datfiles.html 
# A DataPortal object can load data in a consistent manner, and this data can be used to simply initialize all Set and Param components in a model.
# DataPortal objects can be used to initialize both concrete and abstract models in a uniform manner, which is important in some scripting 
# applications. But in practice, this capability is only necessary for abstract models.

# In a different file named <name>.dat, things are defined as follows:

# SET:
# set I := 1 2 3 ;      simple set
# set J := 1..3 ;       range set

#     SET of TUPLES: 
#     set A : A1 A2 A3 A4 :=
#         1   +  -  -  +
#         2   +  -  +  -
#         3   -  +  -  - ;

#     SET of ARRAYS:
#     set B : B1 B2 B3 :=
#         1   1  2  3
#         2   4  5  6
#         3   7  8  9 ;

# PARAMETER:
# param C := 100 ;    simple parameter
# param D := true;  
 
# set A := a c e;           NOTE: we use a c e to define the index set of the parameter C and D below
# param : B C D :=    parameter with index set
# a  . -1 1.1
# c 30  . 3.3
# e 50 -5   .         the dot (.) is used to indicate that the value is not defined
# ; 

# TABLE:
# table F(A) :        The A must be predefined as a set (?)
# A  F1 F2 F3 :=      F1, F2 and F3 are the columns of the table while A1, A2 and A3 are the rows 
# A1  1  2  3
# A2  4  5  6
# A3  7  8  9
# ;

# if not including the column labels, the table can be defined as follows:
# table columns=4 M(1)={3} :=
# A1 B1 4.3 5.3
# A2 B2 4.4 5.4
# A3 B3 4.5 5.5
# ;

# LOAD:  https://pyomo.readthedocs.io/en/stable/working_abstractmodels/data/dataportals.html
#      TAB File: A text file format that uses tabs to separate columns of values in each row of a table. File C.tab:
# A  Y
# A1 3.3
# A2 3.4
# A3 3.5
#           -> load Y.tab : [A] Y;      NOTE: the [A] is the index set of the parameter Y that is initialized
# or        -> load C.tab format=set : C;    Loads this data into C. NOTE: C must be decelared with two dimensions

#      JSON File: A text file format that uses the JavaScript Object Notation (JSON) format to represent data.
#      CSV File: A text file format that uses comma or other delimiters to separate columns of values in each row of a table.
#      XML File: An extensible markup language for documents and data structures. XML files can represent tabular data in a hierarchical format.
#      XLS File: A spreadsheet data format that is primarily used by the Microsoft Excel application

# INCLUDE: executes the commands in a file. The file is read and interpreted as if the commands were typed directly into the data file.
#          -> include file.dat

# NAMESPACE kayword: used to define a namespace for the data in the data file.
# set C := 1 2 3 ; 
# pyo.namespace ns1                 # if not specified, C is defined as 1,2,3                 
# {                                 # when ns1 is specified, C is defined as 4,5,6
#    set C := 4 5 6 ;               # when ns2 is specified, C is defined as 7,8,9
# }
# pyo.namespace ns2
# {
#    set C := 7 8 9 ;
#}

# DATA PORTAL: It is a class that can be used to load data into a model. 

model = pyo.AbstractModel()
data = pyo.DataPortal()
model.A = pyo.Set(dimen=2)
model.p = pyo.Param(model.A)  # there is not excel.xls file in the folder
#data.load(filename='excel.xls', range='TableName', param=model.p, index=model.A)    # NOTE: the range is required to specify the table of cell data that 
#instance = model.create_instance(data)                                              # is loaded from the spreadsheet.


# ----------------------------------------------------------------------------------------------------------------

# SCALING THE MODEL: https://pyomo.readthedocs.io/en/stable/working_abstractmodels/scaling.html'
# Scaling a model is easy in pyomo. here's an example:

import pyomo.environ as pyo
# create the model
model = pyo.ConcreteModel()
model.x = pyo.Var(bounds=(-5, 5), initialize=1.0)
model.y = pyo.Var(bounds=(0, 1), initialize=1.0)
model.obj = pyo.Objective(expr=1e8*model.x + 1e6*model.y)
model.con = pyo.Constraint(expr=model.x + model.y == 1.0)
# create the scaling factors
model.scaling_factor = pyo.Suffix(direction=pyo.Suffix.EXPORT)
model.scaling_factor[model.obj] = 1e-6 # scale the objective of a magnitude of 1e-6
model.scaling_factor[model.con] = 2.0  # scale the constraint by a factor of 2
model.scaling_factor[model.x] = 0.2    # scale the x variable by a factor of 0.2

scaled_model = pyo.TransformationFactory('core.scale_model').create_using(model)        # create the new scaled model

# print the value of the objective function to show scaling has occurred
print("Scaled model \n")
print("old model.x value = " , pyo.value(model.x))
print("new model.x value = " ,pyo.value(scaled_model.scaled_x))
print(pyo.value(scaled_model.scaled_x.lb))
print(pyo.value(model.obj))
print(pyo.value(scaled_model.scaled_obj))

# cool video
# https://www.youtube.com/watch?v=QbYd3DOf-T4


