import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from vtolParameters import *
import matplotlib

matplotlib.use('TkAgg')


class Visualizer:
    def __init__(self):
        # DATA ARRAY INITIALIZATION
        self.tData = np.array([])
        self.fData = np.array([])
        self.zData = np.array([])
        self.hData = np.array([])
        self.thData = np.array([])
        self.rData = np.array([])
        self.flag = False

        # FIGURE INITIALIZATION
        self.fig = plt.figure()
        self.anim = self.fig.add_subplot(1, 2, 1)
        self.body = None
        self.prop_1 = None
        self.prop_2 = None
        self.f = self.fig.add_subplot(4, 2, 2)
        self.z = self.fig.add_subplot(4, 2, 4)
        self.h = self.fig.add_subplot(4, 2, 6)
        self.th = self.fig.add_subplot(4, 2, 8)

        # ANIMATION SUBPLOT SETUP
        self.anim.set_title('VTOL')
        self.anim.set_xlabel('Position (m)')
        self.anim.set_ylabel('Position (m)')

        # FORCE SUBPLOT SETUP
        self.f.set_title('Controller Force Response')
        self.f.set_xlabel('Time (s)')
        self.f.set_ylabel('Force (N)')
        self.f.grid(True)

        # Z DISPLACEMENT SUBPLOT SETUP
        self.z.set_title('VTOL Height')
        self.z.set_xlabel('Time (s)')
        self.z.set_ylabel('Height (m)')
        self.z.grid(True)

        # H DISPLACEMENT SUBPLOT SETUP
        self.h.set_title('VTOL Height')
        self.h.set_xlabel('Time (s)')
        self.h.set_ylabel('Height (m)')
        self.h.grid(True)

        # TH DISPLACEMENT SUBPLOT SETUP
        self.th.set_title('VTOL Height')
        self.th.set_xlabel('Time (s)')
        self.th.set_ylabel('Height (m)')
        self.th.grid(True)

        self.fig.tight_layout()

        plt.pause(pause)

    def update(self, state, f, r, t):
        z, h, th, tempA, tempB, tempC = state.flatten()
        if not self.flag:
            self.tData = np.array([t0])
            self.fData = f
            self.zData = np.array(z)
            self.hData = np.array(h)
            self.thData = np.array(th)
            self.rData = r
            self.flag = True

        else:
            self.tData = np.append(self.tData, t)
            self.fData = np.append(self.fData, f, 1)
            self.zData = np.append(self.zData, z)
            self.hData = np.append(self.hData, h)
            self.thData = np.append(self.thData, th)
            self.rData = np.append(self.rData, r, 1)

        # ANIMATION PLOT
        xr = z + d * np.cos(-th)
        yr = h - d * np.sin(-th)
        xl = z - d * np.cos(-th)
        yl = h + d * np.sin(-th)
        self.anim.cla()
        self.anim.axhline(y=0, color='black', linewidth=1, zorder=0)
        self.anim.plot([xl, xr], [yl, yr], color='black', linewidth=1, zorder=1)
        self.body = patches.Rectangle((z - cSize / 2, h - cSize / 2), cSize, cSize, angle=np.rad2deg(th), color='r',
                                      zorder=2)
        self.prop_1 = patches.Rectangle((xl - dSize / 2, yl - dSize / 2), dSize, dSize, angle=np.rad2deg(th),
                                        facecolor='r', zorder=3)
        self.prop_2 = patches.Rectangle((xr - dSize / 2, yr - dSize / 2), dSize, dSize, angle=np.rad2deg(th),
                                        facecolor='r', zorder=4)
        self.anim.add_patch(self.body)
        self.anim.add_patch(self.prop_1)
        self.anim.add_patch(self.prop_2)
        self.anim.set_xlim(-animLim / 2, animLim / 2)
        self.anim.set_ylim(-1, animLim - 1)

        # FORCE SUBPLOT
        self.f.cla()
        self.f.set_title('Controller Force Response')
        self.f.set_xlabel('Time (s)')
        self.f.set_ylabel('Force (N)')
        self.f.plot(self.tData, self.fData[0], color='c', label='Right', linestyle='--')
        self.f.plot(self.tData, self.fData[1], color='r', label='Left', linestyle='--')
        self.f.legend(loc='upper right')
        self.f.grid(True)

        # Z SUBPLOT
        self.z.cla()
        self.z.set_title('Z Displacement')
        self.z.set_xlabel('Time (s)')
        self.z.set_ylabel('Displacement (m)')
        self.z.plot(self.tData, self.zData, label='Pos', color='r')
        self.z.plot(self.tData, self.rData[0], label='Ref', color='r', linestyle='--')
        self.z.legend(loc='upper right')
        self.z.grid(True)

        # H SUBPLOT
        self.h.cla()
        self.h.set_title('H Displacement')
        self.h.set_xlabel('Time (s)')
        self.h.set_ylabel('Displacement (m)')
        self.h.plot(self.tData, self.hData, label='Pos', color='r')
        self.h.plot(self.tData, self.rData[1], label='Ref', color='r', linestyle='--')
        self.h.legend(loc='upper right')
        self.h.grid(True)

        # TH SUBPLOT
        self.th.cla()
        self.th.set_title('Angular Displacement')
        self.th.set_xlabel('Time (s)')
        self.th.set_ylabel('Displacement (radians)')
        self.th.plot(self.tData, self.thData, label='Pos', color='r')
        self.th.grid(True)

        self.fig.tight_layout()
        plt.pause(ts)
