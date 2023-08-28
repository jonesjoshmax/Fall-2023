import numpy as np
from math import cos, sin


def rotMax_vb(phi, theta, psi):
    R_vb = np.array([[cos(theta) * cos(psi), sin(phi) * sin(theta) * cos(psi) -
                      cos(phi) * sin(psi), cos(phi) * sin(theta) * cos(psi) + sin(phi) * sin(psi)],
                     [cos(theta) * sin(psi), sin(phi) * sin(theta) * sin(psi) + cos(phi) * cos(psi),
                      cos(phi) * sin(theta) * sin(psi) - sin(phi) * cos(psi)],
                     [-sin(theta), sin(phi) * cos(theta), cos(phi) * cos(theta)]])
    return R_vb
