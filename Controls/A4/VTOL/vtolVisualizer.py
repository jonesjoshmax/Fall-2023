import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from vtolParameters import *
import matplotlib
matplotlib.use('TkAgg')


class Visualizer:
    def __init__(self):
        # DATA ARRAY INITIALIZATION
        self.tData = np.array([t0])
        self.fData = np.array([0])
        self.hData = np.array(state0[1, 0])
        self.rData = np.array([h_r])

        # FIGURE INITIALIZATION
        self.fig = plt.figure()
        self.anim = self.fig.add_subplot(1, 2, 1)
        self.body = None
        self.prop_1 = None
        self.prop_2 = None
        self.f = self.fig.add_subplot(2, 2, 2)
        self.h = self.fig.add_subplot(2, 2, 4)

        # ANIMATION SUBPLOT SETUP
        self.anim.set_title('VTOL')
        self.anim.set_xlabel('Position (m)')
        self.anim.set_ylabel('Position (m)')

        # FORCE SUBPLOT SETUP
        self.f.set_title('Controller Force Response')
        self.f.set_xlabel('Time (s)')
        self.f.set_ylabel('Force (N)')
        self.f.grid(True)

        # DISPLACEMENT SUBPLOT SETUP
        self.h.set_title('VTOL Height')
        self.h.set_xlabel('Time (s)')
        self.h.set_ylabel('Height (m)')
        self.h.legend(loc='upper right')
        self.h.grid(True)

        self.fig.tight_layout()

        # plt.pause(20)

    def update(self, state, f, r):
        self.tData = np.append(self.tData, self.tData[-1] + ts)
        self.fData = np.append(self.fData, f)
        self.hData = np.append(self.hData, state[1, 0])
        self.rData = np.append(self.rData, r)
        h = state[1, 0]

        # ANIMATION PLOT
        self.anim.cla()
        self.anim.axhline(y=0, color='black', linewidth=1, zorder=0)
        self.anim.plot([-d, d], [h, h], color='black', linewidth=1, zorder=1)
        self.body = patches.Rectangle((0 - cSize / 2, h - cSize / 2), cSize, cSize, facecolor='r', zorder=2)
        self.prop_1 = patches.Rectangle((-d - dSize / 2, h - dSize / 2), dSize, dSize, facecolor='r', zorder=3)
        self.prop_2 = patches.Rectangle((d - dSize / 2, h - dSize / 2), dSize, dSize, facecolor='r', zorder=4)
        self.anim.add_patch(self.body)
        self.anim.add_patch(self.prop_1)
        self.anim.add_patch(self.prop_2)
        self.anim.set_xlim(-animLim / 2, animLim / 2)
        self.anim.set_ylim(-1, animLim-1)

        # FORCE SUBPLOT
        self.f.cla()
        self.f.set_title('Controller Force Response')
        self.f.set_xlabel('Time (s)')
        self.f.set_ylabel('Force (N)')
        self.f.grid(True)
        self.f.plot(self.tData, self.fData, label='Force', color='r')

        # DISPLACEMENT SUBPLOT
        self.h.cla()
        self.h.set_title('MSD Displacement')
        self.h.set_xlabel('Time (s)')
        self.h.set_ylabel('Displacement (m)')
        self.h.plot(self.tData, self.hData, label='Pos', color='r')
        self.h.plot(self.tData, self.rData, label='Ref', color='r', linestyle='--')
        self.h.legend(loc='upper right')
        self.h.grid(True)

        self.fig.tight_layout()

        plt.pause(ts)
