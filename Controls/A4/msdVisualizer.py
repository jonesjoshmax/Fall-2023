import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from msdParameters import *
import matplotlib
matplotlib.use('TkAgg')


class Visualizer:
    def __init__(self):
        self.fig = plt.figure()
        self.anim = self.fig.add_subplot(1, 2, 1)
        self.rect = None
        self.f = self.fig.add_subplot(2, 2, 2)
        self.z = self.fig.add_subplot(2, 2, 4)

        self.tData = np.array([t0])
        self.fData = np.array([0])
        self.zData = np.array(state0[0, 0])
        self.rData = np.array([z_r])

        # ANIMATION SUBPLOT SETUP
        self.anim.set_title('Mass Spring Damper')
        self.anim.set_yticks([])
        self.anim.set_xlabel('Position (m)')

        # FORCE SUBPLOT SETUP
        self.f.set_title('Controller Force Response')
        self.f.set_xlabel('Time (s)')
        self.f.set_ylabel('Force (N)')
        self.f.grid(True)

        # DISPLACEMENT SUBPLOT SETUP
        self.z.set_title('MSD Displacement')
        self.z.set_xlabel('Time (s)')
        self.z.set_ylabel('Displacement (m)')
        self.z.legend(loc='upper right')
        self.z.grid(True)

        self.fig.tight_layout()
        plt.pause(10)

    def update(self, state, f, r):
        self.tData = np.append(self.tData, self.tData[-1] + ts)
        self.fData = np.append(self.fData, f)
        self.zData = np.append(self.zData, state[0, 0])
        self.rData = np.append(self.rData, r)

        # ANIMATION PLOT
        self.anim.cla()
        self.anim.axhline(y=-sq / 2, color='black', linewidth=4, zorder=3)
        self.anim.plot([0, state[0, 0]], [0, 0], color='black', linestyle='--', zorder=1)
        self.rect = patches.Rectangle((state[0, 0] - sq / 2, -sq / 2), sq, sq, facecolor='r', zorder=2)
        self.anim.add_patch(self.rect)
        self.anim.set_xlim(0, 15)
        self.anim.set_ylim(-7.5, 7.5)

        # FORCE SUBPLOT
        self.f.cla()
        self.f.set_title('Controller Force Response')
        self.f.set_xlabel('Time (s)')
        self.f.set_ylabel('Force (N)')
        self.f.grid(True)
        self.f.plot(self.tData, self.fData, label='Force', color='r')

        # DISPLACEMENT SUBPLOT
        self.z.cla()
        self.z.set_title('MSD Displacement')
        self.z.set_xlabel('Time (s)')
        self.z.set_ylabel('Displacement (m)')
        self.z.plot(self.tData, self.zData, label='Pos', color='r')
        self.z.plot(self.tData, self.rData, label='Ref', color='r', linestyle='--')
        self.z.legend(loc='upper right')
        self.z.grid(True)

        self.fig.tight_layout()

        plt.pause(ts)
