import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from bbParameters import *
import matplotlib
matplotlib.use('TkAgg')


class Visualizer:
    def __init__(self):
        # DATA ARRAY INITIALIZATION
        self.tData = np.array([])
        self.fData = np.array([])
        self.zData = np.array([])
        self.thData = np.array([])
        self.rData = np.array([])

        # FIGURE INITIALIZATION
        self.fig = plt.figure()
        self.anim = self.fig.add_subplot(1, 2, 1)
        self.ball = None
        self.f = self.fig.add_subplot(3, 2, 2)
        self.th = self.fig.add_subplot(3, 2, 4)
        self.z = self.fig.add_subplot(3, 2, 6)

        # FORCE SUBPLOT SETUP
        self.f.set_title('Controller Force Response')
        self.f.set_xlabel('Time (s)')
        self.f.set_ylabel('Force (N)')
        self.f.grid(True)

        # THETA SUBPLOT
        self.th.set_title('Rod Angle')
        self.th.set_xlabel('Time (s)')
        self.th.set_ylabel('Angle (Deg)')
        self.th.grid(True)

        # Z SUBPLOT
        self.z.set_title('Ball Displacement')
        self.z.set_xlabel('Time (s)')
        self.z.set_ylabel('Magnitude (m)')
        self.z.grid(True)

        self.fig.tight_layout()

        plt.pause(20)

    def update(self, state, f, r, t):
        self.tData = np.append(self.tData, t)
        self.fData = np.append(self.fData, f)
        z = state[0, 0]
        self.zData = np.append(self.zData, z)
        th = state[2, 0]
        self.thData = np.append(self.thData, th)
        self.rData = np.append(self.rData, r)

        # CIRCLE POSITIONING
        h = np.sqrt(pow(radius, 2) + pow(z, 2))
        phi = np.arctan(radius / z) + th
        cxy = np.array([h * np.cos(phi), h * np.sin(phi)])

        # ANIMATION PLOT
        self.anim.cla()
        self.anim.plot([0, l * np.cos(th)], [0, l * np.sin(th)], color='lightcoral', linewidth=2, zorder=1)
        self.ball = patches.Circle(cxy, radius, fc='r')
        self.anim.add_patch(self.ball)
        a = 0.25
        self.anim.set_xlim(0 - a, win - a)
        self.anim.set_ylim(-win / 2, win / 2)

        # FORCE SUBPLOT
        self.f.cla()
        self.f.set_title('Controller Force Response')
        self.f.set_xlabel('Time (s)')
        self.f.set_ylabel('Force (N)')
        self.f.grid(True)
        self.f.plot(self.tData, self.fData, label='Force', color='r')
        self.f.legend(loc='upper right')

        # Z SUBPLOT
        self.z.cla()
        self.z.set_title('Z Displacement')
        self.z.set_xlabel('Time (s)')
        self.z.set_ylabel('Z (m)')
        self.z.grid(True)
        self.z.plot(self.tData, self.zData, label='Z', color='r', zorder=2)
        self.z.plot(self.tData, self.rData, label='Z Ref', color='lightcoral', linestyle='--', zorder=1)
        self.z.legend(loc='upper right')

        # THETA SUBPLOT
        self.th.cla()
        self.th.set_title('Rod Angle')
        self.th.set_xlabel('Time (s)')
        self.th.set_ylabel('Theta (rad)')
        self.th.grid(True)
        self.th.plot(self.tData, self.thData, label='Theta', color='r')
        self.th.legend(loc='upper right')

        plt.pause(ts)
