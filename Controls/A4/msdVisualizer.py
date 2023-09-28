import matplotlib.pyplot as plt
import numpy as np
from msdParameters import *
import matplotlib
matplotlib.use('TkAgg')


class Visualizer:
    def __init__(self):
        self.fig = plt.figure()
        self.anim = self.fig.add_subplot(1, 2, 1)
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

    def update(self, state, f, r):
        self.tData = np.append(self.tData, self.tData[-1] + ts)
        self.fData = np.append(self.fData, f)
        self.zData = np.append(self.zData, state[0, 0])
        self.rData = np.append(self.rData, r)

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
