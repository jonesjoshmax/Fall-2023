import numpy as np
from vtolParameters import *


class Dynamics:
    def __init__(self):
        # INITIAL STATE
        self.state = state0

        # TIME STEP
        self.Ts = ts

        # GENERAL PARAMETERS
        self.m = mc
        self.J = jc
        self.mr = mr
        self.ml = ml
        self.d = d
        self.mu = mu

        # FORCES
        self.g = g
        self.fMax = fMax

    def update(self, fr, fl):
        self.rk4_step(fr, fl)
        y = self.h()
        return y

    def f(self, state, fr, fl):
        z, h, th, zDot, hDot, thDot = state.flatten()

        # EQUATIONS OF MOTION
        zDDot = (-1 * (fr + fl) * np.sin(th) - self.mu * zDot) / (self.m + 2 * self.mr)
        hDDot = ((fr + fl) * np.cos(th)) / (self.m + 2 * self.mr) - self.g
        thDDot = (self.d * (fr - fl)) / (self.J + 2 * self.mr * self.d ** 2)

        # RETURN XDOT
        xdot = np.array([[zDot], [hDot], [thDot], [zDDot], [hDDot], [thDDot]])

        return xdot

    def h(self):
        return self.state

    def rk4_step(self, fr, fl):
        F1 = self.f(self.state, fr, fl)
        F2 = self.f(self.state + self.Ts / 2 * F1, fr, fl)
        F3 = self.f(self.state + self.Ts / 2 * F2, fr, fl)
        F4 = self.f(self.state + self.Ts * F3, fr, fl)
        self.state += self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)
