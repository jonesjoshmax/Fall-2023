import numpy as np
from msdParameters import *


class Dynamics:
    def __init__(self):
        self.m = m
        self.k = k
        self.b = b
        self.state = state0
        self.ts = ts

    def update(self, force):
        self.rk4_step(force)
        y = self.h()
        return y

    def f(self, state, force):
        z, zDot = state.flatten()
        f = force
        zDDot = (f - self.b * zDot - self.k * z) / self.m
        return np.array([[zDot], [zDDot]])

    def h(self):
        y = self.state
        return y

    def rk4_step(self, force):
        # RK4 INTEGRATION
        F1 = self.f(self.state, force)
        F2 = self.f(self.state + self.ts / 2 * F1, force)
        F3 = self.f(self.state + self.ts / 2 * F2, force)
        F4 = self.f(self.state + self.ts * F3, force)
        self.state += self.ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)
