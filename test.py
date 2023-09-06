import numpy as np
from scipy.optimize import fsolve

# Define the system of equations as a function
def equations(variables):
    x, y = variables
    eq1 = (4 * x**2 + (4 * y + 8) * x + 2 * y**2 + 6 * y + 1) * np.exp(x)
    eq2 = (4 * y + 4 * x + 2) * np.exp(x)
    return [eq1, eq2]

# Initial guess for the solution (you can change this)
initial_guess = [1, -1.5]

# Solve the system of equations
solution = fsolve(equations, initial_guess)

# Extract the values of x and y from the solution
x_solution, y_solution = solution

print("Solution:")
print("x =", x_solution)
print("y =", y_solution)
