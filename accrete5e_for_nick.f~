C
C       PROGRAM ACCRETE5E.F
C
C       READS IN COLLISION OUTPUT FROM N-BODY SIMULATIONS
C       AND CALCULATES HF-W ISOTOPIC EVOLUTION
C
C       BASIC APPROACH DOCUMENTED IN NIMMO AND AGNOR (2006)
C
C       VERSION 4B HAS VARIABLE TIMESTEP
C       VERSION 5 ALLOWS VARIABLE INITIAL ISOTOPIC RATIOS
C       OR CORE:MANTLE RATIOS BASED ON PROVENANCE OF OBJECT
C       VERSION5B DOES AWAY WITH TIME ARRAY WHICH MAKES
C       IT SUITABLE FOR VERY LARGE INITIAL PARTICLE NUMBERS
C       WE CAN VERIFY THAT IT WORKS BY COMPARING WITH V5.
C
C       HAVE ADDED DISCRETIZATION OPTION TO TOGGLE BETWEEN
C       BATCH AND FRACTIONAL EQUILIBRATION
C       VERSION 5D INCLUDES DAVE O'BRIEN'S FORMAT
C       VERSION 5E INCORPORATES INCOMPLETE RE-EQUILIBRATION
C


        REAL TIM(25000),XMT(5000),XP(5000),XMO(5000)
        REAL B1(8),B2(8),BB(5000,8),BC(4),SUM(4),YP3(5000)
        REAL BI(8,10),F1(10),F2(10),YM(10),HFW(5000)
        REAL EPS(5000),YP(5000),XP2(5000),YP2(5000)
        REAL EPSTH(5000),YP4(5000),YP5(5000),ECC(5000)
        REAL YP6(5000),TEJ(5000),STRAC(5000),YP7(5000)
        REAL EPSP(25000),XMP(25000),TIMP(1500),XMPP(1500)
        REAL ABIN(50),XBIN(50),CON(50),TPL(50),FAX(50)


        REAL XM(5000),TCOL(5000),DTCOL(5000),AXES(5000)
        REAL Y(10),YPART(5000)
        REAL AN(5000),DWW(10),TFCOL(1500)
        INTEGER IC1(5000),IC2(5000),IPART(1500),NPAR(5000)
        INTEGER ICOL(5000),IPROV(5000),NCOL(5000),NFIN(5000)
        COMMON/PARAM/DHF,DW,XLHF
        COMMON/WSPACE/W1(400000)
        NAMELIST/INP/DHF,DW,THALF,Y0,BI,KMAX,ITH,KSTEP,
     C        DT,XMIX,YPMX,TCORE,IDUM,IXMIX,ILOG,IWRIT,NPROV,
     C        TSTOP,XRATC,TSCALE,IRAY,IFOL,XMFIN,FINFAC,IDSC,FF

C       GEOCHEM. CONSTANTS. DHF AND DW ARE THE PARTITION COEFFTS
C       (MANTLE/CORE) AND MAY BE RELATED TO FRACTIONATION FACTORS
C       AS FOLLOWS
C       DHF=-F2(1+F1)(1-Y)/((F1*Y*(1+F2))
C       DW=-F2(1-Y)/(F1*Y)
C       HERE F2 IS THE HF/W FRACTIONATION FOR THE CORE AND
C       F1 THE FRACTIONATION FACTOR FOR THE MANTLE
C       THESE FRACTIONATION FACTORS ARE DEFINED IN HARPER & JACOBSEN (1996)
C
C       IF TCORE.NE.0. WE LET ALL THE OBJECTS TO DIFFERENTIATE
C       INTO CORE AND MANTLE AT TIME=TCORE
C       YOFSET MAKES SURE THAT THE DIFFERENT PARTICLES DON'T PLOT
C       ON TOP OF EACH OTHER
C       Y IS THE SILICATE FRACTION OF THE PARTICLES (FIXED HERE)
C       XMIX - IF EITHER COLLIDING OBJECT HAS A MASS GREATER THAN XMIX,
C       THEN THE IMPACT IS "LARGE" (AND MAY HAVE DIFFERENT GEOCHEMICAL
C       CONSEQUENCES TO SMALLER IMPACTS)
C       IXMIX=1 ALLOWS US TO DO AN INTERMEDIATE RE-EQUILIBRATION
C       ICIRC IS A COUNTER OF HOW MANY "LARGE" IMPACTS OCCUR.
C       HERE WE ASSUME THAT MASSES HAVE ALREADY BEEN CONVERTED
C       INTO UNITS OF EARTH MASS.
C       IRAY TOGGLES BETWEEN SEAN RAYMOND AND DAVE O'BRIEN INPUT
C       IFOL IS THE ID OF THE PARTICLE TO BE FOLLOWED
C
C 
        TCORE=0.
        XMIX=0.3
        YOFSET=1.
        DHF=10000.
        DW=0.0392
        NPROV=1
        Y0=0.68
        IRAY=1
        IFOL=888
        XMFIN=0.9496
        FINFAC=0.95
        TFIN=0.
C
C       TIMESTEP DT AND HALF-LIFE THALF ARE IN YRS
C       ILOG CONTROLS PLOTTING, IWRIT CONTROLS OUTPUT
C       TSTOP IS THE TIME THE CODE STOPS

        THALF=9.E6
        DT=1.E5
        ILOG=1
        IWRIT=0
        ITH=0
        KSTEP=100
        TSTOP=150.E6
        XRATC=0.1
C
C       KMAX IS NO OF TIMESTEPS, IMAX IS NO OF PARTICLES
C       TSCALE ALLOWS THE TIMESCALE TO BE ARTIFICIALLY STRETCHED
C 
        KMAX=600
        IDSC=1
        ICIRC=0
C
C       IXMIX CONTROLS HOW MIXING/RE-EQUILBRATION HAPPEN
C       DURING IMPACTS. IT SETS HOW THE PARAMETER IMIX (WHICH 
C       CONTROLS THE MIXING SUBROUTINE) IS VARIED DEPENDING ON
C       IMPACT CONDITIONS.

        IXMIX=0
        TSCALE=1.
C
C       FF IS EQUILIBRATION FRACTION. HERE FF=1 IMPLIES
C       NO RE-EQUILIBRATION AND FF=0 IMPLIES COMPLETE RE-EQUILIBRATION

        FF=0.

        XSIZE=300.
        YSIZE=200.
        IF(YPMX.EQ.0.)YPMX=12.
C
C       BI CONTAINS INITIAL CONCENTRATIONS OF
C       ELEMENTS:
C       1 -  182HF WHICH DECAYS TO 
C       2 -  182W
C       3 -  180HF (STABLE)
C       4 -  183W (STABLE)
C       INDICES 1-4 WILL BE USED FOR MANTLE

        BI(1,1)=2.836E-4
        BI(2,1)=1.850664
        BI(3,1)=2.836
        BI(4,1)=1.
c
c       initial guesses for Pd-Ag system
c
c        BI(1,1)=1.106383E-4
c        BI(2,1)=1.0851
c        BI(3,1)=4.617
c        BI(4,1)=1.

C
C       INDICES 5-8 WILL BE USED FOR CORE

        DO J=5,8
          BI(J,1)=BI(J-4,1)
        END DO
C
C       READ IN FILE FOR CONTROL PARAMETERS

        OPEN(UNIT=20,FILE='accrete4.inp')
        READ(20,INP)
        WRITE(6,INP)
C
C       OUTPUT FILES

        OPEN(UNIT=40,FILE='follow.dat')
        OPEN(UNIT=43,FILE='followgmt.dat')

        DT=DT*TSCALE
        DT0=DT
C
C       SET UP INITIAL SILICATE MASS FRACTION

        DO I=1,NPROV
         IF(Y(I).EQ.0.)Y(I)=Y0
         WRITE(6,*) I,' Y = ',Y(I)
        END DO
C
C       READ IN COLLISION DATA FILE. NOTE THAT O'BRIEN DOES
C       NOT NUMBER HIS PARTICLES SEQUENTIALLY (IE THERE ARE GAPS).
C       COLLISION FILE ALSO INCLUDES INITIAL POSITIONS OF PARTICLES.

        OPEN(UNIT=22,FILE='output.dat')
        J=1
        IF(IRAY.NE.2)READ(22,*) IMAX
        IF(IRAY.EQ.2)IMAX=5000
        WRITE(6,*) 'NO OF PARTICLES ',IMAX
C
C       INITIALIZE

        DO I=1,IMAX
          IPROV(I)=1
          NCOL(I)=0
          NPAR(I)=0
          NFIN(I)=I
          IC1(I)=0
          IF(IRAY.EQ.2)XM(I)=0.
        END DO
C
C       READ IN PROVENANCE DATA - HERE WE CAN ALSO READ IN
C       FE FRACTION OF INDIVIDUAL PARTICLES

        YPSUM=0.
        IF(NPROV.GT.1)THEN
          WRITE(6,*) 'PROVENANCE'
          DO N=1,IMAX
            IF(IRAY.NE.1)READ(22,*) NDUM,IPROV(N),AN(N),XMASS
            IF(IRAY.EQ.1)READ(22,*) NDUM,IPROV(N),AN(N),
     C                           XMASS,YTP,ECC(N),TEJ(N)
c            READ(22,*) NDUM,IPROV(N)
CFN
C           CORRECTING MASS-READING ERROR
CFN
            XM(N)=XMASS
            IF(IRAY.EQ.1)YPART(N)=1.-YTP
            IF(IRAY.NE.1)YPART(N)=Y(IPROV(N))
            YPSUM=YPSUM+YPART(N)
            IF(IRAY.NE.2)WRITE(6,*) N,IPROV(N),AN(N),
     C                                   XM(N),YPART(N),TEJ(N)
C
C           WE CAN KEEP TRACK OF THE MIXING OF SOME ARBITRARY
C           TRACER 
C 
            STRAC(N)=0.1*EXP(-AN(N))
          END DO
        ENDIF
        YPSUM=YPSUM/FLOAT(IMAX)
C
C
C       READ IN COLLISION DATA. TCOL IS THE TIME OF THE COLLISION,
C       ICT1 AND ICT2 ARE THE INDICES OF THE TWO BODIES,
C       XMT1 AND XMT2 ARE THEIR MASSES
C
C       SOME OF RAYMOND'S COLLISIONS APPEAR TWICE, WITH THE
C       SECOND COLLISION HAVING XM2=0. WE FIX BY IGNORING
C       SUCH COLLISIONS. ALSO INDEX ORDER IS MESSED UP WHICH
C       WE SOLVE BY JUST LOOPING THROUGH J OURSELVES.

        J=1
        DO WHILE(J.GE.1)
C
C         CORRECTING MASS-READING ERROR

          IF(IRAY.EQ.0)READ(22,*,END=100) J,TCOL(J),ICT1,
     C                XMT1,ICT2,XMT2,AN(ICT1)
          IF(IRAY.EQ.1)READ(22,*,END=100) JT,TCOL(J),ICT1,
     C                XMT1,ICT2,XMT2,AN(ICT1),ECC(ICT1)
          IF(IRAY.EQ.2)READ(22,*,END=100) TCOL(J),ICT1,XMT1,
     C                ICT2,XMT2

          IC1(J)=ICT1
          IC2(J)=ICT2
          TCOL(J)=TCOL(J)*TSCALE
          I1=IC1(J)
          I2=IC2(J)
C
C         NEXT LINES AVOID ERROR OF OVERWRITING MASS FOR IRAY.NE.2

          IF(IRAY.EQ.2)THEN
            IF(XM(I1).EQ.0.)XM(I1)=XMT1
            IF(XM(I2).EQ.0.)XM(I2)=XMT2
            IF(I1.GT.IMAX)IMAX=I1
            IF(I2.GT.IMAX)IMAX=I2
c            write(6,*) TCOL(J),ICT1,XMT1,ICT2,XMT2,i1,i2,iray
          ENDIF
C
C         AVOIDING ZERO-MASS COLLISIONS

          WRITE(6,*) J,TCOL(J),I1,I2,XM(I1),XM(I2)
          IF(XMT2.GT.0.)J=J+1
        END DO
 100    CONTINUE

C
C       IMAX IS TOTAL NUMBER OF PARTICLES
        
        WRITE(6,*) 'IMAX = ',IMAX
        itmp=0
        DO I=1,IMAX
          XMO(I)=XM(I)
          if(xmo(i).gt.0.)then
            itmp=itmp+1
            write(6,*) i,itmp,xmo(i)
          endif
        END DO
C
C       JMAX IS TOTAL NUMBER OF COLLISIONS

        JMAX=J
        IF(IRAY.EQ.1)JMAX=JMAX-1

C
C       HOW MANY PARTICLES ARE THERE?

        DO J=1,JMAX
          NPAR(IC1(J))=1
          NPAR(IC2(J))=1
        END DO
        NPART=0
        DO I=1,IMAX
          IF(NPAR(I).GE.1)NPART=NPART+1
c          IF(NPAR(I).GE.1)WRITE(6,*) NPART,I
        END DO
        WRITE(6,*) 'NPART = ',NPART
C
C       SIMPLE THEORETICAL CALCULATION - TWO PARTICLES COLLIDING

        IF(ITH.EQ.1)THEN 
          JMAX=1
          IMAX=2
        ENDIF
C
C       SET UP TIME STEP, TYPICALLY 1/10 OF TIME BETWEEN COLLISIONS

        DTCOL(1)=TCOL(1)/10.
        DO J=2,JMAX
         DTCOL(J)=(TCOL(J)-TCOL(J-1))/10.
c         write(6,*) j,dtcol(j)
        END DO
        DTCOL(J+1)=DT0
        WRITE(6,*) 'DTCOL ',J,DTCOL(J+1),DT0
C
C       INITIALIZE ISOTOPIC SIGNATURES

        DO N=1,NPROV
          DO I=1,IMAX
            IF(IPROV(I).EQ.N)THEN
c              write(6,*) i,' nprov = ',n
              BB(I,1)=BI(1,N)
              IF(BI(1,N).EQ.0.)BB(I,1)=BI(1,1)
              BB(I,2)=BI(2,N)
              IF(BI(2,N).EQ.0.)BB(I,2)=BI(2,1)
              BB(I,3)=BI(3,N)
              IF(BI(3,N).EQ.0.)BB(I,3)=BI(3,1)
              BB(I,4)=BI(4,N)
              IF(BI(4,N).EQ.0.)BB(I,4)=BI(4,1)
C
C             NEXT ASSIGNMENT HAS CHANGED FROM BI TO BB

              DO J=5,8
               BB(I,J)=BB(I,J-4)
              END DO
C
C             ASSIGN CORE MASS RATIO IF NOT ALREADY ASSIGNED

              IF(IRAY.NE.1)YPART(I)=Y(N)
             ENDIF
           END DO
        END DO
C
C        CHONDRITIC REFERENCE (BC) FOR ISOTOPES. THIS IS
C        WHAT WE USE TO CALCULATE EPS (THE DEVIATION FROM CHONDRITIC)
C        WE ASSUME THAT NPROV=1 IS CHONDRITIC

         DO I=1,4
           BC(I)=BI(I,1)
         END DO
C
C       CALCULATE FRACTIONATION FACTORS. H&J (1996) GIVE FACTORS OF
C       12 AND -1 FOR F1 AND F2, RESPECTIVELY. IF WE CHANGE
C       Y, WE NEED TO CHANGE DHF AND DW ALSO TO KEEP THE SAME F1,F2.
C       SEE H&J (1996) EQ(4)
C       
        DO N=1,NPROV
          F1(N)=(DHF-DW)*(1.-Y(N))/
     C                          (DW*((Y(N)*DHF)+1.-Y(N)))
          F2(N)=Y(N)*(DW-DHF)/(1.+(Y(N)*(DHF-1.)))
          WRITE(6,*) 'FRACTIONATION FACTORS ',F1(N),F2(N)
          YM(N)=1.-Y(N)
        END DO
C
C       NOTE THAT FRAC FACTORS ARE *NOT* USED IN CALCULATING
C       ISOTOPIC OUTCOMES BELOW (BUT DHF AND DW AND Y ARE)
C
C
C       TIMESCALE IN YRS

        XLHF=-LOG(0.5)/THALF
        WRITE(6,*) 'XLHF = ',XLHF
        J=1

C
C       STEP FORWARD IN TIME

        ICFOL=0
        IEJT=0
        DO K=1,KMAX
C
C          VARIABLE TIMESTEP - DT0 CAN BE SET TO BE QUITE
C          LARGE SINCE EARLY COLLISIONS ARE MEASURED BY DTCOL

           IF(DTCOL(J).LE.DT0.AND.ITH.NE.1)THEN
             DT=DTCOL(J)
           ELSE
             DT=DT0
           ENDIF
           IF(J.GT.JMAX)DT=DT0
           IF(K.EQ.1)TIM(K)=DT
           IF(K.GT.1)TIM(K)=TIM(K-1)+DT
           IF(TIM(K).GT.TSTOP)GOTO 101
           IF(IWRIT.EQ.1.OR.MOD(K,KSTEP).EQ.0)
     C            WRITE(6,*) K,TIM(K),J,TCOL(J),DTCOL(J)
C
C          CHECK FOR WHETHER COLLISION OCCURS THIS TIMESTEP

           ICOLK=0
           DO I=1,IMAX
              ICOL(I)=0
           END DO   
C
C          ICOL KEEPS TRACK OF WHICH PARTICLE EXPERIENCES A COLLISION

           IF(TIM(K).LE.TCOL(J).AND.(TIM(K)+DT).GT.TCOL(J))THEN
              ICOLK=1
              ICOL(IC1(J))=1
              ICOL(IC2(J))=-1

              ICT1=IC1(J)
              ICT2=IC2(J)
              write(6,*) 'collide ',tcol(j),ic1(j),ic2(j),ifol
C
C             DOES THE COLLISION AFFECT THE PARTICLE WE ARE FOLLOWING?

              IF(ICT1.EQ.IFOL.OR.ICT2.EQ.IFOL)THEN
                 write(6,*) 'collision ',j,k,ic1(j),ic2(j),
     C                        tcol(j),tim(k),xm(ic1(j)),xm(ic2(j))
                 IFOL=ICT2
                 IF(XM(ICT1).GE.XM(ICT2))IFOL=ICT1
C
C                DAVE OBRIEN HAS DIFFERENT CONVENTION FOR DECIDING
C                WHICH OF THE TWO INDICES IS RETAINED POST-COLLISION

                 IF(IRAY.EQ.2)THEN
                  IFOL=ICT1
                  IF(ICT2.LT.ICT1)IFOL=ICT2
                 ENDIF

                 ICFOL=ICFOL+1
                 IPART(ICFOL)=ICT1
                 TFCOL(ICFOL)=TCOL(J)
                 IF(ICT1.EQ.IFOL)IPART(ICFOL)=ICT2
C
C                GAMT IS THE MASS RATIO (IMPACTOR:TARGET)
C                EPS IS THE PRE-IMPACT TUNGSTEN ANOMALY
C                XM IS THE PRE-IMPACT MASS
C                YPART IS THE SILICATE MASS FRACTION

                 GAMT=XM(ICT1)/XM(ICT2)
                 IF(GAMT.GT.1.)GAMT=1./GAMT
                 XMMT=XM(ICT1)
                 YPTT=YPART(ICT1)
                 EPSTT=EPS(ICT1)
                 IF(XM(ICT2).LT.XMMT.AND.IRAY.NE.2)THEN
                    XMMT=XM(ICT2)
                    YPTT=YPART(ICT2)
                    EPSTT=EPS(ICT2)
                 ENDIF
C
C                DAVE OBRIEN CONVENTION

                 IF(IRAY.EQ.2)THEN
                   IF(ICT2.LT.ICT1)THEN
                     XMMT=XM(ICT2)
                     YPTT=YPART(ICT2)
                     EPSTT=EPS(ICT2)
                   ENDIF
                 ENDIF
C
C                WRITE OUT COLLISION DATA 

                 WRITE(40,*) TCOL(J),ICT1,XM(ICT1),ICT2,
     C                        XM(ICT2),XM(ICT1)+XM(ICT2)
C
C                OUTPUT FOR GMT SCRIPT
C
C                 WRITE(43,*) TCOL(J),GAMT,YPTT,
C&                                0.3*(3.+LOG10(XMMT))
                 WRITE(43,*) TCOL(J),GAMT,EPSTT,
     C                                0.3*(3.+LOG10(XMMT))

                 write(6,*) TCOL(J),ICT1,XM(ICT1),ICT2,
     C                        XM(ICT2),XM(ICT1)+XM(ICT2)
c                 stop
               ENDIF
C
C              NCOL IS THE NUMBER OF COLLISIONS EACH OBJECT SUFFERS

               IF(IRAY.NE.2)THEN
                 IF(XM(ICT1).GE.XM(ICT2))NCOL(ICT1)=NCOL(ICT1)+1
                 IF(XM(ICT1).LT.XM(ICT2))NCOL(ICT2)=NCOL(ICT2)+1
               ELSE
                 IF(ICT2.GT.ICT1)NCOL(ICT1)=NCOL(ICT1)+1
                 IF(ICT2.LT.ICT1)NCOL(ICT2)=NCOL(ICT2)+1
               ENDIF
            ENDIF          
C
C           CAN CHECK TO SEE WHETHER UNIVERSAL CORE DIFFN
C           OCCURS AT A PARTICULAR TIME

            IF(TCORE.NE.0.AND.TIM(K).LE.TCORE
     C                         .AND.(TIM(K)+DT).GT.TCORE) THEN                  
              WRITE(6,*) '******* CORE FORMATION *******'
C
C             MODIFIED TO AVOID THIS STEP FOR
C             BODIES WHICH HAVE ALREADY DIFFERENTIATED

              DO I=1,IMAX
                 DO IB=1,8
                   B1(IB)=BB(I,IB)
                 END DO
C
C                CORE FORMATION IS CALCULATED USING THE "MIX"
C                SUBROUTINE WITH IMIX=2 AND HAVING EACH PARTICLE
C                COLLIDE WITH ITSELF

                 IF(XM(I).GT.0.AND.B1(1).EQ.BC(1))THEN
                    CALL MIX(B1,B1,XM(I),XM(I),
     C       YPART(I),YPART(I),YMIX,FF,IPROV(I),IPROV(I),2)
                     WRITE(6,*) 'PARTICLE ',I,' UNDIFF AT ',TCORE
                 ENDIF
                 DO IB=1,8
                    BB(I,IB)=B1(IB)
                 END DO
C
C                EPS IS THE ISOTOPIC DEVIATION 
C                FROM CHONDRITIC (EPSILON 182W)
C                PREVIOUSLY RECORDED EVERY TIMESTEP K

                 EPS(I)=
     C                       ((B1(2)*BC(4)/(B1(4)*BC(2)))-1.)*1.E4
               END DO
             ENDIF     
C
C            NOW CYCLE THROUGH ALL PARTICLES EACH TIMESTEP

             DO I=1,IMAX
C
C              CALCULATE MANTLE HF/W RATIO RELATIVE
C              TO CHONDRITIC 

               IF(XM(I).GT.0.)HFW(I)=
     C                 (BB(I,3)/BB(I,4))/(BC(3)/BC(4))-1.
C
C              A COLLISION DOES NOT OCCUR - UPDATE GEOCHEM
C              DUE TO RADIOACTIVE DECAY

               IF(ICOL(I).EQ.0)THEN
                 IF(XM(I).GT.0.)THEN
                   DO IB=1,8
                     B1(IB)=BB(I,IB)
                   END DO
                   CALL DECAY(B1,DT)
                   DO IB=1,8
                     BB(I,IB)=B1(IB)
                   END DO
                   EPS(I)=
     C                       ((B1(2)*BC(4)/(B1(4)*BC(2)))-1.)*1.E4
                 ENDIF
               ELSEIF(ICOL(I).EQ.1)THEN
C
C                A COLLISION DOES OCCUR BETWEEN I1 AND I2 . . .

                 I1=IC1(J)
                 I2=IC2(J)
                 DO IB=1,8
                   B1(IB)=BB(I1,IB)
                   B2(IB)=BB(I2,IB)
                 END DO
                 WRITE(6,*) 'COLLIDE ',I1,I2,XM(I1),XM(I2),
     C                            XM(I1)+XM(I2),J,K,TIM(K),IDSC 
 
                 EPST1=((B1(2)*BC(4)/(B1(4)*BC(2)))-1.)*1.E4
                 EPST2=((B2(2)*BC(4)/(B2(4)*BC(2)))-1.)*1.E4
                 WRITE(6,*) 'INITIAL EPSILONS ',EPST1,EPST2
                 write(6,*) b1(2),b2(2),bc(4),b1(4),b2(4),bc(2)
C
C                UPDATE THE GEOCHEMISTRY - EFFECT OF IMPACT
C                WILL DEPEND ON SIZE OF IMPACTOR. DIFFERENT MIXING
C                REGIMES ARE DESCRIBED BY DIFFERENT VALUES OF THE
C                PARAMETER IMIX (SEE SUBROUTINE 'MIX' FOR DETAILS)

                 XRAT=XM(I1)/XM(I2)
                 IBIG=0
                 IF(XRAT.GT.1.)XRAT=XM(I2)/XM(I1)

                 IF(XRAT.GE.XRATC.AND.
     C                  (XM(I1).GE.XMIX.OR.XM(I2).GE.XMIX))THEN
C
C                   FOR LARGE IMPACTS, CORES MAY ACCRETE WITH NO EQUBM
C
CFN                      IMIX=0
                    IBIG=1
                    IMIX=-1
C
C                   IXMIX=3 ALLOWS MAGMA OCEAN (IMIX=1) FOR LARGE IMPACTS
C                   AND COMPLETE MERGING (IMIX=0) FOR SMALLER UNDIFF IMPACTS

                    IF(IXMIX.EQ.3)IMIX=1
                    ICIRC=ICIRC+1
                  ELSE
C
C                   FOR SMALLER IMPACTS, RE-EQUILIBM WILL OCCUR

                    IMIX=2
                    IF(IXMIX.EQ.1.OR.IXMIX.EQ.3)IMIX=1
C
C                   FOR IXMIX=3, WE ALLOW SIMPLE MERGERS IF
C                   BOTH OBJECTS ARE UNDIFFERENTIATED

                    IF(IXMIX.EQ.3.AND.B1(1).EQ.BC(1).
     C                         AND.B2(1).EQ.BC(1))IMIX=0
                  ENDIF
C
C                 CAN APPLY INTERMEDIATE RE-EQUILIBRATION INSTEAD

                  IF(IXMIX.EQ.-1.AND.IBIG.EQ.0)IMIX=-1
C
C                 CAN ONLY DO RE-EQUILIBRATION FOR LARGE IMPACTS)

                  IF(IXMIX.EQ.4.AND.IBIG.EQ.0)IMIX=-1
                  IF(IXMIX.EQ.4.AND.IBIG.EQ.1)IMIX=1

                  WRITE(6,*) 'INITIAL STABLES ',B1(3)
     C     ,B1(4),B1(3)/B1(4),B2(3),B2(4),B2(3)/B2(4)
                  IF(IBIG.EQ.1)WRITE(6,*) 
     C             '*** BIG IMPACT ***'   
C
C                DISCRETIZATION TO ALLOW TOGGLING BETWEEN
C                BATCH AND FRACTIONAL EQUILIBRATION

                 IF(XM(I1).GT.XM(I2))THEN
                   XM1T=XM(I1)
                   XM2T=XM(I2)/FLOAT(IDSC)
                 ELSE
                   XM2T=XM(I2)
                   XM1T=XM(I1)/FLOAT(IDSC)
                 ENDIF
                 DTT=DT/FLOAT(IDSC)
C
C                THE 'MIX' SUBROUTINE IS THE ONE WHICH
C                DOES THE ISOTOPIC MIXING CALCULATIONS
C                ON OUTPUT, THE INPUT ARRAY B1 IS OVERWRITTEN
C                BY DOING THE CALCULATIONS IN MANY STEPS (IDSC>>1), 
C                RATHER THAN 1 STEP (IDSC=1)
C                WE CAN RECOVER THE 'EQUILIBRATIVE' END-MEMBER RATHER
C                THAN THE 'BATCH' END-MEMBER 

                 DO II=1,IDSC
                   CALL MIX(B1,B2,XM1T,XM2T,YPART(I1),
     C               YPART(I2),YMIX,FF,IPROV(I1),IPROV(I2),IMIX)
C
C                  ISOTOPIC DECAY CONTINUES TO HAPPEN

                   CALL DECAY(B1,DTT)
c                   write(6,*) idsc,ii,xm1t,xm2t,b1(1)
                 END DO


                  WRITE(6,*) 'FINAL STABLES '
     C             ,B1(3),B1(4),B1(3)/B1(4)
C
C                 UPDATE PARTICLE MASS CONCENTRATIONS

                  YPART(I1)=YMIX
                  YPART(I2)=YMIX
C
C                 UPDATE TRACER CONCENTRATION

                  IOB1=I1
                  IOB2=I2
                  IF(IRAY.EQ.2.AND.I2.LT.I1)THEN
                    IOB1=I2
                    IOB2=I1
                  ENDIF

                  STRAC(IOB1)=((STRAC(IOB1)*XM(IOB1))+
     C             (STRAC(IOB2)*XM(IOB2)))/(XM(IOB1)+XM(IOB2))
                  STRAC(IOB2)=0.

C
C                 CONSEQUENCES OF COLLISION. MASS ALL ENDS UP IN THE
C                 PARTICLE I1, MASS OF PARTICLE I2 SET TO ZERO
C                 AND CONCENTRATIONS IN PARTICLE I2 =0
C
C                 RAYMOND ALSO USES THIS CONVENTION

                  IF(IRAY.NE.2)THEN
                    XM(I1)=XM(I1)+XM(I2)
                    XM(I2)=0.
                    DO IB=1,8
                       BB(I1,IB)=B1(IB)
                       BB(I2,IB)=0.
                    END DO
                    EPS(I1)=
     C                     ((B1(2)*BC(4)/(B1(4)*BC(2)))-1.)*1.E4
                    EPS(I2)=0.
C
C                   RECORD WHERE DESTROYED PARTICLE(S) END UP

                    NFIN(I2)=I1
                    CALL REPLACE(XMO,NFIN,IMAX,I2,I1)
                    WRITE(6,*) 'FINAL EPSILONS ',EPS(I1),
     C                                    EPS(I2),NPART
                  ELSE
C
C                   DAVE OBRIEN CONVENTION DIFFERENT

                    IOB1=I1
                    IOB2=I2
                    IF(I2.LT.I1)THEN
                      IOB1=I2
                      IOB2=I1
                    ENDIF
                    XM(IOB1)=XM(IOB1)+XM(IOB2)
                    XM(IOB2)=0.
                    DO IB=1,8
                       BB(IOB1,IB)=B1(IB)
                       BB(IOB2,IB)=0.
                    END DO
                    EPS(IOB1)=
     C                     ((B1(2)*BC(4)/(B1(4)*BC(2)))-1.)*1.E4
                    EPS(IOB2)=0. 
                    WRITE(6,*) 'FINAL EPSILONS ',EPS(IOB1),
     C                      EPS(IOB2),NPART
                    write(6,*) b1(2),b1(4),bc(2),bc(4)
C
C                   RECORD WHERE DESTROYED PARTICLE ENDS UP

                    NFIN(IOB2)=IOB1
                    CALL REPLACE(XMO,NFIN,IMAX,IOB2,IOB1)

                  ENDIF

                 IF(I1.EQ.IFOL.OR.I2.EQ.IFOL)THEN
C
C                  WE WOULD LIKE TO FIND TIME OF LAST BIG IMPACT
C                  WHERE 'BIG' IS DEFINED AS >5%

                   IF(XRAT.GT.0.05)THEN
                     TBFAC=TIM(K)
                     BEPSW1=EPST1
                     BEPSW2=EPST2
                     IF(IRAY.NE.2)BEPSW3=EPS(I1)
                     IF(IRAY.EQ.2)BEPSW3=EPS(IOB1)
                     BFACT=XRAT
                   ENDIF
                 ENDIF
C
C
C                 WE WANT TO BE ABLE TO PLOT WHERE AND WHEN
C                 THE "BIG" COLLISIONS OCCUR
C                 MODIFIED OCT 08 TO ONLY PLOT FOR PARTICLE
C                 BEING FOLLOWED

                  IF((I1.EQ.IFOL.OR.I2.EQ.IFOL).AND.IBIG.EQ.1)THEN
                    XP2(ICIRC)=TIM(K)
                    IF(ILOG.GE.2.AND.TIM(K).GT.0.)
     C                               XP2(ICIRC)=LOG10(TIM(K))
                    YP2(ICIRC)=EPS(I1)+(YOFSET*FLOAT(I1-1))
                    IF(EPS(I1).EQ.0.)YP2(ICIRC)=
     C                                  EPS(I2)+(YOFSET*FLOAT(I2-1))
                    YP3(ICIRC)=XM(I2)+XM(I1)
                    IF(ILOG.EQ.2)YP3(ICIRC)=LOG10(YP3(ICIRC))
                  ENDIF
                  ITOT=ITOT-1

                ENDIF
C
C               IF PARTICLE IS EJECTED FROM THE SYSTEM THEN
C               WE ALSO STOP PLOTTING IT
C
c                write(6,*) k,i,tim(k),tim(k-1),tej(i)
                IF(K.GT.1.AND.IRAY.EQ.1.AND.TIM(K).GT.TEJ(I)
     C                           .AND.TIM(K-1).LE.TEJ(I))THEN
                  XM(I)=0.
                  AN(I)=1000.
                  IEJT=IEJT+1
                  WRITE(6,*) '****EJECTED**** ',I,TEJ(I),IEJT
                ENDIF

              END DO
C
C             IF A COLLISION OCCURED THIS TIMESTEP, UPDATE J

              IF(ICOLK.EQ.1)J=J+1
C
C             PLOT VALUES FOR THE OBJECT WE ARE FOLLOWING AND FIND WHEN IT
C             EXCEEDS A CERTAIN FACTOR OF ITS FINAL MASS

              EPSP(K)=EPS(IFOL)
              XMP(K)=XM(IFOL)
              IF(XM(IFOL).GE.(FINFAC*XMFIN).AND.TFIN.EQ.0.)
     C                                            TFIN=TIM(K)
C
C           CALCULATE THEORETICAL VALUE IF ITH=1

            IF(ITH.EQ.1)THEN
C
C             JACOBSEN APPROACH

              Q4=1.E4*BI(3,1)/BI(2,1)
              T7=-EXP(-XLHF*TIM(K))+EXP(-XLHF*TCORE)
              T8=BI(1,1)/BI(3,1)
              EPSTH(K)=Q4*T8*F1(1)*T7
              IF(TIM(K).LT.TCORE)EPSTH(K)=0.
            ENDIF
C
C           NEED TO UPDATE THE CHONDRITIC VALUES TO CALCULATE EPSILON

            BC(2)=BC(2)+(BC(1)*(1.-EXP(-XLHF*DT)))
            BC(1)=BC(1)*EXP(-XLHF*DT)
C
C           CHECK THAT MASS BALANCE IS MAINTAINED

            XMS=0.
            DO JJ=1,4
              SUM(JJ)=0.
            END DO
            DO I=1,IMAX
C             WRITE(6,*) I,XM(I)
             XMT(I)=XM(I)
             XMS=XMS+XM(I)
             YT=Y(IPROV(I))
             YMT=1.-YT
             DO JJ=1,4
              SUM(JJ)=SUM(JJ)+(XM(I)*
     C                     ((YT*BB(I,JJ))+(YMT*BB(I,JJ+4))))
             END DO
            END DO
            IF(IWRIT.EQ.1)THEN 
              WRITE(6,*) 'ITOT = ',ITOT,' SUM = ',XMS
              WRITE(6,*) 'CHEM SUMS ',SUM(1)+SUM(2),SUM(3),SUM(4)
              WRITE(6,*)
            ENDIF
C
C         NEXT TIMESTEP
C 
          END DO
101       CONTINUE

       KMAX=K-1
       WRITE(6,*) 'KMAX = ',KMAX,TIM(KMAX)
       WRITE(6,*) 'TOTAL NUMBER EJECTED ',IEJT
c       stop
C
C      WRITE OUT FINAL MASSES 

       WRITE(6,*) 'FINAL MASSES'
       WRITE(6,*)  'i, mass, y, semi-major axis, N col:'
       XMTOT=0.
       DO I=1,IMAX
        IF(XM(I).NE.0)WRITE(6,*) I,XM(I),YPART(I),AN(I),NCOL(I)
        IF(I.GT.1.OR.IRAY.EQ.1)XMTOT=XMTOT+XM(I)
       END DO
       WRITE(6,*) 'TOTAL SURVIVING MASS: ',XMTOT,KMAX
       WRITE(6,*) 
       WRITE(6,*) 'TRACKING PARTICLE ',IFOL,XM(IFOL),AN(IFOL)
       WRITE(6,*) 'MASS EXCEEDS ',FINFAC,' AT ',TFIN/1.E6,' MYR'
       WRITE(6,*) 'MEAN INITIAL SILICATE MASS FRACTION ',YPSUM
       DO I=1,ICFOL
c        WRITE(6,*) I,IPART(I),TFCOL(I)
       END DO
C
C
C**********************************************************************
C
C      PLOTTING FOLLOWS - COMMENTED OUT BY CP

CP       CALL STARTP(0)
       XMX=4.0
       XMN=0.
       XTICK=0.5
       YMX=0.4 
       YMN=0.
       YTICK=0.05
C
C      PLOT EVOLUTION OF INDIVIDUAL OBJECT BEING FOLLOWED IN MASS, EPS
C      XMP IS THE MASS, TIM IS THE TIME, EPSP IS THE TUNGSTEN ANOMALY

       XMX=TIM(KMAX)
       XMN=0.
       XTICK=10.E6
       YMX=1.6
       YMN=0.
       YTICK=0.1
       ISTART=1
cfn
c kludge 1st aug 08 - remove!
c
       IF(ILOG.EQ.1)THEN
         YMX=0.4
         YMN=-1.
         YTICK=0.2
         do k=1,kmax
           xmp(k)=log10(xmp(k))
         end do
       ELSEIF(ILOG.EQ.2)THEN
         YMX=0.301
         YMN=-3.0
         YTICK=0.5
         DO J=1,KMAX
           XMP(J)=LOG10(XMP(J))
         END DO
       ELSEIF(ILOG.EQ.3)THEN
         YMX=0.12
         YMN=0.
         YTICK=0.01
       ENDIF
C
C      DECIMATE

       J=1
       DO K=1,KMAX
         IF(K.EQ.1.OR.XMP(K).NE.XMP(K-1).OR.MOD(K,10).EQ.0)THEN
           TIMP(J)=TIM(K)
           XMPP(J)=XMP(K)
c           WRITE(6,*) J,TIMP(J),XMPP(J)
           J=J+1
         ENDIF
       END DO
       TIMP(J)=TIM(KMAX)
       XMPP(J)=XMP(KMAX)
       IF(ILOG.GE.2)THEN
          DO K=1,KMAX
            IF(TIMP(K).GT.0.)TIMP(K)=LOG10(TIMP(K))
          END DO 
          XMX=9.
          XMN=3.
          XTICK=1.
          TIMP(J)=LOG10(TIM(KMAX))
       ENDIF
CP       CALL XYPLOT(TIMP,XMPP,J,XMX,XMN,YMX,YMN,
CP&           XTICK,YTICK,XSIZE,YSIZE,1,1)
CP       CALL XYPLOT(TIMP,XMPP,J,XMX,XMN,YMX,YMN,
CP&           XTICK,YTICK,XSIZE,YSIZE,0,1)

C
C      PLOT WHEN "BIG" COLLISIONS OCCUR

CP       CALL PEN(4)
CP       CALL XYPLOT(XP2,YP3,ICIRC,XMX,XMN,YMX,YMN,
CP&           XTICK,YTICK,XSIZE,YSIZE,0,-1)

CP       CALL PICCLE
 
       WRITE(6,*) 'PLOTTING GEOCHEM'
       YMN=-1.
       YTICK=1.
       ISTART=1
C
C      DECIMATE
C
       J=1
       DO K=1,KMAX
         IF(K.EQ.1.OR.XMP(K).NE.XMP(K-1).OR.MOD(K,10).EQ.0)THEN
           TIMP(J)=TIM(K)
           XMPP(J)=EPSP(K)
C           WRITE(6,*) J,TIMP(J),XMPP(J)
           J=J+1
         ENDIF
       END DO
       TIMP(J)=TIM(KMAX)
       XMPP(J)=EPSP(KMAX)
       IF(ILOG.GE.2)THEN
          DO K=1,KMAX
            IF(TIMP(K).GT.0.)TIMP(K)=LOG10(TIMP(K))
          END DO 
          TIMP(J)=LOG10(TIM(KMAX))
       ENDIF
CP       CALL XYPLOT(TIMP,XMPP,J,XMX,XMN,YPMX,YMN,
CP&           XTICK,YTICK,XSIZE,YSIZE,1,1)
CP       CALL XYPLOT(TIMP,XMPP,J,XMX,XMN,YPMX,YMN,
CP&           XTICK,YTICK,XSIZE,YSIZE,0,1)
C
C      WRITE OUT EPSILON EVOLUTION OF PARTICLE WE ARE FOLLOWING

       open(unit=42,file='eps.dat')
       do jj=1,j
         write(42,*) jj,timp(jj),xmpp(jj)
       end do
       close(42)
       IF(ITH.EQ.1)THEN
CP         CALL PEN(3)
         DO J=1,KMAX
           XP(J)=EPSTH(J)+(YOFSET*FLOAT(I-3))
         END DO
CP         CALL XYPLOT(TIM,XP,KMAXP,XMX,XMN,YPMX,YMN,
CP&           XTICK,YTICK,XSIZE,YSIZE,0,1) 
       ENDIF
C
C      PLOT LARGE IMPACTS (INSTANT CORE ACCRETION)

CP       CALL PEN(4)
CP       CALL XYPLOT(XP2,YP2,ICIRC,XMX,XMN,YMX,YMN,
CP&           XTICK,YTICK,XSIZE,YSIZE,0,-1)
CP       CALL PICCLE
C
C      PLOT END-STATES IN MASS,EPS SPACE

       XMX=2.5
       XMN=0.
       XTICK=0.1
       YMX=25.
       YMN=0.
       YTICK=1.
       IF(ILOG.EQ.2)THEN
         XMX=0.5
         XMN=-2.5
         XTICK=1.
       ENDIF
       J=0
C
C      WRITE OUT FINAL CHARACTERISTICS OF ALL SURVIVING PARTICLES

       OPEN(UNIT=28,FILE='end.dat')
       WRITE(6,*) 'j, i, N col, mass, eps, semi-major axis, Hf/W, y'
       DO I=1,IMAX
         IF(XM(I).GT.0.AND.NCOL(I).GT.1) THEN
C
C          ONLY WRITE OUT THOSE OBJECTS WHICH SUFFERED COLLISIONS

           J=J+1
           XP2(J)=XM(I)
           IF(ILOG.EQ.1.OR.ILOG.EQ.2)XP2(J)=LOG10(XM(I))
           YP2(J)=LOG10(EPS(I))
           YP2(J)=EPS(I)
	   YP4(J)=AN(I)
           YP5(J)=YPART(I)*5.
           YP6(J)=ECC(I)
           YP7(J)=STRAC(I)

           WRITE(6,*) J,I,NCOL(I),XM(I),EPS(I),AN(I),
     C                                          HFW(I),YPART(I)
C&                                         STRAC(I),YPART(I)
C           WRITE(6,*) 'STABLE HF W ',BB(I,3),BB(I,4)
           WRITE(28,*) XM(I),EPS(I),AN(I),
     C                              YPART(I),HFW(I),ECC(I)
C           IF(XM(I).GT.XMX)XMX=XM(I)
         ENDIF
       END DO
C       DO I=1,IMAX
C         XP2(I)=XP2(I)/XMX
C       END DO
C       XMX=1.
       JMAX=J
CP       CALL XYPLOT(XP2,YP2,JMAX,XMX,XMN,YMX,YMN,XTICK,
CP&         YTICK,XSIZE,YSIZE,1,-1)
CP       CALL PICCLE

C
C      WRITE OUT LAST BIG IMPACT CHARACTERISTICS

       WRITE(6,*) 'LAST BIG IMPACT ',TBFAC/1.E6,BFACT
       WRITE(6,*) 'EPSILONS ',BEPSW1,BEPSW2,BEPSW3              

CP       CALL ENGPLT

       END
C
C****************************************************************
C
       SUBROUTINE CIRCPLOT(ISTART,X0,Y0,RFAC,XMX,XMN,YMX,YMN,
     C               XTICK,YTICK)
C
       REAL XP(90),YP(90)
       
       PI=4.*ATAN(1.)
       DTH=4.*PI/180.
       XSIZE=150.
       YSIZE=100.
       DX=XMX-XMN
       DY=(YMX-YMN)*(XSIZE/YSIZE)
       DO I=1,90
        TH=DTH*FLOAT(I)
        XT=RFAC*0.02*DX*COS(TH)
        YT=RFAC*0.02*DY*SIN(TH)
        XP(I)=X0+XT
        YP(I)=Y0+YT
       END DO
CP       CALL XYPLOT(XP,YP,90,XMX,XMN,YMX,YMN,XTICK,YTICK,
CP&             XSIZE,YSIZE,ISTART,1)
       IF(ISTART.EQ.1)ISTART=0
       RETURN
       END
C
C*******************************************************************************

       SUBROUTINE MIX(B1,B2,XM1,XM2,Y1,Y2,YMIX,FF,
     C                                   N1,N2,IMIX)

C
       COMMON/PARAM/DHF,DW,XLHF

       REAL B1(8),B2(8),B(8),CK(8)
C
C      B1 AND B2 ARE ARRAYS CONTAINING CONCENTRATIONS OF
C      ELEMENTS:
C      1 - MANTLE 182HF WHICH DECAYS TO 
C      2 - MANTLE 182W
C      3 - MANTLE 180HF (STABLE)
C      4 - MANTLE 183W (STABLE)
C      5 - CORE 182HF WHICH DECAYS TO
C      6 - CORE 182W
C      7 - CORE 180HF
C      8 - CORE 183W
C
C      *** ON OUTPUT, ORIGINAL ARRAY B1 IS OVERWRITTEN WITH OUTPUT ***
C
C      THERE ARE 4 MIXING OPTIONS.
C      IMIX=0  THE TWO CORES MIX, AND THE TWO MANTLES MIX
C              WITHOUT ANY EQUILIBRATION ("MERGER")
C      IMIX=1  THE SMALLER OBJECT IS REHOMOGENIZED, ADDED TO
C              THE MANTLE OF THE BIGGER OBJECT, AND THEN
C              CORE SEPARATION OCCURS. THIS IS THE "MAGMA OCEAN"
C              MODEL OF HALLIDAY ET AL.
C      IMIX=2  BOTH OBJECTS ARE TOTALLY REHOMOGENIZED AND
C              THEN CORE FORMATION OCCURS
C      IMIX=-1 BOTH OBJECTS INSTANTLY SEPARATE INTO CORE
C              AND MANTLE IF THEY HAVE NOT ALREADY DONE SO
C              , AND THEN BEHAVES AS IMIX=0. THIS IS THE
C              "PRIMITIVE DIFFERENTIATION" MODEL OF HALLIDAY ET AL.
C              NOTE THAT IN THIS SCENARIO XMIX IS IRRELEVANT
C
C      WE HAVE NOW ADDED INCOMPLETE RE-EQUILIBRATION TO
C      OPTION IMIX=1, VARYING FF FROM 1 (NO RE-EQUILIBRATION)
C      TO FF=0 (COMPLETE RE-EQUILIBRATION)
C
C      Y IS SILICATE MASS FRACTION

       YM1=1.-Y1
       YM2=1.-Y2
       YMIX=((Y1*XM1)+(Y2*XM2))/(XM1+XM2)

       write(6,*) 'mix ',imix,ym1,ym2,xm2/xm1,ff,dhf,dw
C
C      CHECK INITIAL/FINAL MASS BALANCE

       DO I=1,4
         CK(I)=(XM1*B1(I)*Y1)+(XM2*B2(I)*Y2)+(XM1*B1(I+4)*YM1)
     C                     +(XM2*B2(I+4)*YM2)
       END DO

       IF(IMIX.EQ.0) THEN
          DO I=1,4
            B(I)=((B1(I)*XM1*Y1)+(B2(I)*XM2*Y2))/
     C                                    ((Y1*XM1)+(Y2*XM2))
          END DO
          DO I=5,8
            B(I)=((B1(I)*XM1*YM1)+(B2(I)*XM2*YM2))/
     C                                  ((YM1*XM1)+(YM2*XM2))
          END DO
          DO I=1,8
            B1(I)=B(I)
          END DO
       ELSEIF(IMIX.EQ.2) THEN
C
C         FIRST REHOMOGENIZE EVERYTHING

          DO I=1,4
           B(I)=((((Y1*B1(I))+(YM1*B1(I+4)))*XM1)+
     C               (((Y2*B2(I))+(YM2*B2(I+4)))*XM2))/(XM1+XM2)
          END DO
C
C         NOW DO CORE SEPARATION. HERE DHF AND DW ARE THE
C         PARTITION COEFFTS (CONC(MANTLE)/CONC(CORE))
C         AND Y IS THE MASS FRACTION OF MANTLE (CONSTANT)

          YT=((Y1*XM1)+(Y2*XM2))/(XM1+XM2)
          YTM=1.-YT
          DO I=1,3,2
C
C          HF/W IN MANTLE

           B1(I)=B(I)/(YT+((1.-YT)/DHF))
           B1(I+1)=B(I+1)/(YT+((1.-YT)/DW))
          END DO
          DO I=5,7,2
C
C          HF/W IN CORE

           B1(I)=B(I-4)/(1+(YT*(DHF-1.)))
           B1(I+1)=B(I-3)/(1+(YT*(DW-1.)))          
          END DO

       ELSEIF(IMIX.EQ.1) THEN
c         write(6,*) 'imix=1 ',xm1,xm2,y1,y2
         IF(XM2.LE.XM1)THEN
           YM2=1.-Y2
           YM1=1.-Y1
C         
C          SECTION ADDED FN JULY 05
C          DIFFERENTIATES LARGER OBJECT IF IT IS NOT ALREADY

           IF(B1(1).EQ.B1(5))THEN
c            WRITE(6,*) 'LARGER OBJECT UNDIFF '
            DO I=1,3,2
C
C            HF/W IN MANTLEC
             B(I)=B1(I)/(Y1+((1.-Y1)/DHF))
             B(I+1)=B1(I+1)/(Y1+((1.-Y1)/DW))
            END DO
            DO I=5,7,2
C
C            HF/W IN CORE

             B(I)=B1(I-4)/(1+(Y1*(DHF-1.)))
             B(I+1)=B1(I-3)/(1+(Y1*(DW-1.)))          
            END DO
            DO I=1,8
              B1(I)=B(I)
            END DO
           ENDIF
C
C          DO SAME FOR SMALLER OBJECT

           IF(B2(1).EQ.B2(5))THEN
c            WRITE(6,*) 'SMALLER OBJECT UNDIFF '
            DO I=1,3,2
C
C            HF/W IN MANTLE

             B(I)=B2(I)/(Y2+((1.-Y2)/DHF))
             B(I+1)=B2(I+1)/(Y2+((1.-Y2)/DW))
            END DO
            DO I=5,7,2
C
C            HF/W IN CORE

             B(I)=B2(I-4)/(1+(Y2*(DHF-1.)))
             B(I+1)=B2(I-3)/(1+(Y2*(DW-1.)))          
            END DO
            DO I=1,8
              B2(I)=B(I)
            END DO
           ENDIF
C
C          JACOBSEN AND HARPER SUGGEST W AND HF 
C          OF SMALL OBJECT RE-EQUILIBRATE WITH MANTLE
C          AND ARE THEN SEPARATED TO CORE. I INTERPRET THIS
C          TO MEAN THAT PARTITION HAPPENS AT THIS STAGE,
C          AND THE METAL THEN ACCRETES TO THE CORE
C
          write(6,*) '**** ',b1(2),b1(4),b2(2),b2(6),
     C                                        b2(4),b2(8)
          DO I=1,4
           B(I)=((Y1*B1(I)*XM1)+(Y2*B2(I)*XM2)+
     C                           (YM2*B2(I+4)*XM2)*(1.-FF))
cfn
           B(I)=B(I)/((Y1*XM1)+(Y2*XM2)+(YM2*XM2*(1.-FF)))
           B(I+4)=B(I)
cfn
           B1(I+4)=(YM1*B1(I+4)*XM1)+(YM2*B2(I+4)*XM2*FF)
           B1(I+4)=B1(I+4)/((YM1*XM1)+(YM2*XM2*FF))
          END DO

          YT=((Y1*XM1)+(Y2*XM2))/
     C                 ((Y1*XM1)+(Y2*XM2)+(YM2*XM2*(1.-FF)))
          do i=1,4
            t1=((b(i))*((y1*xm1)+xm2))+(b1(i+4)*ym1*xm1)
c            write(6,*) 'check ',t1/ck(i)
          end do

          write(6,*) '**** ',b(2),b(4),yt
C
C         NOW CARRY OUT PARTITIONING

          DO I=1,3,2
C
C          HF/W IN MANTLE
C

           B1(I)=B(I)/(((1.-YT)/DHF)+YT)
           B1(I+1)=B(I+1)/(((1.-YT)/DW)+YT)
          END DO

          write(6,*) '**** ',b1(2),b1(4),1./(((1.-YT)/DW)+YT)
          DO I=5,7,2
C
C          HF/W IN CORE OF SMALL OBJECT

           B(I)=B(I)/(1.-YT+(YT*DHF))
           B(I+1)=B(I+1)/(1.-YT+(YT*DW))  
          END DO
          do i=1,4
            t1=(b1(i)*((y1*xm1)+(y2*xm2)))+(b1(i+4)*ym1*xm1)+
     C                  (b(i+4)*ym2*xm2)
c            write(6,*) 'check2 ',t1/ck(i)
          end do
C
C         NOW ADD TWO CORES TOGETHER. NOTE THAT CORE SIZE
C         HAS ALREADY INCREASED DUE TO DIRECT ADDITION

          YT2=(YM1*XM1)+(YM2*XM2*FF)
          DO I=5,8
           B1(I)=((B(I)*XM2*YM2*(1.-FF))+(B1(I)*YT2))/
     C                                (YT2+(YM2*XM2*(1.-FF)))
          END DO
C
C        1ST OBJECT IS SMALLER - also needs checking
C
         ELSE

           YM1=1.-Y1     
           YM2=1.-Y2
           IF(B2(1).EQ.B2(5))THEN
c            WRITE(6,*) 'LARGER OBJECT UNDIFF '
            DO I=1,3,2
C
C            HF/W IN MANTLE

             B(I)=B2(I)/(Y2+((1.-Y2)/DHF))
             B(I+1)=B2(I+1)/(Y2+((1.-Y2)/DW))
            END DO
            DO I=5,7,2
C
C            HF/W IN CORE

             B(I)=B2(I-4)/(1+(Y2*(DHF-1.)))
             B(I+1)=B2(I-3)/(1+(Y2*(DW-1.)))          
            END DO
            DO I=1,8
              B2(I)=B(I)
            END DO
           ENDIF
C
C          DO SAME FOR SMALLER OBJECT

           IF(B1(1).EQ.B1(5))THEN
c            WRITE(6,*) 'SMALLER OBJECT UNDIFF '
            DO I=1,3,2
C
C            HF/W IN MANTLE

             B(I)=B1(I)/(Y1+((1.-Y1)/DHF))
             B(I+1)=B1(I+1)/(Y1+((1.-Y1)/DW))
            END DO
            DO I=5,7,2
C
C            HF/W IN CORE

             B(I)=B1(I-4)/(1+(Y1*(DHF-1.)))
             B(I+1)=B1(I-3)/(1+(Y1*(DW-1.)))          
            END DO
            DO I=1,8
              B1(I)=B(I)
            END DO
           ENDIF

          DO I=1,4
           B(I)=((Y1*B1(I)*XM1)+(Y2*B2(I)*XM2)+
     C                           (YM1*B1(I+4)*XM1)*(1.-FF))
cfn
           B(I)=B(I)/((Y1*XM1)+(Y2*XM2)+(YM1*XM1*(1.-FF)))
           B(I+4)=B(I)
cfn
           B2(I+4)=(YM2*B2(I+4)*XM2)+(YM1*B1(I+4)*XM1*FF)
           B2(I+4)=B2(I+4)/((YM2*XM2)+(YM1*XM1*FF))
          END DO

          YT=((Y1*XM1)+(Y2*XM2))/
     C                 ((Y1*XM1)+(Y2*XM2)+(YM1*XM1*(1.-FF)))
C
C          NOW CARRY OUT PARTITION

           DO I=1,3,2
C
C           HF/W IN MANTLE

            B2(I)=B(I)/(((1.-YT)/DHF)+YT)
            B2(I+1)=B(I+1)/(((1.-YT)/DW)+YT)
           END DO
           DO I=5,7,2
C
C           HF/W IN CORE OF SMALL OBJECT

            B(I)=B(I)/(1.-YT+(YT*DHF))
            B(I+1)=B(I+1)/(1.-YT+(YT*DW))      
           END DO
C
C          NOW ADD TWO CORES TOGETHER

           YT2=(YM1*XM1)+(YM2*XM2*FF)
           DO I=5,8
             B2(I)=((B(I)*XM2*YM2*(1.-FF))+(B2(I)*YT2))/
     C                                (YT2+(YM2*XM2*(1.-FF)))
           END DO

           DO I=1,8
             B1(I)=B2(I)
             B2(I)=0.
           END DO

          ENDIF

       ELSEIF(IMIX.EQ.-1)THEN
C
C         SECOND OBJECT SEPARATES INTO CORE AND MANTLE
C         (IT IT HAS NOT ALREADY DONE SO)
          IF(B2(1).EQ.B2(5))THEN
c            WRITE(6,*) 'SECOND OBJECT UNDIFF '
C
C           PARTITION

            DO I=1,3,2
C
C            HF/W IN MANTLE

             B(I)=B2(I)/(Y2+((1.-Y2)/DHF))
             B(I+1)=B2(I+1)/(Y2+((1.-Y2)/DW))
            END DO
            DO I=5,7,2
C
C            HF/W IN CORE

             B(I)=B2(I-4)/(1+(Y2*(DHF-1.)))
             B(I+1)=B2(I-3)/(1+(Y2*(DW-1.)))          
            END DO
          ELSE
            DO I=1,8
             B(I)=B2(I)
            END DO
          ENDIF
C
C         CHECK TO SEE IF OTHER OBJECT ALSO UNDIFF

          IF(B1(1).EQ.B1(5))THEN
c            WRITE(6,*) 'FIRST OBJECT UNDIFF ',XM1,XM2
C
C           PARTITION

            DO I=1,3,2
C
C            HF/W IN MANTLE

             B2(I)=B1(I)/(Y1+((1.-Y1)/DHF))
             B2(I+1)=B1(I+1)/(Y1+((1.-Y1)/DW))
            END DO
            DO I=5,7,2
C
C            HF/W IN CORE

             B2(I)=B1(I-4)/(1.+(Y1*(DHF-1.)))
             B2(I+1)=B1(I-3)/(1.+(Y1*(DW-1.)))          
            END DO
            DO I=1,8
              B1(I)=B2(I)
            END DO
          ENDIF
C
C         NOW COMBINE

          YM1=1.-Y1
          YM2=1.-Y2
          DO I=1,4
            B1(I)=((B1(I)*XM1*Y1)+(B(I)*XM2*Y2))/
     C                                 ((Y1*XM1)+(Y2*XM2))
          END DO
          DO I=5,8
            B1(I)=((B1(I)*XM1*YM1)+(B(I)*XM2*YM2))/
     C                                 ((YM1*XM1)+(YM2*XM2))
          END DO
       ENDIF

c       WRITE(6,*) 'CHECKING MASS BALANCE'
       DO I=1,4
c         CK(I+4)=(XM1*B1(I)*Y1)+(XM2*B2(I)*Y2)+(XM1*B1(I+4)*YM1)
c&                     +(XM2*B2(I+4)*YM2)
          CK(I+4)=(XM1+XM2)*((B1(I)*YMIX)+(B1(I+4)*(1.-YMIX)))
c         WRITE(6,*) I,CK(I+4)/CK(I)
       END DO

       RETURN
       END
C
C************************************************************************
C
       SUBROUTINE DECAY(B1,DT)
C
C      CALCULATES CHANGE IN CONCENTRATIONS OVER TIME DT. ASSUMES
C      NO MASS ADDED TO SYSTEM OVER THIS TIME INTERVAL
C
       COMMON/PARAM/DHF,DW,XLHF

       REAL B1(8)
C
C      B1 AND B2 ARE ARRAYS CONTAINING CONCENTRATIONS OF
C      ELEMENTS:
C      1 - MANTLE 182HF WHICH DECAYS TO 
C      2 - MANTLE 182W
C      3 - MANTLE 180HF (STABLE)
C      4 - MANTLE 183W (STABLE)
C      5 - CORE 182HF
C      6 - CORE 182W
C      7 - CORE 180HF
C      8 - CORE 183W

       B1(2)=B1(2)+(B1(1)*(1.-EXP(-XLHF*DT)))
       B1(1)=B1(1)*EXP(-XLHF*DT)
       B1(6)=B1(6)+(B1(5)*(1.-EXP(-XLHF*DT)))
       B1(5)=B1(5)*EXP(-XLHF*DT)

       RETURN
       END

C************************************************************************
C

       SUBROUTINE REPLACE(XMO,NFIN,JMAX,I2,I1)

       INTEGER NFIN(5000)
       REAL XMO(5000)

       DO J=1,JMAX
         IF(NFIN(J).EQ.I2.AND.XMO(J).GT.0.)NFIN(J)=I1
       END DO
       RETURN
       END
C
C************************************************************************
C
       SUBROUTINE NEBULA(A,T,C)
C
C      EMPIRICAL FORMULA GIVING CONCENTRATION AS A FUNCTION OF
C      SEMI-MAJOR AXIS AND TEMPERATURE
C
       C0=0.25+((T-600.)*0.65/600.)
       C=C0+((A-1.)*0.75/2.)
       IF(C.GT.1.)C=1.

       RETURN
       END
       
