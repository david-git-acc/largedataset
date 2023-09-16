import numpy as np

# Sample data
x = np.array([1, 2, 3, 4, 5])
y = np.array([4, 3, 4, 5, 6])
z = np.array([3, 4, 5, 6, 7])

# Create the design matrix
X = np.column_stack(( x, y, np.ones_like(x)))

# Perform least squares regression
coefficients, residuals, rank, singular_values = np.linalg.lstsq(X, z, rcond=None)
print( np.linalg.lstsq(X, z, rcond=None)[0][0])

# Extract coefficients
a, b, c = coefficients

# Coefficients represent the equation of the 3D regression plane: z = ax + by + c
print(f"Regression plane equation: z = {a:.2f}x + {b:.2f}y + {c:.2f}")