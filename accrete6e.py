##############################################################################
# accrete6e.py
#
# Python 2.7.0 script to calculate Hf-W evolution for n-body core accretion 
# simulations
#
# Nick Zube, completed v1.0 on ?
#
# Adapted from Fortran77 code written by Francis Nimmo.
##############################################################################


# better arrays:
# class mantle, core (hf182, w182, hf180, w183)

def Mix(B1,B2,XM1,XM2,Y1,Y2,YMIX,FF,N1,N2,IMIX,PRNT2,DHF,DW,XLHF):

#      B1 AND B2 ARE ARRAYS CONTAINING CONCENTRATIONS OF ELEMENTS:
#      1 - MANTLE 182HF WHICH DECAYS TO 
#      2 - MANTLE 182W
#      3 - MANTLE 180HF (STABLE)
#      4 - MANTLE 183W (STABLE)
#      5 - CORE 182HF WHICH DECAYS TO
#      6 - CORE 182W
#      7 - CORE 180HF
#      8 - CORE 183W
#  *** ON OUTPUT, ORIGINAL ARRAY B1 IS OVERWRITTEN WITH OUTPUT ***

#      THERE ARE 4 MIXING OPTIONS.
#      IMIX=0  THE TWO CORES MIX, AND THE TWO MANTLES MIX
#              WITHOUT ANY EQUILIBRATION ("MERGER")
#      IMIX=1  THE SMALLER OBJECT IS REHOMOGENIZED, ADDED TO
#              THE MANTLE OF THE BIGGER OBJECT, AND THEN
#              CORE SEPARATION OCCURS. THIS IS THE "MAGMA OCEAN"
#              MODEL OF HALLIDAY ET AL.
#      IMIX=2  BOTH OBJECTS ARE TOTALLY REHOMOGENIZED AND
#              THEN CORE FORMATION OCCURS
#      IMIX=-1 BOTH OBJECTS INSTANTLY SEPARATE INTO CORE
#              AND MANTLE IF THEY HAVE NOT ALREADY DONE SO
#              , AND THEN BEHAVES AS IMIX=0. THIS IS THE
#              "PRIMITIVE DIFFERENTIATION" MODEL OF HALLIDAY ET AL.
#              NOTE THAT IN THIS SCENARIO XMIX IS IRRELEVANT
#
#      WE HAVE NOW ADDED INCOMPLETE RE-EQUILIBRATION TO
#      OPTION IMIX=1, VARYING FF FROM 1 (NO RE-EQUILIBRATION)
#      TO FF=0 (COMPLETE RE-EQUILIBRATION)
#
#      Y IS SILICATE MASS FRACTION

	YM1=1.-Y1
	YM2=1.-Y2
	YMIX=((Y1*XM1)+(Y2*XM2))/(XM1+XM2)

	print 'mix ',imix,ym1,ym2,xm2/xm1,ff,dhf,dw

	# CHECK INITIAL/FINAL MASS BALANCE

	for i in range(1,5):
		CK[I]=((XM1*B1[I]*Y1)+(XM2*B2[I]*Y2)+(XM1*B1[I+4]*YM1) + 
			   (XM2*B2[I+4]*YM2))

	if(IMIX == 0):
		for i in range(1,5):
			B[I]=(((B1[I]*XM1*Y1)+(B2[I]*XM2*Y2)) /
				  ((Y1*XM1)+(Y2*XM2)))

		for i in range(5,9):
			B[I]=(((B1[I]*XM1*YM1)+(B2[I]*XM2*YM2)) /
				  ((YM1*XM1)+(YM2*XM2)))

		for i in range(1,9):
			B1[I]=B[I]

	elif(IMIX == 2):

		# FIRST REHOMOGENIZE EVERYTHING

		for i in range(1,5):
			B[I]=(((((Y1*B1[I])+(YM1*B1[I+4]))*XM1)+
				  (((Y2*B2[I])+(YM2*B2[I+4]))*XM2))/(XM1+XM2))

		# NOW DO CORE SEPARATION. HERE DHF AND DW ARE THE
		# PARTITION COEFFTS (CONC(MANTLE)/CONC(CORE))
		# AND Y IS THE MASS FRACTION OF MANTLE (CONSTANT)

		YT=((Y1*XM1)+(Y2*XM2))/(XM1+XM2)
		YTM=1.-YT
		for i in [1,3]:
			# HF/W IN MANTLE
			B1[I]=B[I]/(YT+((1.-YT)/DHF))
			B1[I+1]=B[I+1]/(YT+((1.-YT)/DW))

		for i in [5,7]:
			# HF/W IN CORE
			B1[I]=B(I-4)/(1+(YT*(DHF-1.)))
			B1[I+1]=B(I-3)/(1+(YT*(DW-1.)))          

	elif(IMIX == 1):
		#print 'imix=1 ',xm1,xm2,y1,y2
		if (XM2 <= XM1):
			YM2=1.-Y2
			YM1=1.-Y1
	   
# SECTION ADDED FN JULY 05
# DIFFERENTIATES LARGER OBJECT IF IT IS NOT ALREADY

			if(B1(1) == B1(5)):
				#print 'LARGER OBJECT UNDIFF '
				for i in [1,3]:
					# HF/W IN MANTLEC
					B[I]=B1[I]/(Y1+((1.-Y1)/DHF))
					SB[I+1]=B1[I+1]/(Y1+((1.-Y1)/DW))

				for i in [5,7]:
					# HF/W IN CORE
					B[I]=B1(I-4)/(1+(Y1*(DHF-1.)))
					B[I+1]=B1(I-3)/(1+(Y1*(DW-1.)))          

				for i in range(1,9):
					B1[I]=B[I]

			# DO SAME FOR SMALLER OBJECT

			if B2(1) == B2(5):
				#print 'SMALLER OBJECT UNDIFF '
				for i in [1,3]:
					# HF/W IN MANTLE
					B[I]=B2[I]/(Y2+((1.-Y2)/DHF))
					B[I+1]=B2[I+1]/(Y2+((1.-Y2)/DW))

				for i in [5,7]:
					# HF/W IN CORE
					B[I]=B2(I-4)/(1+(Y2*(DHF-1.)))
					B[I+1]=B2(I-3)/(1+(Y2*(DW-1.)))          

				for i in range(1,9):
					B2[I]=B[I]


	# JACOBSEN AND HARPER SUGGEST W AND HF 
	# OF SMALL OBJECT RE-EQUILIBRATE WITH MANTLE
	# AND ARE THEN SEPARATED TO CORE. I INTERPRET THIS
	# TO MEAN THAT PARTITION HAPPENS AT THIS STAGE,
	# AND THE METAL THEN ACCRETES TO THE CORE

			print '**** ',b1(2),b1(4),b2(2),b2(6),b2(4),b2(8)
			for i in range(1,5):
				B[I]=((Y1*B1[I]*XM1)+(Y2*B2[I]*XM2)+
					  (YM2*B2[I+4]*XM2)*(1.-FF))

				B[I]=B[I]/((Y1*XM1)+(Y2*XM2)+(YM2*XM2*(1.-FF)))
				B[I+4]=B[I]

				B1[I+4]=(YM1*B1[I+4]*XM1)+(YM2*B2[I+4]*XM2*FF)
				B1[I+4]=B1[I+4]/((YM1*XM1)+(YM2*XM2*FF))

			YT=(((Y1*XM1)+(Y2*XM2))/
				((Y1*XM1)+(Y2*XM2)+(YM2*XM2*(1.-FF))))

			for i in range(1,5):
				t1=((b[i])*((y1*xm1)+xm2))+(b1[i+4]*ym1*xm1)
				#print 'check ',t1/ck(i)

			print '**** ',b(2),b(4),yt

			# NOW CARRY OUT PARTITIONING

			for i in [1,3]:
				#HF/W IN MANTLE
				B1[I]=B[I]/(((1.-YT)/DHF)+YT)
				B1[I+1]=B[I+1]/(((1.-YT)/DW)+YT)


			print '**** ',b1(2),b1(4),1./(((1.-YT)/DW)+YT)
			
			for i in [1,3]:
				# HF/W IN CORE OF SMALL OBJECT
				B[I]=B[I]/(1.-YT+(YT*DHF))
				B[I+1]=B[I+1]/(1.-YT+(YT*DW))  

			for i in range(1,5):
				t1=((b1[i]*((y1*xm1)+(y2*xm2)))+(b1[i+4]*ym1*xm1)+
					(b[i+4]*ym2*xm2))
				#print 'check2 ',t1/ck(i)

			# NOW ADD TWO CORES TOGETHER. NOTE THAT CORE SIZE
			# HAS ALREADY INCREASED DUE TO DIRECT ADDITION

			YT2=(YM1*XM1)+(YM2*XM2*FF)
			for i in range(5,9):
				B1[I]=(((B[I]*XM2*YM2*(1.-FF))+(B1[I]*YT2))/
					   (YT2+(YM2*XM2*(1.-FF))))

			# 1ST OBJECT IS SMALLER - also needs checking

		else:
			YM1=1.-Y1     
			YM2=1.-Y2
			if (B2(1) == B2(5)):
				#print 'LARGER OBJECT UNDIFF '
				for i in [1,3]:
					# HF/W IN MANTLE
					B[I]=B2[I]/(Y2+((1.-Y2)/DHF))
					B[I+1]=B2[I+1]/(Y2+((1.-Y2)/DW))

				for i in [5,7]:
					# HF/W IN CORE
					B[I]=B2(I-4)/(1+(Y2*(DHF-1.)))
					B[I+1]=B2(I-3)/(1+(Y2*(DW-1.)))          

				for i in range(1,9):
					B2[I]=B[I]

			# DO SAME FOR SMALLER OBJECT

		   	if (B1(1) == B1(5)):
				#print 'SMALLER OBJECT UNDIFF '
				for i in [1,3]:
					# HF/W IN MANTLE
					B[I]=B1[I]/(Y1+((1.-Y1)/DHF))
					B[I+1]=B1[I+1]/(Y1+((1.-Y1)/DW))
				for i in [5,7]:
					# HF/W IN CORE
					B[I]=B1(I-4)/(1+(Y1*(DHF-1.)))
					B[I+1]=B1(I-3)/(1+(Y1*(DW-1.)))          

				for i in range(1,9):
					B1[I]=B[I]

			for i in range(1,5):
				B[I]=((Y1*B1[I]*XM1)+(Y2*B2[I]*XM2)+
					  (YM1*B1[I+4]*XM1)*(1.-FF))
				B[I]=B[I]/((Y1*XM1)+(Y2*XM2)+(YM1*XM1*(1.-FF)))
				B[I+4]=B[I]

				B2[I+4]=(YM2*B2[I+4]*XM2)+(YM1*B1[I+4]*XM1*FF)
				B2[I+4]=B2[I+4]/((YM2*XM2)+(YM1*XM1*FF))


			YT=(((Y1*XM1)+(Y2*XM2))/
				((Y1*XM1)+(Y2*XM2)+(YM1*XM1*(1.-FF))))

			# NOW CARRY OUT PARTITION

			for i in [1,3]:
				# HF/W IN MANTLE
				B2[I]=B[I]/(((1.-YT)/DHF)+YT)
				B2[I+1]=B[I+1]/(((1.-YT)/DW)+YT)

			for i in [5,7]:
				# HF/W IN CORE OF SMALL OBJECT
				B[I]=B[I]/(1.-YT+(YT*DHF))
				B[I+1]=B[I+1]/(1.-YT+(YT*DW))      

			# NOW ADD TWO CORES TOGETHER

			YT2=(YM1*XM1)+(YM2*XM2*FF)
			for i in range(5,9):
				B2[I]=(((B[I]*XM2*YM2*(1.-FF))+(B2[I]*YT2))/
					   (YT2+(YM2*XM2*(1.-FF))))

			for i in range(1,9):
				B1[I]=B2[I]
				B2[I]=0.

	elif (IMIX == -1):
		# SECOND OBJECT SEPARATES INTO CORE AND MANTLE
		# (IT IT HAS NOT ALREADY DONE SO)
		if (B2(1) == B2(5)):
			#print 'SECOND OBJECT UNDIFF '

			# PARTITION

			for i in [1,3]:
				# HF/W IN MANTLE
				B[I]=B2[I]/(Y2+((1.-Y2)/DHF))
				B[I+1]=B2[I+1]/(Y2+((1.-Y2)/DW))

			for i in [5,7]:
				# HF/W IN CORE
				B[I]=B2(I-4)/(1+(Y2*(DHF-1.)))
				B[I+1]=B2(I-3)/(1+(Y2*(DW-1.)))          

		else: 
			for i in range(1,9):
				B[I]=B2[I]

		# CHECK TO SEE IF OTHER OBJECT ALSO UNDIFF

		if (B1(1) == B1(5)):
			#print 'FIRST OBJECT UNDIFF ',XM1,XM2

			# PARTITION

			for i in [1,3]:
				# HF/W IN MANTLE
				B2[I]=B1[I]/(Y1+((1.-Y1)/DHF))
				B2[I+1]=B1[I+1]/(Y1+((1.-Y1)/DW))

			for i in [5,7]:
				# HF/W IN CORE
				B2[I]=B1(I-4)/(1.+(Y1*(DHF-1.)))
				B2[I+1]=B1(I-3)/(1.+(Y1*(DW-1.)))          

			for i in range(1,9):
				B1[I]=B2[I]

		# NOW COMBINE

		YM1=1.-Y1
		YM2=1.-Y2
		for i in range(1,5):
			B1[I]=(((B1[I]*XM1*Y1)+(B[I]*XM2*Y2))/
				   ((Y1*XM1)+(Y2*XM2)))

		for i in range(5,9):
			B1[I]=(((B1[I]*XM1*YM1)+(B[I]*XM2*YM2))/
				   ((YM1*XM1)+(YM2*XM2)))

	#print 'CHECKING MASS BALANCE'
	for i in range(1,5):
		#CK[I+4]=((XM1*B1[I]*Y1)+(XM2*B2[I]*Y2)+(XM1*B1[I+4]*YM1)+
		#	      (XM2*B2[I+4]*YM2))
		CK[I+4]=(XM1+XM2)*((B1[I]*YMIX)+(B1[I+4]*(1.-YMIX)))
		#print I,CK(I+4)/CK(I)

#****************************************************************************
