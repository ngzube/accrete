##############################################################################
# Python 2.7.0 script to create 'output.dat' file from Jacobson files.
#
# Nick Zube, completed v1.0 on ?
#
# Accepts input from multiple files and prints a .dat file to be used by 
# accrete5e
#
# Note that Jacobson collision files differ from output.dat in that they have
# impact velocity and angle instead of semi-major axis and eccentricity.
# We obtain these only for the final planets.
##############################################################################

# Assign strings for ratio number (4 or 8) and run number to be converted:
ratio = '4'
run = '1'

#=============================================
# Prints collected data to a text file.

def publish():
    outfile = open('output' + ratio + '-' + run + '.dat',"w")
    outfile.write(str(num_objects) + '\n')
    for i in range(len(an)):
        #Original: NDUM,IPROV,AN,              XM,                          YPART,ECC,TEJ
        #Jacobson: NDUM, -,   Semi-major axis, mass from first collision,   -,    -,  -
        outfile.write(
             str(i+1) + ' ' + iprov[i] + '  ' + an[i] + '  ' + xm[i] + '  ' + 
             ypart[i] + '  ' + ecc[i] + '  ' + tej[i] + '\n')
    for j in range(len(tcol)):
        #Original: TCOL,ICT1,XMT1,ICT2,XMT2,AN,        ECC
        #Jacobson: TCOL,ICT1,XMT1,ICT2,XMT2,Impact_Vel,Impact_Angle
        outfile.write(
             str(j+1) + ' ' + tcol[j] + ' ' + ict1[j] + '  ' + xmt1[j] + 
             '  ' + ict2[j] + '  ' + xmt2[j] + '  ' + an_col[j] + '  ' + 
             ecc_col[j] + '\n')
    outfile.close()


#=============================================
# Read info from Jasboson files

def intake(ratio_string,run_string):
    instring = 'ForNimmo2/' + ratio + 'to1-0.8-Run' + run + '-'
    with open(instring + 'aorig.dat','r') as infile:
        for line in infile:
            entries = line.split()
            iprov.append('1')    # arbitrarily set
            an.append(entries[1])
            xm.append('0')       # appended later
            ypart.append('0.3')  # arbitrarily set
            ecc.append('0')      # arbitrarily set
            tej.append('10E+11') # arbitrarily set                       
        num_objects = len(an)
    
    with open(instring + 'all.dat','r') as infile:
        prev_time = 0.0
        for line in infile:
            entries = line.split()
	    # Due to errors in accrete5e.f if timestamps are the same, we add
            # one second to the time if it matches the previous one
            current_time = float(entries[0])
            if current_time == prev_time:
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
#MAIN SCRIPT

# Arrays for the variables we will want to print in the style of 'output.dat'
# Assigns 6 separate empty lists [] to each named variable
iprov, an, xm, ypart, ecc, tej = ([] for i in range(6))
tcol, ict1, xmt1, ict2, xmt2, an_col, ecc_col = ([] for i in range(7))
num_objects = 0
num_col = 0

## Uncomment code below to run over all Jacobson files

ratio = '4'
numstrs = ['1','2','3','4','5','6','7','8','9','10']
for run in numstrs:
    [num_col,num_objects] = intake(ratio,run)
    publish()
    print 'Finished', ratio, 'to1-0.8-Run', run
ratio = '8'
numstrs += ['11','12','13','14','15','17','18']
for run in numstrs:
    [num_col,num_objects] = intake(ratio,run)
    publish()
    print 'Finished', ratio, 'to1-0.8-Run', run



