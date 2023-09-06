import matplotlib.pyplot as plt
import numpy as np
import A1P2Parameters as p
from signalGenerator import signalGenerator
from A1P2Visualizer import Visualizer

# CLASS INITIATION
z_reference = signalGenerator(amplitude=0.5, frequency=0.1)
h_reference = signalGenerator(amplitude=0.5, frequency=0.1)
zRef = signalGenerator(amplitude=4.0, frequency=0.1, y_offset=5.0)
hRef = signalGenerator(amplitude=2.0, frequency=0.1, y_offset=2.0)
thetaRef = signalGenerator(amplitude=np.pi/8.0, frequency=0.5, y_offset=0.0)
fRef = signalGenerator(amplitude=5, frequency=0.5)
tauRef = signalGenerator(amplitude=5, frequency=0.5)
animation = Visualizer()

t = p.t0
while t < p.t1:
    z_r = z_reference.sin(t)
    z = zRef.sin(t)
    h_r = h_reference.square(t)
    h = hRef.sin(t)
    theta = thetaRef.sin(t)
    f = fRef.sawtooth(t)
    tau = fRef.sawtooth(t)

    state = np.array([[z], [h], [theta], [0.0], [0.0], [0.0]])
    animation.update(state, [z_r, z_r])

    t = t + p.t_plot
    plt.pause(0.1)
