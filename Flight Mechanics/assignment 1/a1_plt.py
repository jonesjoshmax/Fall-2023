import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.animation import FuncAnimation
import rotations as r
import a1_data as p

# Constants
runtime = 2
freq = runtime / (6 * 2 * np.pi)
ts = 0.01
angle = np.pi / 4
f_time = 500
f_count = int(runtime / ts)

s = p.points

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

segments = [[s[0], s[1]], [s[0], s[2]], [s[0], s[3]], [s[0], s[4]], [s[5], s[1]], [s[5], s[2]], [s[5], s[3]],
            [s[5], s[4]],
            [s[1], s[2]], [s[2], s[3]], [s[3], s[4]], [s[4], s[1]], [s[6], s[7]], [s[7], s[8]], [s[8], s[9]],
            [s[9], s[6]],
            [s[10], s[11]], [s[11], s[12]], [s[12], s[13]], [s[13], s[10]], [s[5], s[14]], [s[14], s[15]],
            [s[15], s[5]]]
wireframe = Line3DCollection(segments, colors='r')
ax.add_collection3d(wireframe)

ax.set_xlim([-7, 3])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])


def update_frame(frame):
    ax.cla()
    from math import pi
    import numpy as np
    t = frame * ts
    if frame < f_count / 6:
        angle = pi / 4 * np.array([np.sin(t / freq), 0, 0])
    elif f_count / 6 <= frame < 1 / 3 * f_count:
        angle = pi / 4 * np.array([0, np.sin(t / freq), 0])
    elif f_count * 1 / 3 <= frame < 1 / 2 * f_count:
        angle = pi / 4 * np.array([0, 0, np.sin(t / freq)])
    elif f_count * 1 / 2 <= frame < 2 / 3 * f_count:
        temp = p.points
        temp[:, 0] += np.cos(t / freq)
        rotated_points = temp
    elif f_count * 2 / 3 <= frame < 5 / 6 * f_count:
        temp = p.points
        temp[:, 1] += np.cos(t / freq)
        rotated_points = temp
    else:
        temp = p.points
        temp[:, 2] += np.cos(t / freq)
        rotated_points = temp
    if frame < f_count / 2:
        rotation_matrix = r.Euler2Rotation(angle[0], angle[1], angle[2])
        rotated_points = np.matmul(p.points, rotation_matrix)

    updated_segments = [[rotated_points[0], rotated_points[1]], [rotated_points[0], rotated_points[2]],
                        [rotated_points[0], rotated_points[3]], [rotated_points[0], rotated_points[4]],
                        [rotated_points[5], rotated_points[1]], [rotated_points[5], rotated_points[2]],
                        [rotated_points[5], rotated_points[3]], [rotated_points[5], rotated_points[4]],
                        [rotated_points[1], rotated_points[2]], [rotated_points[2], rotated_points[3]],
                        [rotated_points[3], rotated_points[4]], [rotated_points[4], rotated_points[1]],
                        [rotated_points[6], rotated_points[7]], [rotated_points[7], rotated_points[8]],
                        [rotated_points[8], rotated_points[9]], [rotated_points[9], rotated_points[6]],
                        [rotated_points[10], rotated_points[11]], [rotated_points[11], rotated_points[12]],
                        [rotated_points[12], rotated_points[13]], [rotated_points[13], rotated_points[10]],
                        [rotated_points[5], rotated_points[14]], [rotated_points[14], rotated_points[15]],
                        [rotated_points[15], rotated_points[5]]]

    updated_wireframe = Line3DCollection(updated_segments, colors='r')
    ax.add_collection3d(updated_wireframe)

    ax.set_xlim([-7, 3])
    ax.set_ylim([-5, 5])
    ax.set_zlim([-5, 5])


anim = FuncAnimation(fig, update_frame, frames=f_count, repeat=True, interval=5)

plt.show()
