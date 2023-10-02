import numpy as np
from vtolParameters import *


class Controller:
    def __init__(self):
        self.z, self.h, self.th, self.zDot, self.hDot, self.thDot = state0.flatten()

    def update(self, h_r, state):
        self.z, self.h, self.th, self.zDot, self.hDot, self.thDot = state.flatten()
        # FEEDBACK LINEARIZED FORCE
        f_fl = g * (mc + 2 * mr)
        # LINEARIZED FORCE
        f_tilde = kp * (h_r - self.h) - kd * self.hDot
        # TOTAL FORCE
        F = f_fl + f_tilde
        F = self.sat(F, fMax)
        return F

    @staticmethod
    def sat(u, limit):
        if abs(u) > limit:
            u = limit * np.sign(u)
        return u
