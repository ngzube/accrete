# accrete
-planetary accretion code with Hf/W tracking by Francis Nimmo, UCSC
-non-master branch edits by Nick Zube.

PROJECT FLOW:

==============
[Master run file]
==============

run: CSH script that executes mkinput.py, then accrete5e_for_nick.f, then stores input and output data files in a time-labeled folder. Run this file to activate the complete ACCRETE progam package.


==============
[Input files]   <===
==============

output.dat: list of initial conditions and collisions of objects. Read by main program.
Particle # - iprovenance - semi-major? - mass - y partition fraction - eccentricity - time till ejection
(stored in arrays: NDUM,IPROV,AN,XM,YPART,ECC,TEJ)
(#Note: YPART is usually set constant by our program)
Time of collision - ID 1 - Mass 1- ID 2 - Mass 2 - semi-major axis - eccentricity
TCOL-ICT1-XMT1-ICT2-XMT2-AN-ECC

mkinput.py: Python script creates a window to allow user to set variable defaults for accrere4.inp

makeinput.m : redundant version of mkinput.py, written in Matlab

==============
[Main Program]
==============
accrete5e_for_nick.f (Fortran77)

-Inputs collision data to track features of particles involved.
-Allows control of Y (silicate fraction), DW (partition coefficients),
 mixing factors, level of re-equilibration, and individual particle tracking.
-Reports time-evolving stats on individual particle and final stats on
 surviving particles.

Opens the following files:

Read:
Unit 20 = accrete4.inp
Unit 22 = output.dat

Write:
Unit 28 = end.dat
Unit 40 = follow.dat
Unit 42 = eps.dat
Unit 43 = followgmt.dat

==============
[Output files] ===> stored in /data in a timestamped folder
==============

end.dat: Results for surviving particles. Almost the same as printed output.
-Mass, epsilon, semi-major axis, y (silicate fraction), Hf/W, ECC (unknown, read from output.dat)

eps.dat: list of time evolution of epsilon_W value for the chosen particle.

follow.dat: times and characteristics of collisions by our followed particle.
-TCOL(J), ICT1,XM(ICT1),ICT2,XM(ICT2),XM(ICT1)+XM(ICT2)
-time of collision, ID of target, mass of target, ID of impactor, mass of impactor, total mass

followgmt.dat: more values for the same collisions in follow.dat
-TCOL(J),GAMT,EPSTT,0.3*(3.+LOG10(XMMT))
-time of collision, mass ratio impactor:target, tungsten anom of smaller?, calculation with smaller mass 

================
[Analysis files]
================

accplot.m: plot the dEpsilon_W (tungsten isotope anomaly) and mass vs. time for chosen particle

accplot_compare.m: allows plotting of multiple datasets at once




[Other contributors]
Nimmo, Francis
Kleine, Thorsten
Jacobson, Seth
Morbidelli, Alessandro
O'Brien, David
Walsh, Kevin
Halliday, Alexander
Agnor, C
Yin, Qingzhu
Jacobsen, Stein


