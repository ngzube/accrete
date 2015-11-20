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


# classes are used to control namespace and make code commands
# relate to actual chemical equations
class concentration:
	#A class representing Hf or W, with istotopes
	def __init__(self,decay,stable):
		self.decay = decay
		self.stable = stable
	def __iter__(self):
		for i in [self.decay,self.stable]:
			yield i

class feature:
	#A class representing core or mantle, with elements
	def __init__(self,hf,w,y=1):
		self.hf = hf
		self.w = w
		self.y = y
	def __iter__(self):
		for i in [self.hf,self.w]:
			yield i

class body:
	#A class representing a body, with features
	def __init__(self,mantle,core,mass=0):
		self.mantle = mantle
		self.core = core
		self.mass = mass
	def __iter__(self):
		for i in [self.mantle,self.core]:
			yield i

def Differentiate(bod,dhf,dw):
	if not isinstance(bod,body):
		print('Type exception in bod assignment for def Differentiate')
		return

	if body.mantle.hf.decay == body.core.hf.decay:
		# If object is undifferentiated, we differentiate it.

		y = body.mantle.y
		for c_element, m_element, d in zip(body.core,body.mantle,[dhf,dw]):
			#(hf, w)_core; (hf, w)_mantle; (dhf, dw)
			for c, m in zip(c_element, m_element):
				#(decay, stable)
				# Core concentration is calculated first because it
				# depends on original mantle concentration.
				c = m/(1.+y*(d-1.))
				m = m/(y+(1.-y)/d)
					

def Mix(B1,B2,XM1,XM2,Y1,Y2,YMIX,FF,IMIX,DHF,DW):
# removed N1,N2,PRINT2,XLHF

#      B1 AND B2 ARE ARRAYS CONTAINING CONCENTRATIONS OF ELEMENTS:
#      1 - MANTLE 182HF WHICH DECAYS TO 
#      2 - MANTLE 182W
#      3 - MANTLE 180HF (STABLE)
#      4 - MANTLE 183W (STABLE)
#      5 - CORE 182HF WHICH DECAYS TO
#      6 - CORE 182W
#      7 - CORE 180HF
#      8 - CORE 183W

	temp = body(feature(concentration(0,0), concentration(0,0), 0),
				feature(concentration(0,0), concentration(0,0), 0), 
				0)
	body1 = body(feature(concentration(B1[0],B1[2]), 
						 concentration(B1[1],B1[3]), Y1),
				 feature(concentration(B1[4],B1[6]), 
				 		 concentration(B1[5],B1[7]), 1.-Y1), 
				 XM1)
	body2 = body(feature(concentration(B2[0],B2[2]), 
						 concentration(B2[1],B2[3]), Y2),
				 feature(concentration(B2[4],B2[6]), 
				 		 concentration(B2[5],B2[7]), 1.-Y2), 
				 XM2)

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



def FullMix(body1,body2):
	if (not isinstance(body1,body)) or (not isinstance(body2,body):
		print('Type exception in body assignment for def FullMix')
		return

	for feat1, feat2 in zip(body1, body2):
		for 
		conc = (({conc1}*body1.m*body.{feat1}.y + {conc2}*body2.m*{feat2}.y)
				/ (body1.{feat1}.y*body1.m + body2.{feat2}.y*body1.m)

	for i in range(0,4):
		B[i]=(((B1[i]*XM1*Y1)+(B2[i]*XM2*Y2)) /
			  ((Y1*XM1)+(Y2*XM2)))

	for i in range(4,8):
		B[i]=(((B1[i]*XM1*YM1)+(B2[i]*XM2*YM2)) /
			  (((1.-Y1)*XM1)+((1.-Y1)*XM2)))

	for i in range(0,8):
		B1[i]=B[i]



	if(IMIX == 0):
		for i in range(0,4):
			B[i]=(((B1[i]*XM1*Y1)+(B2[i]*XM2*Y2)) /
				  ((Y1*XM1)+(Y2*XM2)))

		for i in range(4,8):
			B[i]=(((B1[i]*XM1*YM1)+(B2[i]*XM2*YM2)) /
				  ((YM1*XM1)+(YM2*XM2)))

		for i in range(0,8):
			B1[i]=B[i]

	elif(IMIX == 2):

		# FIRST REHOMOGENIZE EVERYTHING

		for i in range(0,4):
			B[i]=(((((Y1*B1[i])+(YM1*B1[i+4]))*XM1)+
				  (((Y2*B2[i])+(YM2*B2[i+4]))*XM2))/(XM1+XM2))

		# NOW DO CORE SEPARATION. HERE DHF AND DW ARE THE
		# PARTITION COEFFTS (CONC(MANTLE)/CONC(CORE))
		# AND Y IS THE MASS FRACTION OF MANTLE (CONSTANT)

		YT=((Y1*XM1)+(Y2*XM2))/(XM1+XM2)
		YTM=1.-YT
		for i in [0,2]:
			# HF/W IN MANTLE
			B1[i]=B[i]/(YT+((1.-YT)/DHF))
			B1[i+1]=B[i+1]/(YT+((1.-YT)/DW))

		for i in [4,6]:
			# HF/W IN CORE
			B1[i]=B[i-4]/(1+(YT*(DHF-1.)))
			B1[i+1]=B[i-3]/(1+(YT*(DW-1.)))          

	elif(IMIX == 1):
		#print 'imix=1 ',xm1,xm2,y1,y2
		if (XM2 <= XM1):
			YM2=1.-Y2
			YM1=1.-Y1
	   
# SECTION ADDED FN JULY 05
# DIFFERENTIATES LARGER OBJECT IF IT IS NOT ALREADY

			if(B1[0] == B1[4]):
				#print 'LARGER OBJECT UNDIFF '
				for i in [0,2]:
					# HF/W IN MANTLEC
					B[i]=B1[i]/(Y1+((1.-Y1)/DHF))
					B[i+1]=B1[i+1]/(Y1+((1.-Y1)/DW))

				for i in [4,6]:
					# HF/W IN CORE
					B[i]=B1[i-4]/(1+(Y1*(DHF-1.)))
					B[i+1]=B1[i-3]/(1+(Y1*(DW-1.)))          

				for i in range(1,9):
					B1[i]=B[i]

			# DO SAME FOR SMALLER OBJECT

			if B2[0] == B2[4]:
				#print 'SMALLER OBJECT UNDIFF '
				for i in [0,2]:
					# HF/W IN MANTLE
					B[i]=B2[i]/(Y2+((1.-Y2)/DHF))
					B[i+1]=B2[i+1]/(Y2+((1.-Y2)/DW))

				for i in [4,6]:
					# HF/W IN CORE
					B[i]=B2[i-4]/(1+(Y2*(DHF-1.)))
					B[i+1]=B2[i-3]/(1+(Y2*(DW-1.)))          

				for i in range(0,8):
					B2[i]=B[i]


	# JACOBSEN AND HARPER SUGGEST W AND HF 
	# OF SMALL OBJECT RE-EQUILIBRATE WITH MANTLE
	# AND ARE THEN SEPARATED TO CORE. i INTERPRET THIS
	# TO MEAN THAT PARTITION HAPPENS AT THIS STAGE,
	# AND THE METAL THEN ACCRETES TO THE CORE

			print '**** ',b1[2],b1[4],b2[2],b2[6],b2[4],b2[8]
			for i in range(0,4):
				B[i]=((Y1*B1[i]*XM1)+(Y2*B2[i]*XM2)+
					  (YM2*B2[i+4]*XM2)*(1.-FF))

				B[i]=B[i]/((Y1*XM1)+(Y2*XM2)+(YM2*XM2*(1.-FF)))
				B[i+4]=B[i]

				B1[i+4]=(YM1*B1[i+4]*XM1)+(YM2*B2[i+4]*XM2*FF)
				B1[i+4]=B1[i+4]/((YM1*XM1)+(YM2*XM2*FF))

			YT=(((Y1*XM1)+(Y2*XM2))/
				((Y1*XM1)+(Y2*XM2)+(YM2*XM2*(1.-FF))))

			for i in range(0,4):
				t1=((b[i])*((y1*xm1)+xm2))+(b1[i+4]*ym1*xm1)
				#print 'check ',t1/ck(i)

			print '**** ',b[2],b[4],yt

			# NOW CARRY OUT PARTITIONING

			for i in [0,2]:
				#HF/W IN MANTLE
				B1[i]=B[i]/(((1.-YT)/DHF)+YT)
				B1[i+1]=B[i+1]/(((1.-YT)/DW)+YT)


			print '**** ',b1[2],b1[4],1./(((1.-YT)/DW)+YT)
			
			for i in [4,6]:
				# HF/W IN CORE OF SMALL OBJECT
				B[i]=B[i]/(1.-YT+(YT*DHF))
				B[i+1]=B[i+1]/(1.-YT+(YT*DW))  

			for i in range(0,4):
				t1=((b1[i]*((y1*xm1)+(y2*xm2)))+(b1[i+4]*ym1*xm1)+
					(b[i+4]*ym2*xm2))
				#print 'check2 ',t1/ck(i)

			# NOW ADD TWO CORES TOGETHER. NOTE THAT CORE SIZE
			# HAS ALREADY INCREASED DUE TO DIRECT ADDITION

			YT2=(YM1*XM1)+(YM2*XM2*FF)
			for i in range(4,8):
				B1[i]=(((B[i]*XM2*YM2*(1.-FF))+(B1[i]*YT2))/
					   (YT2+(YM2*XM2*(1.-FF))))

			# 1ST OBJECT IS SMALLER - also needs checking

		else:
			YM1=1.-Y1     
			YM2=1.-Y2
			if (B2[0] == B2[4]):
				#print 'LARGER OBJECT UNDIFF '
				for i in [0,2]:
					# HF/W IN MANTLE
					B[i]=B2[i]/(Y2+((1.-Y2)/DHF))
					B[i+1]=B2[i+1]/(Y2+((1.-Y2)/DW))

				for i in [4,6]:
					# HF/W IN CORE
					B[i]=B2[i-4]/(1+(Y2*(DHF-1.)))
					B[i+1]=B2[i-3]/(1+(Y2*(DW-1.)))          

				for i in range(0,8):
					B2[i]=B[i]

			# DO SAME FOR SMALLER OBJECT

			if (B1[0] == B1[4]):
				#print 'SMALLER OBJECT UNDIFF '
				for i in [0,2]:
					# HF/W IN MANTLE
					B[i]=B1[i]/(Y1+((1.-Y1)/DHF))
					B[i+1]=B1[i+1]/(Y1+((1.-Y1)/DW))
				for i in [4,6]:
					# HF/W IN CORE
					B[i]=B1[i-4]/(1+(Y1*(DHF-1.)))
					B[i+1]=B1[i-3]/(1+(Y1*(DW-1.)))          

				for i in range(0,8):
					B1[i]=B[i]

			for i in range(0,4):
				B[i]=((Y1*B1[i]*XM1)+(Y2*B2[i]*XM2)+
					  (YM1*B1[i+4]*XM1)*(1.-FF))
				B[i]=B[i]/((Y1*XM1)+(Y2*XM2)+(YM1*XM1*(1.-FF)))
				B[i+4]=B[i]

				B2[i+4]=(YM2*B2[i+4]*XM2)+(YM1*B1[i+4]*XM1*FF)
				B2[i+4]=B2[i+4]/((YM2*XM2)+(YM1*XM1*FF))


			YT=(((Y1*XM1)+(Y2*XM2))/
				((Y1*XM1)+(Y2*XM2)+(YM1*XM1*(1.-FF))))

			# NOW CARRY OUT PARTITION

			for i in [0,2]:
				# HF/W IN MANTLE
				B2[i]=B[i]/(((1.-YT)/DHF)+YT)
				B2[i+1]=B[i+1]/(((1.-YT)/DW)+YT)

			for i in [4,6]:
				# HF/W IN CORE OF SMALL OBJECT
				B[i]=B[i]/(1.-YT+(YT*DHF))
				B[i+1]=B[i+1]/(1.-YT+(YT*DW))      

			# NOW ADD TWO CORES TOGETHER

			YT2=(YM1*XM1)+(YM2*XM2*FF)
			for i in range(4,8):
				B2[i]=(((B[i]*XM2*YM2*(1.-FF))+(B2[i]*YT2))/
					   (YT2+(YM2*XM2*(1.-FF))))

			for i in range(0,8):
				B1[i]=B2[i]
				B2[i]=0.

	elif (IMIX == -1):
		# SECOND OBJECT SEPARATES INTO CORE AND MANTLE
		# (IT IT HAS NOT ALREADY DONE SO)
		if (B2[0] == B2[4]):
			#print 'SECOND OBJECT UNDIFF '

			# PARTITION

			for i in [0,2]:
				# HF/W IN MANTLE
				B[i]=B2[i]/(Y2+((1.-Y2)/DHF))
				B[i+1]=B2[i+1]/(Y2+((1.-Y2)/DW))

			for i in [4,6]:
				# HF/W IN CORE
				B[i]=B2[i-4]/(1+(Y2*(DHF-1.)))
				B[i+1]=B2[i-3]/(1+(Y2*(DW-1.)))          

		else: 
			for i in range(0,8):
				B[i]=B2[i]

		# CHECK TO SEE IF OTHER OBJECT ALSO UNDIFF

		if (B1[0] == B1[4]):
			#print 'FIRST OBJECT UNDIFF ',XM1,XM2

			# PARTITION

			for i in [0,2]:
				# HF/W IN MANTLE
				B2[i]=B1[i]/(Y1+((1.-Y1)/DHF))
				B2[i+1]=B1[i+1]/(Y1+((1.-Y1)/DW))

			for i in [4,6]:
				# HF/W IN CORE
				B2[i]=B1[i-4]/(1.+(Y1*(DHF-1.)))
				B2[i+1]=B1[i-3]/(1.+(Y1*(DW-1.)))          

			for i in range(1,9):
				B1[i]=B2[i]

		# NOW COMBINE

		YM1=1.-Y1
		YM2=1.-Y2
		for i in range(0,4):
			B1[i]=(((B1[i]*XM1*Y1)+(B[i]*XM2*Y2))/
				   ((Y1*XM1)+(Y2*XM2)))

		for i in range(4,8):
			B1[i]=(((B1[i]*XM1*YM1)+(B[i]*XM2*YM2))/
				   ((YM1*XM1)+(YM2*XM2)))

	#print 'CHECKING MASS BALANCE'
	for i in range(0,4):
		#CK[i+4]=((XM1*B1[i]*Y1)+(XM2*B2[i]*Y2)+(XM1*B1[i+4]*YM1)+
		#	      (XM2*B2[i+4]*YM2))
		CK[i+4]=(XM1+XM2)*((B1[i]*YMIX)+(B1[i+4]*(1.-YMIX)))
		#print i,CK(i+4)/CK(i)

#****************************************************************************
