import numpy as np


class AvaliaInd:

    def __int__(
        self,
        populacao,
        numero_pavimentos,
        dimensao_min_y,
        lx,
        ly,
        hmax,
        bmax,
        q,
        gpr,
        gpl,
        ccml,
        cpm,
        cap,
        cad,
        numind,
        NYMAX,
        NVV,
        numgen,
        iterator,
        F,
        NX,
        LL,
        LLJ,
        LLR,
    ):

        fckpm = np.zeros(4, dtype=int)
        fckml = np.zeros(4, dtype=int)
        DL = 0  # Direcao da laje 1 (direcao y) e 0 (direcao x)
        HL = np.zeros(32, dtype=float)
        PA = np.zeros(32, dtype=float)
        APL = np.zeros(32, dtype=float)
        YG = np.zeros(64, dtype=float)
        A = np.zeros(64, dtype=float)
        II = np.zeros(64, dtype=float)
        XMAX = np.zeros(64, dtype=float)
        carga = np.zeros(6, dtype=float)
        ml = np.zeros(6, dtype=float)
        rl = np.zeros(6, dtype=float)
        BP = np.zeros(4, dtype=float)

        NMAX = np.zeros(32, dtype=int)  # QUANTIDADE MAX DE CORDOALHAS POR CAMADA
        NA = np.zeros(16, dtype=int)
        NB = np.zeros(8, dtype=int)
        NPT = np.zeros(4, dtype=int)  # QUANTIDADDE DE BARRAS PASSIVAS DE TRACAO
        BP = np.zeros(4, dtype=float)  # BITOLAS PASSIVAS
        HV = np.zeros(32, dtype=float)  # ALTURA DA VIGA
        BV = np.zeros(32, dtype=float)  # LARGURA DA VIGA

        # LL = np.zeros(NX, dtype=int)

        for i in range(4):
            fckpm[i] = 35 + (i - 1) * 5  # 35,40,45,50 (valores fckpm)
            fckml[i] = 20 + (i - 1) * 5  # 20,25,30,35	(valores fckml)

        # 		Defini��o propriedades da laje se��o PM - T&A
        # 				   Banco Dados - Laje

        for i in range(4):
            HL[i] = 0.09  # Altura da Laje(m)
            A[i] = 0.0669983  # �rea da laje (m2)
            YG[i] = 0.045  # CG da laje (m)
            II[i] = 0.000063  # Momento de in�rcia da laje (m4)
            XMAX[i] = 0.065  # M�ximo X (LN)

        for i in range(4, 9):
            HL[i] = 0.13
            A[i] = 0.0918954
            YG[i] = 0.06784
            II[i] = 0.00018
            XMAX[i] = 0.07  # M�ximo valor do X (compress�o)

        for i in range(9, 15):
            HL[i] = 0.17
            A[i] = 0.1136454
            YG[i] = 0.08847
            II[i] = 0.000396
            XMAX[i] = 0.075

        for i in range(15, 21):
            HL[i] = 0.2
            A[i] = 0.1267849
            YG[i] = 0.1
            II[i] = 0.00063
            XMAX[i] = 0.0725

        for i in range(21, 27):
            HL[i] = 0.21
            A[i] = 0.135401
            YG[i] = 0.108
            II[i] = 0.000734
            XMAX[i] = 0.08

        for i in range(27, 32):
            HL[i] = 0.26
            A[i] = 0.1816019
            YG[i] = 0.129
            II[i] = 0.00144
            XMAX[i] = 0.085
        # 	                	For�a de Protensao (MN) - LAJES
        #
        # 	                        PA=N.Acor.1453.0,97.(10-6)
        #
        # 		                     Sinal (-) / Compressao

        PA[1] - 0.184350828
        PA[2] - 0.245801104
        PA[3] - 0.30725138
        PA[4] - 0.368701656
        PA[5] - 0.245801104
        PA[6] - 0.341640984
        PA[7] - 0.431843224
        PA[8] - 0.52430052
        PA[9] - 0.62577804
        PA[10] = -0.245801104
        PA[11] = -0.341640984
        PA[12] = -0.431843224
        PA[13] = -0.52430052
        PA[14] = -0.62577804
        PA[15] = -0.74980612
        PA[16] = -0.431843
        PA[17] = -0.524301
        PA[18] = -0.625778
        PA[19] = -0.749806
        PA[20] = -1.143313
        PA[21] = -1.429142
        PA[22] = -0.431843
        PA[23] = -0.524301
        PA[24] = -0.625778
        PA[25] = -0.749806
        PA[26] = -1.143313
        PA[27] = -1.429142
        PA[28] = -1.499612
        PA[29] = -2.286627
        PA[30] = -0.625778
        PA[31] = -0.749806
        PA[32] = -1.143313

        #
        # 	           �rea de Protens�o Total no painel da Laje
        #

        APL[1] = 0.0001308
        APL[2] = 0.0001744
        APL[3] = 0.000218
        APL[4] = 0.0002616
        APL[5] = 0.0001744
        APL[6] = 0.000242
        APL[7] = 0.0003064
        APL[8] = 0.000372
        APL[9] = 0.000444
        APL[10] = 0.0001744
        APL[11] = 0.0002424
        APL[12] = 0.0003064
        APL[13] = 0.000372
        APL[14] = 0.000444
        APL[15] = 0.000532
        APL[16] = 0.000306
        APL[17] = 0.000372
        APL[18] = 0.000444
        APL[19] = 0.000532
        APL[20] = 0.000811
        APL[21] = 0.001014
        APL[22] = 0.000306
        APL[23] = 0.000372
        APL[24] = 0.000444
        APL[25] = 0.000532
        APL[26] = 0.000811
        APL[27] = 0.001014
        APL[28] = 0.001064
        APL[29] = 0.001622
        APL[30] = 0.000444
        APL[31] = 0.000532
        APL[32] = 0.000811

        #
        #       	 LISTAS das vari�veis VIGAS
        #
        #
        #      	 Qde de barras passivas de tra��o

        NPT[1] = 0
        NPT[2] = 2
        NPT[3] = 4
        NPT[4] = 6

        # 	    �rea das Bitolas Passivas dispon�veis

        BP[1] = 0.000028  # 6.0mm
        BP[2] = 0.000050  # 8.0mm
        BP[3] = 0.000080  # 10.0mm
        BP[4] = 0.000125  # 12.5mm

        #       QDE DE CABOS CAMADA "A"

        NA[1] = 3
        NA[2] = 5
        NA[3] = 6
        NA[4] = 7
        NA[5] = 8
        NA[6] = 10
        NA[7] = 13
        NA[8] = 14
        NA[9] = 15
        NA[10] = 16
        NA[11] = 17
        NA[12] = 18
        NA[13] = 19
        NA[14] = 20
        NA[15] = 21
        NA[16] = 23

        #      QDE DE CABOS CAMADA "B"

        NB[1] = 0
        NB[2] = 2
        NB[3] = 4
        NB[4] = 6
        NB[5] = 8
        NB[6] = 10
        NB[7] = 12
        NB[8] = 14

        # 		Caracter�sticas Geom�tricas da VIGA

        for i in range(5):
            HV[i] = 0.20 + [i] * 0.05  # Altura
            HV[i + 5] = HV[i]
            HV[i + 10] = HV[i]
            HV[i + 15] = HV[i]
            HV[i + 20] = HV[i]
            HV[i + 25] = HV[i]
            BV[i] = 0.40  # Base
            BV[i + 5] = 0.50
            BV[i + 10] = 0.60
            BV[i + 15] = 0.70
            BV[i + 20] = 0.80
            BV[i + 25] = 0.90
            NMAX[i] = 13  # Qde m�xima de cordoalhas por base de viga
            NMAX[i + 5] = 15
            NMAX[i + 10] = 17
            NMAX[i + 15] = 19
            NMAX[i + 20] = 21
            NMAX[i + 25] = 23

        #   Complemento	das listas das Vigas (32 poss�veis)

        HV[31] = HV[29]
        BV[31] = BV[29]
        NMAX[31] = NMAX[29]
        HV[32] = HV[30]
        BV[32] = BV[30]
        NMAX[32] = NMAX[30]
        # 	               ROTINA PARA DECODIFICA��O
        #
        # 	  Com: As vari�veis que come�am com "A" s�o auxiliares
        #
        # 	  Com: Este "K" vem do Loop no programa principal (k=1 at� numind)
        #

        # J� � o pr�prio valor

        PM = 2 * populacao[iterator][0] + 1 * populacao[iterator][1] + 1  # Auxiliar
        CML = 2 * populacao[iterator][2] + 1 * populacao[iterator][3] + 1  # Auxiliar

        VL = (
            16 * populacao[iterator][4]
            + 8 * populacao[iterator][5]
            + 4 * populacao[iterator][6]
            + 2 * populacao[iterator][7]
            + 1 * populacao[iterator][8]
            + 1
        )  # Auxiliar

        ANPT = 2 * populacao[iterator][9] + 1 * populacao[iterator][10] + 1  # Auxiliar Lista NPT

        ABP = 2 * populacao[iterator][11] + 1 * populacao[iterator][12] + 1  # Auxiliar p a lista BP

        ANA = (
            8 * populacao[iterator][13]
            + 4 * populacao[iterator][14]
            + 2 * populacao[iterator][15]
            + 1 * populacao[iterator][16]
            + 1
        )  # Auxiliar

        ANB = 4 * populacao[iterator][17] + 2 * populacao[iterator][18] + 1 * populacao[iterator][19] + 1  # Auxiliar

        NY = 0

        for i in range(NYMAX):

            NY = NY + populacao[iterator][(20 + i)] * (2 ** (NYMAX - i))

            NY = NY + 1

            VV = 0

        for i in range(NVV):
            VV = VV + populacao[iterator][(20 + NYMAX + i)] * (2 ** (NVV - i) - 1)
        VV = VV + 1

        #                     REDU��O DO DOM�NIO DA BASE
        #
        #                   T�CNICA: ALTERAR O VALOR DE VV
        #
        # 	EXISTE UM ESPA�O INFACT�VEL MAS FAZ-SE TRANSFORMACAO NA LISTA
        #

        if bmax == 0.40:
            if VV > 5:
                if VV < 11:
                    VV -= 5
                else:
                    VV -= 10

        if bmax == 0.50:
            if VV > 10:
                VV -= 5

        if bmax == 0.60:
            if VV == 0.16:
                VV = 15

        if bmax == 0.70:
            if VV > 20 and VV < 26:
                VV -= 5
            else:
                VV -= 10

        if bmax == 0.80:
            if vv > 25:
                vv -= 5

#
#			  AJUSTE DO NA P NAO ULTRAPASSAR O NMAX
#


        if NA[ANA] > NMAX[VV]:
            NA[ANA] = NMAX[VV]


#							MORFOG�NESE (NA x NB)
#
#	           Troca por um fen�tipo que melhor se adapte ao problema	            				   
        if NB[ANB] > NA[ANA]:
            NBAUX = NB[ANB]
            NB[ANB] = NA[ANA]
            NA[ANA] = NBAUX


#   Ajuste dos V�os M�nimos
#
#   Penaliza exageradamente
        AJY = ly / dimensao_min_y

        if NY > AJY:
            NY = NY * 100

#       C�lculo dos V�os

        LLJ=(lx/NX)*(1-DL)+(ly/NY)*(DL)		 # (m) JA FOI CALCULADO
        LLV=(lx/NX)*(DL)+(ly/NY)*(1-DL)		 # (m)

        LLJC=LLJ-BV(VV)      # V�o laje corrigido (m)
