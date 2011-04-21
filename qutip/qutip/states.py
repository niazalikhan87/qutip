#This file is part of QuTIP.
#
#    QuTIP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#    QuTIP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with QuTIP.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2011, Paul D. Nation & Robert J. Johansson
#
###########################################################################
from scipy import *
from Qobj import Qobj
from basis import basis

def coherent_state(N, alpha):
    """
    Generate the matrix representation of a coherent state
    N the number of states
    alpha the coherent state amplitude (complex)
    """
    data = zeros([N,N])
    for m in range(N):
        for n in range(N):
            data[m,n] = exp(-abs(alpha) ** 2) * ((alpha ** n) / sqrt(factorial(n))) * ((conjugate(alpha) ** m) / sqrt(factorial(m)))

    return Qobj(data);

def dm_fock_state(N, m):
    """
    Generate the density matrix for a fock state

    @param N the number of states
    @param m the fock state number
    """
    psi = basis(N, m)
    return psi * psi.dag()

