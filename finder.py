##############################################################################
# Python 2.7.0 functions to find types of files or directories.
#
# Nick Zube, completed v1.0 on 2015-11-05
#
##############################################################################

import fnmatch
import os

##############################################

# Produces a generator containing all files in 'directory' matching 'pattern'
# (regular expression)

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                filename = os.path.join(root, filename)
                yield filename

##############################################

# Produces a generator containing all directories in 'directory' matching 
# 'pattern' (regular expression)

def find_dirs(directory, pattern):
    for root, dirs, files in os.walk(directory):
        dirs.sort()
        for dirname in dirs:
            if fnmatch.fnmatch(dirname, pattern):
                filename = os.path.join(root, dirname)
                yield dirname
