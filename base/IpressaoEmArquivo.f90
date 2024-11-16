!=======================================================================================
!OK-ISO9001
				subroutine IniciarArqOut (arqou,unid)
!
!			Subrotina para inicializar arquivos de saida de dados e resultados do
!	problema.
!	Variáveis:
!		arqou	- arquivo de saida do problema
!		existe	- variável de trabalho do tipo lógica
!		resposta- variável de trabalho do tipo caracter
!		ia		- indicador de arquivo.Se igual a
!				  0 => arquivo ainda indefinido
!				  1 => arquivo foi definido
!
!=======================================================================================

!	Declaracao de variaveis

	implicit real*8 (a-h,o-z)
	integer unid
	character*24 arqou
	logical existe
	character*1 resposta
      
!	Saida em arquivo:

	ia = 0
	arquivo: do while (ia.eq.0)
		inquire (file=arqou,exist=existe)
		if (existe) then
30			write (*,'(/,5x,''Arquivo de Saida '',a24,'' já Existe. Pode Continuar? &
				 &(s/n) ===> '',\)') arqou
			read (*,'(a1)',err=30) resposta
			if (resposta /= 's') then
20				write (*,'(/,5x,''Novo Arquivo de Saida (Incluir Extensao) ===>'',\)')
				read (*,'(a24)',err=20) arqou
				cycle
			else
				open (unit=unid,file=arqou,status='old')
			end if
		else
			open (unit=unid,file=arqou,status='new')
		end if
      
!		Impressao do cabecalho      
      
!		write (unid,'(90(1h*),//,''S A O D E R C O F  -  STRUCTURAL ANALYSIS AND OPT&
!			  &IMUM DESIGN OF REINFORCED CONCRETE FRAMES'', &
!			  &  /,23x,''Versao 1.0'',/,23x, &
!			  &  ''Antonio Macario Cartaxo de Melo'',/,23x, &
!			  &  ''Rio de Janeiro - Agosto/97'',//,90(1h*),/)')
!		write (unid,'(/,''Arquivo de saida: '',a24)') arqou
		ia = 1
	end do arquivo
	
	return
    end      
