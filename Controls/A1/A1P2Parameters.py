import numpy as np

# PHYSICAL
mc = 1.0  # kg
mr = 0.25  # kg
ml = 0.25  # kg
jc = 0.0042  # kg*m^2
d = 0.3  # m
g = 9.8  # m/s**2
mu = 0.1  # kg/s

# ANIMATION
w = 0.2
h = 0.2
gap = 0.3
h2 = 0.1
l = 20

# INITIAL CONDITIONS
z0 = 12.0  # ,m
h0 = 10.0  # ,m
th0 = 0.0 * np.pi / 180  # ,rads
dz0 = 0.0  # ,m/s
dh0 = 0.0  # ,m/s
dth0 = 0.0  # ,rads/s

# TIMING
t0 = 0.0  # s
t1 = 10  # s
ts = 0.0001  # s
t_plot = 0.1  # s

# SATURATION
F_max = 25000.0  # N
