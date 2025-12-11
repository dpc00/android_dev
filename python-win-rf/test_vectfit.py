from vectfit import vectfit
import numpy as np
import matplotlib as mpl

mpl.use("QT5Agg")

from pylab import *

# Create some test data using known poles and residues
# Substitute your source of data as needed

# Note our independent variable lies along the imaginary axis
test_s = 1j * np.linspace(1, 1e5, 800)

# Poles are produced in complex conjugate pairs
test_poles = [
    -4500,
    -41000,
    -100 + 5000j,
    -100 - 5000j,
    -120 + 15000j,
    -120 - 15000j,
    -3000 + 35000j,
    -3000 - 35000j,
]

# As are the associated resdiues
test_residues = [
    -3000,
    -83000,
    -5 + 7000j,
    -5 - 7000j,
    -20 + 18000j,
    -20 - 18000j,
    6000 + 45000j,
    6000 - 45000j,
]

# d == offset, h == slope
test_d = 0.2
test_h = 2e-5
test_f = vectfit.model(test_s, test_poles, test_residues, test_d, test_h)

# Run algorithm, results hopefully match the known model parameters
poles, residues, d, h = vectfit.vectfit_auto(test_f, test_s, n_poles=5)
fitted = vectfit.model(test_s, poles, residues, d, h)
figure()
# plot(test_s.imag, test_f.real)
# plot(test_s.imag, test_f.imag)
plot(test_s.imag, fitted.real)
plot(test_s.imag, fitted.imag)
show()
