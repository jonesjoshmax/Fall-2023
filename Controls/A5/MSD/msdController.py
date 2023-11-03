import numpy as np
from msdParameters import *


class Controller:
    def __init__(self):
        self.m = m
        self.k = k
        self.b = b

        self.kp = kp
        self.kd = kd
        self.ki = ki

        self.zDot = 0.0
        self.int = 0.0
        self.e0 = 0.0
        self.z0 = 0.0
        self.sig = 0.05
        self.beta = (2.0 * self.sig - ts) / (2.0 * self.sig + ts)

    def update(self, z_r, state):
        z, zDot = state.flatten()
        f_e = k * z
        f_tilde = self.kp * (z_r - z) - self.kd * zDot
        f = f_e + f_tilde
        f = self.sat(f, fMax)
        return f

    def update2(self, z_r, state):
        z, tempo = state.flatten()
        f_e = k * z
        e = z_r - z
        self.int = self.int + (ts / 2) * (e + self.e0)
        self.zDot = self.beta * self.zDot + (1 - self.beta) * (z - self.z0) / ts
        f = self.kp * e - self.kd * self.zDot + self.ki * self.int
        f = f + f_e
        f = self.sat(f, fMax)
        self.e0 = e
        self.z0 = z
        return f

    @staticmethod
    def sat(u, limit):
        if abs(u) > limit:
            u = limit * np.sign(u)
        return u
