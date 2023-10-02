import numpy as np
from msdParameters import *


class Controller:
    def __init__(self):
        self.m = m
        self.k = k
        self.b = b

        self.kp = kp
        self.kd = kd

    def update(self, z_r, state):
        z, zDot = state.flatten()
        f_e = k * z
        f_tilde = self.kp * (z_r - z) - self.kd * zDot
        f = f_e + f_tilde
        return f
