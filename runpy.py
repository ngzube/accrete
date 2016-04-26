#############################################################################
# Python 2.7.0 script to run accrete5e over all data
#
# Nick Zube
# University of California - Santa Cruz, Earth & Planetary Science
#
# v1.0, 2016-04-25: Completed conversion from cs script. Current runtime
#                   is around 45 mins for the 140 runs.
#
#############################################################################

from datetime import datetime
from os import listdir,path,system
import finder

# Use string 'dat' to create a timestamped folder, identifying the run
dat = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
print 'Run began at', dat
ful = 'run_'+dat
system("mkdir data/" + ful)

''' 
# ***ONLY NECESSARY BEFORE FIRST RUN, WHEN OUTPUT IS NOT YET FORMATTED***
# 
# Run script to create formatted input files
system("python convertFULL.py")
print 'Jacobson files converted to normal output'
system("mv output* Jac_output/")
print 'Output files moved to Jac_output directory'
'''

# Compile and rename main Fortran program
system("gfortran accrete5e_for_nick.f")
system("mv a.out accrete5e_for_nick")
print 'Program compiled'

###############################################################
# Main loop: over all converted output.dat files

# Run over a naturally (alphanumerically) sorted list of the .dat files
filelist = finder.natsort(listdir('Jac_output/'))
for name in filelist:
    print name

    # Avoid files we are not interested in
    if ('output' in name) and ('~' not in name):

        with open(path.join('Jac_output/',name),'r') as filename:

            # Get the part of string name with the run info
            base = name.split('output')[1].split('.dat')[0].split('-')
            if len(base) == 3:
                ratio,emass,nrun = base
            elif len(base)==2: 
                ratio,nrun = base
            else:
                print "*****File name error for",filename,'*****'

            # Correct any mis-named runs so that everything has RunXX format
            if len(nrun) == 1:
                nrun = '0' + nrun

            # Copy current .dat file to accrete directory
            system("cp " + path.join('Jac_output',name) + " output.dat")
            # Make an input file based on its default settings in mkinput.py
            system("python mkinput.py")
            # Run main Fortran isotope code
            system("./accrete5e_for_nick")
            print 'Program complete'
            foldername = ratio + '-1-' + emass + '-Run' + nrun
            outloc = "data/" + ful + "/" + foldername
            system("mkdir " + outloc)
            # Move inputs and outputs to new folder
            system("mv accrete4.inp " + outloc)
            system("mv *.dat " + outloc)
            print 'Stored data in', outloc
###############################################################

print 'Final data files stored in data/' + ful

# Create graphical outputs










# ***DEPRICATED*** 
# Originally scanning an individual run cared about "following" individual
# objects. This could be achieved by creating a "followlist.txt" that 
# contains the Run ID of object to be followed, then passing each as an 
# argument during the creation of accrete4.inp by mkinput.py. We ignore this 
# because our main # intent is to analyze hundreds of runs for statistics, 
# not individual pieces of them.
'''
# Get list of particles to follow for each data file

with open('followlist.txt','r') as follow:
    followlist = []
    for line in follow:
        followlist = followlist + [line]
i = 0

#Later, in the "with open as filename" loop:
    system("python mkinput.py -fol " + followlist[i])
    i = i + 1
'''