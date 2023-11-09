from numpy import zeros
from numpy import arange
from numpy import array

# MODEL SETTING
model = 'f22.stl'

# GRAPHING SETTINGS
g_lim = 5
scale = 0.05

# TIME SETTINGS
plt = 500
temp = plt
t0 = 0
t1 = 300
ts = 0.01
t_array = arange(t0, t1 + ts, plt * ts)
pause = 0.01

# INERTIAL PARAMETERS
jx = 0.824
jy = 1.135
jz = 1.759
jxz = 0.120
g = 9.806650
mass = 13.5

# INITIAL CONDITIONS
# MATRIX CONTAINING PN PE PD, [[PN], [PE], [PD]]
pDir = zeros((3, 1))
# MATRIX CONTAINING ANGLES, [[PHI], [THETA], [PSI]]
ang = zeros((3, 1))
# MATRIX CONTAINING UVW, [[U], [V], [W]]
uvw = zeros((3, 1))
# MATRIX CONTAINING PQR, [[P], [Q], [R]]
pqr = zeros((3, 1))
# MATRIX CONTAINING FORCES, [[FX], [FY], [FZ]]
f = zeros((3, 1))
# EXTERNAL MOMENTS [[L], [M], [N]]
lmn = zeros((3, 1))
# DEFLECTIONS [[Da], [De], [Dr], [Dt]]
defL = zeros((4, 1))

# AERODYNAMIC PARAMETERS
S = 0.55
b = 2.90
c = 0.19
S_prop = 0.2027
rho = 1.2682
e = 0.9
AR = b ** 2 / S
cl0 = 0.23
cd0 = 0.043
cm0 = 0.0135
cla = 5.61
cda = 0.030
cma = -2.74
clq = 7.95
cdq = 0.0
cmq = -38.21
clDe = 0.13
cdDe = 0.0135
cmDe = -0.99
M = 50
alpha0 = 0.47
epsilon = 0.16
cdp = 0.0
cY0 = 0.0
cL0 = 0.0
cN0 = 0.0
cYb = -0.98
cLb = -0.13
cNb = 0.073
cYp = 0.0
cLp = -0.51  # ell=p
cNp = -0.069
cYr = 0.0
cLr = 0.25
cNr = -0.095
cYDa = 0.075
cLDa = 0.17
cNDa = -0.011
cYDr = 0.19
cLDr = 0.0024
cNDr = -0.069
cProp = 1
kMotor = 80
kOmega = 0
kTp = 0
