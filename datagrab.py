##############################################################################
# Python 2.7.0 script to pull plot data from final data files.
#
# Nick Zube, completed v1.0 on 2015-11-12
#
# Accepts input from multiple files and prints a .dat file to be used by 
# plotting software.
#
##############################################################################

import finder
import groups
import os
import re

# USER-DEFINED VARIABLES

# folders to pull data from
datadir = 'data/run_2015-11-13_14:42:20'
rawdir = 'ForNimmo2'

# output file name
filePrefix = 'mass_semi_epsilon_'
fileSuff = ('4to1', '8to1')
runcount = (10, 18)

# minimum mass to plot
# Recommend about 0.08, the starting size of larger planetesimals
massMin = 0.08

# Numbers related to columns where data is stored
# Our output files:
id_f = 0
mass = 1
epsilon = 2
semi_wrong = 3
y = 4
HfW = 5
ecc_wrong = 6

# Jacobson "final.dat" raw data files:
id_i = 1
mass_i = 2
semi_i = 3
ecc = 4
inc = 5

#=============================================
# Stores the attributes of a planetesimal: mass, semi-major axis, epsilon
class planet:
    """A class to hold data for a single planet"""
    def __init__(self, mas, ep, sem=0):
        self.m = mas
        self.e = ep
        self.s = sem
    def addSemi(self, sem):
        self.s = sem

#=============================================
# Prints collected data to a .dat file.
def publish(suffx,runs):
    with open(filePrefix + suffx + '.dat', 'w') as outfile:
        for num, run in sorted(runs.iteritems()):
            for key, obj in sorted(run.iteritems()):
                outfile.write(
                    "\t".join([obj.m, obj.s, obj.e, key, 'Run'+num+'\n']))
    outfile.close()

#=============================================

# For each run type
for suff, runsize in zip(fileSuff,runcount):

    # Dictionaries for singleruns in a runtype; keys are run #
    runs = {}
    # runtype is first number of raw file title; e.g. 4, 8
    runtype = suff[0]

    prevdir = '_Run00_'
    # For each directory pertaining to that run type,
    for dirname in finder.find_dirs(datadir, runtype + '-1*'):
        # Dictionary for planets in a single run; keys are planet ID
        singlerun = {}
        print 'Pulling from dir', dirname
        # If the current run is not the same as previous, continue
        prevrun = prevdir.split("Run",1)[1][0:2]
        currun = dirname.split("Run",1)[1][0:2]
        if (prevrun != currun):
            # For each file in that directory matching our phrase,
            for filename in finder.find_files(
                   os.path.join(datadir, dirname), 'end.dat'):
                print 'Found new end.dat file: ', filename
                # Open that file.
                with open(filename, 'r') as infile:
                    for line in infile:
                        entries = line.split()
                        #Record entries
                        if float(entries[mass]) > massMin:
                            singlerun[entries[id_f]] = planet(
                             entries[mass], entries[epsilon], '0')
                            print 'key=',entries[id_f]]
                        else: print 'Didnt include ID', entries[id_f]
            #print 'singlerun=',singlerun
            print 'Runkey=',currun
            runs[currun] = singlerun
        prevdir = dirname

    print '******************************************'
    # Get semi-major axes from raw Jacobson *final.dat files (sorted)
    for filename in finder.find_files(rawdir, runtype+'*final.dat'):
        print 'Found file:', filename
        # Need to check whether run is one or two digits because of 
        # bad Jacobson naming convention
        first_digit = filename.split("Run",1)[1][0]
        second_digit = filename.split("Run",1)[1][1]
        try:
            test = int(second_digit)
            currun = first_digit + second_digit
            del test
        except ValueError:
            currun = '0' + first_digit
        # Open the file.
        with open(filename, 'r') as infile:
            print 'Currun',currun
            for line in infile:
                entries = line.split()
                print 'ID', entries[id_i], 'Mass',entries[mass_i],'Run', currun
                #print runs[currun]
                # If a specific ID is in our dictionary of that run,
                if entries[id_i] in runs[currun]:
                    runs[currun][entries[id_i]].addSemi(entries[semi_i])
                else:
                    print 'NOT HERE! Probably too small.'

    # Open a file, store data about that runtype
    publish(suff,runs)