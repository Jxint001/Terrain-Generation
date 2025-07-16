import numpy as np
import math

# Constants
NRANDVEC = 8
x_max = z_max = 512

# This is the pre-generated gradient vector table
# Question: Why use only 8 rand grad vec instead of 360?

# RANDVEC2_TABLE = np.array([[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [-1, -1], [1, -1]])

RANDVEC2_TABLE = np.array([
    [1, 0], [0, 1], [-1, 0], [0, -1],
    [1/math.sqrt(2), 1/math.sqrt(2)], 
    [-1/math.sqrt(2), 1/math.sqrt(2)],
    [-1/math.sqrt(2), -1/math.sqrt(2)],
    [1/math.sqrt(2), -1/math.sqrt(2)]
])