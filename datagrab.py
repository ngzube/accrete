##############################################################################
# Python 2.7.0 script to pull plot data from final data files.
#
# Nick Zube, completed v1.0 on 2015-11-12
#
# Accepts input from multiple files and prints a .dat file to be used by 
# plotting software.
#
# For easy debugging, uncomment the print statements.
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

# Jacobson "final.dat" raw data files; order of columns:
id_i = 1
mass_i = 2
semi_i = 3
ecc = 4
inc = 5

#=============================================
# Stores the attributes of a planetesimal: mass, semi-major axis, epsilon
# (tungsten anomaly), 90% mass, time of reaching 90% mass
class planet:
	"""A class to hold data for a single planet"""
	def __init__(self, mas, ep, sem='0', m90='0', t90='0'):
		self.m = mas
		self.e = ep
		self.s = sem
		self.m90 = m90
		self.t90 = t90
	#def addSemi(self, sem):
	#    self.s = sem

#=============================================
# If a file is named with only one digit, changes it to 0+digit
# and returns run number as 2 digits.
def correctRunNumber(filename):
	first_digit = filename.split("Run",1)[1][0]
	second_digit = filename.split("Run",1)[1][1]
	# if there is a second digit in the filename, use both digits
	try:
		test = int(second_digit)
		currun = first_digit + second_digit
		del test
	# if there is not a second digit, add a 0 prefix
	except ValueError:
		currun = '0' + first_digit
	return currun
 #=============================================
# Prints collected data to a .dat file.
def publish(suffx,runs):
	with open(filePrefix + suffx + '.dat', 'w') as outfile:
		for num, run in sorted(runs.iteritems()):
			for key, obj in sorted(run.iteritems()):
				outfile.write(
					"\t".join([obj.m, obj.s, obj.e, key, 'Run'+num,
					obj.m90, str(float(obj.m)*0.9), obj.t90+'\n']))
	outfile.close()

#=============================================
# Stores data in this structure:
# runs -> a dictionary holding many singlerun, with their IDs as keys
# singlerun -> a planet, with attributes for mass, epsilon, and semi-maj axis
#
# First, loop over all output files created by accrete5e.f, looking
# for mass and d_epsilon_W (tungsten anomaly)

# For each run type
for suff, runsize in zip(fileSuff,runcount):

	# Dictionaries for singleruns in a runtype; keys are run #
	runs = {}
	# runtype is first number of raw file title; e.g. 4, 8
	runtype = suff[0]

	prevdir = '_Run00_'

	#LOOP 1: Pulling mass and epsilon from end.dat
	# For each directory pertaining to that run type,
	for dirname in finder.find_dirs(datadir, runtype + '-1*'):
		# Dictionary for planets in a single run; keys are planet ID
		singlerun = {}
		#print 'Pulling from dir', dirname
		# If the current run is not the same as previous, continue
		prevrun = prevdir.split("Run",1)[1][0:2]
		currun = dirname.split("Run",1)[1][0:2]
		if (prevrun != currun):
			# For each file in that directory matching our phrase,
			for filename in finder.find_files(
				   os.path.join(datadir, dirname), 'end.dat'):
				#print 'Found new end.dat file: ', filename
				# Open that file.
				with open(filename, 'r') as infile:
					for line in infile:
						entries = line.split()
						#Record entries
						if float(entries[mass]) > massMin:
							singlerun[entries[id_f]] = planet(
							 entries[mass], entries[epsilon]) #, '0'
							#print 'key=',entries[id_f]]
						#else: print 'Didnt include ID', entries[id_f]
			##print 'singlerun=',singlerun
			#print 'Runkey=',currun
			runs[currun] = singlerun
		prevdir = dirname

	# LOOP 2: Get time of 90% mass from raw Jacobson all.dat files (sorted)
	for filename in finder.find_files(rawdir, runtype+'*all.dat'):
		# Need to check whether run is one or two digits because of 
		# bad Jacobson naming convention
		currun = correctRunNumber(filename)
		massfin, mass90, b4mass, time90 = {}, {}, {}, {}
		with open(filename,'r') as infile:
			# Iterate backwards from last line of file
			for line in reversed(infile.readlines()):
				entries = line.split()

				time9 = entries[0]
				idee9 = entries[1]
				mass9 = float(entries[2])

				#massf = runs[currun][idee].m

				# Exclude objects below massmin
				if (mass9 > massMin):
					# If we haven't stored a time for this ID already,
					if (idee9 not in time90):
						# If no final mass stored yet, add one with key = ID
						if (idee9 not in massfin):
							massfin[idee9] = mass9
						# If there is a final stored, check if we reached 90%
						# If so, store time and this 90% mass
						elif (mass9 <= 0.9*massfin[idee9]):
							mass90[idee9] = mass9
							time90[idee9] = time9
						else: b4mass[idee9] = mass9

			for ide, tim in time90.iteritems():
				if ide in runs[currun]:
					runs[currun][ide].t90 = tim
					runs[currun][ide].m90 = str(b4mass[ide])

	#print '******************************************'
	#LOOP 3: Get semi-major axes from raw Jacobson final.dat files (sorted)
	for filename in finder.find_files(rawdir, runtype+'*final.dat'):
		#print 'Found file:', filename
		currun = correctRunNumber(filename)
		# Open the file.
		with open(filename, 'r') as infile:
			#print 'Currun',currun
			for line in infile:
				entries = line.split()
				#print 'ID', entries[id_i], 'Mass',entries[mass_i],'Run', currun
				##print runs[currun]
				# If a specific ID is in our dictionary of that run,
				if entries[id_i] in runs[currun]:
					#runs[currun][entries[id_i]].addSemi(entries[semi_i])
					runs[currun][entries[id_i]].s = entries[semi_i]
				#else: print 'NOT HERE! Probably too small.'

	# Open a file, store data about that runtype
	publish(suff,runs)