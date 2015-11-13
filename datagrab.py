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
import os
import re

# USER-DEFINED VARIABLES

# folders to pull data from
datadir = 'data/run_2015-11-12_18:10:30'
rawdir = 'ForNimmo2'

# output file name
filePrefix = 'mass_semi_epsilon_'
fileSuff = ('4to1', '8to1')
runcount = (10, 18)

# minimum mass to plot
# Recommend at least 0.08, the starting size of larger planetesimals
massMin = 0.08

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
# Prints collected data to a text file.
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
                        if float(entries[1]) > massMin:
                            singlerun[entries[0]] = planet(
                             entries[1], entries[2], '0')
                            print 'key=',entries[0]
                        else: print 'Didnt include ID', entries[0]
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
                print 'ID', entries[1], 'Mass',entries[2],'Run', currun
                #print runs[currun]
                # If a specific ID is in our dictionary of that run,
                if entries[1] in runs[currun]:
                    runs[currun][entries[1]].addSemi(entries[3])
                else:
                    print 'NOT HERE!'

    # Open a file, store data about that runtype
    publish(suff,runs)