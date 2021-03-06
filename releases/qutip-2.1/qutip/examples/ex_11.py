#
#Calculates the Q-function of Schrodinger cat state
#formed from a superposition of two coherent states.
#
from qutip import *
from pylab import * #loads matplotlib

def run():
    #Number of basis states
    N = 20 

    #amplitude of coherent states
    alpha=2.0+2j

    #define ladder oeprators
    a = destroy(N)

    #define displacement oeprators
    D1=displace(N,alpha)
    D2=displace(N,-alpha)

    #create superposition of coherent states
    psi=(D1+D2)*basis(N,0)

    #calculate Q-function
    xvec = linspace(-6,6,200)
    yvec=xvec
    Q=qfunc(psi,xvec,yvec)

    #plot Q-function as filled contour
    plt=contourf(xvec,yvec,Q,100)
    xlim([-6,6])
    ylim([-6,6])
    title('Q - function of Schrodinger cat')

    #add a colorbar for pseudoprobability
    cbar=colorbar(plt)#create colorbar
    cbar.ax.set_ylabel('Probability')
    #show plot
    show()
        
if __name__ == "__main__":
    run()
