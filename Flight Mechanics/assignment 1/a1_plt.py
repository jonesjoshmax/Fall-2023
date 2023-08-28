import matplotlib.pyplot as plt
import a1 as p
from mpl_toolkits.mplot3d.art3d import Line3DCollection

s = p.points
segments = [
    [(s[0]), (s[1])],   # FUSELAGE CONNECTORS
    [(s[0]), (s[2])],
    [(s[0]), (s[3])],
    [(s[0]), (s[4])],
    [(s[5]), (s[1])],
    [(s[5]), (s[2])],
    [(s[5]), (s[3])],
    [(s[5]), (s[4])],
    [(s[1]), (s[2])],
    [(s[2]), (s[3])],
    [(s[3]), (s[4])],
    [(s[4]), (s[1])],
    [(s[6]), (s[7])],   # FRONT WING
    [(s[7]), (s[8])],
    [(s[8]), (s[9])],
    [(s[9]), (s[6])],
    [(s[10]), (s[11])],   # TAIL WING
    [(s[11]), (s[12])],
    [(s[12]), (s[13])],
    [(s[13]), (s[10])],
    [(s[5]), (s[14])],   # VERT STAB
    [(s[14]), (s[15])],
    [(s[15]), (s[5])],
]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
wireframe = Line3DCollection(segments, colors='r')

ax.add_collection3d(wireframe)
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])

plt.show()
