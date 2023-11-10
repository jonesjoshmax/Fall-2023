import numpy as np
from Parameters import *
from MAV import MAV
from Trim import Trim

mav = MAV()
gamma = mav.gamma

trim = Trim()
Va = 35
angle = np.deg2rad(0)
radius = np.inf
xTrim, uTrim = trim.minTrim(Va, angle, radius)

VaT = np.sqrt(xTrim[3, 0] ** 2 + xTrim[4, 0] ** 2 + xTrim[5, 0] ** 2)
aT = np.arctan(xTrim[5, 0] / xTrim[3, 0])
bT = np.arctan(xTrim[4, 0] / VaT)
thT = xTrim[7, 0]

g0 = gamma[0]
g3 = gamma[3]
g4 = gamma[4]

cpp = g3 * cLp + g4 * cNp
cPDa = g3 * cLDa + g4 * cNDa
aPh1 = -.5 * rho * VaT ** 2 * S * b * cpp * (b / (2 * VaT))
aPh2 = .5 * rho * VaT ** 2 * S * b * cPDa
aTh1 = -(rho * VaT ** 2 * c * S) / (2 * jy) * cmq * (c / (2 * VaT))
aTh2 = -(rho * VaT ** 2 * c * S) / (2 * jy) * cma
aTh3 = (rho * VaT ** 2 * c * S) / (2 * jy) * cmDe
aV1 = ((rho * VaT * S) / M) * (cd0 + (cda * aT) + (cdDe * uTrim[0, 0])) + (rho * S_prop) / M * cProp * VaT
aV2 = (rho * S_prop) / M * cProp * kMotor ** 2 * uTrim[3, 0]
aV3 = g * np.cos(thT - aT)

z = 0.707

# ROLL
trRoll = 2
wRoll = 2.2 / trRoll
kdRoll = (2 * z * wRoll - aPh1) / aPh2
kpRoll = wRoll ** 2 / aPh1
kiRoll = 0

# COURSE
trCourse = 1
wCourse = 2.2 / trCourse
zCourse = 0.5
kdCourse = 0
kpCourse = (2 * zCourse * wCourse * VaT) / g
kiCourse = (wCourse ** 2 * VaT) / g

# PITCH
zPitch = 0.1
trPitch = 0.1
wPitch = 2.2 / trPitch
kdPitch = (2 * zPitch * wPitch - aTh1) / aTh3
kpPitch = (wPitch ** 2 - aTh2) / aTh3
kiPitch = 0
kDCth = kpPitch * aTh3 / (aTh2 + kpPitch * aTh3)

# ALTITUDE
trAlt = 10.0
wAlt = 2.2 / trAlt
kdAlt = 0
kpAlt = 2 * z * wAlt / (kDCth * VaT)
kiAlt = wAlt ** 2 / (kDCth * VaT)

# AIRSPEED
trVa = 1.0
wVa = 2.2 / trVa
kdVa = 0
kpVa = (aV1 - 2 * z * wVa) / kDCth
kiVa = wVa ** 2 / (kDCth * g)

# THROTTLE
trThr = 0.01
wThr = 2.2 / trThr
kdThr = 0
kpThr = (2 * z * wThr - aV1) / aV2
kiThr = wThr ** 2 / aV2
