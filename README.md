# accrete
- planetary accretion code with Hf/W tracking by Francis Nimmo, UCSC
- non-master branch edits by Nick Zube.

PROJECT FLOW:

## Master run file
**run:** CSH script that can run the following (all can also be run individually):
- convert.py: using Jacobson output files, re-style them in O'Brien format to work with accrete5e.f
- Move these new files to a directory, Jac_output/
- accrete5e_for_nick.f: Compile the main Hf/W program by Francis Nimmo
- Loop over all runs, checking which particles to follow with the file followlist.txt, then running mkinput.py to set environment variables for each run, then running accrete5e.exe on each
- store input and output data files in a time-labeled directory within data/
- datagrabber.py: to compile lists of mass, semi-major axis, and epsilon for all surviving particles in each runtype
- accplot.py: create various plots of the acquired data

## Input files   <===
**output.dat:** list of initial conditions and collisions of objects. Read by main program. Requires Raymond or O'Brien format.

- Particle # - iprovenance - semi-major - mass - y partition fraction - eccentricity - time till ejection
- stored in arrays: NDUM,IPROV,AN,XM,YPART,ECC,TEJ
- *Note: YPART is usually set constant by our program*
- Time of collision - ID 1 - Mass 1- ID 2 - Mass 2 - semi-major axis - eccentricity
- TCOL-ICT1-XMT1-ICT2-XMT2-AN-ECC

**mkinput.py:** Python script can create a window to allow user to set variable defaults for accrere4.inp. Can also be run automatically without input, relying on default values set at top of code.

## Main Program
**accrete5e_for_nick.f** (Fortran77)
- Inputs collision data to track features of particles involved.
- Allows control of Y (silicate fraction), DW (partition coefficients),
mixing factors, level of re-equilibration, and individual particle tracking.
- Reports time-evolving stats on individual particle and final stats on
surviving particles.
-Adjusting the PRNT2 variable allows for screen output or output to a text file.

Opens the following files:

- *Read:*
- Unit 20 = accrete4.inp
- Unit 22 = output.dat

- *Write:*
- Unit 28 = end.dat
- Unit 29 = screen_output.dat (optional)
- Unit 40 = follow.dat
- Unit 42 = eps.dat
- Unit 43 = followgmt.dat

## Output files ===> stored in /data in a timestamped folder
**end.dat:** Results for surviving particles. Almost the same as printed output.
-Mass, epsilon, semi-major axis, y (silicate fraction), Hf/W, ECC (unknown, read from output.dat)

**eps.dat:** list of time evolution of epsilon_W value for the chosen particle.

**follow.dat:** times and characteristics of collisions by our followed particle.
-TCOL(J), ICT1,XM(ICT1),ICT2,XM(ICT2),XM(ICT1)+XM(ICT2)
-time of collision, ID of target, mass of target, ID of impactor, mass of impactor, total mass

**followgmt.dat:** more values for the same collisions in follow.dat
-TCOL(J),GAMT,EPSTT,0.3*(3.+LOG10(XMMT))
-time of collision, mass ratio impactor:target, tungsten anom of smaller, calculation with smaller mass 

## Analysis files
**datagrabber.py:** Python script to search for finished output files and compile lists of surviving particles, their mass, semi-major axis, dEpsilon, ID, and Run#.

**accplot.py: Python; plot variations of dEpsilon, mass, semi-major for groups of runs

**accplot.m:** Matlab; plot the dEpsilon_W (tungsten isotope anomaly) and mass vs. time for chosen particle

**accplot_compare.m:** Matlab; allows plotting of multiple datasets at once

Other contributors:
> Nimmo, Francis;
Kleine, Thorsten;
Jacobson, Seth;
Morbidelli, Alessandro;
O'Brien, David;
Walsh, Kevin;
Halliday, Alexander;
Agnor, C;
Yin, Qingzhu;
Jacobsen, Stein;

