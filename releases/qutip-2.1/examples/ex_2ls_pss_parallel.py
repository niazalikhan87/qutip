#
# Landau-Zener-Stuckelberg interferometry: steady state of repeated Landau-Zener
# like avoided-level crossing, as a function of driving amplitude and bias.
#
from qutip import *
import os
import time

# set up the parameters and start calculation
delta  = 1.0  * 2 * pi  # qubit sigma_x coefficient
w      = 2.0  * 2 * pi  # driving frequency
T      = 2 * pi / w     # driving period 
gamma1 = 0.00001        # relaxation rate
gamma2 = 0.005          # dephasing  rate

eps_list = linspace(-10.0, 10.0, 101) * 2 * pi
A_list   = linspace(  0.0, 10.0, 101) * 2 * pi

# pre-calculate the necessary operators
sx = sigmax(); sz = sigmaz(); sm = destroy(2); sn = num(2)

# collapse operators
c_op_list = [sqrt(gamma1) * sm, sqrt(gamma2) * sz]  # relaxation and dephasing

# ODE settings (for list-str format)
options = Odeoptions()
options.rhs_reuse = True
options.atol = 1e-6 # reduce accuracy to speed
options.rtol = 1e-5 # up the calculation a bit

# for function-callback style time-dependence
def hamiltonian_t(t, args):
    """ evaluate the hamiltonian at time t. """
    H0 = args[0]
    H1 = args[1]
    w  = args[2]
    return H0 + H1 * sin(w * t)

# a task function for the for-loop parallelization: 
# the m-index is parallelized in loop over the elements of p_mat[m,n]
def task(args):

    m, eps = args
    H0 = - delta/2.0 * sx - eps/2.0 * sz
    p_mat_m = zeros(len(A_list))

    # this trick avoid problem with cython code generator in 
    # multiple threads trying to write to the same file (for list-str format)
    if options.rhs_filename == None:
        odeconfig.cgen_num = os.getpid()

    for n, A in enumerate(A_list):
        H1 = (A/2) * sz

        # function callback format
        #args = (H0, H1, w); H_td = hamiltonian_t

        # list-str format
        args = {'w': w}; H_td = [H0, [H1, 'sin(w * t)']]

        # list-function format
        #args = w; H_td = [H0, [H1, lambda t, w: sin(w * t)]]

        U = propagator(H_td, T, c_op_list, args, options)
        rho_ss = propagator_steadystate(U)

        p_mat_m[n] = real(expect(sn, rho_ss))

    return [m, p_mat_m]

# start a parallel for loop over the list bias point values (eps_list)
start_time = time.time()
p_mat_list = parfor(task, enumerate(eps_list))
print 'time elapsed = ' + str(time.time() - start_time) 

# assemble a matrix p_mat from list of (index,array) tuples returned by parfor
p_mat = zeros((len(eps_list),len(A_list)))
for m, p_mat_m in p_mat_list:
    p_mat[m,:] = p_mat_m

# Plot the results
from pylab import *
A_mat, eps_mat = meshgrid(A_list/(2*pi), eps_list/(2*pi))
pcolor(eps_mat, A_mat, p_mat)
xlabel(r'Bias point $\epsilon$')
ylabel(r'Amplitude $A$')
title('Steadystate excitation probability\n$H = -\\frac{1}{2}\\Delta\\sigma_x -\\frac{1}{2}\\epsilon\\sigma_z - \\frac{1}{2}A\\sin(\\omega t)$\n')
show()
