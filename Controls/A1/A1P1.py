import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib
import time

matplotlib.use('TkAgg')


class Simulation:
    def __init__(self):
        self.m = 5.0
        self.k = 3.0
        self.b = 0.5
        self.freq = 10
        self.amp = 10
        self.z_0 = [0, 0]
        self.t = 0.0
        self.t_end = 90
        self.ts = 0.04
        self.t_array = np.arange(self.t, self.t_end + self.ts, self.ts)

    def dz_dt(self, z, t):
        F = np.sin(self.freq * t) * self.amp
        dz1 = z[1]
        dz2 = (F - self.b * z[1] - self.k * z[0]) / self.m
        return [dz1, dz2]

    def run_simulation(self):
        z = odeint(self.dz_dt, self.z_0, self.t_array)
        F = np.sin(self.freq * self.t_array) * self.amp
        data = [(t, z_0[0]) for t, z_0 in zip(self.t_array, z)]
        force_data = list(zip(self.t_array, F))
        return data, force_data


class Visualizer:
    def __init__(self, simulation_data, force_data):
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(8, 12))
        self.line, = self.ax1.plot([], [], lw=2, color='red')
        self.force_line, = self.ax3.plot([], [], lw=2, color='red')
        self.dashed_line, = self.ax2.plot([], [], lw=2, color='black', linestyle='--')
        self.vertical_line, = self.ax2.plot([], [], lw=2, color='black')  # Vertical line in the second plot
        self.ground, = self.ax2.plot([], [], lw=2, color='black')  # New horizontal line below square
        self.point = self.ax2.scatter([], [], marker='s', color='red', s=150)
        self.ax1.set_xlabel('Time (s)')
        self.ax1.set_ylabel('Position (m)')
        self.ax2.set_xlabel('Position (m)')
        self.ax2.set_xlim(-1, 1)
        self.ax2.set_ylim(-1, 1)
        self.ax3.set_xlabel('Time (s)')
        self.ax3.set_ylabel('Force (N)')
        self.data = simulation_data
        self.force_data = force_data

    def update_plots(self, t):
        if t == 1:
            plt.pause(10)
        z_0 = self.data[t][1]
        self.line.set_data([self.data[i][0] for i in range(t + 1)], [self.data[i][1] for i in range(t + 1)])
        self.point.set_offsets([(z_0, 0)])
        self.force_line.set_data([self.force_data[i][0] for i in range(t + 1)],
                                 [self.force_data[i][1] for i in range(t + 1)])
        self.dashed_line.set_data([-.75, z_0], [0, 0])  # Update horizontal line position
        self.vertical_line.set_data([-.75, -.75], [-1, 1])  # Update vertical line position
        self.ground.set_data([-10, 10], [-.1, -.1])  # Update new horizontal line position
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax1.width(1)
        self.ax3.relim()
        self.ax3.autoscale_view()
        self.ax3.width(1)
        plt.pause(0.0001)
        self.ax2.set_yticklabels([])

    def visualize(self):
        for t in range(len(self.data)):
            self.update_plots(t)


sim = Simulation()
simulation_data, force_data = sim.run_simulation()

vis = Visualizer(simulation_data, force_data)
vis.visualize()
