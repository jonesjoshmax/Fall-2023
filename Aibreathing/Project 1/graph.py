import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


class graph:
    def __init__(self, parameter):
        # FIGURE INITIALIZATION
        self.fig = plt.figure(figsize=(16, 10))
        self.fm = self.fig.add_subplot(2, 2, 1)
        self.tsfc = self.fig.add_subplot(2, 2, 2)
        self.f = self.fig.add_subplot(2, 2, 3)
        self.n = self.fig.add_subplot(2, 2, 4)

        # F / mDOT SUBPLOT SETUP
        self.fm.set_title('Force by ' + r'$\dot{m}_{0}$')
        self.fm.set_xlabel(parameter)
        self.fm.set_ylabel(r'$\frac{F}{\dot{m}}$ $\frac{N}{\frac{kg}{s}}$')
        self.fm.grid()

        # TSFC SUBPLOT SETUP
        self.tsfc.set_title('TSFC')
        self.tsfc.set_xlabel(parameter)
        self.tsfc.set_ylabel(r'TSFC $\frac{g}{kN-s}$')
        self.tsfc.grid()

        # FUEL AIR RATIO SUBPLOT SETUP
        self.f.set_title('Fuel Air Ratio')
        self.f.set_xlabel(parameter)
        self.f.set_ylabel(r'Ratio')
        self.f.grid()

        # EFFICIENCIES SUBPLOT SETUP
        self.n.set_title('Efficiencies')
        self.n.set_xlabel(parameter)
        self.n.set_ylabel(r'%')
        self.n.grid()

    def plot(self, data, step, cycle, param):
        fm = data[0]
        tsfc = data[1]
        f = data[2]
        nt = data[3] * 100
        np = data[4] * 100
        no = data[5] * 100

        # F / mDOT SUBPLOT
        self.fm.plot(step, fm, color='r')
        self.fm.set_xlim([min(step), max(step)])

        # TSFC SUBPLOT
        self.tsfc.plot(step, tsfc, color='r')
        self.tsfc.set_xlim([min(step), max(step)])

        # FUEL AIR RATIO SUBPLOT
        self.f.plot(step, f, color='r')
        self.f.set_xlim([min(step), max(step)])

        # EFFICIENCY SUBPLOT
        self.n.plot(step, nt, color='r', label=r'$\eta_{T}$')
        self.n.plot(step, np, color='g', label=r'$\eta_{P}$')
        self.n.plot(step, no, color='b', label=r'$\eta_{O}$')
        self.n.set_xlim([min(step), max(step)])
        self.n.legend()

        # SHOW PLOT
        self.fig.savefig(cycle + param, dpi='figure', format=None)
        self.fig.show()
