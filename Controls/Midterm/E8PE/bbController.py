import numpy as np
from bbParameters import *


class Controller:
    def __init__(self):
        self.z, self.zDot, self.th, self.thDot, = state0.flatten()

    # UPDATE FUNCTION
    def update(self, z_r, state):
        self.z, self.zDot, self.th, self.thDot = state.flatten()
        f = self.force(z_r)
        return f

    # PROPORTIONAL DERIVATIVE CALCULATION
    def force(self, z_r):
        # OUTER LOOP
        th_r = kp_z * (z_r - self.z) - kd_z * self.zDot
        # INNER LOOP
        f = kp_th * (th_r - self.th) - kd_th * self.thDot
        # EQUILIBRIUM FORCE
        f_e = (m1 * g * self.z / l) + (m2 * g / 2)
        # RETURN FORCE
        f_tilde = f + f_e
        return f_tilde

    @staticmethod
    def sat(u, limit):
        if abs(u) > limit:
            u = limit * np.sign(u)
        return u
