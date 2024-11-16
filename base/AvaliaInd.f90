! Sub-rotina para a avaliação de um indivíduo.
! Decodifica as variáveis e retorna o valor da função aptidão.

SUBROUTINE AvaliaInd(pop, numpav, dminx, dminy, lx, ly, hmax, bmax, &
	q, gpr, gpl, ccml, cpm, cap, cad, numind, NXMAX, NYMAX, NVV, numgen, k, F)
		IMPLICIT NONE
		REAL, INTENT(IN) :: dminx, dminy, lx, ly, hmax, bmax, q, gpr, &
		gpl, cap, cad
		REAL, INTENT(OUT) :: F
		INTEGER, INTENT(IN) :: numind, NXMAX, NYMAX, NVV, numgen, k, numpav
		INTEGER, DIMENSION(numind,numgen), INTENT(IN) :: pop
		REAL, DIMENSION(4), INTENT(IN) :: ccml, cpm
	 	
	! F                = Função aptidão
	! Custo total      = Função objetivo (sem as restrições)
	! k                = indica os indivíduos a serem avaliados

! Contadores inteiros

   INTEGER :: i,j,p

	
!	             Definição Variáveis lOCAIS 
!
!	               Variáveis de Projeto
!
!	         Variáveis da configuração estrutural
!

	integer NX,NY ! Número de vãos na direção X e Y	- VP
	integer DL ! Direção da laje: 1 (direção Y) e 0 (direção X) - VP
	REAL :: AJX,AJY

!	             Variáveis Auxiliares

	REAL :: LLJ,LLV,RPILAR ! Vão da laje e vão da viga E REACAO NO PILAR
	REAL :: LP, SP  		   ! LP= Lado pilar SP=SEÇÃO DO PILAR
	REAL :: RO				! TAXA AÇO PILAR
	REAL :: LLJC               ! Vão da laje corrigido (descontado BV)
!
!	            Variáveis do material
!

	INTEGER, DIMENSION(4) :: fckpm,fckml   ! Fck pré-moldado e moldado in loco
	INTEGER	pm,cml               ! Contadores dos fcks - VP

!
!	          Variáveis Quantidade Peças
!
	INTEGER  QDP
	REAL     QDL,QDV  ! Qdes de viga, laje e pilar


!            Variáveis dos custos


	REAL :: DOP, CDOP  ! Despesas operacionais lajes
	REAL :: CTV, CTL, CTP,CTT ! CUSTOS TRANSPORTE
	REAL :: CTMV, CTML, CTMP, CTMT, CUSTONEO  ! CUSTOS MONTAGEM
					   
!
!	               Variáveis da Laje
!
!	             Variáveis de Projeto: VL
	 
	INTEGER :: VL ! Caracteriza a laje
	REAL, DIMENSION(32) :: HL, PA, APL   ! Força Protensão antes transferência (MN)
										 ! Área de Protensão na Laje (m2)
!	             Variáveis Auxiliares

	real m,AC,YGC  ! relação fcks, área capa corrigida, cg sç composta
	real IC        ! Momento inércia sç composta 
	REAL, DIMENSION(64) :: YG,A,II,XMAX ! dados seção isolada
	real ep,epc,winf,wsup,wcinf,wcsup  ! excentricidades e módulos LAJES
	REAL, DIMENSION(6) :: carga,ml,rl  !Auxiliares cálculo esforços
	real mld,vld  !Momento e cortante de cálculo (faixa de 1.2m)
	real TINF,TSUP,TCINF,TCSUP  ! Tensões na LAJE
	real SCP,SPT,PT,PINF ! Auxiliares na protensão
	real TINPT,TSUPT,TINPI,TSUPI	!Tensões protensão
	real TDESI,TDESS,TTI,TTS,TTII,TTSS,TMI,TMS ! Tensões atuantes transitórias
	real DES,FF,LCJ,LTJ,LCK,LTK ! Tensões Limites
	real XTL,XL,ZL,ZLA,ZLB,MRESL  ! Auxiliares ELU
	real bxl, DDL, penl     ! Beta x da Laje, altura útil Laje e penalidade Laje
	REAL :: cfi, cft, fi, ft, EIL ! Contra-flecha e flecha das lajes 
	
!	 
!	                Variáveis da Viga
!
!	              Variáveis de Projeto: VV
 
	INTEGER :: VV
	REAL, DIMENSION(32) :: HV,BV          ! Geometria da Viga
	REAL HT                               ! Altura total do pavimento 
	INTEGER, DIMENSION(32) :: NMAX  	  ! Qde máx. de cordoalha por camada
	INTEGER :: ANA,ANB,NBAUX                ! Qde de cordoalhas por camada
	INTEGER, DIMENSION(16) :: NA
	INTEGER, DIMENSION(8) :: NB
	INTEGER, DIMENSION(4) :: NPT          ! Qde de barras passivas de tração
 	REAL, DIMENSION(4) :: BP             ! bitolas passivas 

!	               Variáveis Auxiliares (geometria e tensões)

	real AV,PPV,ME,YGV,IV ! Área, peso próprio, mom. estático,cg, m. inércia
	real AVC,PPVC,MEC,YGCV,IVC               ! Dados sç composta
	real EPA,EPB,EPCV                        ! Excentricidade sç isolada
	real EPCA,EPCB,EPCCV                     ! Excentricidade sç composta
	real DA,DB,APA,APB,AS                    ! Altura útil e área de armaduras
	real WVI,WVS,WCVI,WCVS                   ! Módulos resistentes
	real MVT,MVPP,MVG,MVQ,MVD                ! Momentos
	real TVI,TVS,TVPPI,TVPPS,TVGI,TVQ        ! Tensões
	real bxv,penv                            ! Beta X Viga e Penalidade Viga
	INTEGER :: ANPT,ABP						 ! Auxiliares Contador
	
!
!				 Variáveis auxiliares (Protensão)
!	
	real PAV,SOMA,SOMA2,SPTV,PAT,SOMA3,PATS,PROTSUP
	real VTINPT,VTSUPT,VPINF,VTINPI,VTSUPI
	real LTJV,LTKV,DESCOMPV,FFISSV
	real TDIV,TDSV,TTIV,TTSV,TTIIV,TTSSV,TMIV,TMSV 

!		     	Variáveis auxiliars (ELU) / (ELS)

	real XV,ZA,ZB,MRESV
	REAL :: cfiv,cftv, fiv, ftv

!			   Variáveis das Restrições

	REAL, DIMENSION(17) :: GL
	REAL, DIMENSION(20) :: GV
	
!
!		     	Variáveis Aptidão / CUSTOS
!
	real vpmv,vpml,vpmp,vml,vapv,vapl,vadv  ! Volume dos materiais
	real :: custoconc, CUSTOCONCML,custoprot,custoad,custotal, CUSTOFAB ! Custos Material
	REAL :: CUSTOCIS,CUSTOPE,CUSTOLIG
	real pentotal            ! Somatório Penalidades
	REAL :: LPL,NLP,QDPL,PTAL,LPV,NVP,QDPV,PTAV


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!   TESTE PARA NÃO REPETIR A LEITURA

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!IF (K.EQ.1) THEN 



!
!                   BANCO DE DADOS
!	
!		Listas das Variáveis dos Materiais
!            Resitências Materiais (fcks)
!
	do i=1,4
	fckpm(i)=35+(i-1)*5	 !  35,40,45,50 (valores fckpm)
	enddo

	do i=1,4
	fckml(i)=20+(i-1)*5	 !  20,25,30,35	(valores fckml)
	enddo
 
!	 
!			        LISTAS LAJES
!
!       	  Vinculação da variável VL das Lajes
!	       Propriedades geométricas das Lajes
!			    Painéis de b=1,20 m
!
!		Definição propriedades da laje seção PM - T&A
!				   Banco Dados - Laje

	do i=1,4
	HL(i)=0.09	         ! Altura da Laje(m)
	A(i)=0.0669983		 ! Área da laje (m2)
	YG(i)=0.045		     ! CG da laje (m)
	II(i)=0.000063		 ! Momento de inércia da laje (m4)
	XMAX(i)=0.065       ! Máximo X (LN)
	enddo

	do i=5,9
	HL(i)=0.13
	A(i)=0.0918954
	YG(i)=0.06784
	II(i)=0.00018
	XMAX(i)=0.07   ! Máximo valor do X (compressão)
	enddo

	do i=10,15
	HL(i)=0.17
	A(i)=0.1136454
	YG(i)=0.08847
	II(i)=0.000396
	XMAX(i)=0.075
	enddo

	do i=16,21
	HL(i)=0.2
	A(i)=0.1267849
	YG(i)=0.1
	II(i)=0.00063
	XMAX(i)=0.0725
	enddo

	do i=22,27
	HL(i)=0.21
	A(i)=0.135401
	YG(i)=0.108
	II(i)=0.000734
	XMAX(i)=0.08
	enddo

	do i=28,32	      
	HL(i)=0.26
	A(i)=0.1816019
	YG(i)=0.129
	II(i)=0.00144
	XMAX(i)=0.085
	enddo

!	                	Força de Protensão (MN) - LAJES
!
!	                        PA=N.Acor.1453.0,97.(10-6)
!
!		                     Sinal (-) / Compressão

      PA(1)=-0.184350828
      PA(2)=-0.245801104
      PA(3)=-0.30725138
      PA(4)=-0.368701656
      PA(5)=-0.245801104
      PA(6)=-0.341640984
      PA(7)=-0.431843224
      PA(8)=-0.52430052
      PA(9)=-0.62577804
      PA(10)=-0.245801104
      PA(11)=-0.341640984
      PA(12)=-0.431843224
      PA(13)=-0.52430052
      PA(14)=-0.62577804
      PA(15)=-0.74980612
      PA(16)=-0.431843
      PA(17)=-0.524301
      PA(18)=-0.625778
      PA(19)=-0.749806
      PA(20)=-1.143313
      PA(21)=-1.429142
      PA(22)=-0.431843
      PA(23)=-0.524301
      PA(24)=-0.625778
      PA(25)=-0.749806
      PA(26)=-1.143313
      PA(27)=-1.429142
      PA(28)=-0.431843
      PA(29)=-0.524301
      PA(30)=-0.625778
      PA(31)=-0.749806
      PA(32)=-1.143313
     

!
!	           Área de Protensão Total no painel da Laje
!

      APL(1)=0.0001308
      APL(2)=0.0001744
      APL(3)=0.000218
      APL(4)=0.0002616
      APL(5)=0.0001744
	  APL(6)=0.000242
      APL(7)=0.0003064
      APL(8)=0.000372
      APL(9)=0.000444
      APL(10)=0.0001744
      APL(11)=0.0002424
      APL(12)=0.0003064
      APL(13)=0.000372
      APL(14)=0.000444
      APL(15)=0.000532
      APL(16)=0.000306
      APL(17)=0.000372
      APL(18)=0.000444
      APL(19)=0.000532
      APL(20)=0.000811
      APL(21)=0.001014
      APL(22)=0.000306
      APL(23)=0.000372
      APL(24)=0.000444
      APL(25)=0.000532
      APL(26)=0.000811
      APL(27)=0.001014
      APL(28)=0.000306
      APL(29)=0.000372
      APL(30)=0.000444
      APL(31)=0.000532
      APL(32)=0.000811
      
!     
!       	 LISTAS das variáveis VIGAS
!
!
!      	 Qde de barras passivas de tração
		
      NPT(1)=0
      NPT(2)=2
      NPT(3)=4
      NPT(4)=6
      	
!	    Área das Bitolas Passivas disponíveis

     	BP(1)=0.000028   ! 6.0mm
    	BP(2)=0.000050	 ! 8.0mm
    	BP(3)=0.000080	 ! 10.0mm
    	BP(4)=0.000125	 ! 12.5mm

!       QDE DE CABOS CAMADA "A"

	   NA(1)=3;NA(2)=5;NA(3)=6;NA(4)=7
	   NA(5)=8;NA(6)=10;NA(7)=13;NA(8)=14
	   NA(9)=15;NA(10)=16;NA(11)=17;NA(12)=18
	   NA(13)=19;NA(14)=20;NA(15)=21;NA(16)=23

!      QDE DE CABOS CAMADA "B"
 
	   NB(1)=0;NB(2)=2;NB(3)=4;NB(4)=6
	   NB(5)=8;NB(6)=10;NB(7)=12;NB(8)=14

!
!		Características Geométricas da VIGA
!

      do i=1,5
    	HV(i)=0.20+(i-1)*0.05			 ! Altura
     	HV(i+5)=HV(i)
    	HV(i+10)=HV(i)
     	HV(i+15)=HV(i)
    	HV(i+20)=HV(i)
		HV(i+25)=HV(i)
    	BV(i)=0.40	 ! Base
    	BV(i+5)=0.50
    	BV(i+10)=0.60
    	BV(i+15)=0.70
    	BV(i+20)=0.80
		BV(i+25)=0.90
    	NMAX(i)=13	 ! Qde máxima de cordoalhas por base de viga
    	NMAX(i+5)=15
    	NMAX(i+10)=17
    	NMAX(i+15)=19
    	NMAX(i+20)=21
		NMAX(i+25)=23
	  enddo

!   Complemento	das listas das Vigas (32 possíveis)

		HV(31)=HV(29);BV(31)=BV(29);NMAX(31)=NMAX(29)
		HV(32)=HV(30);BV(32)=BV(30);NMAX(32)=NMAX(30)


!!!!!!!!!!!!!!!!!!!!!!
!
! FIM DO TESTE

!!!!!!!!!!!!!!!!!!!!!

!ENDIF


!
!	               ROTINA PARA DECODIFICAÇÃO
!
!	  Com: As variáveis que começam com "A" são auxiliares
!
!	  Com: Este "K" vem do Loop no programa principal (k=1 até numind)
!
   


 	DL=POP(k,1)	                                     ! Já é o próprio valor

	PM=2*POP(k,2)+1*POP(k,3)+1   ! Auxiliar
	CML=2*POP(k,4)+1*POP(k,5)+1   ! Auxiliar

	VL=16*POP(k,6)+8*POP(k,7)+4*POP(k,8)+2*POP(k,9) &
	+1*POP(k,10)+1	 ! Auxiliar

	ANPT=2*POP(k,11)+1*POP(k,12)+1         ! Auxiliar Lista NPT

	ABP=2*POP(k,13)+1*POP(k,14)+1                      ! Auxiliar p a lista BP

	ANA=8*POP(k,15)+4*POP(k,16)+2*POP(k,17)+1*POP(k,18)+1	 ! Auxiliar 
	
	ANB=4*POP(k,19)+2*POP(k,20)+1*POP(k,21)+1				 ! Auxiliar

	NX=0

	DO i=1,NXMAX

	NX=NX+POP(k,(21+i))*(2**(NXMAX-i))

	ENDDO

	NX=NX+1

	NY=0

	DO i=1,NYMAX

	NY=NY+POP(k,(21+NXMAX+i))*(2**(NYMAX-i))

	ENDDO

	NY=NY+1

	VV=0

	DO i=1,NVV

	VV=VV+POP(k,(21+NXMAX+NYMAX+i))*(2**(NVV-i))

	ENDDO

	VV=VV+1

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!                     REDUÇÃO DO DOMÍNIO DA BASE
!
!                   TÉCNICA: ALTERAR O VALOR DE VV
!
!	EXISTE UM ESPAÇO INFACTÍVEL MAS FAZ-SE TRANSFORMACAO NA LISTA
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	IF (BMAX.EQ.0.40)   THEN
					  IF (VV.GT.5) THEN 
					               IF (VV.LT.11) THEN
								                 VV=VV-5
												 ELSE
												 VV=VV-10
								   ENDIF
					  ENDIF
	ENDIF
						
	IF (BMAX.EQ.0.50)  THEN
	                   IF (VV.GT.10)  THEN
					                  VV=VV-5
					   ENDIF
  	ENDIF

	IF (BMAX.EQ.0.60)  THEN
	                   IF (VV.EQ.16)  THEN
					                  VV=15
					   ENDIF
	ENDIF				   				   

	IF (BMAX.EQ.0.70)   THEN
					  IF (VV.GT.20) THEN 
					               IF (VV.LT.26) THEN
								                 VV=VV-5
												 ELSE
												 VV=VV-10
								   ENDIF
					  ENDIF
	ENDIF
						
	IF (BMAX.EQ.0.80)  THEN
	                   IF (VV.GT.25)  THEN
					                  VV=VV-5
					   ENDIF
	ENDIF

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!			  AJUSTE DO NA P NAO ULTRAPASSAR O NMAX
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	IF (NA(ANA).GT.NMAX(VV))   THEN
	                           NA(ANA)=NMAX(VV)
							   ENDIF
  							   

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!																		   !
!							MORFOGÊNESE (NA x NB)
!
!	           Troca por um fenótipo que melhor se adapte ao problema					   
!																		   !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	IF (NB(anb).GT.NA(ana)) THEN
	              NBAUX=NB(anb)
				  NB(anb)=NA(ana)
				  NA(ana)=NBAUX
				  ENDIF

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!							   !
!   Ajuste dos Vãos Mínimos
!
!   Penaliza exageradamente
!	   
!							   !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

 AJX=LX/DMINX

 IF (NX.GT.AJX)   THEN
                  NX=NX*100
 ENDIF
 
 AJY=LY/DMINY
 
 IF (NY.GT.AJY)   THEN
                  NY=NY*100
 ENDIF				  				    
	
!       Cálculo dos Vãos

	LLJ=(LX/NX)*(1-DL)+(LY/NY)*(DL)		 ! (m)
	LLV=(LX/NX)*(DL)+(LY/NY)*(1-DL)		 ! (m)

	LLJC=LLJ-BV(VV)      ! Vão laje corrigido (m)

!
!					LAJES ALVEOLARES
!
!		            Rotina de Cálculo
!
!	  Comentário: A tração tem sinal + e a compressão -


!          Definição propriedades seção composta da Laje
!		   Painel de b=1,2 m

	M=(real(fckml(cml))/real(FCKPM(pm)))**0.5
	AC=M*1.2*0.05
 	YGC=((A(VL)*YG(VL))+(AC*(HL(VL)+0.025)))/(A(VL)+AC) 
	
    IC=II(VL)+A(VL)*((YGC-YG(VL))**2)+((M*1.2*(0.05**3))/12)+AC* &
	(HL(VL)+0.025-YGC)**2

!		 Excentricidades e Módulos resistentes das Lajes

	EP=YG(VL)-0.012-0.006	! (m) seção isolada, adotado CL=1,2cm
	EPC=YGC-0.012-0.006	! (m) seção composta

	WINF=II(VL)/YG(VL)
	WSUP=II(VL)/(YG(VL)-HL(VL))
 	WCINF=IC/YGC
	WCSUP=IC/(YGC-HL(VL)-0.05)

!       Cálculo dos momentos e tensões nas Lajes
!
!	  Com: Cálculo por painel (b=1.2m)
!

	Carga(1)=A(VL)*2.5	      ! Peso próprio Laje (Tf/m)
	Carga(2)=0.125*1.2    ! Peso capa (tf/m)
	Carga(3)=gpr*1.2	  ! Pav+Rev	  (tf/m)
	Carga(4)=gpl*1.2	  ! Paredes sobre Laje (tf/m)
	Carga(5)=q*1.2		  ! Carga acidental	(tf/m)
	Carga(6)=0.05*1.2      ! Carga de trabalho sobre a laje (tf/m) (50kg/m2)

	do i=1,6,1
	ML(i)=Carga(i)*(LLJC**2)/8	 ! Momento em tf.m/(b=1.2m)
	RL(i)=Carga(i)*(LLJ)/2 ! Reação/Cortante (tf) por painel (b=1.2m)
	enddo
!	
!	   Ações de Cálculo por painel (MN.m e MN)
!
	MLD=(1.3*ML(1)+1.4*(ML(2)+ML(3)+ML(4)+ML(5)))/100 ! Mom. de cálculo  Laje
	VLD=(1.3*RL(1)+1.4*(RL(2)+RL(3)+RL(4)+RL(5)))/100 ! Cortante de cálc. laje

!         Tensões Fase de concretagem (peça isolada)
!
!		   Tf/100=MN
      
	TINF=((ML(1)+ML(2)+ML(6))/WINF)/100   ! (MPa)
	TSUP=((ML(1)+ML(2)+ML(6))/WSUP)/100	  ! (MPa)

!		Tensões após concretagem (seção composta)

	TCINF=((ML(3)+ML(4)+ML(5))/WCINF)/100	! (MPa)
	TCSUP=((ML(3)+ML(4)+ML(5))/WCSUP)/100	! (MPa)

!	  Força de Protensão

!	  Protensão inicial - Ato da transferência (PA)
!
!	PA=NC*ACOR*1453*0.97   ! Força de protensão inicial (MN)
!
!	  NC*Acor=PA/0.001409


!	  Protensão após transferência (PT)

	SCP=(PA(VL)/A(VL))+PA(VL)*(EP**2/II(VL)) ! MPa (sinal -)

	SPT=(-1)*((PA(VL)/A(VL))+PA(VL)*(EP/WINF))+ &
	(195000/(0.85*5600*(fckpm(pm)**0.5)))*SCP	 ! (sinal -)

	PT=PA(VL)-APL(VL)*SPT	! MN

!	  Restrição - Término da protensão

	

!	  Protensão tempo infinito (PINF)

	PINF=0.75*PA(VL)		 ! Perda Estimada (75% da força inicial) 

!	  Tensões devido à Protensão

	TINPT=(PT/A(VL))+PT*(EP/WINF)	  ! Tensões na seção PM após
	TSUPT=(PT/A(VL))+PT*(EP/WSUP)	  ! transferência da protensão

	TINPI=(PINF/A(VL))+PINF*(EP/WINF)  ! Tensõe na seção PM num tempo infinito
	TSUPI=(PINF/A(VL))+PINF*(EP/WSUP)

!        RESTRIÇÕES - Verificações em vazio

!         Tensões atuantes em vazio (MPa)

  	TDESI=TINPT+(ML(1)/WINF)/100     ! Desmoldagem Inferior
	TDESS=TSUPT+(ML(1)/WSUP)/100     ! Desmoldagem Superior
	TTI=TINPT+0.8*(ML(1)/WINF)/100   ! Transporte Inferior (0.8)
	TTS=TSUPT+0.8*(ML(1)/WSUP)/100   ! Transporte Superior (0.8)
	TTII=TINPT+1.3*(ML(1)/WINF)/100  ! Transporte Inferior (1.3)
	TTSS=TSUPT+1.3*(ML(1)/WSUP)/100  ! Transporte Superior (1.3)
	TMI=TINPT+TINF                   ! Montagem Inferior 
	TMS=TSUPT+TSUP 		             ! Montagem Superior

!	  Tensões ELS  (MPa)
!	 Descompressão

	DES=((ML(1)+ML(2))/WINF)/100+TINPI+((ML(3)+ML(4))/WCINF)/100+ &
	0.3*(ML(5)/WCINF)/100

!	 Formação de fissura (MPa)

	FF=((ML(1)+ML(2))/WINF)/100+TINPI+((ML(3)+ML(4))/WCINF)/100+ &
	0.4*(ML(5)/WCINF)/100

!		Tensões Limites

	LCJ=0.49*fckpm(pm)                 ! Limite compressão fckj (Transitória)
	LTJ=1.2*0.7*0.3*((0.7*fckpm(pm))**(2/3)) ! Limite tração fckj 

	LCk=0.7*fckpm(pm)                ! Limite compressão fck   (ELS)
	LTk=1.2*0.7*0.3*((fckpm(pm))**(2/3)) ! Limite tração fck / seção "T" (ELS)

!
!		 Solicitações Normais - ELU	(Lajes Alveolares)
!
!	 Obs: Será testada a rotina que não necessita do cálculo do pré
!		  alongamento
!

	DDL=(HL(VL)+0.03875)  ! Altura útil da laje simplificada

	XTL=2551.05*APL(VL)/FCKML(CML) ! Para o painel b=1.2m

	IF (XTL.LE.0.05) THEN

	XL=XTL
	ZL=DDL-0.4*XL
	MRESL=APL(VL)*1486.9*ZL

	ELSE

	XL=((1486.9*APL(VL)-0.0291*fckml(cml))/(0.58285*FCKPM(PM)))+0.05
	ZLA=DDL-0.4*XL
	ZLB=DDL-0.02
	MRESL=(0.0291*fckml(cml)*ZLB)+(0.58285*FCKPM(PM)*(XL-0.05)*ZLA)

	ENDIF

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!																		  !
!                     ROTINA FLECHAS EM LAJES							  !
!																		  !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!                     CONTRA-FLECHA (PROTENSÃO)

	cfi=(PA(VL)*EP*LLJC)/(8*4760*(FCKPM(PM)**0.5)*II(VL)) ! Contra-flecha INICIAL

	cft=cfi*2.2   ! Estimativa contra-flecha TOTAL (SINAL"-")

!                         FLECHA  (CARREGAMENTO)

	fi=3*(Carga(1)+Carga(2)+Carga(3)+Carga(4)+0.3*Carga(5))*(LLJC**4)/100
	
	EIL=(384*4760*(FCKPM(PM)**0.5)*IC)   ! Flecha inicial (SÇ COMPOSTA)

	

	ft=(fi/EIL)*2.5   ! Estimativa flecha TOTAL (SINAL "+")
					  ! Total=2.5*Inicial


!
!		RESTRIÇÕES
!
!	  Restrições estado vazio - Inferior (comprimida)
! 		Em módulo p compensar o sinal (-) compressão
!
! Obs: Alguns valores referências são multiplicados p aumentar a margem
!
						   
	IF (ABS(TDESI).LE.LCJ) THEN 
	                       GL(1)=0
	                       ELSE 
						   GL(1)=ABS(TDESI/LCJ)-1
	ENDIF
	
     	IF (ABS(TTI).LE.LCJ) THEN 
		                     GL(2)=0
	                         ELSE 
							 GL(2)=ABS(TTI/LCJ)-1
	ENDIF				    

	IF (ABS(TTII).LE.LCJ) THEN 
	                      GL(3)=0
	                      ELSE
						  GL(3)=ABS(TTII/LCJ)-1
	ENDIF

	IF (ABS(TMI).LE.LCJ) THEN 
	                     GL(4)=0
	                     ELSE
						 GL(4)=ABS(TMI/LCJ)-1
	ENDIF

!	  Restrições em vazio - Superior (tracionada)
!		  Não precisa ser em módulo

	IF (TDESS.LE.(2*LTJ)) THEN 
	                  GL(5)=0
	                  ELSE
					  GL(5)=ABS(TDESS/(2*LTJ))-1
	ENDIF

!	IF (TTS.LE.(2*LTJ)) THEN
    IF (TTS.LE.((0.7*fckpm(pm))**0.5)) THEN	    ! Limite ACI

	                GL(6)=0
	                ELSE
					GL(6)=ABS(TTS/((0.7*fckpm(pm))**0.5))-1
	ENDIF

	IF (TTSS.LE.(2*LTJ)) THEN
	                 GL(7)=0
	                 ELSE 
					 GL(7)=ABS(TTSS/(2*LTJ))-1
	ENDIF  

	IF (TMS.LE.(2*LTJ)) THEN 
	                GL(8)=0
	                ELSE 
					GL(8)=ABS(TMS/(2*LTJ))-1
	ENDIF

!		  ELS - Descompressão e Formação de Fissura

	IF (DES.LE.0) THEN 
	              GL(9)=0			   ! ELS - Descompressão
              ELSE 
				  GL(9)=DES
	ENDIF

	IF (FF.LE.(2*LTK)) THEN 	   ! Limite Tração JEM
	               GL(10)=0		   ! ELS -Formação Fissura
	               ELSE 
				   GL(10)=(FF/(2*LTK))-1
    ENDIF

!	   Restrição do X dentro da peça (acima dos alvéolos)

	IF (XL.LE.XMAX(VL)) THEN 
	                    GL(11)=0		   ! Restrição X (dentro laje)
	                    ELSE 
       					GL(11)=(XL/XMAX(VL))-1
	ENDIF

!		ELU e Beta X

	IF (MRESL.GE.MLD) THEN 
	                  GL(12)=0	           	! Restrição Momento
	                  ELSE 
					  GL(12)=(MLD/MRESL)-1
   ENDIF

	BXL=XL/DDL						 ! Beta X Laje: Serão aceitos domínios 2 e 3

	IF (BXL.GT.0) THEN 
	                  GL(13)=0
	                  ELSE 
					  GL(13)=ABS(BXL)    ! Evitar q BX seja negativo
	ENDIF
	
     	IF (BXL.LE.0.6) THEN 
		                GL(14)=0
	                    ELSE 
						GL(14)=(BXL/0.6)-1
	ENDIF
	
	IF (LLJ.GE.(DMINX*(1-DL)+DMINY*(DL))) THEN 
	                                      GL(15)=0
	                                      ELSE 
										  GL(15)=((DMINX*(1-DL)+DMINY*(DL))/LLJ)-1
	ENDIF  ! Distância Mínima entre Pilares
	
	!           VERIFICAÇÃO FLECHAS
	
	IF ((ft+cft).LE.(1.05*LLJ/250))      THEN	! Margem para o deslocamento
	                                GL(16)=0
									ELSE
									GL(16)=((FT+CFT)/(1.05*LLJ/250))-1
	ENDIF
!
!	 RESTRIÇÃO DE RELAÇÃO VÃO/ALTURA LAJE (BIJAN)
!	
	IF ((LLJ/(HL(VL)+0.05)).LE.45) THEN
	                               GL(17)=0
								   ELSE
								   GL(17)=((LLJ/(HL(VL)+0.05))/45)-1
	ENDIF

	
								 							   
!
!	   Somatório Penalidades Lajes
!

	PENL=GL(1)+GL(2)+GL(3)+GL(4)+GL(5)+GL(6)+GL(7)+GL(8)+GL(9)+GL(10)+ &
	GL(11)+GL(12)+GL(13)+GL(14)+GL(15)+GL(16)+GL(17)

!
!			  VIGA "T" INVERTIDA
!			    
!	           Rotina de Cálculo
!    	
!
!	 Propriedades geométricas Viga isolada
!  
    	AV=((BV(VV)+0.3)*HV(VV))+(BV(VV)*(HL(VL)-0.05)) ! Área Viga (isolada) m2
    	PPV=AV*2.5                                      ! PP Viga tf/m

	    ME=((BV(VV)+0.3)*(HV(VV)**2)/2)+BV(VV)*(HL(VL)-0.05)* &
	    (HV(VV)+(HL(VL)-0.05)/2)						! Momento Estático

	    YGV=ME/AV                                       ! cg Viga isolada

!	 Momento Inércia Viga Isolada

	IV=(BV(VV)+0.30)*(HV(VV)**3)/12+(BV(VV)+0.30)*HV(VV)* &
	   (((HV(VV)/2)-YGV)**2)+BV(VV)*((HL(VL)-0.05)**3)/12+BV(VV)* &
       (HL(VL)-0.05)*((HV(VV)+((HL(VL)-0.05)/2)-YGV)**2)

!	  Propriedades seção composta

	AVC=AV+BV(VV)*0.10 !Área seção composta m2

	MEC=((BV(VV)+0.3)*(HV(VV)**2)/2)+ &
	    BV(VV)*(HL(VL)-0.05)*(HV(VV)+(HL(VL)-0.05)/2)+ &
		BV(VV)*0.10*(HV(VV)+HL(VL)+0.05)

	YGCV=MEC/AVC
	
    PPVC=PPV+(BV(VV)*0.10*2.5)  ! PP Viga seção composta (Tf/m)
	 
!	 Momento Inércia seção composta

	IVC=(BV(VV)+0.30)*(HV(VV)**3)/12+ &
	    (BV(VV)+0.30)*HV(VV)*(((HV(VV)/2)-YGCV)**2)+ &
		 BV(VV)*((HL(VL)+0.05)**3)/12+ &
		 BV(VV)*(HL(VL)+0.05)*((HV(VV)+((HL(VL)+0.05)/2)-YGCV)**2)
		

!	 Excentricidades de cada Camada (METRO)

    	EPA=YGV-0.05;EPB=YGV-0.10
	
        EPCA=YGCV-0.05;EPCB=YGCV-0.10

!	  Módulo Resistente

	WVI=IV/YGV;WVS=IV/(YGV-(HV(VV)+HL(VL)-0.05))
	WCVI=IVC/YGCV;WCVS=IVC/(YGCV-(HV(VV)+HL(VL)+0.05))

 	 
!	 Momentos e Tensões (Verificação transitória na fase de montagem)

	MVT=(((RL(1)+RL(2))/1.2)*2+PPV)*(LLV**2)/8	! Momento transitório (Tf.m)
	                                            ! PP e capa + PPviga


	TVI=MVT/(100*WVI);TVS=MVT/(100*WVS)   ! Tensões na seção isolada (MPa)

!	 Momentos e Tensões Verificação transitória somente devido ao peso próprio

	MVPP=(PPV*(LLV**2))/8	 ! momento devido ao pp da viga	(Tf.m)

	TVPPI=MVPP/(100*WVI) ! tensões devido ao pp da viga	(MPa)

	TVPPS=MVPP/(100*WVS)

!   Tensoes devido ao peso de paredes sobre a viga

!	MVPAR=(GPV*(LLV**2))/8

!	TVPAR=MVPAR/(100*WCVI)

!	 Momentos e tensões durante vida útil (ELS)
!
!  Com: Divide por 1.2 p/ calcular carga por metro na viga
!
!  Com: Multiplica por 2 p/ considerar a contribuição dos dois lados de lajes
!

	MVG=(((RL(3)+RL(4))/1.2)*2)*(LLV**2)/(2*8) ! Tf.m / Pav+Rev+Paredes na Laje

	MVQ=(RL(5)/1.2)*2*(LLV**2)/(2*8)   ! Tf.m / Sobre-Carga (q)

	TVGI=MVG/(WCVI*100)	! Tensões devido pav+rev+par rel. à sç composta(MPa)

	TVQ=MVQ/(WCVI*100)	! Tensões devido à sc (q) rel. à sç composta (MPa)

!	 Cálculo Momento de Cálculo

	MVD=(((1.3*RL(1)+1.4*RL(2)+1.4*(RL(3)/2)+1.4*(RL(4)/2)+1.4*(RL(5)/2))*(2/1.2)+1.3*PPV)* &
	((LLV-LP)**2)/8)/100		! Momento de cálculo MN.m

!
!	REAÇÕES NOS PILARES
!

  RPILAR=((RL(1)+RL(2)+RL(3)+RL(4)+RL(5))*(2/1.2)+PPV)*LLV*NUMPAV*1.02  ! [TF]

  !   CONSIDERA A CARGA TOTAL NO PILAR + 2% PARA O PP

  IF (RPILAR.LE.380) THEN 
                     SP=0.16
					 LP=0.4
					 ELSE
					 IF (RPILAR.LE.600) THEN
					                    SP=0.25
										LP=0.5
										ELSE
										SP=0.36
										LP=0.6
					 ENDIF
  ENDIF

!	
!	  PROTENSÃO EM VIGAS
!

!	  Protensão na Pista (MN)

	PAV=-0.97*(NA(ANA)+NB(ANB))*0.0001014*1453   ! MN	(sinal - / Compressão)

	SOMA=(NA(ANA)*EPA+NB(ANB)*EPB)*0.97*0.0001014*1453*(-1) !(Sinal -)
	 
	SOMA2=(NA(ANA)*(EPA**2)+NB(ANB)*(EPB**2))* &
	      0.97*0.0001014*1453*(-1)				  !(Sinal -)

	SPTV=(-1)*((PAV/AV)+(SOMA/WVI))+(40.966/(FCKPM(PM)**0.5))* &
	     ((PAV/AV)+(SOMA2/IV))

!	 Protensão após trasnferência (MN)

	PAT=PAV-(NA(ANA)+NB(ANB))*0.0001014*SPTV

	
	SOMA3=PAT*(REAL(NA(ANA))*EPA/(REAL(NA(ANA))+REAL(NB(ANB))))+ &
	PAT*(REAL(NB(ANB))*EPB/(REAL(NA(ANA))+REAL(NB(ANB))))

	VTINPT=(PAT/AV)+(SOMA3/WVI)

	VTSUPT=(PAT/AV)+(SOMA3/WVS)

!	 Protensão em um tempo infinito (MN)

	VPINF=0.8*PAV	  ! PERDA ESTIMADA (20%)

	VTINPI=(VPINF/AV)+(0.8*SOMA/WVI)

	VTSUPI=(VPINF/AV)+(0.8*SOMA/WVS)


!		Tensões Limites

!	LCJ=0.49*fckpm(pm)                 ! Limite compressão fckj (Transitória)
	LTJV=1.5*0.7*0.3*((0.7*fckpm(pm))**(2/3)) ! Limite tração fckj(Retangular) 

!	LCk=0.7*fckpm(pm)                ! Limite compressão fck   (ELS)
	LTkV=1.5*0.7*0.3*((fckpm(pm))**(2/3)) ! Limite tração fck   (ELS)




!	   Tensões ELS (MPa)

	DESCOMPV=TVI+TVGI+0.3*TVQ+VTINPI
	FFISSV=TVI+TVGI+0.4*TVQ+VTINPI

!
!		Tensões atuantes nas fases transitórias
!

	TDIV=VTINPT+TVPPI	! Desmoldagem Inferior
	TDSV=VTSUPT+TVPPS	! Desmoldagem Superior
	TTIV=VTINPT+0.8*TVPPI	! Transporte Inferior 0.8
	TTSV=VTSUPT+0.8*TVPPS	! Transporte Superior 0.8
	TTIIV=VTINPT+1.3*TVPPI	! Transporte Inferior 1.3
	TTSSV=VTSUPT+1.3*TVPPS	! Transporte Superior 1.3
	TMIV=VTINPI+TVI			! Montagem Inferior
	TMSV=VTSUPI+TVS			! Montagem Superior

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!				  PROTENSÃO SUPERIOR (Considerado apenas na transitória)
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	IF  (TTSV.GT.(2*LTJV))  THEN 
	                        
							PATS=0.85*(-0.5716)   ! 4 CABOS, CONSIDERANDO 85% (MN)
							EPCV=YGV-(HV(VV)-0.05)
							EPCCV=YGCV-(HV(VV)-0.05)
							PROTSUP=(PATS/AV)+(PATS*EPCV/WVS)
							TTSV=TTSV+PROTSUP

							ENDIF

	IF (TMSV.GT.(2*LTJV))   THEN

							PATS=0.85*(-0.5716)   ! 4 CABOS, CONSIDERANDO 85% (MN)
							EPCV=YGV-(HV(VV)-0.05)
							EPCCV=YGCV-(HV(VV)-0.05)
							PROTSUP=(PATS/AV)+(PATS*EPCV/WVS)
							TMSV=TMSV+PROTSUP

							ENDIF

	IF (TDSV.GT.(2*LTJV))   THEN

							PATS=0.85*(-0.5716)   ! 4 CABOS, CONSIDERANDO 85% (MN)
							EPCV=YGV-(HV(VV)-0.05)
							EPCCV=YGCV-(HV(VV)-0.05)
							PROTSUP=(PATS/AV)+(PATS*EPCV/WVS)
							TDSV=TDSV+PROTSUP

							ENDIF



!	   ESTADO LIMITE ÚLTIMO

	HT=HV(VV)+HL(VL)+0.05 !   Altura total do pavimento (m)

	DA=HT-0.05;DB=HT-0.10 ! Braços de alavanca (m)

!	EP=195000 ! Módulo aço protensão MPa
!	ES=210000 ! Módulo aço MPa

	APA=NA(ANA)*0.0001014;APB=NB(ANB)*0.0001014

	AS=NPT(ANPT)*BP(ABP)

!
!	  Rotina 2006 p Cálculo de X (Linha-Neutra)
!		  Cálculo do momento resistente
!
	XV=(1486.9*(APA+APB)+434.8*(AS))/(0.4857*fckpm(pm)*BV(VV))

	ZA=HT-0.05-0.4*XV  ! Braço de alavanca camada A (m)
	ZB=ZA-0.05		   ! Braço de alavanca camada B (m)

	MRESV=1486.9*(APA*ZA+APB*ZB) ! Momento resistido pela seção (MN.m)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!																		!
!				ROTINA FLECHAS VIGAS									!
!																		!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	cfiv=(PAT*EPA*LLV)/(8*4760*(FCKPM(PM)**0.5)*IV)

	cftv=cfiv*2.5

	fiv=(3*((RL(1)+RL(2)+RL(3)+RL(4)+0.3*RL(5))*(2/1.2)+PPV)*(LLV**4)) &
	    /(100*384*4760*(FCKPM(PM)**0.5)*IVC)

	ftv=fiv*2.5

!
!		 RESTRIÇÃO (Resistente tem q ser superior ao de cálculo)
!
!		 Estado em Vazio -  
!

!          ZONA INFERIOR - COMPRIMIDA ?

	IF (ABS(TDIV).LE.LCJ) THEN 
	                      GV(1)=0
	                      ELSE 
						  GV(1)=ABS(TDIV/LCJ)-1
	ENDIF
	
	IF (ABS(TTIV).LE.LCJ)  THEN 
	                       GV(2)=0
	                       ELSE 
						   GV(2)=ABS(TTIV/LCJ)-1
    ENDIF				    

	IF (ABS(TTIIV).LE.LCJ) THEN 
	                       GV(3)=0
	                       ELSE 
						   GV(3)=ABS(TTIIV/LCJ)-1
	ENDIF

	IF (ABS(TMIV).LE.LCJ)  THEN 
	                       GV(4)=0
	                       ELSE 
						   GV(4)=ABS(TMIV/LCJ)-1
	ENDIF

!        ZONA SUPERIOR - TRACIONADA ?

!	IF (TDSV.LE.(2*LTJV)) THEN 	! Limite sugerido JEM
	IF (TDSV.LE.((0.7*FCKPM(PM))**0.5)) THEN	! Limite ACI
	                  GV(5)=0
	                  ELSE 
!					  GV(5)=ABS(TDSV/(2*LTJV))-1
					  GV(5)=ABS(TDSV/((0.7*FCKPM(PM))**0.5))-1

	ENDIF

!	IF (TTSV.LE.(2*LTJV))     THEN 
	IF (TTSV.LE.((0.7*FCKPM(PM))**0.5))   THEN 
	                      GV(6)=0
	                      ELSE 
						  GV(6)=ABS(TTSV/((0.7*FCKPM(PM))**0.5))-1
	ENDIF

!	IF (TTSSV.LE.(2*LTJV))     THEN
 	IF (TTSSV.LE.((0.7*FCKPM(PM))**0.5))  THEN

	                       GV(7)=0
	                       ELSE 
						   GV(7)=ABS(TTSSV/((0.7*FCKPM(PM))**0.5))-1
	ENDIF  

!	IF (TMSV.LE.(2*LTJV))    THEN 
	IF (TMSV.LE.((0.7*FCKPM(PM))**0.5))  THEN
	                     GV(8)=0
	                     ELSE 
						 GV(8)=ABS(TMSV/((0.7*FCKPM(PM))**0.5))-1
	ENDIF

!
!	     ELS
!

!       DESCOMPRESSAO

	IF (DESCOMPV.LE.0.05)   THEN ! Adotado 0.05 como margem e referência
	                     GV(9)=0				  
	                     ELSE 
						 GV(9)=(DESCOMPV/0.05)-1
	ENDIF

!	  FORMACAO DE FISSURA

	IF (FFISSV.LE.(2*LTKV))   THEN 			   ! Limite Tração JEM
	                      GV(10)=0			   ! ELS - Formação Fissura
	                      ELSE 
						  GV(10)=(FFISSV/(2*LTKV))-1
	ENDIF

!
!		ELU e Beta X
!

	IF (MRESV.GE.(0.98*MVD))   THEN 
	                    GV(11)=0					! Restrição do Momento
	                    ELSE
						IF (MRESV.LE.0)  THEN
						                      GV(11)=1-(MRESV/(0.98*MVD))
											  ELSE 
						                      GV(11)=ABS((0.98*MVD)/MRESV)-1
						ENDIF
	ENDIF

	BXV=XV/DA

	IF (BXV.GT.0)   THEN 
	                    GV(12)=0				! Beta X Viga
	                    ELSE 
						GV(12)=ABS(BXV)
	ENDIF
	
    IF (BXV.LE.(1.02*0.6))     THEN 
	                    GV(13)=0			   ! Beta X Viga
	                    ELSE 
						GV(13)=(BXV/(1.02*0.6))-1
	ENDIF

!	   Geometria
	
    IF (NA(ANA).LE.NMAX(VV))	THEN 
	                    GV(14)=0		   ! Qde cabos camada
	                    ELSE 
						GV(14)=(REAL(NA(ANA))/REAL(NMAX(VV)))-1
	ENDIF

	IF (NB(ANB).LE.NMAX(VV)) THEN 
	                    GV(15)=0		   ! Qde cabos camada
	                    ELSE 
						GV(15)=(REAL(NB(ANB))/REAL(NMAX(VV)))-1
	ENDIF
	
    IF (HT.LE.HMAX) THEN 
	                GV(16)=0			  ! Altura máxima do pavimento
	                ELSE 
					GV(16)=(HT/HMAX)-1
	ENDIF
	
    IF (BV(VV).LE.BMAX) THEN 
	                    GV(17)=0		  ! Largura máxima viga
	                    ELSE 
						GV(17)=((100*BV(VV))/BMAX)-1	!TESTE: Diminuição Domínio
	ENDIF
	    
	IF (LLV.GE.(DMINX*(DL)+DMINY*(1-DL))) THEN 		! Distância mínima entre pilares 
	                                      GV(18)=0
		                                  ELSE 
						            GV(18)=((DMINX*(DL)+DMINY*(1-DL))/LLV)-1
    ENDIF
	

	IF (NA(ANA).GE.NB(ANB)) THEN			  ! Evitar mais ferros na segunda camada(NB(ANB))
	              GV(19)=0		  ! em relação à primeira(NA)
				  ELSE
				  GV(19)=(REAL(NB(ANB))/REAL(NA(ANA)))-1
	ENDIF
	
!         Flechas

	IF ((CFTV+FTV).LE.(1.05*LLV/250))   THEN
	                               GV(20)=0
								   ELSE
								   GV(20)=((CFTV+FTV)/(1.05*LLV/250))-1
	ENDIF							    			  					        					 						     
        							   
!
!	   Somatório Penalidades Vigas
!
	PENV=GV(1)+GV(2)+GV(3)+GV(4)+GV(5)+GV(6)+GV(7)+GV(8)+GV(9)+GV(10)+ &
	GV(11)+GV(12)+GV(13)+GV(14)+GV(15)+GV(16)+GV(17)+GV(18)+GV(19)+GV(20)

!	   PENALIDADE TOTAL

	PENTOTAL=1+15*(PENL+PENV)    ! Intensidade penalização K=10
 
!
!		  ROTINA PARA CONTAR ELEMENTOS
!
	QDV=NX*(NY+1)*DL+NY*(NX+1)*(1-DL) ! Qde de vigas PAVIMENTO

!	QDV=QDV*NUMPAV                    !QDE VIGAS TOTAL
	  	
	QDL=(real(NX)*LLV/1.2)*NY*DL+(real(NY)*LLV/1.2)*NX*(1-DL) ! Qde de lajes PAVIMENTO

!	QDL=QDL*NUMPAV                    ! QDE LAJES TOTAL

	QDP=(NX+1)*(NY+1) ! Qde de pilares

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!	   Cálculo Função Aptidão
!
!	   Comentário: O vão da laje é subtraído da largura da viga
!				   e o da viga do lado do pilar
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	
	VPMV=((BV(VV)+0.3)*HV(VV)+BV(VV)*(HL(VL)-0.05))*(LLV-LP) ! Volume Vigas
	VPML=A(VL)*(LLJ-BV(VV))		                        ! Volume Lajes

	VML=(LX*LY-real(QDP)*SP)*0.05+BV(VV)*0.05*(LLV-LP)*QDV ! Vol. CAPA + COMPLEMENTO VIGA

	VPMP=SP*3.5*1.15           				 ! Volume Pilar - 01 LANCE
											 ! 1.15 para considerar o Console

!   CÁLCULO TAXA AÇO PILAR

	IF (PM.GT.1) THEN
	             IF (PM.EQ.2) THEN
				              RO=120
							  IF (PM.EQ.3)   THEN
							                 RO=90
											 ELSE
											 RO=60
											 ENDIF
				 ENDIF
				 ELSE
				 RO=150
	ENDIF

!   AÇO DEMAIS ELEMENTOS

	VAPV=(NA(ANA)+NB(ANB))*0.0001014*(LLV-LP)    ! Volume aço protensão Viga 
	VAPL=APL(VL)*(LLJ-BV(VV))		         ! Volume aço protensão Laje
	VADV=NPT(ANPT)*BP(ABP)*(LLV-LP)               ! Volume aço doce Viga

		
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!	       Custo do concreto das vigas, complemento vigas e lajes

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

CUSTOCONC=((VPMV*CPM(PM)*QDV)*1.5+(VPML*CPM(PM)*QDL)+ &
(VPMP*CPM(PM)*QDP*1.5))*NUMPAV

CUSTOCONCML=VML*CCML(CML)*1.3*NUMPAV

! 1.5 pq concreto viga e pilar é mais caro

! EM 20/11/06 FOI DESCONSIDERADO O CUSTO FUNDAÇÃO
	
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	! Custo Pilar: REVER!!!!!!!!
	! X 1.2 pconsiderar fundação!!!!!!!!!!!
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!     Custo despesas operacionais em LAJES

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

IF (VL.LT.28) THEN
              DOP=24
			  ELSE
			  DOP=36          ! Custos despesas operacionais unitários
			  ENDIF
CDOP=QDL*(LLJ-BV(VV))*1.2*DOP*NUMPAV       ! Custos despesas operacionais total

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!     CUSTOS TRANSPORTE								   !

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

IF ((LLV-LP).GT.12) THEN
                    CTV=1600
					ELSE
					CTV=1000
					ENDIF

IF ((LLJ-BV(VV)).GT.12) THEN
                    CTL=1600
					ELSE
					CTL=1000
					ENDIF

IF (NUMPAV.GT.3) THEN
                 CTP=1600
				 ELSE
				 CTP=1000
				 ENDIF   

CTT=(((VPMV*QDV*CTV)/10)+((VPML*QDL*CTL)/10)+((VPMP*QDP*CTP)/10))*NUMPAV

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!     CUSTO MONTAGEM					 !

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

CTMV=ceiling((QDV/16)+(QDL/24))   ! 1100 GUINDASTE E 400 MO

! CTML=(QDL/24)*1500

CTMP=(QDP/8)*1500

CTMT=1500*CTMV*NUMPAV+CTMP




!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!	   CUSTOS DAS PERDAS DA PISTA E NÚMERO DE PISTAS UTILIZADAS
!
!	              OBS: ROTINA EM CONSTRUÇÃO	/ falta custo utilizaçao
!										  falta acrescentar na funcao custo
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!LPL=140                     ! COMPRIMENTO PISTA LAJE

!NLP=(LPL-MOD(LPL,LLJC))/LLJC  ! NUMERO LAJES POR PISTA

!QDPL=((QDL-MOD(QDL,NLP))/NLP)+1  ! QDE PISTAS P CONFECCIONAR AS LAJES

!IF (MOD(QDL,NLP).EQ.0) THEN
!					   QDPL=QDPL-1
!					   ENDIF

!PTAL=((QDPL*LPL)-(QDL*LLJC))*APL(VL)*7857 ! PERDA DO AÇO DE PROTENSAO EM KG

!LPV=60						! COMPRIMENTO PISTA VIGA

!NVP=(LPV-MOD(LPV,LLV))/LLV	! NUMERO VIGAS POR PISTA

!QDPV=((QDV-MOD(QDV,NVP))/NVP)+1  ! QDE DE PISTAS P CONFECCIONAR AS VIGAS

!IF (MOD(QDV,NVP).EQ.0) THEN
!                       QDPV=QDPV-1
!					   ENDIF

!PTAV=((QDPV*LPV)-(QDV*LLV))*(NA(ANA)+NB(ANB))*0.0001014*7810	! PERDA AÇO DE PROT EM KG


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!	                        Custo Aços: PROTENSÃO E PASSIVO
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	CUSTOPROT=(1.085*VAPV*7810.65*QDV+VAPL*7857*QDL)*CAP*NUMPAV

	CUSTOAD=(VADV*7760*QDV*CAD+VPMP*RO*QDP*CAD)*NUMPAV

	CUSTOCIS=5.6*(((BV(VV)-0.05)+(HV(VV)-0.05))*2+0.12)*BV(VV)* &
	         (LLV-LP)*QDV*CAD*NUMPAV

	CUSTOPE=0.86912*(LLV-LP)*QDV*NUMPAV*CAD  ! CUSTO PORTA ESTRIBO 4 6mm

	CUSTOLIG=12.125*QDP*NUMPAV*CAD        ! CUSTO ARM LIGAÇÃO 5 12.5mm (C=2,5 m)

	CUSTONEO=QDP*2*NUMPAV*22.5   ! R$ 22.5

! 1.085 pq cordoalha em viga é mais cara

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!	                     CUSTO TOTAL MATERIAIS

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	CUSTOFAB=(CUSTOCONC+CUSTOPROT+CUSTOAD+CDOP+CUSTOCIS+CUSTOPE)*1.33

	CUSTOTAL=(CUSTOFAB+CUSTOCONCML+CTT+CTMT+CUSTONEO+CUSTOLIG)/NUMPAV

	F=CUSTOTAL*PENTOTAL 
	
!       Com: Valor que será jogado no vetor APT(k) do Main Program AG.f90  

	

! Apresentação dos valores encontrados para cada indivíduo	
!		WRITE (*, '(1X,A,I3,A)') "--- Individuo ", K, " ---"
!		WRITE (*, '(/)', ADVANCE = "NO")
!		
!		DO p=1,numgen
!
!			WRITE (*, '(I1)', ADVANCE = "NO") pop(K,p)
!
!		END DO
	

	

		
!		PAUSE 'Pressione ENTER para continuar.'
	
END SUBROUTINE AvaliaInd