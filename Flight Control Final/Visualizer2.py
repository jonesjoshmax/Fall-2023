import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import Parameters as p
import numpy as np
import matplotlib
matplotlib.use('TkAgg')


class Visualizer:
    def __init__(self, yon):
        self.fig = None
        self.plane = None
        self.verts = None
        self.g_lim = p.g_lim
        self.ts = p.ts
        self.t = 1

        self.ang = None

        self.polyF = yon.polyF
        self.polyC = yon.polyC
        self.polyW = yon.polyW
        self.polyA = yon.polyA
        self.polyB = yon.polyB

        self.sky = np.array([110 / 255, 185 / 255, 255 / 255])
        self.fig = plt.figure()
        self.plane = self.fig.add_subplot(projection='3d', aspect='equal',
                                          facecolor=np.array([175 / 255, 100 / 255, 75 / 255]))
        self.plane.set_xlabel(r'X (m)')
        self.plane.set_ylabel(r'Y (m)')
        self.plane.set_zlabel(r'Z (m)')
        self.plane.set_xlim([-self.g_lim, self.g_lim])
        self.plane.set_ylim([-self.g_lim, self.g_lim])
        self.plane.set_zlim([-self.g_lim, self.g_lim])

    def update(self, verts, data, aSens, bSens):
        if self.t == 1:
            plt.pause(10)

        self.verts = verts
        self.ang = data[6:9]

        # PLANE SUBPLOT
        self.plane.cla()
        self.plane.set_xlabel(r'X (m)')
        self.plane.set_ylabel(r'Y (m)')
        self.plane.set_zlabel(r'Z (m)')
        faces = np.arange(0, len(self.verts)).reshape(-1, 3)
        poly3d = Poly3DCollection([self.verts[polygon] for polygon in faces], facecolors='grey', alpha=1, zorder=100)
        self.plane.add_collection3d(self.polyC)
        self.plane.add_collection3d(self.polyW)
        self.plane.add_collection3d(self.polyA)
        self.plane.add_collection3d(self.polyB)
        self.plane.add_collection3d(poly3d)
        if data[1, 0] > 25:
            for i in range(np.shape(aSens)[0]):
                self.plane.plot([data[0, 0], aSens[i, 0]], [data[1, 0], aSens[i, 1]], [data[2, 0], data[2, 0]],
                                linestyle='--', color='r', zorder=80 + i, alpha=.2)
            for i in range(np.shape(bSens)[0]):
                self.plane.plot([data[0, 0], bSens[i, 0]], [data[1, 0], bSens[i, 1]], [data[2, 0], data[2, 0]],
                                linestyle='--', color='r', zorder=90 + i, alpha=.2)
        self.plane.set_xlim([-self.g_lim + data[0, 0], self.g_lim + data[0, 0]])
        self.plane.set_ylim([-self.g_lim + data[1, 0], self.g_lim + data[1, 0]])
        self.plane.set_zlim([-self.g_lim + data[2, 0] + 50, self.g_lim + data[2, 0] + 50])
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
        self.plane.grid(False)
        self.plane.axis('off')
        self.plane.view_init(elev=80, azim=90)
        plt.pause(.1)
        self.t += 1
