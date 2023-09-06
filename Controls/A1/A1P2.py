import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
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

        self.r1 = np.random.random() * 30
        self.r2 = self.r1
        self.freq0 = np.random.random() * 10
        self.freq1 = self.freq0
        self.t0 = 0.0  # s
        self.t1 = 1.0  # s
        self.ts = 0.01  # ts
        self.t_array = np.arange(self.t0, self.t1 + self.ts, self.ts)  # s
        self.x0 = np.zeros(6)

    def dx_dt(self, x, t):
        fr = np.sin(self.freq0 * t) * self.r1 + 2 * self.r1
        fl = np.sin(self.freq1 * t) * self.r2 + 2 * self.r2
        dx1 = x[1]
        dx2 = self.d / (self.jc + 2 * self.mr * pow(self.d, 2)) * (fr - fl)
        dx3 = x[3]
        dx4 = ((fr + fl) * np.cos(x[0]) / (self.mc + 2 * self.mr)) - self.g
        dx5 = x[5]
        dx6 = -1 / (self.mc + 2 * self.mr) * ((np.sin(x[0]) * (fr + fl)) + self.u * x[4])
        return [dx1, dx2, dx3, dx4, dx5, dx6]

    def simulate(self):
        x = odeint(self.dx_dt, self.x0, self.t_array)
        fr = np.sin(self.freq0 * self.t_array) * self.r1 + 2 * self.r1
        fl = np.sin(self.freq1 * self.t_array) * self.r2 + 2 * self.r2
        data = [(t, x0[0], x0[2], x0[4]) for t, x0 in zip(self.t_array, x)]
        force_data = list(zip(self.t_array, fr, fl))
        return data, force_data


class Visualizer:
    def __init__(self, simulation_data, force_data):
        self.fig, (self.ax1, self.ax2, self.ax3, self.ax4) = plt.subplots(4, 1, figsize=(8, 12))
        self.data = simulation_data
        self.force_data = force_data
        self.line0, = self.ax1.plot([], [], lw=2, color='red')
        self.line1, = self.ax2.plot([], [], lw=2, color='red')
        self.line2, = self.ax3.plot([], [], lw=2, color='red')
        self.line3, = self.ax4.plot([], [], lw=2, color='red')

    def update_plots(self, t):
        self.line0.set_data([self.data[i][0] for i in range(t + 1)], [self.data[i][0] for i in range(t + 1)])
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.line1.set_data([self.data[i][0] for i in range(t + 1)], [self.data[i][2] for i in range(t + 1)])
        self.ax2.relim()
        self.ax2.autoscale_view()
        self.line2.set_data([self.data[i][0] for i in range(t + 1)], [self.data[i][2] for i in range(t + 1)])
        self.ax3.relim()
        self.ax3.autoscale_view()
        self.line3.set_data([self.force_data[i][0] for i in range(t + 1)], [self.force_data[i][1] for i in range(t + 1)])
        self.ax4.relim()
        self.ax4.autoscale_view()
        plt.pause(0.0001)

    def visualize(self):
        for t in range(len(self.data)):
            self.update_plots(t)


sim = Simulation()
sim_data, force_data = sim.simulate()

vis = Visualizer(sim_data, force_data)
vis.visualize()
