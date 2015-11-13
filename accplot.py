
import numpy as np
import matplotlib.pyplot as plt


#=============================================
def plotter3(filename, xcol = 0, ycol = 1, zcol = 2, title = '', 
             colormap = 'gnuplot2'):
    
    with open(filename, 'r') as infile:
        x, y, z = ([] for i in range(3))
        for line in infile:
            entries = line.split()
            x.append(float(entries[xcol]))
            y.append(float(entries[ycol]))
            z.append(np.random.rand(50))  #float(entries[zcol])
    infile.close()
    #print x, '\n', y, '\n', z
    if(len(x) == len(y) and len(y) == len(z) and len(z) == len(x)):
        plt.get_cmap(colormap)
        plt.scatter(x, y, c=z, cmap = 'gnuplot2')
        plt.rc('text', usetex=True)
        #plt.axis([xmin, xmax, ymin, ymax])
        plt.title(r'\textit{$Mass\: vs. \:semi-major \:vs. \:\epsilon_{W}$}')
        plt.ylabel(r"Mass ($M_{\oplus}$)")
        plt.xlabel('Semi-major axis ($AU$)')
        #plt.colorbar()
        plt.show()
    else:
        print 'Error: Data column sizes do not match\n'

#=============================================
def plotter3Size(filename, xcol = 0, ycol = 1, zcol = 2, title = ''):
    
    with open(filename, 'r') as infile:
        x, y, z = ([] for i in range(3))
        for line in infile:
            entries = line.split()
            x.append(float(entries[xcol]))
            y.append(float(entries[ycol]))
            z.append(float(entries[zcol]))
    infile.close()
    if(len(x) == len(y) and len(y) == len(z) and len(z) == len(x)):

        #z = [100*i for i in z] # direct version
        z = [100*i**2 for i in z] # area version
        plt.scatter(x, y, s=z)
        #plt.axis([xmin, xmax, ymin, ymax])
        plt.rc('text', usetex=True)
        plt.title(title + 
            r'\textit{$\epsilon_{W}\: vs. \:semi-major \:vs. \:mass$}')
        plt.ylabel(r"Tungsten anomaly ($\epsilon_{W}$)")
        plt.xlabel('Semi-major axis ($AU$)')
        plt.show()
    else:
        print 'Error: Data column sizes do not match\n'

#=============================================

title = '4:1 mass ratio '
plotter3Size('mass_semi_epsilon_4to1.dat', 1, 2, 0, title)

title = '8:1 mass ratio '
plotter3Size('mass_semi_epsilon_8to1.dat', 1, 2, 0, title)