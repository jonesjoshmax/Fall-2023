import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import Parameters as p
import numpy as np
import matplotlib
matplotlib.use('TkAgg')


class Visualizer:
    def __init__(self):
        # FIGURE INITIALIZATION
        self.fig = None
        self.plane = None
        self.force = None
        self.moment = None
        self.ppp = None
        self.uvw = None
        self.ang = None
        self.pqr = None
        self.verts = None

        # TIME INITIALIZATION
        self.t0 = p.t0
        self.t1 = p.t1
        self.ts = p.ts
        self.t = 1

        # ARRAY INITIALIZATION
        self.t_array = p.t_array
        self.pppData = p.pDir
        self.angData = p.ang
        self.uvwData = p.uvw
        self.pqrData = p.pqr
        self.fData = p.f
        self.lmnData = p.lmn

    def initialization(self):
        self.t0 = 0
        self.t1 = 10
        self.ts = 0.01

        self.fig = plt.figure()
        self.plane = self.fig.add_subplot(1, 3, 1, projection='3d')
        self.force = self.fig.add_subplot(2, 3, 2)
        self.moment = self.fig.add_subplot(2, 3, 5)
        self.ppp = self.fig.add_subplot(4, 3, 3)
        self.uvw = self.fig.add_subplot(4, 3, 6)
        self.ang = self.fig.add_subplot(4, 3, 9)
        self.pqr = self.fig.add_subplot(4, 3, 12)
        self.fig.subplots_adjust(right=.975, top=.95, left=.025, bottom=.05, hspace=.5)

        # PLANE SUBPLOT
        self.plane.set_xlabel(r'X (m)')
        self.plane.set_ylabel(r'Y (m)')
        self.plane.set_zlabel(r'Z (m)')
        self.plane.set_xlim([-100, 100])
        self.plane.set_ylim([-100, 100])
        self.plane.set_zlim([-100, 100])

        # FORCE SUBPLOT
        self.force.set_title('Force')
        self.force.set_xlabel('Time (s)')
        self.force.set_ylabel('Newton (N)')
        self.force.plot(self.t_array[0], self.fData[0, 0], label=r'$f_{x}$', color='r')
        self.force.plot(self.t_array[0], self.fData[1, 0], label=r'$f_{y}$', color='g')
        self.force.plot(self.t_array[0], self.fData[2, 0], label=r'$f_{z}$', color='b')
        self.force.legend(loc='upper right')
        self.force.grid(True)

        # MOMENT SUBPLOT
        self.moment.set_title('Moment')
        self.moment.set_xlabel('Time (s)')
        self.moment.set_ylabel('Newton-Meter (Nm)')
        self.moment.plot(self.t_array[0], self.lmnData[0, 0], label=r'l', color='r')
        self.moment.plot(self.t_array[0], self.lmnData[1, 0], label=r'm', color='g')
        self.moment.plot(self.t_array[0], self.lmnData[2, 0], label=r'n', color='b')
        self.moment.legend(loc='upper right')
        self.moment.grid(True)

        # PPP SUBPLOT
        self.ppp.set_title(r'$p_{n}, p_{e}, p_{d}$')
        self.ppp.set_xlabel('Time (s)')
        self.ppp.set_ylabel('Position (m)')
        self.ppp.plot(self.t_array[0], self.pppData[0, 0], label=r'$p_{n}$', color='r')
        self.ppp.plot(self.t_array[0], self.pppData[1, 0], label=r'$p_{e}$', color='g')
        self.ppp.plot(self.t_array[0], self.pppData[2, 0], label=r'$p_{d}$', color='b')
        self.ppp.legend(loc='upper right')
        self.ppp.grid(True)

        # UVW SUBPLOT
        self.uvw.set_title(r'$u, v, w$')
        self.uvw.set_xlabel('Time (s)')
        self.uvw.set_ylabel('Ground Velocity (m/s)')
        self.uvw.plot(self.t_array[0], self.uvwData[0, 0], label=r'u', color='r')
        self.uvw.plot(self.t_array[0], self.uvwData[1, 0], label=r'v', color='g')
        self.uvw.plot(self.t_array[0], self.uvwData[2, 0], label=r'w', color='b')
        self.uvw.legend(loc='upper right')
        self.uvw.grid(True)

        # ANG SUBPLOT
        self.ang.set_title(r'$\phi, \theta, \psi$')
        self.ang.set_xlabel('Time (s)')
        self.ang.set_ylabel('Angles (rad)')
        self.ang.plot(self.t_array[0], self.angData[0, 0], label=r'$\phi$', color='r')
        self.ang.plot(self.t_array[0], self.angData[1, 0], label=r'$\theta$', color='g')
        self.ang.plot(self.t_array[0], self.angData[2, 0], label=r'$\psi$', color='b')
        self.ang.legend(loc='upper right')
        self.ang.grid(True)

        # PQR SUBPLOT
        self.pqr.set_title(r'$p, q, r$')
        self.pqr.set_xlabel('Time (s)')
        self.pqr.set_ylabel('Body Angles (rad)')
        self.pqr.plot(self.t_array[0], self.pqrData[0, 0], label=r'p', color='r')
        self.pqr.plot(self.t_array[0], self.pqrData[1, 0], label=r'q', color='g')
        self.pqr.plot(self.t_array[0], self.pqrData[2, 0], label=r'r', color='b')
        self.pqr.legend(loc='upper right')
        self.pqr.grid(True)

    def update(self, verts, data, f, lmn):
        self.verts = verts
        self.t += 1

        # PLANE SUBPLOT
        self.plane.cla()
        self.plane.set_xlabel(r'X (m)')
        self.plane.set_ylabel(r'Y (m)')
        self.plane.set_zlabel(r'Z (m)')
        faces = np.arange(0, len(self.verts)).reshape(-1, 3)
        poly3d = Poly3DCollection([self.verts[polygon] for polygon in faces], facecolors='red', linewidths=.25,
                                  edgecolors='black')
        self.plane.add_collection3d(poly3d)
        self.plane.set_xlim([-100, 100])
        self.plane.set_ylim([-100, 100])
        self.plane.set_zlim([-100, 100])

        # FORCE SUBPLOT
        self.force.cla()
        self.force.set_title('Force')
        self.force.set_xlabel('Time (s)')
        self.force.set_ylabel('Newton (N)')
        self.fData = np.append(self.fData, f, 1)
        self.force.plot(self.t_array[:self.t], self.fData[0], label=r'$f_{x}$', color='r')
        self.force.plot(self.t_array[:self.t], self.fData[1], label=r'$f_{y}$', color='g')
        self.force.plot(self.t_array[:self.t], self.fData[2], label=r'$f_{z}$', color='b')
        self.force.legend(loc='upper right')
        self.force.grid(True)

        # MOMENT SUBPLOT
        self.moment.cla()
        self.moment.set_title('Moment')
        self.moment.set_xlabel('Time (s)')
        self.moment.set_ylabel('Newton-Meter (Nm)')
        self.lmnData = np.append(self.lmnData, lmn, 1)
        self.moment.plot(self.t_array[:self.t], self.lmnData[0], label=r'l', color='r')
        self.moment.plot(self.t_array[:self.t], self.lmnData[1], label=r'm', color='g')
        self.moment.plot(self.t_array[:self.t], self.lmnData[2], label=r'n', color='b')
        self.moment.legend(loc='upper right')
        self.moment.grid(True)

        # PPP SUBPLOT
        self.ppp.cla()
        self.ppp.set_title(r'$p_{n}, p_{e}, p_{d}$')
        self.ppp.set_xlabel('Time (s)')
        self.ppp.set_ylabel('Position (m)')
        self.pppData = np.append(self.pppData, np.array([[data[0, 0]], [data[1, 0]], [data[2, 0]]]), 1)
        self.ppp.plot(self.t_array[:self.t], self.pppData[0], label=r'$p_{n}$', color='r')
        self.ppp.plot(self.t_array[:self.t], self.pppData[1], label=r'$p_{e}$', color='g')
        self.ppp.plot(self.t_array[:self.t], self.pppData[2], label=r'$p_{d}$', color='b')
        self.ppp.legend(loc='upper right')
        self.ppp.grid(True)

        # UVW SUBPLOT
        self.uvw.cla()
        self.uvw.set_title(r'$u, v, w$')
        self.uvw.set_xlabel('Time (s)')
        self.uvw.set_ylabel('Ground Velocity (m/s)')
        self.uvwData = np.append(self.uvwData, np.array([[data[3, 0]], [data[4, 0]], [data[5, 0]]]), 1)
        self.uvw.plot(self.t_array[:self.t], self.uvwData[0], label=r'u', color='r')
        self.uvw.plot(self.t_array[:self.t], self.uvwData[1], label=r'v', color='g')
        self.uvw.plot(self.t_array[:self.t], self.uvwData[2], label=r'w', color='b')
        self.uvw.legend(loc='upper right')
        self.uvw.grid(True)

        # ANG SUBPLOT
        self.ang.cla()
        self.ang.set_title(r'$\phi, \theta, \psi$')
        self.ang.set_xlabel('Time (s)')
        self.ang.set_ylabel('Angles (rad)')
        self.angData = np.append(self.angData, np.array([[data[6, 0]], [data[7, 0]], [data[8, 0]]]), 1)
        self.ang.plot(self.t_array[:self.t], self.angData[0], label=r'$\phi$', color='r')
        self.ang.plot(self.t_array[:self.t], self.angData[1], label=r'$\theta$', color='g')
        self.ang.plot(self.t_array[:self.t], self.angData[2], label=r'$\psi$', color='b')
        self.ang.legend(loc='upper right')
        self.ang.grid(True)

        # PQR SUBPLOT
        self.pqr.cla()
        self.pqr.set_title(r'$p, q, r$')
        self.pqr.set_xlabel('Time (s)')
        self.pqr.set_ylabel('Body Angles (rad)')
        self.pqrData = np.append(self.pqrData, np.array([[data[9, 0]], [data[10, 0]], [data[11, 0]]]), 1)
        self.pqr.plot(self.t_array[:self.t], self.pqrData[0], label=r'p', color='r')
        self.pqr.plot(self.t_array[:self.t], self.pqrData[1], label=r'q', color='g')
        self.pqr.plot(self.t_array[:self.t], self.pqrData[2], label=r'r', color='b')
        self.pqr.legend(loc='upper right')
        self.pqr.grid(True)

        plt.pause(self.ts)
