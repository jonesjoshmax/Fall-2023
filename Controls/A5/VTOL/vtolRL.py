from vtolParameters import *
import control as ctl
import matplotlib.pyplot as plt

# ROOT LOCUS H
numH = [1]
denH = [mc + 2 * mr, kdH, kpH, 0]
tfH = ctl.tf(numH, denH)
ctl.rlocus(tfH)

# ROOT LOCUS Z
numZ = [-(g * (mc + 2 * mr))]
denZ = [mc + 2 * mr, mu - (g * (mc + 2 * mr)) * kdZ, -(g * (mc + 2 * mr)) * kpZ, 0]
tfZ = ctl.tf(numZ, denZ)
ctl.rlocus(tfZ)
