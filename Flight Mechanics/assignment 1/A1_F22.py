import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation
from stl import mesh
import rotations as r


class Assign1:
    def __init__(self, file):
        self.filename = file

    @property
    def stl_to_vertices(self):
        mesh_data = mesh.Mesh.from_file(self.filename)
        vertices = mesh_data.vectors.reshape(-1, 3)
        return vertices


class Visualizer:
    def __init__(self, vertices):
        self.start_translation = None
        self.ax_translations = None
        self.ax_angles = None
        self.x_center = None
        self.y_center = None
        self.max_range = None
        self.z_range = None
        self.x_range = None
        self.y_range = None
        self.z_center = None
        self.fig = None
        self.ax = None
        self.vertices = vertices
        self.t0 = 0.0
        self.t1 = 12.0
        self.ts = 0.01
        self.freq = self.t1 / (6 * 2 * np.pi)
        self.f_count = int(self.t1 / self.ts)
        self.pitch_max = pi / 4
        self.roll_max = pi / 4
        self.yaw_max = pi / 4

        # Initialize arrays to store angles and translations
        self.angles = np.zeros((self.f_count, 3))
        self.translations = np.zeros((self.f_count, 3))

    def initialize(self):
        # Create subplots for angles and translations
        self.fig = plt.figure(figsize=(10, 6))
        self.ax = self.fig.add_subplot(121, projection='3d')  # 3D visualization
        self.ax_angles = self.fig.add_subplot(222)  # Angles subplot
        self.ax_translations = self.fig.add_subplot(224)  # Translations subplot

        faces = np.arange(0, len(self.vertices)).reshape(-1, 3)
        poly3d = Poly3DCollection([self.vertices[polygon] for polygon in faces], facecolors='grey', linewidths=.25,
                                  edgecolors='black')
        self.ax.add_collection3d(poly3d)
        self.x_range = self.vertices[:, 0].ptp()
        self.y_range = self.vertices[:, 1].ptp()
        self.z_range = self.vertices[:, 2].ptp()
        self.max_range = max(self.x_range, self.y_range, self.z_range)
        self.x_center = (self.vertices[:, 0].min() + self.vertices[:, 0].max()) / 2
        self.y_center = (self.vertices[:, 1].min() + self.vertices[:, 1].max()) / 2
        self.z_center = (self.vertices[:, 2].min() + self.vertices[:, 2].max()) / 2
        self.ax.set_xlim([self.x_center - self.max_range / 2, self.x_center + self.max_range / 2])
        self.ax.set_ylim([self.y_center - self.max_range / 2, self.y_center + self.max_range / 2])
        self.ax.set_zlim([self.z_center - self.max_range / 2, self.z_center + self.max_range / 2])

        # Set up angles subplot
        self.ax_angles.grid(True)
        self.ax_angles.set_title('Angles')
        self.ax_angles.set_xlabel('Time (10 ms)')
        self.ax_angles.set_ylabel('Angle (degrees)')

        # Set up translations subplot
        self.ax_translations.grid(True)
        self.ax_translations.set_title('Translations')
        self.ax_translations.set_xlabel('Time (10 ms)')
        self.ax_translations.set_ylabel('Translation')

    def update(self, frame):
        self.ax.cla()
        vert = self.vertices
        angle = np.array([0, 0, 0])
        t = frame * self.ts
        if 0 < frame < self.f_count / 6:
            angle = self.pitch_max * np.array([np.sin(t / self.freq), 0, 0])
        elif self.f_count / 6 <= frame < self.f_count / 3:
            angle = self.roll_max * np.array([0, np.sin(t / self.freq), 0])
        elif self.f_count / 3 <= frame < self.f_count / 2:
            angle = self.yaw_max * np.array([0, 0, np.sin(t / self.freq)])
        elif self.f_count / 2 <= frame < self.f_count * 2 / 3:
            vert[:, 1] += 2.5 * np.cos(t / self.freq)
        elif self.f_count * 2 / 3 <= frame < self.f_count * 5 / 6:
            vert[:, 0] += 2.5 * np.cos(t / self.freq)
        else:
            vert[:, 2] += 2.5 * np.cos(t / self.freq)

        if frame == 0:
            self.start_translation = np.mean(vert, axis=0)

        translation = np.mean(vert, axis=0) - self.start_translation

        if 0 < frame < self.f_count / 2:
            r_mat = r.Euler2Rotation(angle[0], angle[1], angle[2])
            vert = np.matmul(vert, r_mat)

        self.angles[frame, :] = angle
        self.translations[frame, :] = translation

        faces = np.arange(0, len(vert)).reshape(-1, 3)
        poly3d = Poly3DCollection([vert[polygon] for polygon in faces], facecolors='grey', linewidths=.25,
                                  edgecolors='black')
        self.ax.add_collection3d(poly3d)
        self.ax.set_xlim([self.x_center - self.max_range / 2, self.x_center + self.max_range / 2])
        self.ax.set_ylim([self.y_center - self.max_range / 2, self.y_center + self.max_range / 2])
        self.ax.set_zlim([self.z_center - self.max_range / 2, self.z_center + self.max_range / 2])

        # ANGLES
        self.ax_angles.clear()
        self.ax_angles.plot(range(frame + 1), np.degrees(self.angles[:frame + 1, 0]), label='Pitch (Degrees)',
                            color='r')
        self.ax_angles.plot(range(frame + 1), np.degrees(self.angles[:frame + 1, 1]), label='Roll (Degrees)', color='g')
        self.ax_angles.plot(range(frame + 1), np.degrees(self.angles[:frame + 1, 2]), label='Yaw (Degrees)', color='b')
        self.ax_angles.grid(True)
        self.ax_angles.legend(loc='upper right')
        self.ax_angles.set_title('Angles')
        self.ax_angles.set_xlabel('Time (10 ms)')
        self.ax_angles.set_ylabel('Angle (degrees)')

        # TRANSLATIONS
        self.ax_translations.clear()
        self.ax_translations.plot(range(frame + 1), self.translations[:frame + 1, 1], label='X (m)', color='r')
        self.ax_translations.plot(range(frame + 1), self.translations[:frame + 1, 0], label='Y (m)', color='g')
        self.ax_translations.plot(range(frame + 1), self.translations[:frame + 1, 2], label='Z (m)', color='b')
        self.ax_translations.grid(True)
        self.ax_translations.legend(loc='upper right')
        self.ax_translations.set_title('Translations')
        self.ax_translations.set_xlabel('Time (10 ms)')
        self.ax_translations.set_ylabel('Translation')


temp = Assign1('f22.stl')
vertices = temp.stl_to_vertices
visualizer = Visualizer(vertices)
visualizer.initialize()


def init():
    return visualizer.ax,


ani = FuncAnimation(
    visualizer.fig,
    visualizer.update,
    frames=visualizer.f_count,
    init_func=init,
    interval=1,
    blit=False,
    repeat=True
)

plt.show()
