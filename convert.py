##############################################################################
# Python 2.7.0 script to create 'output.dat' file from Jacobson files.
#
# Nick Zube, completed v1.0 on ?
#
# Accepts input from multiple files and prints a .dat file to be used by 
# accrete5e
##############################################################################

# Assign strings for ratio number (4 or 8) and run number to be converted:
ratio = '4'
run = '1'

# publish prints collected data to a text file.
def publish():
    outfile = open('output' + ratio + '-' + run + '.dat',"w")
    outfile.write(num_objects + '\n')
    for i in range(len(iprov)):
        # NDUM,IPROV,AN,XM,YPART,ECC,TEJ
        outfile.write(
             str(i) + ' ' + iprov[i] + '  ' + an[i] + '  ' + xm[i] + '  ' + \
             ypart[i] + '  ' + ecc[i] + '  ' + tej[i] + '\n')
    for j in range(len(tcol)):
        # TCOL-ICT1-XMT1-ICT2-XMT2-AN-ECC
        outfile.write(
             str(j) + tcol[j] + ' ' + ict1[j] + '  ' + xmt1[j] + '  ' + \ 
             ict2[j] + '  ' + xmt2[j] + '  ' + ant[j] + '  ' + ecct[j] + '\n')
    outfile.close()

def intake(ratio_string,run_string):
    instring = ratio + 'to1-0.8-Run' + run + '-'
    with open(instring + 'aorig.dat','r') as infile:
        for line in infile:
            entries = line.split()
            semi.append(entries[1])
        num_objects = len(semi)
    
    with open(instring + 'all.dat','r') as infile:
        for line in infile:
            entries = line.split()
            tcol.append(entries[0])
            ict1.append(entries[1])
            xmt1.append(entries[2])
            ict2.append(entries[3])
            xmt2.append(entries[4])
            vel.append(entries[5])
            angle.append(entries[6])
        num_col = len(tcol)
        


#	iprov.append(entries[0])
#	an.append(entries[1])
#	xm.append(entries[2])
#	ypart.append(entries[3])
#	ecc.append(entries[4])
#	tej.append(entries[5])


# Arrays for the variables we will want to print in the style of 'output.dat'
semi = []
iprov, an, xm, ypart, ecc, tej = ([] for i in range(6))
tcol, ict1, xmt1, ict2, xmt2, ant, ecct = ([] for i in range(7))

# Uncomment code below to run over all Jacobson files

#ratio = '4'
#numstrs = ['1','2','3','4','5','6','7','8','9','10']
#for run in numstrs
   #intake(ratio,run)
#ratio = '8'
#numstrs += ['11','12','13','14','15','17','18']
#for run in [numstrs]
intake(ratio,run)




