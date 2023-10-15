import numpy as np
from bbParameters import *


class Dynamics:
    def __init__(self):
        self.state = state0
        self.ts = ts

    def update(self, force):
        self.rk4_step(force)
        y = self.h()
        return y

    @staticmethod
    def f(state, force):
        z, zDot, th, thDot = state.flatten()
        zDDot = (z * pow(thDot, 2)) - (g * np.sin(th))
        thDDot = ((force * l * np.cos(th)) - (2 * m1 * z * zDot * thDot) - (m1 * g * z * np.cos(th)) -
                  ((m2 * g * l / 2) * np.cos(th))) / ((m2 * pow(l, 2)) / 3 + (m1 * pow(z, 2)))
        return np.array([[zDot], [zDDot], [thDot], [thDDot]])

    def h(self):
        y = self.state
        return y

    def rk4_step(self, force):
        F1 = self.f(self.state, force)
        F2 = self.f(self.state + self.ts / 2 * F1, force)
        F3 = self.f(self.state + self.ts / 2 * F2, force)
        F4 = self.f(self.state + self.ts * F3, force)
        self.state += self.ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)

    @staticmethod
    def sat(u, limit):
        if abs(u) > limit:
            u = limit * np.sign(u)
        return u
