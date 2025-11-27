import os
import matplotlib as mpl
from PySpice.Spice.Parser import SpiceParser

mpl.use("QT5Agg")

import PySpice.Logging.Logging as Logging
import skrf as rf
from pylab import *

from skrf import Network
from skrf import VectorFitting
from nanovna_read import fetch_2_RI

rf.stylely()
fitting = False

from PySpice.Plot.BodeDiagram import bode_diagram

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger = Logging.setup_logging()
    sf = r'c:\projects\sNp\4mloop.s1p'
    cf = 'temp.cir'
    try:
        n = fetch_2_RI()
        n.frequency.unit = 'Hz'
        # n.write_touchstone(sf, form='ma')
    except OSError as e:
        print(e)
        n = Network(sf)
        n.frequency.unit = 'Hz'
    b3 = False
    try:
        b1 = os.path.exists(sf)
        b2 = os.path.exists(cf)
        if b1 and b2:
            b3 = os.path.getmtime(cf) < os.path.getmtime(sf)
        else:
            if b1:
                b3 = True
        fitting = b3
    except Exception as e:
        print(e)
        fitting = b3
    fitting = True
    if fitting:
        vf = VectorFitting(n)
        vf.max_iterations = 30
        vf.max_tol = 1e-6
        vf.vector_fit(2, 2, 'log')
        print("poles")
        print(vf.poles)
        print("zeroes")
        print(vf.zeros)
        vf.plot_pz(0,0)
        plt.savefig('pz.svg')
        plt.clf()
        vf.write_spice_subcircuit_s(cf)
        # vf.plot_convergence()
        # plt.savefig('convergence.svg')
        # plt.clf()
        # for i in range(0, 1):
        #     for j in range(0, 1):
        #         vf.plot_s_mag(i, j)
        #         plt.savefig('temp_s' + str(i + 1) + str(j + 1) + '.svg')
        #         plt.clf()
        # import test_lark
    mcf = 'main.cir'
    parser = SpiceParser(mcf)
    circuit = parser.build_circuit()
    print(circuit)
    # cs = circuit.simulator()
    # an = cs.ac('dec', 101, 1e6, 30e6)
    # figure = plt.figure(1, (20, 10))
    # plt.title("Bode Diagram of Simulated ?")
    # axes = (plt.subplot(211), plt.subplot(212))
    # bode_diagram(axes=axes,
    #              frequency=an.frequency,
    #              gain=20 * np.log10(np.absolute(an.vout)),
    #              phase=np.angle(an.vout, deg=False),
    #              marker='.',
    #              color='blue',
    #              linestyle='-',
    #              )
    # for axe in axes:
    #     axe.axvline(x=break_frequency, color='red')

    # plt.tight_layout()
    # plt.show()
    # print()
    # import ngspyce as ng

    # ng.source('main.cir')
    # ng.ac('dec', 201, 1e6, 30e6)
    # f = open('temp.vec', 'w')
    # print(ng.plots())
    # for p in ng.plots():
    #     for v in ng.vector_names(p):
    #         print(p, v, end='\r\n')
    #         f.writelines(p + ', ' + v + '\n')
    #         f.writelines(str(ng.vector(v, p)))
    # f.close()
