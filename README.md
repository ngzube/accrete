# accrete
-planetary accretion code with Hf/W tracking by Francis Nimmo, UCSC
-non-master branch edits by Nick Zube.

PROJECT FLOW:

==============
[Input files]   <===
==============

output.dat: list of initial positions and collisions of 1054 objects. Read by main program.

makeinput.m : allows user to input variable values for use in main program.
 Outputs a file called accrete4.inp to be read by main program.

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
[Output files] ===>
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

accplot.m: plot the dEps_W (tungsten isotope anomaly) and mass vs. time for chosen particle
