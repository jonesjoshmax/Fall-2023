import numpy as np
import matplotlib.pyplot as plt

width = 5000
height = 3000
resolution = 1

dSize = width * resolution
dXY = np.linspace(-width / 2, width / 2, dSize)
dZ = np.linspace(0, height, dSize)
n = dXY.size
c = 20

x, y = np.meshgrid(dXY, dXY)

z = height / 10 * (np.cos(x / width * c) + np.cos(y / width * c))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, color='green', alpha=.5, rcount=c, ccount=c)
plt.show()
