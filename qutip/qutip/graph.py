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
# Copyright (C) 2011-2012, Paul D. Nation & Robert J. Johansson
#
###########################################################################

from pylab import *
from matplotlib import cm
from qutip.istests import *


#
# A collection of various visalization functions.
#


# Adopted from the SciPy Cookbook.
def _blob(x, y, w, w_max, area):
    """
    Draws a square-shaped blob with the given area (< 1) at
    the given coordinates.
    """
    hs = sqrt(area) / 2
    xcorners = array([x - hs, x + hs, x + hs, x - hs])
    ycorners = array([y - hs, y - hs, y + hs, y + hs])

    fill(xcorners, ycorners, color=cm.jet(int((w+w_max) * 256 / (2*w_max))))

# Adopted from the SciPy Cookbook.
def hinton(rho):
    """Draws a Hinton diagram for visualizing a density matrix. 
    
    Parameters
    ----------
    rho : qobj
        Input density matrix.
    
    Raises
    ------
    ValueError
        Input argument is not a quantum object.
        
    """
    if not isoper(rho):
        raise ValueError("argument must be a quantum operator")

    W = rho.full()

    clf()
    height, width = W.shape
  
    w_max = 1.25 * max(abs(diag(matrix(W))))
    if w_max <= 0.0:
        w_max = 1.0

    fill(array([0,width,width,0]),array([0,0,height,height]), color=cm.jet(128))
    axis('off')
    axis('equal')
    for x in range(width):
        for y in range(height):
            _x = x+1
            _y = y+1
            if real(W[x,y]) < 0.0:
                _blob(_x - 0.5, height - _y + 0.5,  abs(W[x,y]), w_max, min(1,abs(W[x,y])/w_max))
            else:
                _blob(_x - 0.5, height - _y + 0.5, -abs(W[x,y]), w_max, min(1,abs(W[x,y])/w_max))


def matrix_histogram(M, xlabels, ylabels, title, limits=None, ax=None):
    """
    Draw a histogram for the matrix M, with the given x and y labels and title.

    Parameters
    ----------
    M : Matrix of Qobj
        The matrix to visualize

    xlabels : list of strings
        list of x labels

    ylabels : list of strings
        list of y labels

    title : string
        title of the plot

    limits : list/array with two float numbers
        The z-axis limits [min, max] (optional)

    ax : a matplotlib axes instance
        The axes context in which the plot will be drawn.
    
    Returns
    -------

        An matplotlib axes instance for the plot.

    Raises
    ------
    ValueError
        Input argument is not valid.

    """

    if isinstance(M, Qobj):
        # extract matrix data from Qobj
        M = M.full()

    n=size(M) 
    xpos,ypos=meshgrid(range(M.shape[0]),range(M.shape[1]))
    xpos=xpos.T.flatten()-0.5 
    ypos=ypos.T.flatten()-0.5 
    zpos = zeros(n) 
    dx = dy = 0.8 * ones(n) 
    dz = real(M.flatten()) 
    
    if limits: # check that limits is a list type
        z_min = limits[0]
        z_max = limits[1]
    else:
        z_min = min(dz)
        z_max = max(dz)
        
    norm=mpl.colors.Normalize(z_min, z_max) 
    cmap=get_cmap('jet') # Spectral
    colors=cmap(norm(dz))

    if ax == None:
        fig = plt.figure()
        ax = Axes3D(fig, azim=-35, elev=35)

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors)
    plt.title(title)

    # x axis
    ax.axes.w_xaxis.set_major_locator(IndexLocator(1,-0.5))
    ax.set_xticklabels(xlabels) 
    ax.tick_params(axis='x', labelsize=14)

    # y axis
    ax.axes.w_yaxis.set_major_locator(IndexLocator(1,-0.5)) 
    ax.set_yticklabels(ylabels) 
    ax.tick_params(axis='y', labelsize=14)

    # z axis
    ax.axes.w_zaxis.set_major_locator(IndexLocator(1,0.5))
    ax.set_zlim3d([z_min, z_max])

    # color axis
    cax, kw = mpl.colorbar.make_axes(ax, shrink=.75, pad=.02)
    cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm)

    return ax