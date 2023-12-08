from pyomo.environ import *

# Create a simple model
model = ConcreteModel()
model.x = Var(within=NonNegativeReals)
model.obj = Objective(expr=model.x, sense=minimize)

# Print the model
model.pprint()

# Solve the model
SolverFactory('glpk').solve(model)

# Display the results
print("\nResults:")
model.display()
