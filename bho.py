import pyomo.environ as pyo

print("\n\n")
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