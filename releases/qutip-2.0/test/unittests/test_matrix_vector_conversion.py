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


from qutip import *

import unittest

class TestMatrixVector(unittest.TestCase):

    """
    A test class for the QuTiP function for matrix/vector conversion.
    """

    def setUp(self):
        """
        setup
        """

    def testMatrixVectorMatrix(self):
        """
        Conversion matrix to vector to matrix
        """
        M = rand(10, 10)
        V = mat2vec(M)
        M2 = vec2mat(V)
        self.assertTrue(norm(M-M2) == 0.0)

    def testVectorMatrixVector(self):
        """
        Conversion vector to matrix to vector
        """
        V = rand(100)     # a row vector
        M = vec2mat(V)
        V2 = mat2vec(M).T # mat2vec returns a column vector
        self.assertTrue(norm(V-V2) == 0.0)
        
        
    def testVectorMatrixIndexConversion(self):
        """
        Conversion between matrix and vector indices
        """
        N = 10 
        for I in range(N*N):
            i,j = vec2mat_index(N, I)
            I2  = mat2vec_index(N, i, j) 
            self.assertTrue(I == I2)

    def testVectorMatrixIndexCompability(self):
        """
        Test compability between matrix/vector conversion and the corresponding
        index conversion.
        """
        N = 10 
        M = rand(N, N)
        V = mat2vec(M)
        for I in range(N*N):
            i,j = vec2mat_index(N, I)
            self.assertTrue(V[I][0] == M[i,j])


if __name__ == '__main__':

    unittest.main()
