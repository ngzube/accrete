############################################################
# Python 2.7.0 script to create an input file for accrete5e.
#
# Nick Zube, completed v1.0 on 2015-10-09
# Accepts input from a window and prints a txt file to be used by accrete5e
############################################################

# Tkinter is a GUI package in Python
from Tkinter import *

prompts = ['nprov: UNKNOWN. for loop max. 1 indicates chondritic?',
    'ff, Equilibration fraction (0 = complete, 1 = none)',
    'tstop: The time code will stop',
    'iray: toggle between Raymond or OBrien input',
    'ilog: plotting toggle',
    'idsc: number of impact pieces in equilibration (1=batch, 100=fully eq)',
    'ixmix: sets imix to control mixing/re-equilibration',
    'xmix: min mass required for a "large" impact',
    'xratc: used in mixing with IF XRAT >= XRATC, IBIG = 1, ICIRC++',
    'ifol: ID of particle to be followed',
    'dw: tungsten partition coefficient. DW = -F2(1-Y) / (F1*Y)',
    'tscale: allows timescale to be artificially stretched',
    'kmax: # of time steps',
    'kstep: variable used in MOD(k,kstep) to occasionally write',
    'dt: timestep in yrs',
    'ypmx: plotting y-axis']
variables = ['nprov','ff','tstop','iray','ilog','idsc','ixmix',
    'xmix','xratc','ifol','dw','tscale','kmax','kstep','dt',
    'ypmx']
num_inputs = 16
defaults = ['6','0.','1.5e8','1','1','1','1',
    '100.','0.7','38','0.034','1.','20000','100','2.5e5',
    '20.']

# Typical changes to default values:
# FF default may be 0 or 1
# IDSC default may be 1 or 100
# IFOL may be any particle ID#


# publish prints collected data to a text file. Activates on a button push.
def publish():
    outfile = open('accrete4.inp',"w")
    outfile.write(' &inp\n')
    for i in range(len(variables)):
        outfile.write(variables[i] + '=' + v[i].get() + ',')
    outfile.write('\n&end\n')
    outfile.close()
    root.destroy()

# Open input window and assign title
root = Tk()
root.title("Create 'accrete4.inp' file")
# Lists for containing Entry and StringVar objects
e = []
v = []           
for i in range(len(prompts)):
    va = StringVar()
    en = Entry(root, textvariable=va)
    en.grid(row=i,column=0)
    en.insert(0,defaults[i])
    v.append(va)
    e.append(en)
    Label(text=prompts[i]).grid(row=i,column=1,sticky=W)
Button(root,text='OK',command=publish).grid(column=1,row=i+1,sticky=W)
# mainloop runs the frame on a loop until it is closed (upon button press)
root.mainloop()

