#############################################################################
# Python 2.7.0 script to create 'output.dat' file from Jacobson files.
#
# Nick Zube
# University of California - Santa Cruz, Earth & Planetary Science
#
# v1.0, 2015-12-01: completed
# v1.1, 2016-04-19: tightened up imports to only include necessary functions
#
# Accepts input from multiple files and prints .dat files to be used by 
# accrete5e
#
# Note that Jacobson collision files differ from output.dat in that they have
# impact velocity and angle instead of semi-major axis and eccentricity.
# We obtain these only for the final planets.
#############################################################################

import finder
import fnmatch
import os

# Assign default values for those not included in Jacobson files
iprov0 = '1'
ypart0 = '0.3'
ecc0 = '0'
tej0 = '10E+11'
runMass = ['1','2','4','8']
eMass = ['0.2','0.5','0.8']
loc = 'ForNick'

#=============================================
# Prints collected data to a text file.

def publish():
    with open('output' + ratio + '-' + run + '.dat',"w") as outfile:
        outfile.write(str(n_objects) + '\n')
        for i in range(len(an)):
            #Original: NDUM,IPROV,AN,       XM,               YPART,ECC,TEJ
            #Jacobson: NDUM, -,   Semi-maj, mass from 1st collis, -,    -,  -
            outfile.write(' '.join([
                str(i+1), iprov[i], an[i], xm[i], ypart[i], ecc[i], tej[i], 
                '\n']))
        for j in range(len(tcol)):
            #Original: TCOL,ICT1,XMT1,ICT2,XMT2,AN,        ECC
            #Jacobson: TCOL,ICT1,XMT1,ICT2,XMT2,Impact_Vel,Impact_Angle
            outfile.write(' '.join([
                 str(j+1), tcol[j], ict1[j], xmt1[j], ict2[j], xmt2[j], 
                 an_col[j], ecc_col[j], '\n']))
    outfile.close()


#=============================================
# Read info from large batch of Jasboson files

def intake2(location):

    filelist = finder.natsort(os.listdir(location))
    aorig_list = []
    all_list = []

    for filename in filelist:
        if 'aorig' in filename:
            aorig_list.append(filename)
        if 'all' in filename:
            all_list.append(filename)

    for aorigfile,allfile in zip(aorig_list,all_list):

        iprov, an, xm, ypart, ecc, tej = ([] for i in range(6))
        tcol, ict1, xmt1, ict2, xmt2, an_col, ecc_col = ([] for i in range(7))
        num_objects = 0
        num_col = 0
        ratio, emass, run = ('' for i in range(3))  
        print aorigfile,allfile  


        ratio = aorigfile[0]
        emass = aorigfile[5:8]
        run = aorigfile[12:14]
        if '-' in run:
            run = '0'+run[0]  
        print [ratio,emass,run]

        with open(os.path.join(location,aorigfile)) as infile:
            print 'Opened',aorigfile
            for line in infile:
                entries = line.split()
                iprov.append(iprov0)
                an.append(entries[1])
                xm.append('0')  # found later when checking collisions
                ypart.append(ypart0)
                ecc.append(ecc0)
                tej.append(tej0)                       
            num_objects = len(an)                        

        with open(os.path.join(location,allfile)) as infile:
            print 'Opened',allfile
            prev_time = 0.0
            for line in infile:
                if 'MapAt' in line:
                    continue
                entries = line.split()
# Due to errors in accrete5e.f if timestamps are the same, we add
# one second to the time if it matches the previous one
                current_time = float(entries[0])
                if current_time <= prev_time:
                    #print '******SAME TIME*******',current_time
                    current_time+=(abs(prev_time-current_time)+1.0)
                    #print 'Revised time:',current_time
                tcol.append(str(current_time))
                prev_time = current_time
                ict1.append(entries[1])
                xmt1.append(entries[2])
                ict2.append(entries[3])
                xmt2.append(entries[4])
                an_col.append(entries[5]) 
                # actually impact velocity, not semi-major
                ecc_col.append(entries[6]) 
                # actually impact angle, not eccentricity

# Assign masses from the first time a body appears in collisions
            #print xm
                if(xm[int(entries[1])-1]=='0'): 
                    xm[int(entries[1])-1] = entries[2]
                if(xm[int(entries[3])-1]=='0'): 
                    xm[int(entries[3])-1] = entries[4]
            #print xm
            num_col = len(tcol)        



        output_name = 'output' + ratio + '-' + emass + '-' + run + '.dat'
        print 'Creating',output_name,'...'
        with open(output_name,"w") as outfile:
                outfile.write(str(num_objects) + '\n')
                for i in range(len(an)):
                    #Original: NDUM,IPROV,AN,     XM,               YPART,ECC,TEJ
                    #Jacobson: NDUM, -, Semi-maj, mass from 1st event, -,    -,  -
                    outfile.write(' '.join([
                        str(i+1), iprov[i], an[i], xm[i], ypart[i], ecc[i], 
                        tej[i], '\n']))
                for j in range(len(tcol)):
                    #Original: TCOL,ICT1,XMT1,ICT2,XMT2,AN,        ECC
                    #Jacobson: TCOL,ICT1,XMT1,ICT2,XMT2,Impact_Vel,Impact_Angle
                    outfile.write(' '.join([
                         str(j+1), tcol[j], ict1[j], xmt1[j], ict2[j], xmt2[j], 
                         an_col[j], ecc_col[j], '\n']))
        outfile.close()

#=============================================

def intake(ratio_string,run_string):
    num_objects = 0
    num_col = 0
    instring = 'ForNimmo2/' + ratio + 'to1-' + emass + '-Run' + run + '-'
    with open(instring + 'aorig.dat','r') as infile:
        for line in infile:
            entries = line.split()
            iprov.append(iprov0)
            an.append(entries[1])
            xm.append('0')       # adjusted later when checking collisions
            ypart.append(ypart0)
            ecc.append(ecc0)
            tej.append(tej0)                       
        num_objects = len(an)
        #print num_objects
    
    with open(instring + 'all.dat','r') as infile:
        prev_time = 0.0
        for line in infile:
            entries = line.split()
	    # Due to errors in accrete5e.f if timestamps are the same, we add
            # one second to the time if it matches the previous one
            current_time = float(entries[0])
            if current_time == prev_time:
                print '****************SAME TIME***************',current_time
                current_time += 1.0
            tcol.append(str(current_time))
            prev_time = current_time
            ict1.append(entries[1])
            xmt1.append(entries[2])
            ict2.append(entries[3])
            xmt2.append(entries[4])
            an_col.append(entries[5]) # actually impact velocity, not semi-major
            ecc_col.append(entries[6]) # actually impact angle, not eccentricity

            # Assign masses from the first time a body appears in collisions
	    if(xm[int(entries[1])-1]=='0'): xm[int(entries[1])-1] = entries[2]
	    if(xm[int(entries[3])-1]=='0'): xm[int(entries[3])-1] = entries[4]
        num_col = len(tcol)
    return num_col, num_objects
        
#==================================
#MAIN SCRIPT:

# Code to run over all Jacobson files
intake2(loc)

'''
## Code to run over small set of Jacobson files ##
ratio = '4'
runnums = (str(x+1) for x in range(10))
for run in runnums:
    # Assigns 6 separate empty lists [] to each named variable
    iprov, an, xm, ypart, ecc, tej = ([] for i in range(6))
    tcol, ict1, xmt1, ict2, xmt2, an_col, ecc_col = ([] for i in range(7))
    n_objects = 0
    n_col = 0
    [n_col,n_objects] = intake(ratio,run)
    if len(run) < 2: run = '0'+run
    publish()
    #print 'Finished', ratio, 'to1-0.4-Run', run

ratio = '8'
runnums = (str(x+1) for x in range(18))
for run in runnums:
    iprov, an, xm, ypart, ecc, tej = ([] for i in range(6))
    tcol, ict1, xmt1, ict2, xmt2, an_col, ecc_col = ([] for i in range(7))
    n_objects = 0
    n_col = 0
    [n_col,n_objects] = intake(ratio,run)
    if len(run) < 2: run = '0'+run
    publish()
    #print 'Finished', ratio, 'to1-0.8-Run', run

'''

'''
############### Code to run on a single file ###############
ratio = '8'
run = '18'
iprov, an, xm, ypart, ecc, tej = ([] for i in range(6))
tcol, ict1, xmt1, ict2, xmt2, an_col, ecc_col = ([] for i in range(7))
n_objects = 0
n_col = 0
[num_col,num_objects] = intake(ratio,run)
publish()
print 'Finished', ratio, 'to1-0.8-Run', run
'''