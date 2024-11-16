

PROGRAM AG

! Variáveis
! count  = atribui à semente dos números aleatórios valor baseado no clock do sistema
! Seed   = semente para a geração de números aleatórios
! R      = número aleatório
! numind = número de indivíduos da população
! numgen = PARÂMETRO número de genes do cromossomo ou indivíduo
! pop    = matriz da população corrente
! subpop = matriz da subpopulação ou população intermediária
! AllocateStatus = usada pelo programa na alocação de memória (recebe 0 se a alocação tiver sucesso)
! apt    = (real) vetor das aptidões
! elit   = número de indivíduos que participarão do elitismo
! ger    = contador das gerações
! maxger = número máximo de gerações
! cruz   = taxa de cruzamento
! pmut   = taxa de mutação
! mut    = matriz da mutação
! rank   = matriz dos indivíduos que participarão do cruzamento
! subrank = matriz dos filhos resultantes do cruzamento
! aptger = vetor contendo a melhor aptidão de cada de gerações
! med = aptidão média de cada geração
! aptmed = vetor com a aptidão média de cada geração
	
IMPLICIT NONE


REAL :: dminx,dminy,lx,ly,hmax,bmax  ! Vãos e limites geométricos peças
REAL :: AJX, AJY
INTEGER :: NXMAX, NYMAX, NVV
REAL :: q,gpr,gpl       ! Cargas
REAL :: mx,my   ! Modulações em X e Y
REAL, DIMENSION(4) :: cpm,ccml      ! Custos do concreto por Fck R$/m3
REAL :: cap,cad         ! Custo aço protensão e passivo R$/kg
INTEGER :: NUMPAV         ! Número de pavimentos do prédio
REAL :: R, F, pmut, med
REAL, ALLOCATABLE, DIMENSION(:) :: apt, subapt, aptger, aptmed
INTEGER :: count, numind, numgen, AllocateStatus, i, j, k, elit, ger, maxger, cruz, &
          indou, selcruz=2, teste
INTEGER, DIMENSION(1)  :: Seed
INTEGER, ALLOCATABLE, DIMENSION(:,:) :: pop, subpop, rank, subrank, mut
CHARACTER :: arqou*20, arqout*24

! Interface das subrotinas

INTERFACE
	SUBROUTINE AvaliaInd(pop, numpav, dminx, dminy, lx, ly, hmax, bmax, &
	q, gpr, gpl, ccml, cpm, cap, cad, numind,NXMAX,NYMAX,NVV, numgen, k, F)
		IMPLICIT NONE
		REAL, INTENT(IN) :: dminx, dminy, lx, ly, hmax, bmax, q, gpr, &
		gpl, cap, cad
		REAL, INTENT(OUT) :: F
		INTEGER, INTENT(IN) :: numind,NXMAX,NYMAX,NVV, numgen, k, numpav
		INTEGER, DIMENSION(numind,numgen), INTENT(IN) :: pop
		REAL, DIMENSION(4), INTENT(IN) :: ccml, cpm
	END SUBROUTINE AvaliaInd

	SUBROUTINE AvaliaIndF(subpop, SUBAPT, numpav, dminx, dminy, lx, ly, hmax, bmax, &
	q, gpr, gpl, ccml, cpm, cap, cad, numind,NXMAX,NYMAX,NVV, numgen, k, F)
		IMPLICIT NONE
		REAL, INTENT(IN) :: dminx, dminy, lx, ly, hmax, bmax, q, gpr, &
		gpl, cap, cad 
		REAL, INTENT(OUT) :: F
		INTEGER, INTENT(IN) :: numind,NXMAX,NYMAX,NVV, numgen, k, numpav
		INTEGER, DIMENSION(numind,numgen), INTENT(IN) :: subpop
		REAL, DIMENSION(NUMIND), INTENT(IN) :: SUBAPT
		REAL, DIMENSION(4), INTENT(IN) :: ccml, cpm
	END SUBROUTINE AvaliaIndF

	SUBROUTINE OrdenaPop(pop, numind, numgen, apt, subpop, subapt)
		IMPLICIT NONE
		INTEGER, INTENT(IN) :: numind, numgen
		INTEGER, DIMENSION(numind,numgen), INTENT(IN) :: pop
		INTEGER, DIMENSION(numind,numgen), INTENT(OUT) :: subpop
		REAL, DIMENSION(numind), INTENT(IN) :: apt
		REAL, DIMENSION(numind), INTENT(OUT) :: subapt
	END SUBROUTINE OrdenaPop

!	SUBROUTINE CruzUmPonto(rank, subrank, numgen, cruz)
!		IMPLICIT NONE
!		INTEGER, INTENT(IN) :: numgen, cruz
!		INTEGER, DIMENSION(cruz,numgen), INTENT(IN) :: rank
!		INTEGER, DIMENSION(cruz,numgen), INTENT(OUT) :: subrank
!	END	SUBROUTINE CruzUmPonto
	
	SUBROUTINE CruzUniforme(rank, subrank, numgen, cruz)
		IMPLICIT NONE
		INTEGER, INTENT(IN) :: numgen, cruz
		INTEGER, DIMENSION(cruz,numgen), INTENT(IN) :: rank
		INTEGER, DIMENSION(cruz,numgen), INTENT(OUT) :: subrank
	END	SUBROUTINE CruzUniforme

END INTERFACE

!----------------------------------------------------------------------
!		Abrir arquivos de entrada e saida

	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Entre com o nome do arquivo de saida (sem extensao): "
	READ *, arqou

		indou = index (arqou,' ') - 1
		arqout = arqou(:indou)//'.sai'
		call IniciarArqOut (arqout,6)

!----------------------------------------------------------------------

! Entrada de dados

	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Entre o numero de pavimentos: "
	READ *, NUMPAV
	WRITE (6, '(1X,A,I3,A)') "NUMPAV = ", NUMPAV

	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Entre distancia minima pilares X(m): "
	READ *, dminx
	WRITE (6, '(1X,A,F6.3,A)') "DMINX = ", DMINX

	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Entre distancia minima pilares Y(m): "
	READ *, dminY
	WRITE (6, '(1X,A,F6.3,A)') "DMINY = ", DMINY

	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Dimensao pavimento X(m): "
	READ *, LX
	WRITE (6, '(1X,A,F6.3,A)') "LX = ", LX

	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Dimensao pavimento Y(m): "
	READ *, LY
	WRITE (6, '(1X,A,F6.3,A)') "LY = ", LY

	! Altura máxima do pavimento (Laje+Viga+Capa)=HT
	
	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Altura maxima pavimento (laje+viga)(m): "
	READ *, HMAX
	WRITE (6, '(1X,A,F6.3,A)') "HMAX = ", HMAX

	! Largura máxima da vig BV(VV)
	
	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Largura maxima da viga(m): (.40,.50.. ou .90) "
	READ *, BMAX
	WRITE (6, '(1X,A,F6.3,A)') "BMAX = ", BMAX

	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Sobre-Carga (Tf/m2): "
	READ *, q
	WRITE (6, '(1X,A,F6.3,A)') "Q = ", q

	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Carga Permanente - PAV+REV (Tf/m2): "
	READ *, gpr
	WRITE (6, '(1X,A,F6.3,A)') "GPR = ", gpr

	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Paredes sobre laje (Tf/m2): "
	READ *, gpl
	WRITE (6, '(1X,A,F6.3,A)') "GPL = ", gpl


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! CUSTO CONCRETO CML
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


	ccml(1)=147
	ccml(2)=158
	ccml(3)=171
	ccml(4)=185

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! CUSTO CONCRETO CPM
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


   cpm(1)=185
   cpm(2)=200
   cpm(3)=216
   cpm(4)=233


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!  CUSTO DOS AÇOS

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

   cap=7

   cad=4



!	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Modulacao direcao X(m): "
!	READ *, MX
!	WRITE (6, '(1X,A,F6.3,A)') "Modulo X = ", MX

!	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Modulacao direcao Y(m): "
!	READ *, MY
!	WRITE (6, '(1X,A,F6.3,A)') "Modulo Y = ", MY


	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Entre o numero de individuos da populacao: "
	READ *, numind
	WRITE (6, '(1X,A,I3,A)') "Pop = ", numind, " individuos"
	
	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Entre o numero de individuos para elitismo: "
	READ *, elit
	WRITE (6, '(1X,A,I3,A)') "Elitismo = ", elit, " individuo(s)"
	
	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Entre o numero de geracoes ou ciclos desejado: "
	READ *, maxger
	WRITE (6, '(1X,A,I4,A)') "Ciclo = ", maxger, " geracoes"
	
	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Entre a taxa de cruzamento (%): "
	READ *, cruz
	WRITE (6, '(1X,A,I3)') "Taxa de cruzamento (%): ", cruz
	cruz = (cruz*numind)/100

!   Transformação de "cruz" em um número PAR

	IF (MOD(cruz,2) /= 0) THEN
		cruz = cruz+1
	END IF ! 'cruz' deve ser par
	WRITE (*, '(1X,A,I3)') "Num. de individuos participantes do cruzamento: ", cruz
	WRITE (6, '(1X,A,I3)') "Num. de individuos participantes do cruzamento: ", cruz

!	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Entre o tipo de cruzamento ( 1 - Um Ponto, 2 - Uniforme): "
!	READ *, selcruz
!	WRITE (6, '(1X,A,I3)') "Tipo de cruzamento( 1 - Um Ponto, 2 - Uniforme): ", selcruz

	WRITE (*, '(/,1X,A)', ADVANCE = "NO") "Entre a taxa de mutacao (%): "
	READ *, pmut
	WRITE (6, '(1X,A,F5.3)') "Taxa mutacao (%): ", pmut
	pmut=pmut/100

!
!    DETERMINAÇÃO TAMANHO DO CROMOSSOMO EM FUNÇÃO MODULAÇÃO MÍNIMA
!
!	 FAIXAS DE VÃOS: 1-4 (2BITS) ; 1-8 (3BITS) ; 1-16 (4BITS)
!
!	 NXMAX e NYMAX : NÚEROS DE BITS DE NA E NB
!
	AJX=LX/DMINX        ! AJUSTE DIREÇÃO X

	IF (AJX.GT.4) THEN
	              IF (AJX.LT.9) THEN
				                NXMAX=3
								ELSE
								NXMAX=4
				  ENDIF

				  ELSE
				  NXMAX=2
	ENDIF
						
	AJY=LY/DMINY		! AJUSTE DIREÇÃO Y

	IF (AJY.GT.4) THEN
	              IF (AJY.LT.9) THEN
				                NYMAX=3
								ELSE
								NYMAX=4
				  ENDIF

				  ELSE
				  NYMAX=2
	ENDIF
   
!
!   DETERMINAÇÃO TAMANHO DO CROMOSSOMO EM FUNÇÃO DA BASE VIGA
!
	
	IF (BMAX.GT.0.60) THEN
	                  NVV=5
					  ELSE
					  NVV=4
					  ENDIF
!
!  TAMANHO TOTAL DO CROMOSSOMO "NUMGEN"
!

   NUMGEN=21+NXMAX+NYMAX+NVV

		
	PAUSE 'Pressione ENTER para continuar.'

! Alocação das matrizes e dos vetores
	ALLOCATE (pop(numind,numgen), STAT=AllocateStatus)
	IF (AllocateStatus /= 0) STOP "*** Memoria insuficiente ***"
	pop = 0
	ALLOCATE (subpop(numind,numgen), STAT=AllocateStatus)
	IF (AllocateStatus /= 0) STOP "*** Memoria insuficiente ***"
	subpop = 0
	ALLOCATE (apt(numind), STAT=AllocateStatus)
	IF (AllocateStatus /= 0) STOP "*** Memoria insuficiente ***"
	apt = 0
	ALLOCATE (subapt(numind), STAT=AllocateStatus)
	IF (AllocateStatus /= 0) STOP "*** Memoria insuficiente ***"
	subapt = 0
	ALLOCATE (aptger(maxger + 1), STAT=AllocateStatus)
	IF (AllocateStatus /= 0) STOP "*** Memoria insuficiente ***"
	aptger = 0
	ALLOCATE (aptmed(maxger + 1), STAT=AllocateStatus)
	IF (AllocateStatus /= 0) STOP "*** Memoria insuficiente ***"
	aptmed = 0
	med = 0
	ALLOCATE (rank(cruz,numgen), STAT=AllocateStatus)
	IF (AllocateStatus /= 0) STOP "*** Memoria insuficiente ***"
	rank = 0
	ALLOCATE (subrank(cruz,numgen), STAT=AllocateStatus)
	IF (AllocateStatus /= 0) STOP "*** Memoria insuficiente ***"
	subrank = 0
	ALLOCATE (mut(numind,numgen), STAT=AllocateStatus)
	IF (AllocateStatus /= 0) STOP "*** Memoria insuficiente ***"
	mut = 0

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!          Rotina População inicial MAIOR -  29 maio 2006
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	! Inicialização da semente de números aleatórios pelo valor do clock do processador

	CALL SYSTEM_CLOCK( count )
	Seed = count
	CALL RANDOM_SEED( PUT = Seed )
	
	!
	! Geração de números binários aleatórios para o preenchimento população inicial
	!
    !		   Pop inicial 10 * Número de Indivíduos
	!

	Geracao_Inicial: DO i=1,10*numind

		DO j=1,numgen

			CALL RANDOM_NUMBER( R )
			IF (R >= 0.5) THEN
				pop(i,j) = 1
			ELSE 
				pop(i,j) = 0
			END IF

		END DO

	END DO Geracao_inicial

	! AVALIAR E ORDENAR 
	!
	! PREPARANDO P ENTRADA NO CICLO
	!

	   POP_INICIAL_MAIOR: DO k=1,10*numind

			CALL AvaliaInd(pop, numpav, dminx, dminy, lx, ly, hmax, bmax, &
	q, gpr, gpl, ccml, cpm, cap, cad, numind,NXMAX,NYMAX,NVV, numgen, k, F)
			apt(k) = F ! Atribuição do valor de F desse indivíduo ao vetor das aptidões
		        
				END DO POP_INICIAL_MAIOR

	   CALL OrdenaPop(pop, numind, numgen, apt, subpop, subapt)

	   POP=0

	   DO K=1,NUMIND

		  DO J=1,NUMGEN

		     POP(K,J)=SUBPOP(K,J)

		  ENDDO
	   
	   ENDDO

	 !
	 ! POP INICIAL PRONTA P ENTRAR NO CICLO EVOLUCIONARIO
	 !

		
! Início do ciclo evolucionário
!
! Com: Neste loop serão geradas "maxger" gerações em função do estabelecido
!

	CicloEvolucionario: DO ger=1,maxger

	! Avaliação da população
		Avaliar: DO k=1,numind

			CALL AvaliaInd(pop, numpav, dminx, dminy, lx, ly, hmax, bmax, &
	q, gpr, gpl, ccml, cpm, cap, cad, numind,NXMAX,NYMAX,NVV, numgen, k, F)
			apt(k) = F ! Atribuição do valor de F desse indivíduo ao vetor das aptidões
		        END DO Avaliar

! Com: Qdo volta da subrotina Avaliar se tem o valor da aptidão APT(k)

		! Cálculo da aptidão média da geração
		med=0
		Media: DO i=1,numind
			med = apt(i) + med
		      END DO Media 
		med = med / numind
		! Grava a média dessa geração no vetor 'aptmed'
		aptmed(ger) = med

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!		PRINT '(/, 1X, A)', "--- Vetor Aptidoes ---"

!		Impressao_aptidao: DO i=1,numind			  
!		                   PRINT '(1X, E8.2)', apt(i)
!		                   ENDDO Impressao_aptidao

!		PRINT '(1X, A, E8.2)', "Media = ", med
!		PRINT *

!		PAUSE 'Pressione ENTER para continuar.'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!
!                     Ordenação da população
!

		CALL OrdenaPop(pop, numind, numgen, apt, subpop, subapt)

		! Com: Qdo volta da subrotina Ordenação tem-se: Subpop e Subapt
		!      ordenadas

!		PRINT '(/, 1X, A, I4, A)', "--- Geracao", (ger-1), " ---"
!		PRINT '(1X, 39I1)', ((pop(i,j), j=1,numgen), i=1,numind)
!		PRINT '(/, 1X, A)', "--- Vetor Aptidoes ---"
!		Imprime_apt: DO i=1,numind
!		             PRINT '(1X, F8.2)', apt(i)
!                    ENDDO Imprime_apt
!		PRINT *
!		PRINT '(/, 1X, A)', "--- SubPopulacao Ordenada ---"
!		PRINT '(1X, 39I1)', ((subpop(i,j), j=1,numgen), i=1,numind)
!		PRINT '(/, 1X, A)', "--- Vetor Aptidoes Ordenado ---"
!       Imprime_apt_ordenada: DO i=1,numind
!		                      PRINT '(1X, F8.2)', subapt(i)
!                             ENDDO Imprime_apt_ordenada 
!		PRINT *
		! Grava a melhor aptidão no vetor 'aptger'
		aptger(ger) = subapt(1)
!		PAUSE 'Pressione ENTER para continuar.'

	! Geração da nova população
		pop = 0	  ! Zera a matriz pop para receber os valores na ordem

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!				
!                   ELITISMO
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

		Elitismo: DO i=1,elit

			DO j=1,numgen
			
				pop(i,j)=subpop(i,j)
			
			END DO

		END DO Elitismo

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!					ROTINA DOS GEMEOS: 29/03/2006
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	   GEMEOS: DO i=1,(elit-1)

				  teste=0

				  DO j=1,numgen

				  IF (pop((i+1),j).eq.pop(i,j))  THEN

												 teste=0

												 ELSE

												 teste=teste+1
				  ENDIF

				  ENDDO

				  IF (teste.eq.0)  THEN
				   
								   DO j=1,numgen

								   rank((elit+1),j)=pop(i+1,j)

								   pop((i+1),j)=subpop((elit+1),j)

								   ENDDO
				  ENDIF

			   ENDDO GEMEOS
			   
!
!	PREPARANDO OS INDIVIDUOS PARA O CRUZAMENTO
!
		Rankear: DO i=1,cruz

			DO j=1,numgen	
			
				rank(i,j) = subpop((i+elit),j)
			
			END DO

		END DO Rankear 

!		PRINT '(/, 1X, A)', "--- SubPopulacao Ordenada ---"
!		PRINT '(1X, 39I1)', ((subpop(i,j), j=1,numgen), i=1,numind)
!		PRINT '(/, 1X, A)', "--- Rank ---"
!		PRINT '(1X, 39I1)', ((rank(i,j), j=1,numgen), i=1,cruz)
!		PRINT *
!		PAUSE 'Pressione ENTER para continuar.'

	! Cruzamento (De um ponto ou Uniforme)

		subrank = 0

	! 	Com: Por enquanto apenas cruzamento Uniforme

	!	IF (Selcruz == 1) THEN
	!		CALL CruzUmPonto(rank, subrank, numgen, cruz)
	!	ELSE

			IF (Selcruz == 2) THEN
				CALL CruzUniforme(rank, subrank, numgen, cruz)
			ELSE
				STOP 'Escolha um tipo de cruzamento.'
			END IF
	
	! Reprodução (Substituição)
		Subst: DO i=1,cruz
			DO j=1,numgen
				pop((i+elit),j) = subrank(i,j) ! Os filhos assumem a posição na 
				                               ! nova geração
			END DO
		END DO Subst

!		PRINT '(/, 1X, A, I4, A)', "--- Geracao", ger, " ---"
!		PRINT '(1X, 39I1)', ((pop(i,j), j=1,numgen), i=1,numind)

	! Completar a população aleatoriamente

		Preencher: DO i=(elit+cruz+1),numind

			DO j=1,numgen

				CALL RANDOM_NUMBER( R )
				IF (R >= 0.5) THEN
					pop(i,j) = 1
				ELSE 
					pop(i,j) = 0
				END IF

			END DO

		END DO Preencher

!		PRINT '(/, 1X, A,)', "--- Preenchimento aleatorio ---"
!		PRINT '(/, 1X, A, I4, A)', "--- Geracao", ger, " ---"
!		PRINT '(1X, 39I1)', ((pop(i,j), j=1,numgen), i=1,numind)
!		PRINT *
!		PAUSE 'Pressione ENTER para continuar.'

!    MUTAÇÃO
!
!    Com: todos os indivíduos da população estão sujeitos a sofrer mutação
!         exceto os escolhidos pelo elitismo

   	! Geração de números binários aleatórios para o preenchimento da Matriz MUT

	Mutacao: DO i=(elit+1),numind ! Livra o Elitismo da mutação

		DO j=1,numgen

			CALL RANDOM_NUMBER( R )
			    mut(i,j) = R 
				IF (R.LE.pmut) THEN 
				                        IF (POP(i,j).EQ.1) THEN 
				                                  POP(i,j)=0
				                                  ELSE 
												  POP(i,j)=1
												  ENDIF
								
				ENDIF			
		END DO

	END DO Mutacao


	END DO CicloEvolucionario

	! Com: Qdo sai do último ciclo evolucionário tem-se uma pop q precisa ser ordenada
!
! Avaliação da última geração
!
!
	DO k=1,numind
		CALL AvaliaInd(pop, numpav, dminx, dminy, lx, ly, hmax, bmax, &
	q, gpr, gpl, ccml, cpm, cap, cad, numind,NXMAX,NYMAX,NVV, numgen, k, F)
		apt(k) = F
	END DO

	DO i=1,numind
		med = apt(i) + med
	END DO 
	med = med / numind
	aptmed(maxger + 1) = med

!	PRINT '(/, 1X, A)', "--- Vetor Aptidoes ---"
!
!		Impressao_aptidao: DO i=1,numind			  
!		                   PRINT '(1X, F8.2)', apt(i)
!		                   ENDDO Impressao_aptidao
!
!		PRINT '(1X, A, F8.2)', "Media = ", med
!		PRINT *

!
! Ordenação da última geração
!

	CALL OrdenaPop(pop, numind, numgen, apt, subpop, subapt)

!		PRINT '(/, 1X, A, I4, A)', "--- Geracao", (ger-1), " ---"
!		PRINT '(1X, 39I1)', ((pop(i,j), j=1,numgen), i=1,numind)
!		PRINT '(/, 1X, A)', "--- Vetor Aptidoes ---"
!		Imprime_apt: DO i=1,numind
!		             PRINT '(1X, F8.2)', apt(i)
!                    ENDDO Imprime_apt
!		PRINT *
		PRINT '(/, 1X, A)', "--- SubPopulacao Ordenada ---"
		PRINT '(1X, 39I1)', ((subpop(i,j), j=1,numgen), i=1,numind)
		PRINT '(/, 1X, A)', "--- Vetor Aptidoes Ordenado ---"
       Imprime_apt_ordenada: DO i=1,numind
		                     PRINT '(1X, E8.2)', subapt(i)
                             ENDDO Imprime_apt_ordenada 
		PRINT *

!           Grava a melhor aptidão no vetor 'aptger'

	aptger(maxger + 1) = subapt(1)

!	WRITE (6, '(1X,A)') "--- Melhores aptidoes de cada geracao ---"
!	WRITE (6, '(E8.2,A,I4,A)') aptger
!	WRITE (6, '(1X,A)') "--- Aptidoes medias de cada geracao ---"
!	WRITE (6, '(E8.2)') aptmed
!	WRITE (6, '(/,1X,A)') "--- Resultado ---"

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!																		 !
!			Imprime as melhores APTIDÕES de cada geração                 !
!																		 !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		
	WRITE (6, '(1X,A)') "--- Melhores aptidoes de cada geracao ---"
   	DO K=1,(maxger+1)
	WRITE (6, '(1X,A,I5,A,E10.4)') "APT(",K,")=", aptger(K)
	ENDDO
!	WRITE (6, '(1X,A)') "--- Aptidoes medias de cada geracao ---"
!	DO K=1,(maxger+1)
!	WRITE (6, '(1X,A,I4,A,E8.2)') "APTM(",K,")=", aptmed(K)
!	ENDDO

!
!  Volta a Subrotina AvaliaindF apenas para imprimir os resultados
!

	Imprime_SubPop: DO k=1,numind
	CALL AvaliaindF(subpop, subapt, numpav, dminx, dminy, lx, ly, hmax, bmax, &
	q, gpr, gpl, ccml, cpm, cap, cad, numind,NXMAX,NYMAX,NVV, numgen, k, F)
					ENDDO Imprime_SubPop 


	
	PAUSE 'Pressione ENTER para continuar.'

END PROGRAM AG