
##############################################################################
# Python 2.7.0 script to create plots from datagrabber.py output.
#
# Nick Zube, completed v1.0 on 2015-11-12
#
##############################################################################

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# Output files to read from
files = ('mass_semi_epsilon_4to1.dat','mass_semi_epsilon_8to1.dat')

# Actual values for current planets
Earth = {'mass':1.,'semi':1.,'hfw':[9.,18.],'area':1.**(2./3.),
         'eps':[1.8,2.],'color':'blue','name':'Earth'}
Mars = {'mass':0.107,'semi':1.524,'hfw':[2.,4.],'area':0.107**(2./3.),
        'eps':[2.1,2.5],'color':'red','name':'Mars'}
Venus = {'mass':0.815,'semi':0.723,'hfw':[0,0],'area':0.815**(2./3.),
        'eps':[0,0],'color':'yellow','name':'Venus'}

# Datagrabber.py output, by column number:
#(0       1    2    3    4   5    6       7      8     9     10    11)
#(mass, semi, eps, hfw, id, run, m_t90, m2_t90, t90, imass, isemi  mw-semi)
outCols = {'mass':0,'semi':1, 'eps':2, 'hfw':3, 'id':4, 'run':5, 'm_t90':6, 
           't90':8, 'imass':9, 'isemi':10, 'ssum':11}
vartypes = {'mass':'mass','semi':'semi-major\:axis', 'eps':'\epsilon_{W}', 
            'hfw':'mantle\:f^{Hf/W}', 'id':'ID', 'run':'Run #', 
            'm_t90':'90%\:mass', 
            't90':'time\:when\:90%\:of\:final\:mass\:is\:accreted', 
           'imass':'initial\:mass', 'isemi':'initial\:semi-major\:axis',
           'ssum':'mass-weighted\:semi-major\:axis'}
varunits = {'mass':'M_{E}','semi':'AU', 'eps':'', 'hfw':'', 'id':'', 'run':'',
            'm_t90':'M_{E}', 't90':'Myr','imass':'M_{E}', 'isemi':'AU',
            'ssum':'AU'}

# Function for initial mantle f_Hf/W
fhfw_func = lambda a: 13.+(12.*(2./math.pi)*np.arctan((1.3-a)/0.3))


#=============================================
# Local: plot actual values for present-day planets
def addPlanets(xvar,yvar,plotMass=False,massZoom=150.,planets=[Earth,Mars]):

    for planet in planets:

        # Error control
        ############################################
        if 'name' in planet: nom = planet['name']
        else: nom = '{NAME UNKNOWN - not assigned}'

        if 'color' not in planet: 
            print 'No color assigned for planet', nom
            planet['color'] = "none"

        if (xvar or yvar) not in planet: 
            print ('x or y value requested in def addPlanets is not ' +
            'present in planet ' + nom)
            continue

        if (xvar or yvar) is ('color' or 'name' or 'area'):
            print ('x or y value requested in def addPlanets is not ' +
            'plottable for planet ' + nom)
            continue
        ############################################

        # If a characteristic has two values in an array, this is a 
        # spread of uncertainty.
        uncertainX = isinstance(planet[xvar],list)
        uncertainY = isinstance(planet[yvar],list)
        # Set what no uncertainty will be visually represented as on a box
        minUnc = 0.01

        # Generate uncertainty lengths, midpoints, and box corners
        if uncertainX:
            xlen = planet[xvar][1] - planet[xvar][0]
            xmid = planet[xvar][1] - (xlen/2.)
            x = planet[xvar][0]
        else:
            xlen, xmid, x = minUnc, planet[xvar], planet[xvar]-(minUnc/2.)

        if uncertainY:
            ylen = planet[yvar][1] - planet[yvar][0]
            ymid = planet[yvar][1] - (ylen/2.)
            y = planet[yvar][0]
        else:
            ylen, ymid, y = minUnc, planet[yvar], planet[yvar]-(minUnc/2.)

        # Case 1: Either uncertain. Use boxes to represent.
        # Rectangle((xpos,ypos),xlen,ylen,darkness(0-1),color_string)
        if uncertainX or uncertainY:
            ax1 = plt.gca()
            print x,y,xlen,ylen,'AND',xmid,ymid
            ax1.add_patch(
                patches.Rectangle((x,y),xlen,ylen,alpha=0.3,
                                  facecolor=planet['color']))
            # If masses represented, plot dots as well, 
            # using midpoint of uncertainty as location.
            if plotMass:
                plt.scatter(xmid, ymid, massZoom*planet['area'], 
                            c=planet['color'])
            addNote(planet['name'],xmid,ymid,xmid-70.,ymid-30)

        # Case 2: Neither uncertain. Use dots.
        elif not (uncertainX or uncertainY):
            if plotMass:
                plt.scatter(planet[xvar],planet[yvar],
                            massZoom*planet[area], c=planet['color'])
            else:
                plt.scatter(planet[xvar], planet[yvar], 
                            c=planet['color'])
            addNote(planet['name'],xmid,ymid,xmid-60,ymid-20)

#=============================================
# Local: add a text annotation with an arrow to a point
def addNote(text,x,y,xtext,ytext):
    plt.annotate(
        text, xy=(x,y), xycoords='data',
        xytext=(xtext, ytext), textcoords='offset points', 
        arrowprops=dict(arrowstyle="->"))


#=============================================
# Local: return plot labels
def getLabels(filename, xvar, yvar):

    title = getTitle(filename)
    title2 = ('$' + vartypes[yvar] + '\: vs. \:' + 
              vartypes[xvar] + '$')

    if varunits[xvar] is not '':
        xlabel = r'$\mathrm{' + vartypes[xvar] + ', ' + varunits[xvar] + '}$'
    else:
        xlabel = r'$\mathrm{' + vartypes[xvar] + '}$'

    if varunits[yvar] is not '':
        ylabel = r'$\mathrm{' + vartypes[yvar] + ', ' + varunits[yvar] + '}$'
    else:
        ylabel = 'mantle ' + r'$\mathrm{' + vartypes[yvar] + '}$'

    return [title,title2,xlabel,ylabel]

#=============================================
# Local: return data type based on title
def getTitle(filename):

    if '4' in filename: title = '4:1 mass ratio'
    elif '8' in filename: title = '8:1 mass ratio'
    else: title = ''
    return title

#=============================================
# Local: read file and creat plot points
def barePlotter(filename, xvar, yvar, plotMass=False, massZoom=150, 
                col='grey',getMax=False):

    with open(filename, 'r') as infile:    
        x, y, m = ([] for i in range(3))
        for line in infile:
            entries = line.split()
            x.append(float(entries[outCols[xvar]]))
            y.append(float(entries[outCols[yvar]]))
            m.append(float(entries[outCols['mass']]))
        infile.close()

    name = getTitle(filename)
    if (len(x) and len(y)) == len(m):
        if plotMass:
            area = [massZoom*i**(2./3.) for i in m]
            plt1 = plt.scatter(x, y, s=area, c=col, marker='o', 
                               label=name)
        else:
            plt1 = plt.scatter(x, y, c=col, marker='o',label=name)
    else:
        print 'Error: Input column sizes dont match in def barePlotter\n'
        return

    if getMax:
        return[plt1,[min(x),max(x),min(y),max(y)]]
    else:
        return plt1

#=============================================
# Global: Plot function given string arguments to set variables
def plotter(filename, xvar, yvar, plotMass=False, massZoom=150., 
            addPlanetz=False,axis=[],getMax=True):

    # Enable TeX formatting and create labels
    plt.rc('text', usetex=True)

    # Set axis limits
    if getMax:
        plt1, axis = barePlotter(filename, xvar, yvar, plotMass, massZoom,
                                 getMax=getMax)
    else:
        plt1 = barePlotter(filename, xvar, yvar, plotMass, massZoom)        

    if addPlanetz:
        addPlanets(xvar,yvar,plotMass=plotMass,massZoom=massZoom)
    if axis:
        xmin, xmax, ymin, ymax = axis[0], axis[1], axis[2], axis[3]
        plt.axis([0, xmax*1.3, 0, ymax*1.3])

    [title,title2,xlabel,ylabel] = getLabels(filename, xvar, yvar)
    plt.title(title + ' ' + title2)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

#=============================================
# Global: Histogram function given string argument to set variable
def hist(filename, xvar, bins=[]):

    # Enable TeX formatting and create labels
    plt.rc('text', usetex=True)
    with open(filename, 'r') as infile:    
        x = []
        for line in infile:
            entries = line.split()
            x.append(float(entries[outCols[xvar]]))
        infile.close()

    if isinstance(bins,list):
        if len(bins) is 3:
            plt.hist(x,bins=np.linspace(bins[0],bins[1],bins[2]))
        else:
            plt.hist(x,bins=np.linspace(0,max(x)*1.2,20))
    else:
        print 'Bad argument for paramters bins in def hist'

    [title,title2,xlabel,ylabel] = getLabels(filename, xvar, xvar)
    plt.title(title + '$\:histogram$')
    plt.ylabel('$Counts$')
    plt.xlabel(xlabel)

#============================================
# Global: Plot multiple sets of data on a single plot
def multiPlotter(datasets,legend=True,axis='None',colors="cmyrgkw"):

    # Data sets are passed in the following way:
    # datasets = (set1,set2,etc...)
    # set1 = (filename, xvar, yvar, plotMass=, massZoom=, addPlanetz=)

    # If any data sets have plotMass or addPlanetz as True, they will
    # be true for all after that one. BUG: Can cause error if first is false
    # and others true.
    plts = []
    massFlag, planetFlag = False, False
    color_index = 0

    for args in datasets:

        # Default variable assignment is mixed with error checking
        filename, xvar, yvar = args[0], args[1], args[2]

        try:
            if isinstance(args[3],bool): 
                plotMass=args[3]
                if plotMass: massFlag = True
            else: plotMass = False
        except IndexError: plotMass = False

        try:
            if isinstance(args[4],(int,float)): massZoom=args[4]
            else: massZoom = 150.
        except IndexError: massZoom = 150.

        try:
            if isinstance(args[5],bool): 
                addPlanetz=args[5]
                if addPlanetz: planetFlag = True
            else: addPlanetz=False
        except IndexError: addPlanetz=False


        plts.append(barePlotter(filename, xvar, yvar, massFlag, massZoom,
                    col=colors[color_index]))
        color_index += 1

    # Set plot labels
    plt.rc('text', usetex=True)
    [title,title2,xlabel,ylabel] = getLabels(filename, xvar, yvar)
    #plt.title(title2)
    plt.ylabel(ylabel,family='serif',size='large')
    plt.xlabel(xlabel,family='sans-serif',size='large')

    if planetFlag:
        addPlanets(xvar,yvar,massFlag)

    if isinstance(axis,list):
        plt.axis([axis[0], axis[1], axis[2], axis[3]])
    if legend:
        plt.legend()



#============================================
# Add a function line to a plot
def addFunc(f,xmin=0,xmax=100):
    x = np.linspace(xmin,xmax,1000)
    y = []
    for i in range(len(x)): 
        y.append(f(x[i]))
    ax1 = plt.gca()
    ax1.plot(x,y,'black')
#=============================================




datasets = []
for i in files:
    # dataset is [filename, xvar, yvar, plotMass=, massZoom=, addPlanetz=]
    datasets.append([i,'semi','hfw',True,150.,True])
multiPlotter(datasets,axis=[0,4,0,25])
addFunc(fhfw_func,xmin=0,xmax=4)
plt.show()



# Plot a single data set with a function
#for i in files:
#    plotter(i, xvar='semi', yvar='ssum',plotMass=False)
#    plt.show()

#for i in files:
#    plotter(i, xvar='semi', yvar='ssum',plotMass=False)
#    plt.show()






##################
# EXAMPLES
###################

# Plot a histogram
#for i in files:
#    hist(i, xvar='semi')
#    plt.show()


# Plot a single data set with a function
#for i in files:
#    plotter(i, xvar='semi', yvar='hfw',plotMass=True)
#    addFunc(fhfw_func,xmin=0,xmax=4)
#    plt.show()

# Plot two data sets
#datasets = []
#for i in files:
    # dataset is [filename, xvar, yvar, plotMass=, massZoom=, addPlanetz=]
#    datasets.append([i,'semi','hfw',True,150.,True])
#multiPlotter(datasets)
#plt.show()

'''
datasets = []
for i in files:
    # dataset is [filename, xvar, yvar, plotMass=, massZoom=, addPlanetz=]
    datasets.append([i,'semi','eps',False,150.,True])
multiPlotter(datasets)
plt.show()

datasets = []
for i in files:
    # dataset is [filename, xvar, yvar, plotMass=, massZoom=, addPlanetz=]
    datasets.append([i,'semi','eps',True,150.,True])
multiPlotter(datasets)
plt.show()


datasets = []
for i in files:
    # dataset is [filename, xvar, yvar, plotMass=, massZoom=, addPlanetz=]
    datasets.append([i,'semi','hfw',False,150.,True])
multiPlotter(datasets)
addFunc(fhfw_func,xmin=0,xmax=4)
plt.show()

datasets = []
for i in files:
    # dataset is [filename, xvar, yvar, plotMass=, massZoom=, addPlanetz=]
    datasets.append([i,'semi','hfw',True,150.,True])
multiPlotter(datasets)
addFunc(fhfw_func,xmin=0,xmax=4)
plt.show()

datasets = []
for i in files:
    # dataset is [filename, xvar, yvar, plotMass=, massZoom=, addPlanetz=]
    datasets.append([i,'mass','eps',False,150.,True])
multiPlotter(datasets)
plt.show()

datasets = []
for i in files:
    # dataset is [filename, xvar, yvar, plotMass=, massZoom=, addPlanetz=]
    datasets.append([i,'eps','hfw',False,150.,True])
multiPlotter(datasets)
plt.show()

datasets = []
for i in files:
    datasets.append([i,'eps','hfw',True,150.,True])
multiPlotter(datasets)
plt.show()

datasets = []
for i in files:
    datasets.append([i,'mass','hfw',False,150.,True])
multiPlotter(datasets)
plt.show()

datasets = []
for i in files:
    datasets.append([i,'semi','ssum',False])
multiPlotter(datasets)
plt.show()

datasets = []
for i in files:
    datasets.append([i,'semi','ssum',True])
multiPlotter(datasets)
plt.show()
'''
