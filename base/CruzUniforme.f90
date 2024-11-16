! Sub-rotina para o Uniforme
! Seleciona um local para a permutação entre os pais.

SUBROUTINE CruzUniforme(rank, subrank, numgen, cruz)

! pai e mae escolhidos na ordem do rank 

IMPLICIT NONE
INTEGER, INTENT(IN) :: numgen, cruz
INTEGER, DIMENSION(cruz,numgen), INTENT(IN) :: rank	     ! Pais
INTEGER, DIMENSION(cruz,numgen), INTENT(OUT) :: subrank	 ! Filhos
INTEGER :: i, j
INTEGER, DIMENSION(numgen) :: masc	   ! Máscara para os cruzamentos
REAL :: R

!Geração da máscara
!
! Com: É gerada uma máscara para cada geração

	DO j=1,numgen

		CALL RANDOM_NUMBER( R )
		IF (R >= 0.5) THEN
			masc(j) = 1
		ELSE 
			masc(j) = 0
		END IF

	END DO
  
subrank = 0	   ! Zerar a matriz dos filhos

! pai=i
! mãe=i+1

Cruzamento: DO i=1,cruz,2

		DO j=1,numgen
	
		Filho1: IF (masc(j) == 0) THEN
			subrank(i,j) = rank(i,j)
		ELSE
			subrank(i,j) = rank((i+1),j)
		END IF Filho1

		Filho2: IF (masc(j) == 1) THEN
			subrank((i+1),j) = rank(i,j)
		ELSE
			subrank((i+1),j) = rank((i+1),j)
		END IF Filho2
				
	END DO

!	PRINT '(/, 1X, A)', "--- Rank ---"
!	PRINT '(1X, 39I1)', ((rank(p,q), q=1,numgen), p=1,cruz)
!	PRINT '(/,1X, A, I3, A)', "--- Cruzamento ", i, " ---"
!	WRITE (*,'(1X,A,I3)') "Posicao do individuo pai: ", i
!	WRITE (*,'(1X,A,I3)') "Posicao do individuo mae: ", i+1
!	PRINT '(1X,A,39I1)', "Mascara:", masc
!	PRINT '(1X,A,39I1)', "Pai:    ", (rank(pai,q), q=1,numgen)
!	PRINT '(1X,A,39I1)', "Mae:    ", (rank(mae,q), q=1,numgen)
!	PRINT '(1X,A,39I1)', "Filho1: ", (subrank(i,q), q=1,numgen)
!	PRINT '(1X,A,39I1)', "Filho2: ", (subrank((i+1),q), q=1,numgen)
!	PRINT '(/, 1X, A)', "--- SubRank (Filhos) ---"
!	PRINT '(1X, 39I1)', ((subrank(p,q), q=1,numgen), p=1,cruz)

!	PAUSE 'Pressione ENTER para continuar.'

END DO Cruzamento

END	SUBROUTINE CruzUniforme
