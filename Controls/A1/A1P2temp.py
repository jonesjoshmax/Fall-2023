import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


class Simulation:
    def __init__(self):
        self.mc = 1.0  # kg
        self.mr = 0.25  # kg
        self.ml = 0.25  # kg
        self.jc = 0.0042  # kgm^2
        self.d = 0.3  # m
        self.u = 0.1  # kg/s
        self.g = 9.8  # m/s^2

        self.t0 = 0.0  # s
        self.t1 = 1.0  # s
        self.ts = 0.01  # ts
        self.t_array = np.arange(self.t0, self.t1 + self.ts, self.ts)  # s
        self.initCons = [0, 0, 0, 0, 0, 0]

    def StateSpace(self, theta):
        A = np.matrix([[0, 0, 0, 1, 0, 0],
                       [0, 0, 0, 0, 1, 0],
                       [0, 0, 0, 0, 0, 1],
                       [0, 0, 0, 0, 0, 0],
                       [1, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0]
                       ])
        B = np.matrix([[0, 0],
                       [0, 0],
                       [0, 0],
                       [-np.sin(theta) / (self.mc + 2 * self.mr), -np.sin(theta) / (self.mc + 2 * self.mr)],
                       [np.cos(theta) / (self.mc + 2 * self.mr), np.cos(theta) / (self.mc + 2 * self.mr)],
                       [self.d / (self.jc + 2 * self.mr * pow(self.d, 2)),
                        self.d / (self.jc + 2 * self.mr * pow(self.d, 2))]
                       ])
        C = np.matrix([[0, 0, 0, 1, 0, 0],
                       [0, 0, 0, 0, 1, 0],
                       [0, 0, 0, 0, 0, 1],
                       ])
        D = np.matrix([[0, 0],
                       [0, 0],
                       [0, 0]])

        sys = sp.signal.StateSpace(A, B, C, D)
        u = np.ones((len(self.t_array), 2))
        t, y, x = sp.signal.lsim(sys, u, self.t_array)
        return t, y, x


sim = Simulation()
t, y, x = sim.StateSpace(np.pi / 4)
x1 = x[:, 0]
x2 = x[:, 1]
plt.figure(2)
plt.plot(t, x1, t, x2, t, y)
plt.title("Step Response")
plt.xlabel("t")
plt.ylabel("x1 and x2")
plt.grid()
plt.show()
