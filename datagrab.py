##############################################################################
# Python 2.7.0 script to pull plot data from final data files.
#
# Nick Zube
# University of California - Santa Cruz, Earth & Planetary Science
#
# v1.0, 2015-11-12: completed
#
# Accepts input from multiple files and prints a .dat file to be used by 
# plotting software.
#
# For easy debugging, uncomment the print statements.
##############################################################################

import finder
#import groups
import numpy as np
import os
import re

# USER-DEFINED VARIABLES

# folders to pull data from
datadir = 'data/k10/run_2016-03-16_10:55:17'
rawdir = 'ForNimmo2'
jacdir = 'Jac_output'

# output file names
filePrefix = 'mass_semi_epsilon_'
fileSuff = ('1to1','2to1','4to1', '8to1')
runcount = (10, 18)

# minimum mass to plot
# Recommend about 0.08, the starting size of larger planetesimals
massMin = 0.07

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
id_j = 1
mass_j = 2
semi_j = 3
ecc = 4
inc = 5

# Output.dat files produced by convert.py; order of columns:
o_id = 0
o_semi = 2
o_mass = 3

o_id1 = 2
o_m1 = 3
o_id2 = 4
o_m2 = 5

#=============================================
# Stores the attributes of a planetesimal: mass, semi-major axis, epsilon
# (tungsten anomaly), 90% mass, time of reaching 90% mass
class planet:
	"""A class to hold data for a single planet"""
	def __init__(self, mas='0.0', ep='0.0', hfw='0.0', sem='0.0', 
				 m90='0.0', t90='0.0', imass='0.0', isemi='0.0',
				 mws='0.0', mwstop=0, mwsbot=0,var=0):
		self.m = mas
		self.e = ep
		self.s = sem
		self.h = hfw
		self.m90 = m90
		self.t90 = t90
		self.im = imass
		self.ism = isemi
		self.mwstop = mwstop
		self.mwsbot = mwsbot
		self.mws = mws
		self.var = var

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
					"\t".join([obj.m, obj.s, obj.e, obj.h, key, 'Run'+num,
					obj.m90, str(float(obj.m)*0.9), obj.t90, obj.im,
					obj. ism, obj.mws, str(obj.mwsbot)+'\n']))
	outfile.close()
	print 'created file', filePrefix+suffx

#=============================================

# Collect a table of data for relation to real planets
def makeTable(suffx,runs):

	Earth = {'mass':1.,'semi':1.,'hfw':13.6,'eps':1.9,
			 'hfsig':4.3,'esig':0.1,'name':'Earth',
			 'm_low':0.8,'m_upp':1.2,'a_low':0.5,'a_upp':1.5}
	Mars = {'mass':0.107,'semi':1.524,'hfw':2.4,'eps':2.3,
			'hfsig':0.9,'esig':0.2,'name':'Mars',
			'm_low':0.8,'m_upp':1.2,'a_low':1.,'a_upp':2.3}

	# Seth-recommended bounds:
	#m_upper = 2
	#m_lower = 0.5
	#a_lowerE = 0.387 
	#a_upperE = 1.524
	#a_lowerM = 1
	#a_upperM = 2.3

	with open('table' + suffx + '.dat', 'w') as outfile:
		for realBody in [Earth,Mars]:
			outfile.write(realBody['name']+'\n')
			Msums = planet(mas=0,sem=[],t90=[],hfw=[],ep=[])
			Asums = planet(mas=0,sem=[],t90=[],hfw=[],ep=[])

			for num, run in sorted(runs.iteritems()):
				for key, obj in sorted(run.iteritems()):
					m = float(obj.m)
					s = float(obj.s)
					print key,num,m,obj.s,obj.h,obj.e,obj.t90
					if ((m >= realBody['mass']*realBody['m_low']) and 
						(m <= realBody['mass']*realBody['m_upp'])):
					
						if ((s >= realBody['semi']*realBody['a_low']) and 
							(s <= realBody['semi']*realBody['a_upp'])):
							print "\nSelected:",obj.m,obj.s,obj.h,obj.e,obj.t90,Msums.m
							Msums.h.append(float(obj.h))
							Msums.e.append(float(obj.e))
							Msums.t90.append(float(obj.t90))
							Msums.m += 1.
							Asums.h.append(float(obj.h))
							Asums.e.append(float(obj.e))
							Asums.t90.append(float(obj.t90))
							Asums.m += 1.


			#Take averages
			mhavg = np.mean(Msums.h)
			mhsd = np.std(Msums.h)
			meavg = np.mean(Msums.e)
			mesd = np.std(Msums.e)
			mtavg = np.mean(Msums.t90)/1.e6
			mtsd = np.std(Msums.t90)/1.e6
			print [i/1.e6 for i in Msums.t90],mtavg,mtsd,'\n\n'
			ahavg = np.mean(Asums.h)
			ahsd = np.std(Asums.h)
			aeavg = np.mean(Asums.e)
			aesd = np.std(Asums.e)
			atavg = np.mean(Asums.t90)/1.e6
			atsd = np.std(Asums.t90)/1.e6

			outfile.write(",".join(
				[str(realBody['m_low'])+" < 1 ME < "+str(realBody['m_upp']), 
				str(mhavg), str(mhsd), str(meavg), str(mesd), 
				str(mtavg), str(mtsd), str(Msums.m)+'\n']))
			outfile.write(",".join(
				[str(realBody['a_low'])+" < 1 AU <  "+str(realBody['a_upp']), 
				str(ahavg), str(ahsd), str(aeavg), str(aesd), 
				str(atavg), str(atsd), str(Asums.m)+'\n']))

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

	#print '******************************************'
	# LOOP 1: Pulling mass and epsilon from end.dat

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
							 entries[mass], entries[epsilon], entries[HfW])
							#print 'key=',entries[id_f]]
						#else: print 'Didnt include ID', entries[id_f]
			##print 'singlerun=',singlerun
			#print 'Runkey=',currun
			runs[currun] = singlerun
		prevdir = dirname

	#print '******************************************'
	# LOOP 2: Get time of 90% mass from raw Jacobson all.dat files (sorted)

	for filename in finder.find_files(rawdir, runtype+'*all.dat'):
		# Need to check whether run is one or two digits because of 
		# bad Jacobson naming convention
		currun = correctRunNumber(filename)
		massfin, mass90, b4mass, time90, b4time = {}, {}, {}, {}, {}
		massini = {}
		with open(filename,'r') as infile:
			# Iterate backwards from last line of file
			text = infile.readlines()
			for line in reversed(text):
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
						else: 
							b4mass[idee9] = mass9
							b4time[idee9] = time9

			for ide, tim in time90.iteritems():
				if ide in runs[currun]:
					runs[currun][ide].t90 = b4time[ide]
					runs[currun][ide].m90 = str(b4mass[ide])

			# Iterate forwards to get initial mass
			for line in (text):
				entries = line.split()
				if (entries[1] not in massini):
					massini[entries[1]] = entries[2]

			for ide, mi in massini.iteritems():
				if ide in runs[currun]:
					runs[currun][ide].im = mi

	#print '******************************************'
	# LOOP 3: Get semi-major axis from raw Jacobson final.dat files (sorted)

	for filename in finder.find_files(rawdir, runtype+'*final.dat'):
		#print 'Found file:', filename
		currun = correctRunNumber(filename)

		with open(filename, 'r') as infile:
			#print 'Currun',currun
			for line in infile:
				entries = line.split()
				#print 'ID', entries[id_j], 'Mass',entries[mass_j],'Run', currun
				##print runs[currun]
				# If a specific ID is in our dictionary of that run,
				if entries[id_j] in runs[currun]:
					runs[currun][entries[id_j]].s = entries[semi_j]

	#print '******************************************'
	# LOOP 4: Get init semi-maj axis from Jacobson aorig.dat files (sorted)
	
	for filename in finder.find_files(rawdir, runtype+'*aorig.dat'):
		currun = correctRunNumber(filename)
		# Open the file.
		with open(filename, 'r') as infile:
			for line in infile:
				entries = line.split()
				# If a specific ID is in our dictionary of that run,
				if entries[0] in runs[currun]:
					runs[currun][entries[0]].ism = entries[1]

	#print '******************************************'
	# LOOP 5: Get mass-weighted semi-major axis from output.dat files

	for filename in finder.find_files(jacdir, '*'+runtype+'-*.dat'):

		currun = filename.split("-",1)[1][:2]
		objs = {}
		first = True
		linenum, nObjs = 0, 0

		with open(filename, 'r') as infile:
			for line in infile:
				entries = line.split()

				if linenum is 0:
					nObjs = float(entries[0])
				# If reading initial objects:
				elif linenum <= nObjs:
					iobj = entries[o_id]
					mobj = entries[o_mass]
					sobj = entries[o_semi]
					objs[iobj] = planet(mas=mobj, sem=sobj,
						mwstop = float(mobj)*float(sobj), 
						mwsbot = float(mobj))
				# If reading collisions:
				else:
					bigID = entries[o_id1]
					smallID = entries[o_id2]
					bigMass = entries[o_m1]
					smallMass = entries[o_m2]
					if float(smallMass) > float(bigMass): 
						bigID = entries[o_id2]
						smallID = entries[o_id1]
						bigMass = entries[o_m2]
						smallMass = entries[o_m1]

					objs[bigID].mwstop = (
						objs[bigID].mwstop + objs[smallID].mwstop)
					objs[bigID].mwsbot = (
						objs[bigID].mwsbot + objs[smallID].mwsbot)

				linenum += 1

			for key, i in objs.iteritems():
				#print key, i
				if i.mwsbot != 0:
					i.mws = str(i.mwstop/i.mwsbot)
				if key in runs[currun]:
					runs[currun][key].mws = i.mws
					runs[currun][key].mwsbot = i.mwsbot


	#print '******************************************'


	# Open a file, store data about that runtype
	publish(suff,runs)
	#makeTable(suff,runs)
