# Trying to understand the stupid sintax

import pyomo.environ as pyo

# defining the model
model = pyo.AbstractModel()

# Defining a set
model.I = pyo.Set()

# Defining Parameters
model.p = pyo.Param(model.I)

# Defining Variables
model.x = pyo.Var(model.I)

print("\n\n\n")
model.I.display()
model.p.display()
model.x.display()
print("\n\n\n")

# Defining data
Data = {None: {
    'I': {None: [1,2,3,4]},
    'p': {1:1, 2:2, 3:2, 4:2}
}}

# creating an instance
inst = model.create_instance(Data)

inst.pprint()
print("\n\n\n")

