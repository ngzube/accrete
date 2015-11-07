##############################################################################
# Python 2.7.0 script to pull plot data from final data files.
#
# Nick Zube, completed v1.0 on ?
#
# Accepts input from multiple files and prints a .dat file to be used by 
# plotting software.
#
##############################################################################

import finder
import os
import re

# folder to pull data from
datadir = 'data/run_2015-11-06_14:45:54'
rawdir = 'ForNimmo2'

# output file name
filePrefix = 'mass_semi_epsilon_'
fileSuffix = ('4to1', '8to1')

massMin = 0.1

matches = []

# For an individual run type,
for suff in fileSuffix:
    runtype = suff[0]
    print 'Suffix =', suff, '; Runtype =', runtype
    # Open a file to store data about that run type.
    with open(filePrefix + suff, 'w') as outfile:
        print 'Opened', filePrefix+suff
        # For each directory pertaining to that run type,
        print 'Checking string ', runtype+'-1'
        prevdir = '*Run00*'
        for dirname in finder.find_dirs(datadir, runtype + '-1*'):
            print 'Pulling from dir ', dirname
            # If the current run is not the same as the previous folder, continue
            prevrun = prevdir.split("Run",1)[1][0:2]
            currun = dirname.split("Run",1)[1][0:2]
            if (prevrun != currun):
                # For each file in that directory matching our phrase,
                for filename in finder.find_files(
                       os.path.join(datadir, dirname), 'end.dat'):
                    print 'Found end file: ', filename
                    # Open that file.
                    with open(filename, 'r') as infile:
                        for line in infile:
                            entries = line.split()
                            #print entries
                            if float(entries[0]) > massMin:
                                #  Mass                 Epsilon
                                outfile.write(
                                   entries[0] + '   ' + entries[1] + '   ' + dirname +
                                   '\n')
            prevdir = dirname


#(,*.final.dat)
#semi.append(entries[3])
