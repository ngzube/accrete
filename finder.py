#############################################################################
# Python 2.7.0 functions to find types of files or directories.
#
# Nick Zube
# University of California - Santa Cruz, Earth & Planetary Science
#
# v1.0, 2015-11-05: completed
# v1.1, 2016-04-25: tightened up imports to only include necessary functions
#
#############################################################################

from fnmatch import fnmatch
from os import path, walk
from re import split

##############################################

# Produces a generator containing all files in 'directory' matching 'pattern'
# (regular expression), naturally sorted alphabetically (see natsort method)

def find_files(directory, pattern):
    for root, dirs, files in walk(directory):
        files = natsort(files)
        dirs = natsort(dirs)
        for filename in files:
            if fnmatch(filename, pattern):
                filename = path.join(root, filename)
                yield filename

##############################################

# Produces a generator containing all directories in 'directory' matching 
# 'pattern' (regular expression), naturally sorted alphabetically

def find_dirs(directory, pattern):
    for root, dirs, files in walk(directory):
        dirs = natsort(dirs)
        for dirname in dirs:
            if fnmatch(dirname, pattern):
                filename = path.join(root, dirname)
                yield dirname

##############################################

# Sorts a list "naturally" so that result will be '1','2','3','10','20', 
# rather than '1','10','2','20','3',etc.
def natsort(l):
    return sorted(l, key=lambda a: 
        [int(s) if s.isdigit() else s for s in split(r'(\d+)', a)])
