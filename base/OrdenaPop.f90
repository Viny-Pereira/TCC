! Sub-rotina para a ordenação da população em ordem crescente de aptidão.
! Recebe a matriz população e o vetor aptidões
! Retorna a matriz subpop ordenada e o vetor subapt ordenado

SUBROUTINE OrdenaPop(pop, numind, numgen, apt, subpop, subapt)

! copiaapt = cópia do vetor aptidão para ser manipulado na ordenação de subpop
! m = cópia do vetor MINLOC para possibilitar o uso do valor inteiro contido no mesmo.

IMPLICIT NONE
INTEGER, INTENT(IN) :: numind, numgen
INTEGER, DIMENSION(numind,numgen), INTENT(IN) :: pop
INTEGER, DIMENSION(numind,numgen), INTENT(OUT) :: subpop
REAL, DIMENSION(numind), INTENT(IN) :: apt
REAL, DIMENSION(numind), INTENT(OUT) :: subapt
INTEGER :: i, j
INTEGER, DIMENSION(1) :: m, n
REAL, DIMENSION(numind) :: copiaapt

subapt = 0

! Cópia do vetor aptidão para ser ordenado
copiaapt = apt

! Ordenação de subpop e subapt
n = MAXLOC(copiaapt)

DO i=1,numind

	DO j=1,numgen

! MINLOC fornece um vetor de tamanho igual ao número de dimensões do vetor alvo.
		m = MINLOC(copiaapt)

! Cópia do indivíduo de menor aptidão da matriz pop para a subpop
		subpop(i,j) = pop(m(1),j)

	END DO

!	PRINT *, 'Local do valor minimo anterior das aptidoes = ', m
!	PRINT *

! A posição da menor aptidão recebe o valor mais alto vezes 2, para que o próximo mínimo
! possa ser selecionado
	copiaapt(m(1)) = 2 * copiaapt(n(1))
!	PRINT '(/, 1X, A)', "--- Copia do Vetor Aptidoes Atual---"
!   Imprime_copiapt: DO j=1,numind
!	                 PRINT '(1X, F8.2)', copiaapt(j)
!                    ENDDO Imprime_copiaapt
!	PRINT *


! Preenchimento do vetor subapt ordenado

	subapt(i) = apt(m(1))

!	PRINT '(/, 1X, A)', "--- Vetor Aptidoes Ordenado Atual---"
!	Imprime_subapt: DO j=1,numind
!	                PRINT '(1X, F8.2)', subapt(j)
!                   ENDDO Imprime_subapt  
!	PRINT *
!	PAUSE 'Pressione ENTER para continuar.'

END DO

END SUBROUTINE OrdenaPop