from canyonVector import canyonVector
import matplotlib.pyplot as plt

at = canyonVector(dist=50, ang=30, n=300)
at.store()

fig = plt.figure()
ax = fig.add_subplot()
ax.plot(at.a[:, 0], at.a[:, 1], 'black')
ax.plot(at.b[:, 0], at.b[:, 1], 'black')
ax.set_aspect('equal')
plt.show()
