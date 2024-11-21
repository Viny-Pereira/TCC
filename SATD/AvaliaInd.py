import numpy as np


class AvaliadorDeIndividuos:
    def __init__(
        self,
        POP,
        numpav,
        dminx,
        dminy,
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
        nxmax,
        nymax,
        nvv,
        numgen,
        k,
        F,
    ):
        """
        Inicializa a classe AvaliadorDeIndividuos com os parâmetros fornecidos.

        Parâmetros:
        pop (ndarray): Matriz da população de indivíduos.
        numpav (int): Número de pavimentos.
        dminx (float): Distância mínima no eixo X.
        dminy (float): Distância mínima no eixo Y.
        lx (float): Comprimento no eixo X.
        ly (float): Comprimento no eixo Y.
        hmax (float): Altura máxima.
        bmax (float): Largura máxima.
        q (float): Outro parâmetro de avaliação.
        gpr, gpl, ccml, cpm, cap, cad (array-like): Conjuntos de parâmetros adicionais.
        numind (int): Número de indivíduos na população.
        nxmax, nymax (int): Parâmetros máximos de dimensões no eixo X e Y.
        nvv (int): Parâmetro específico para a avaliação.
        numgen (int): Número de gerações.
        k (int): indica os indivíduos a serem avaliados.
        F : Função aptidão
        """
        self.POP = POP
        self.numpav = numpav
        self.DMINX = dminx
        self.DMINY = dminy
        self.LX = lx
        self.LY = ly
        self.hmax = hmax
        self.bmax = bmax
        self.Q = q
        self.GPR = gpr
        self.GPL = gpl
        self.ccml = ccml
        self.cpm = cpm
        self.cap = cap
        self.cad = cad
        self.numind = numind
        self.NXMAX = nxmax
        self.NYMAX = nymax
        self.NVV = nvv
        self.numgen = numgen
        self.k = k
        # Inicializa lista de penalidades (GL) com zeros
        self.GL = np.zeros(17)
        # Inicializa os resultados de restrição
        self.GV = np.zeros(8)

        # Definindo o tamanho total da matriz
        n = 32

        # Inicializando os arrays com zeros
        self.HL = np.zeros(n)  # Altura da Laje (m)
        self.A = np.zeros(n)  # Area da Laje (m2)
        self.YG = np.zeros(n)  # CG da Laje (m)
        self.II = np.zeros(n)  # Momento de inercia da Laje (m4)
        self.XMAX = np.zeros(n)  # Linha neutra máxima

        # Inicialização das variáveis de vigas
        self.NPT = np.zeros(5)  # Qde de barras passivas de tração
        self.BP = np.zeros(5)  # Área das Bitolas Passivas disponíveis
        self.NA = np.zeros(16)  # QDE DE CABOS CAMADA "A"
        self.NB = np.zeros(8)  # QDE DE CABOS CAMADA "B"
        self.HV = np.zeros(32)  # Altura da Viga
        self.BV = np.zeros(32)  # Base da Viga
        self.NMAX = np.zeros(32)  # Qde máxima de cordoalhas por base de viga
        self.GL = np.zeros(17)  # Qde máxima de cordoalhas por base de viga
        self.GV = np.zeros(20)  # Qde máxima de cordoalhas por base de viga

        self.LLJ, self.LLV, self.LLJC = self.calcular_vaos()
        self.M, self.AC, self.YGC, self.IC = self.calculate_hollow_slab_properties()
        self.EP, self.EPC, self.WINF, self.WSUP, self.WCINF, self.WCSUP = (
            self.calculate_excentricity_modulus()
        )
        self.loads = self.calculate_slab_loads()
        self.ML, self.RL, self.MLD, self.VLD = self.calculate_moments_and_stresses()
        self.TINF, self.TSUP = self.calculate_stresses_concreting_phase()
        self.TCINF, self.TCSUP = self.calculate_stresses_after_concreting()
        self.PT = self.calculate_prestress_after_transfer()
        self.PINF = self.calculate_infinite_time_prestress()
        self.TINPT, self.TSUPT, self.TINPI, self.TSUPI = (
            self.calculate_stresses_due_to_prestress()
        )
        (
            self.TDESI,
            self.TDESS,
            self.TTI,
            self.TTS,
            self.TTII,
            self.TTSS,
            self.TMI,
            self.TMS,
        ) = self.calculate_void_stresses()

        self.LCJ, self.LTJ, self.LCK, self.LTK = self.calculate_stress_limits()
        self.DES, self.FF = self.calculate_els_stresses_slab()
        self.XL, self.DDL, self.MRESL = self.calculate_elu_solicitations()
        self.CFI, self.CFT = self.calculate_deflection_slab()
        self.fi, self.ft = self.calculate_deflection_loading()
        self.PENL = self.calculate_penalties()

    def avaliar_individuo(self):
        if self.k == 1:
            self.initialize_material_properties()
            self.initialize_panel_properties()
            self.initialize_prestressing_forces()
            self.initialize_beam_properties()

    def initialize_material_properties(self):
        """Inicializa as propriedades dos materiais."""
        self.FCKPM = 35 + np.arange(4) * 5  # fck para pré-moldado
        self.FCKML = 20 + np.arange(4) * 5  # fck para moldado in loco

    def initialize_panel_properties(self):
        """
        Inicializa os valores para as lajes em termos de altura, área,
        centro de gravidade, momento de inércia e força de protensão.
                        Definição propriedades da laje seção PM - T&A
                        Banco Dados - Laje"""

        # Atribuições para os diferentes intervalos de i
        self.HL[0:4], self.A[0:4], self.YG[0:4], self.II[0:4], self.XMAX[0:4] = (
            0.09,
            0.0669983,
            0.045,
            0.000063,
            0.065,
        )
        self.HL[4:9], self.A[4:9], self.YG[4:9], self.II[4:9], self.XMAX[4:9] = (
            0.13,
            0.0918954,
            0.06784,
            0.00018,
            0.07,
        )
        (
            self.HL[9:15],
            self.A[9:15],
            self.YG[9:15],
            self.II[9:15],
            self.XMAX[9:15],
        ) = (0.17, 0.1136454, 0.08847, 0.000396, 0.075)
        (
            self.HL[15:21],
            self.A[15:21],
            self.YG[15:21],
            self.II[15:21],
            self.XMAX[15:21],
        ) = (0.2, 0.1267849, 0.1, 0.00063, 0.0725)
        (
            self.HL[21:27],
            self.A[21:27],
            self.YG[21:27],
            self.II[21:27],
            self.XMAX[21:27],
        ) = (0.21, 0.135401, 0.108, 0.000734, 0.08)
        (
            self.HL[27:32],
            self.A[27:32],
            self.YG[27:32],
            self.II[27:32],
            self.XMAX[27:32],
        ) = (0.26, 0.1816019, 0.129, 0.00144, 0.085)

        # Inicializar força de protensão e áreas de protensão
        self.initialize_prestressing_forces()

    def initialize_prestressing_forces(self):
        """
        Inicializa os valores das forças de protensão (PA) e áreas de protensão (APL) para os painéis das lajes.
        """
        self.PA = np.array(
            [
                -0.184350828,
                -0.245801104,
                -0.30725138,
                -0.368701656,
                -0.245801104,
                -0.341640984,
                -0.431843224,
                -0.52430052,
                -0.62577804,
                -0.245801104,
                -0.341640984,
                -0.431843224,
                -0.52430052,
                -0.62577804,
                -0.74980612,
                -0.431843,
                -0.524301,
                -0.625778,
                -0.749806,
                -1.143313,
                -1.429142,
                -0.431843,
                -0.524301,
                -0.625778,
                -0.749806,
                -1.143313,
                -1.429142,
                -0.431843,
                -0.524301,
                -0.625778,
                -0.749806,
                -1.143313,
            ]
        )

        # Vetor da Área de Protensão Total (m²)
        self.APL = np.array(
            [
                0.0001308,
                0.0001744,
                0.000218,
                0.0002616,
                0.0001744,
                0.000242,
                0.0003064,
                0.000372,
                0.000444,
                0.0001744,
                0.0002424,
                0.0003064,
                0.000372,
                0.000444,
                0.000532,
                0.000306,
                0.000372,
                0.000444,
                0.000532,
                0.000811,
                0.001014,
                0.000306,
                0.000372,
                0.000444,
                0.000532,
                0.000811,
                0.001014,
                0.000306,
                0.000372,
                0.000444,
                0.000532,
                0.000811,
            ]
        )

    def initialize_beam_properties(self):
        """
        Inicializa as propriedades das vigas, incluindo
        a quantidade de barras passivas, áreas de bitolas,
        e características geométricas da viga.
        """
        # Quantidade de barras passivas de tração
        self.NPT = np.array([0, 2, 4, 6])

        # Área das bitolas passivas disponíveis (6mm; 8mm; 10mm; 12.5mm)
        self.BP = np.array([0.000028, 0.000050, 0.000080, 0.000125])

        # Quantidade de cabos na camada "A"
        self.NA = np.array([3, 5, 6, 7, 8, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23])

        # Quantidade de cabos na camada "B"
        self.NB = np.array([0, 2, 4, 6, 8, 10, 12, 14])

        # Características geométricas da viga
        # Usando operações vetorizadas para Altura da Viga
        base_HV = 0.20 + np.arange(5) * 0.05
        self.HV[:5] = base_HV
        self.HV[5:10] = base_HV
        self.HV[10:15] = base_HV
        self.HV[15:20] = base_HV
        self.HV[20:25] = base_HV
        self.HV[25:30] = base_HV

        # Usando operações vetorizadas para Base da Viga
        self.BV[:5] = 0.40
        self.BV[5:10] = 0.50
        self.BV[10:15] = 0.60
        self.BV[15:20] = 0.70
        self.BV[20:25] = 0.80
        self.BV[25:30] = 0.90

        # Usando operações vetorizadas para NMAX
        self.NMAX[:5] = 13
        self.NMAX[5:10] = 15
        self.NMAX[10:15] = 17
        self.NMAX[15:20] = 19
        self.NMAX[20:25] = 21
        self.NMAX[25:30] = 23

        # Complemento das listas das Vigas
        self.HV[30] = self.HV[28]
        self.BV[30] = self.BV[28]
        self.NMAX[30] = self.NMAX[28]
        self.HV[31] = self.HV[29]
        self.BV[31] = self.BV[29]
        self.NMAX[31] = self.NMAX[29]

    def get_panel_properties(self):
        """
        Retorna as propriedades dos painéis em um formato de dicionário.
        """
        return {
            "Altura": self.HL,
            "Área": self.A,
            "Centro de Gravidade": self.YG,
            "Momento de Inércia": self.II,
            "XMAX": self.XMAX,
            "Força de Protensão": self.PA,
            "Área de Protensão": self.APL,
        }

    def decodificar(self, k):
        """
        Rotina para decodificação do indivíduo k na população.

        Parâmetros:
        k (int): Índice do indivíduo a ser decodificado.

        Retorna:
        dict: Dicionário contendo os valores decodificados.
        """
        # DL é o próprio valor da coluna POP(k,1)
        self.DL = self.POP[k, 0]

        # Auxiliares
        self.PM = 2 * self.POP[k, 1] + self.POP[k, 2] + 1
        self.CML = 2 * self.POP[k, 3] + self.POP[k, 4] + 1

        # VL auxiliar
        self.VL = (
            +16 * self.POP[k, 5]
            + 8 * self.POP[k, 6]
            + 4 * self.POP[k, 7]
            + 2 * self.POP[k, 8]
            + 1 * self.POP[k, 9]
            + 1
        )

        # ANPT auxiliar para a lista NPT
        self.ANPT = 2 * self.POP[k, 10] + 1 * self.POP[k, 11] + 1

        # ABP auxiliar para a lista BP
        self.ABP = 2 * self.POP[k, 12] + 1 * self.POP[k, 13] + 1

        # ANA auxiliar
        self.ANA = (
            8 * self.POP[k, 14]
            + 4 * self.POP[k, 15]
            + 2 * self.POP[k, 16]
            + 1 * self.POP[k, 17]
            + 1
        )

        # ANB auxiliar
        self.ANB = 4 * self.POP[k, 18] + 2 * self.POP[k, 19] + 1 * self.POP[k, 20] + 1

        # NX decodificação
        self.NX = self.calculate_nx(k)
        # NY decodificação
        self.NY = self.calculate_ny(k)

        # VV decodificação
        VV = self.calculate_vv(k, self.NX, self.NY)

        # Redução do domínio da base
        self.VV = self.reduce_domain(VV)

        # AJUSTE DO NA P NAO ULTRAPASSAR O NMAX
        if self.NA[self.ANA] > self.NMAX[self.VV]:
            self.NA[self.ANA] = self.NMAX[self.VV]

        # MORFOGÊNESE (NA x NB)
        # Troca por um fenótipo que melhor se adapte ao problema

        if self.NB[self.ANB] > self.NA[self.ANA]:
            self.NB[self.ANB], self.NA[self.ANA] = self.NA[self.ANA], self.NB[self.ANB]

    def calculate_nx(self, k):
        """
        Calcula NX.
        """
        NX = 0
        for i in range(1, self.NXMAX + 1):
            NX += self.subpop[k, 20 + i] * (2 ** (self.NXMAX - i))
        return NX + 1

    def calculate_ny(self, k):
        """
        Calcula NY.
        """
        NY = 0
        for i in range(1, self.nymax + 1):
            NY += self.subpop[k, 20 + self.nxmax + i] * (2 ** (self.nymax - i))
        return NY + 1

    def calculate_vv(self, k):
        """
        Calcula VV.
        """
        VV = 0
        for i in range(1, self.nvv + 1):
            VV += self.subpop[k, 20 + self.nxmax + self.nymax + i] * (
                2 ** (self.nvv - i)
            )
        return VV + 1

    def reduce_domain(self, VV):
        """
        Reduz o domínio da base.
        """
        if self.bmax == 0.40:
            if VV > 5:
                VV = VV - 5 if VV < 11 else VV - 10
        elif self.bmax == 0.50:
            if VV > 10:
                VV -= 5
        elif self.bmax == 0.60:
            if VV == 16:
                VV = 15
        elif self.bmax == 0.70:
            if VV > 20:
                VV = VV - 5 if VV < 26 else VV - 10
        elif self.bmax == 0.80:
            if VV > 25:
                VV -= 5
        return VV

    def display_results(self, k):
        """
        Exibe os resultados da decodificação.
        """
        print(f"NX: {self.NX}")
        print(f"NY: {self.NY}")
        print(f"DL: {self.DL}")
        print(f"PM: {self.PM}")
        print(f"CML: {self.CML}")
        print(f"VL: {self.VL}")
        print(f"VV: {self.VV}")
        print(f"NA[{self.ANA}]: {self.NA[self.ANA]}")
        print(f"NB[{self.ANB}]: {self.NB[self.ANB]}")
        print(f"ANPT: {2 * self.POP[k, 10] + 1 * self.POP[k, 11] + 1}")
        print(f"ABP: {2 * self.POP[k, 12] + 1 * self.POP[k, 13] + 1}")

    def penalizar_vanos(self):
        """
        Aplica penalizações nos vãos, se necessário.

        Parâmetros:
        NX (int): Número de divisões no eixo X.
        NY (int): Número de divisões no eixo Y.

        Retorna:
        NX (int): NX penalizado, se necessário.
        NY (int): NY penalizado, se necessário.
        """
        # Calcula os ajustes
        AJX = self.LX / self.DMINX
        AJY = self.LY / self.DMINY

        # Aplica penalização onde necessário
        self.NX = np.where(self.NX > AJX, self.NX * 100, self.NX)
        self.NY = np.where(self.NY > AJY, self.NY * 100, self.NY)

    def calcular_vaos(self):
        """
        Calcula os vãos corrigidos com base em NX e NY.

        Parâmetros:
        NX (int): Número de divisões no eixo X.
        NY (int): Número de divisões no eixo Y.

        Retorna:
        LLJC (float): Vão laje corrigido.
        """
        # Cálculos dos vãos
        LLJ = (self.LX / self.NX) * (1 - self.DL) + (self.LY / self.NY) * self.DL
        LLV = (self.LX / self.NX) * self.DL + (self.LY / self.NY) * (1 - self.DL)

        # Correção do vão laje com base na largura da viga
        LLJC = self.LLJ - self.BV[self.VV]

        return LLJ, LLV, LLJC

    # LAJES ALVEOLARES

    def calculate_hollow_slab_properties(self):
        """
        Calcula as propriedades da seção composta da laje.
        Painel b=1.2m
        """
        # Cálculo do fator Momento
        M = (self.FCKML[self.CML] / self.FCKPM[self.PM]) ** 0.5

        # Área da seção composta
        AC = self.M * 1.2 * 0.05

        # Coordenada do centro de gravidade da seção composta
        YGC = (
            +(self.A[self.VL] * self.YG[self.VL])
            + (self.AC * (self.HL[self.VL] + 0.025))
        ) / (self.A[self.VL] + self.AC)

        # Momento de inércia da seção composta
        IC = (
            self.II[self.VL]
            + self.A[self.VL] * ((self.YGC - self.YG[self.VL]) ** 2)
            + (self.M * 1.2 * (0.05**3)) / 12
            + self.AC * (self.HL[self.VL] + 0.025 - self.YGC) ** 2
        )

        return AC, YGC, IC

    def calculate_excentricity_modulus(self):
        """
        Calcula as excentricidades e os módulos resistentes das lajes.

        Parâmetros:
        YGC (float): Centro de gravidade da seção composta.
        IC (float): Momento de inércia da seção composta.
        """
        # Excentricidade seção isolada e composta
        EP = self.YG[self.VL] - 0.012 - 0.006  # (m) seção isolada
        EPC = self.YGC - 0.012 - 0.006  # (m) seção composta

        # Módulos resistentes
        WINF = self.II[self.VL] / self.YG[self.VL]
        WSUP = self.II[self.VL] / (self.YG[self.VL] - self.HL[self.VL])
        WCINF = self.IC / self.YGC
        WCSUP = self.IC / (self.YGC - self.HL[self.VL] - 0.05)

        return EP, EPC, WINF, WSUP, WCINF, WCSUP

    def calculate_slab_loads(self):
        """
        Calcula as cargas aplicadas na laje.
        Painel b=1.2m
        """

        # Define constants and panel width
        panel_width = 1.2
        # Load calculation per panel (b=1.2m)
        loads = np.array(
            [
                self.A[self.VL] * 2.5,  # Self-weight (tf/m)
                0.125 * panel_width,  # Cap weight (tf/m)
                self.GPR * panel_width,  # Pav+Rev (tf/m)
                self.GPL * panel_width,  # Wall load on the slab (tf/m)
                self.Q * panel_width,  # Accidental load (tf/m)
                0.05 * panel_width,  # Workload on slab (tf/m)
            ]
        )

        return loads

    def calculate_moments_and_stresses(self):
        """
        Calcula os momentos e as reações (cortantes) para cada carga.
        Painel b=1.2m

        Parâmetros:
        Carga (ndarray): Array de cargas aplicadas.

        Retorna:
        ML (ndarray): Momentos por painel (tf.m).
        RL (ndarray): Reações (cortantes) por painel (tf).
        MLD (float): Momento de cálculo (MN.m).
        VLD (float): Cortante de cálculo (MN).
        """

        # Calculate moments and reactions using vectorized operations
        ML = self.loads * (self.LLJC**2) / 8  # Moments in tf.m (b=1.2m)
        RL = self.loads * (self.LLJ) / 2  # Reactions in tf (per panel b=1.2m)

        # Design actions per panel (MN.m and MN)
        MLD = (
            1.3 * self.ML[0] + 1.4 * np.sum(self.ML[1:])
        ) / 100  # Design moment in MN.m
        VLD = (
            1.3 * self.RL[0] + 1.4 * np.sum(self.RL[1:])
        ) / 100  # Design shear force in MN

        return ML, RL, MLD, VLD

    def calculate_stresses_concreting_phase(self):
        """
        Calculate stresses during the concreting phase (isolated piece).
        :param WINF: Módulo resistente inferior
        :param WSUP: Módulo resistente superior
        :return: TINF (tensão inferior) e TSUP (tensão superior) em MPa
        """
        TINF = (self.ML[0] + self.ML[1] + self.ML[5]) / self.WINF / 100  # MPa
        TSUP = (self.ML[0] + self.ML[1] + self.ML[5]) / self.WSUP / 100  # MPa
        return TINF, TSUP

    def calculate_stresses_after_concreting(self):
        """
        Calculate stresses after concreting (composite section).
        :param WCINF: Módulo resistente inferior da seção composta
        :param WCSUP: Módulo resistente superior da seção composta
        :return: TCINF (tensão inferior) e TCSUP (tensão superior) em MPa
        """
        TCINF = (self.ML[2] + self.ML[3] + self.ML[4]) / self.WCINF / 100  # MPa
        TCSUP = (self.ML[2] + self.ML[3] + self.ML[4]) / self.WCSUP / 100  # MPa
        return TCINF, TCSUP

    def calculate_prestress_after_transfer(self):
        """
        Calculate prestress after transfer.
        :param PA: Força de protensão inicial
        :param EP: Excentricidade
        :param WINF: Módulo resistente inferior
        :param WSUP: Módulo resistente superior
        :param fckpm: Resistência do concreto da laje protendida
        :return: PT (força de protensão após transferência)
        """
        SCP = self.PA[self.VL] / self.A[self.VL]
        +self.PA[self.VL] * (self.EP**2 / self.II[self.VL])  # Mself.Pa

        SPT = (-1) * (
            (self.PA[self.VL] / self.A[self.VL])
            + self.PA[self.VL] * (self.EP / self.WINF)
        )
        +(195000 / (0.85 * 5600 * (self.FCKPM[self.PM] ** 0.5))) * SCP

        PT = self.PA[self.VL] - self.APL[self.VL] * SPT  # MN
        return PT

    def calculate_infinite_time_prestress(self):
        """
        Calculate the prestress force at infinite time (PINF).
        :param PA: Força de protensão inicial
        :return: PINF (força de protensão após tempo infinito) em MN
        """
        PINF = 0.75 * self.PA[self.VL]  # MN
        return PINF

    def calculate_stresses_due_to_prestress(self):
        """
        Calculate stresses in the prestressed section after transfer.
        :param PT: Protensão após transferência
        :param EP: Excentricidade
        :param WINF: Módulo resistente inferior
        :param WSUP: Módulo resistente superior
        :param PINF: Protensão em tempo infinito
        :return: Tensões inferiores e superiores
        """
        TINPT = (self.PT / self.A[self.vl]) + self.PT * (self.EP / self.WINF)  # MPa
        TSUPT = (self.PT / self.A[self.vl]) + self.PT * (self.EP / self.WSUP)  # MPa
        TINPI = (self.PINF / self.A[self.vl]) + self.PINF * (self.EP / self.WINF)  # MPa
        TSUPI = (self.PINF / self.A[self.vl]) + self.PINF * (self.EP / self.WSUP)  # MPa
        return TINPT, TSUPT, TINPI, TSUPI

    # Método para cálculo de tensões atuantes em vazio

    def calculate_void_stresses(self):
        """
        Calculate void stresses during demolding, transport, and assembly.
        :param ML: Momentos atuantes
        :param TINPT: Tensão inferior após protensão
        :param TSUPT: Tensão superior após protensão
        :return: Tensões atuantes em vazio
        """
        TDESI = self.TINPT + (self.ML[0] / self.WINF) / 100  # Desmoldagem Inferior
        TDESS = self.TSUPT + (self.ML[0] / self.WSUP) / 100  # Desmoldagem Superior
        TTI = (
            self.TINPT + 0.8 * (self.ML[0] / self.WINF) / 100
        )  # Transporte Inferior (0.8)
        TTS = (
            self.TSUPT + 0.8 * (self.ML[0] / self.WSUP) / 100
        )  # Transporte Superior (0.8)
        TTII = (
            self.TINPT + 1.3 * (self.ML[0] / self.WINF) / 100
        )  # Transporte Inferior (1.3)
        TTSS = (
            self.TSUPT + 1.3 * (self.ML[0] / self.WSUP) / 100
        )  # Transporte Superior (1.3)
        TMI = self.TINPT + self.TINF
        TMS = self.TSUPT + self.TSUP
        return TDESI, TDESS, TTI, TTS, TTII, TTSS, TMI, TMS

    # Método para cálculo dos limites de tensões
    def calculate_stress_limits(self):
        """
        Calculate stress limits for compression and tension.
        :param fckpm: Resistência do concreto
        :return: Limites de compressão e tração
        """
        LCJ = 0.49 * self.FCKPM[self.PM]  # Limite compressão (transitória)
        LTJ = (
            1.2 * 0.7 * 0.3 * ((0.7 * self.FCKPM[self.PM]) ** (2 / 3))
        )  # Limite tração (transitória)
        LCk = 0.7 * self.FCKPM[self.PM]  # Limite compressão (ELS)
        LTk = 1.2 * 0.7 * 0.3 * (self.FCKPM[self.PM] ** (2 / 3))  # Limite tração (ELS)
        return LCJ, LTJ, LCk, LTk

    # Método para cálculo de tensões ELS
    def calculate_els_stresses_slab(self):
        """
        Calculate the ELS stresses (MPa) for decompression and crack formation.
        :param WINF: Módulo resistente inferior
        :param WCINF: Módulo resistente inferior da seção composta
        :param TINPI: Tensão na seção em tempo infinito
        :return: DES (tensão de descompressão), FF (tensão de formação de fissura)
        """
        # Descompressão
        DES = (
            ((self.ML[0] + self.ML[1]) / self.WINF) / 100
            + self.TINPI
            + ((self.ML[2] + self.ML[3]) / self.WCINF) / 100
            + 0.3 * (self.ML[4] / self.WCINF) / 100
        )

        # Formação de Fissura
        FF = (
            ((self.ML[0] + self.ML[1]) / self.WINF) / 100
            + self.TINPI
            + ((self.ML[2] + self.ML[3]) / self.WCINF) / 100
            + 0.4 * (self.ML[4] / self.WCINF) / 100
        )

        return DES, FF

    # Método para calcular solicitações normais ELU
    def calculate_elu_solicitations(self):
        """
        Calculate the normal solicitations in the Ultimate Limit State (ELU) for hollow core slabs.
        :return: XL (Distance from the neutral axis), DDL (Effective slab height), MRESL (Resisting moment for the slab)
        """
        # Altura útil da laje simplificada (DDL)
        DDL = self.HL[self.VL] + 0.03875

        # Cálculo de XTL para o painel b=1.2m
        XTL = 2551.05 * self.APL[self.VL] / self.FCKML[self.CML]

        # Verificação de XTL e cálculo de XL, ZL e MRESL
        if XTL <= 0.05:
            # Primeiro caso (XTL <= 0.05)
            XL = XTL
            ZL = DDL - 0.4 * XL
            MRESL = self.APL[self.VL] * 1486.9 * ZL

        else:
            # Segundo caso (XTL > 0.05)
            XL = (
                (1486.9 * self.APL[self.VL] - 0.0291 * self.FCKML[self.CML])
                / (0.58285 * self.FCKPM[self.PM])
            ) + 0.05
            ZLA = DDL - 0.4 * XL
            ZLB = DDL - 0.02
            MRESL = (
                0.0291 * self.FCKML[self.CML] * ZLB
                + 0.58285 * (XL - 0.05) * self.FCKPM[self.PM] * ZLA
            )

        return XL, DDL, MRESL

    # FLECHAS EM LAJES

    def calculate_deflection_slab(self):
        """
        Calculate the initial and total deflection (contra-flecha) for a slab.

        :return: CFI (Initial deflection) and CFT (Total deflection)
        """

        CFI = (self.PA[self.VL] * self.EP * self.LLJC) / (
            8 * 4760 * self.FCKPM[self.PM] ** (0.5) * self.II[self.VL]
        )  # Contra-flecha INICIAL
        CFT = CFI * 2.2  # Estimativa contra-flecha TOTAL
        return CFI, CFT

    def calculate_deflection_loading(self):
        """
        Calculate the deflection of the slab under loading conditions based on the initial deflection (flecha) and total deflection (flecha total).
        :return: Initial deflection (fi) and total deflection (ft)
        """
        fi = (
            3 * np.sum(self.loads[:4]) + 0.3 * self.loads[4] * (self.LLJC**4) / 100
        )  # Flecha inicial
        EIL = (
            384 * 4760 * self.FCKPM[self.PM] ** (0.5) * self.IC
        )  # Flecha inicial (seção composta)
        ft = (fi / EIL) * 2.5  # Estimativa flecha TOTAL
        return fi, ft

    # Restricoes
    def calculate_penalties(self):

        # Restrições para TDESI, TTI, TTII, TMI
        self.GL[0] = (
            0 if abs(self.TDESI) <= self.LCJ else abs(self.TDESI / self.LCJ) - 1
        )
        self.GL[1] = 0 if abs(self.TTI) <= self.LCJ else abs(self.TTI / self.LCJ) - 1
        self.GL[2] = 0 if abs(self.TTII) <= self.LCJ else abs(self.TTII / self.LCJ) - 1
        self.GL[3] = 0 if abs(self.TMI) <= self.LCJ else abs(self.TMI / self.LCJ) - 1

        # Restrições em vazio - Superior (tracionada)

        # Restrição TDESS
        self.GL[4] = (
            0 if self.TDESS <= (2 * self.LTJ) else abs(self.TDESS / (2 * self.LTJ)) - 1
        )

        # Restrição TTS usando limite ACI
        self.GL[5] = (
            0
            if self.TTS <= (0.7 * np.sqrt(self.FCKPM[self.PM]))
            else abs(self.TTS / (0.7 * np.sqrt(self.FCKPM[self.PM]))) - 1
        )
        # Restrições TTSS, TMS
        self.GL[6] = (
            0 if self.TTSS <= (2 * self.LTJ) else abs(self.TTSS / (2 * self.LTJ)) - 1
        )
        self.GL[7] = (
            0 if self.TMS <= (2 * self.LTJ) else abs(self.TMS / (2 * self.LTJ)) - 1
        )

        # ELS - Descompressão e Formação de Fissura
        self.GL[8] = 0 if self.DES <= 0 else self.DES
        self.GL[9] = 0 if self.FF <= (2 * self.LTK) else (self.FF / (2 * self.LTK)) - 1

        # Restrição X dentro da peça (acima dos alvéolos)
        self.GL[10] = (
            0 if self.XL <= self.XMAX[self.VL] else (self.XL / self.XMAX[self.VL]) - 1
        )

        # ELU e Beta X
        self.GL[11] = 0 if self.MRESL >= self.MLD else (self.MLD / self.MRESL) - 1

        # Beta X Laje
        BXL = self.XL / self.DDL
        self.GL[12] = 0 if BXL >= 0 else abs(BXL)
        self.GL[13] = 0 if BXL <= 0.6 else (BXL / 0.6) - 1

        # Distância mínima entre pilares
        min_pillar_dist = self.DMINX * (1 - self.DL) + self.DMINY * self.DL
        self.GL[14] = (
            0 if self.LLJ >= min_pillar_dist else (min_pillar_dist / self.LLJ) - 1
        )

        # Verificação de flechas
        self.GL[15] = (
            0
            if (self.ft + self.CFT) <= (1.05 * self.LLJ / 250)
            else ((self.ft + self.CFT) / (1.05 * self.LLJ / 250)) - 1
        )

        # Restrição de relação vão/altura laje (BIJAN)
        self.GL[16] = (
            0
            if (self.LLJ / (self.HL[self.VL] + 0.05)) <= 45
            else ((self.LLJ / (self.HL[self.VL] + 0.05)) / 45) - 1
        )
        # Somatório das penalidades (PENL)
        PENL = np.sum(self.GL[:17])  # Soma dos primeiros 17 elementos de GL
        return PENL

    # CRIAR UMA NOVA CLASSE

    # VIGA "T" INVERTIDA
    def viga_T_invertida(self):
        # Constantes pré-calculadas
        self.pp_concrete = 2.5  # Peso específico do concreto tf/m³
        self.AV = self.calc_area_isolated_beam()
        self.PPV = self.calc_ppv()

    def calc_area_isolated_beam(self):
        """
        Calcula a área da seção transversal da viga isolada.

        Returns:
            float: Área da seção transversal da viga isolada.
        """
        return (self.BV[self.VV] + 0.3) * self.HV[self.VV] + self.BV[self.VV] * (
            self.HL[self.VL] - 0.05
        )

    def calc_ppv(self):
        """
        Calcula o peso próprio da viga isolada.

        Returns:
            float: Peso próprio da viga (tf/m).
        """
        return self.AV * self.pp_concrete

    def calc_inertia_isolated_beam(self):
        """
        Calcula o momento de inércia da viga isolada e o centro de gravidade.

        Returns:
            tuple: Centro de gravidade (ygv) e momento de inércia (iv).
        """
        ME = (self.BV[self.VV] + 0.3) * (self.HV[self.VV] ** 2) / 2
        +self.BV[self.VV] * (self.HL[self.VL] - 0.05) * (
            self.HV[self.VV] + (self.HL[self.VL] - 0.05) / 2
        )
        YGV = ME / self.AV
        IV = (
            (self.BV[self.VV] + 0.3) * (self.HV[self.VV] ** 3) / 12
            + self.BV[self.VV] * ((self.HL[self.VL] - 0.05) ** 3) / 12
            + (self.BV[self.VV] + 0.3)
            * self.HV[self.VV]
            * ((self.HV[self.VV] / 2 - YGV) ** 2)
            + self.BV[self.VV]
            * (self.HL[self.VL] - 0.05)
            * ((self.HV[self.VV] + (self.HL[self.VL] - 0.05) / 2 - YGV) ** 2)
        )
        return YGV, IV

    def calc_composite_section_properties(self):
        """
        Calcula as propriedades da seção composta, considerando a viga e a laje.

        Returns:
            tuple: Área da seção composta (avc), centro de gravidade (ygcv) e momento de inércia (ivc).
        """
        AVC = self.AV + self.HV[self.VV] * 0.1
        MEC = (
            (self.BV[self.VV] + 0.3) * (self.HV[self.VV] ** 2 / 2)
            + self.BV[self.VV] * (self.HL[self.VL] - 0.05) * (self.HV[self.VV])
            + (self.HL[self.VL] - 0.05 / 2)
            + self.BV[self.VV] * 0.1 * (self.HV[self.VV] + self.HL[self.VL] + 0.05)
        )
        YGCV = MEC / AVC
        IVC = (
            (self.BV[self.VV] + 0.30) * (self.HV[self.VV] ** 3) / 12
            + (self.BV[self.VV] + 0.30)
            * self.HV[self.VV]
            * (((self.HV[self.VV] / 2) - YGCV) ** 2)
            + self.BV[self.VV] * ((self.HL[self.VL] + 0.05) ** 3) / 12
            + self.BV[self.VV]
            * (self.HL[self.VL] + 0.05)
            * (((self.HV[self.VV] + ((self.HL[self.VL] + 0.05) / 2)) - YGCV) ** 2)
        )
        return AVC, YGCV, IVC

    def calc_ppvc(self):
        """
        Calcula o peso próprio da viga isolada.

        Returns:
            float: Peso próprio da viga (tf/m).
        """
        return self.PPV + self.BV[self.VV] * 0.1 * 2.5

    def calculate_layer_eccentricity(self):
        """
        Calculate the eccentricity values for different layers in the slab.

        :return: Tuple containing:
            - EPA (float): Eccentricity for layer A based on YGV
            - EPCA (float): Eccentricity for layer CA based on YGCV
            - EPB (float): Eccentricity for layer B based on YGV
            - EPCB (float): Eccentricity for layer CB based on YGCV
        """
        epa = self.YGV - 0.05
        epca = self.YGCV - 0.05
        epb = self.YGV - 0.10
        epcb = self.YGCV - 0.10

        return epa, epca, epb, epcb

    def calculate_resistant_modulus(self):
        """
        Calculate the resistant modulus for different layers in the slab.

        :return: Tuple containing:
            - WVI (float): Resistant modulus for the slab based on YGV
            - WVS (float): Resistant modulus for the slab adjusted by HV and HL
            - WCVI (float): Resistant modulus for composite section based on YGCV
            - WCVS (float): Resistant modulus for composite section adjusted by HV and HL
        """
        wvi = self.IV / self.YGV
        wvs = self.IV / (self.YGV - (self.HV(self.VV) + self.HL(self.VL) - 0.05))

        wcvi = self.IVC / self.YGCV
        wcvs = self.IVC / (self.YGCV - (self.HV(self.VV) + self.HL(self.VL) + 0.05))

        return wvi, wvs, wcvi, wcvs

    def momentos_tensoes(self):
        av, PPV, ygv, iv = self.propriedades_geometrica_viga_isolada()
        avc, mec, ygcv, ppvc, ivc = self.propriedades_secao_composta()
        self.EPA = ygv - 0.05
        self.EPB = ygv - 0.10
        self.EPCA = ygcv - 0.05
        self.EPCB = ygcv - 0.10

        # Módulo Resistente
        self.WVI = iv / ygv
        self.WVS = iv / (ygv - (self.HV[self.VV] + self.HL[self.VL]) - 0.05)
        self.WCVI = ivc / ygcv
        self.WCVS = ivc / (ygcv - (self.HV[self.VV] + self.HL[self.VL]) + 0.05)
        # Momentos e tensões na fase de montagem
        MVT = (
            (((self.RL[0] + self.RL[1]) / 1.2) * 2 + PPV) * (self.LLV**2) / 8
        )  # Momento transitório (Tf.m)
        TVI = MVT / (100 * self.WVI)  # Tensaona secao isolada (MPA)
        TVS = MVT / (100 * self.WVS)

        # Momentos e tensões devido ao peso próprio
        MVPP = (
            PPV * (self.LLV**2)
        ) / 8  # Momento devido ao peso próprio da viga (Tf.m)
        TVPPI = MVPP / (100 * self.WVI)  # Tensões devido ao peso próprio da viga (MPa)
        TVPPS = MVPP / (100 * self.WVS)

        # Momentos e tensões durante a vida útil (ELS)
        MVG = (
            (((self.RL[2] + self.RL[3]) / 1.2) * 2) * (self.LLV**2) / (2 * 8)
        )  # Tf.m / Pav + Rev + Paredes
        MVQ = (self.RL[4] / 1.2) * 2 * (self.LLV**2) / (2 * 8)  # Tf.m / Sobrecarga (q)

        TVGI = MVG / (self.WCVI * 100)  # Tensões devido a pav + rev + par (MPa)
        TVQ = MVQ / (self.WCVI * 100)  # Tensões devido à sobrecarga (MPa)

        return TVI, TVS, TVPPI, TVPPS, TVGI, TVQ

    def reacoes_pilares(self):
        av, PPV, ygv, iv = self.propriedades_geometrica_viga_isolada()
        rpilar = (
            (np.sum(self.RL[:5]) * (2 / 1.2) + PPV) * self.LLV * self.num_pav * 1.02
        )  # Reação no pilar (TF)

        # Definição de SP e LP com base em RPILAR
        if rpilar <= 380:
            sp = 0.16
            lp = 0.4
        elif rpilar <= 600:
            sp = 0.25
            lp = 0.5
        else:
            sp = 0.36
            lp = 0.6
        self.LP = lp
        self.SP = sp
        return rpilar, sp, lp

    def momento_calculo(self):
        av, PPV, ygv, iv = self.propriedades_geometrica_viga_isolada()
        # Cálculo do momento de cálculo
        MVD = (
            (
                (
                    1.3 * self.RL[0]
                    + 1.4 * self.RL[1]
                    + 1.4 * (self.RL[2] / 2)
                    + 1.4 * (self.RL[3] / 2)
                    + 1.4 * (self.RL[4] / 2)
                )
                * (2 / 1.2)
                + 1.3 * (1.3 * PPV)
            )
            * ((self.LLV - self.LP) ** 2)
            / 8
        ) / 100  # Momento de cálculo (MN.m)
        return MVD

    # PROTENSÃO EM VIGAS

    def protensao_vigas(self):
        av, PPV, ygv, iv = self.propriedades_geometrica_viga_isolada()

        # Protensão na pista (MN)

        PAV = (
            -0.97 * (self.NA[self.ANA] + self.NB[self.ANB]) * 0.0001014 * 1453
        )  # MN (sinal - / Compressão)
        soma = (
            (self.NA[self.ANA] * self.EPA + self.NB[self.ANB] * self.EPB)
            * 0.97
            * 0.0001014
            * 1453
            * (-1)
        )  # Sinal -
        soma2 = (
            (self.NA[self.ANA] * (self.EPA**2) + self.NB[self.ANB] * (self.EPB**2))
            * 0.97
            * 0.0001014
            * 1453
            * (-1)
        )  # Sinal -

        # Protensão após transferência (MN)
        SPTV = (-1) * ((PAV / av) + (soma / self.WVI)) + (
            40.966 / (self.FCKPM[self.PM] ** 0.5)
        ) * ((PAV / av) + (soma2 / iv))

        self.PAT = PAV - (self.NA[self.ANA] + self.NB[self.ANB]) * 0.0001014 * SPTV

        soma3 = self.PAT * (
            self.NA[self.ANA] * self.EPA / (self.NA[self.ANA] + self.NB[self.ANB])
        ) + self.PAT * (
            self.NB[self.ANB] * self.EPB / (self.NA[self.ANA] + self.NB[self.ANB])
        )

        vtinpt = (self.PAT / av) + (soma3 / self.WVI)
        vtsupt = (self.PAT / av) + (soma3 / self.WVS)

        # Protensão em um tempo infinito (MN)
        VPINF = 0.8 * PAV  # Perda estimada (20%)
        VTINPI = (VPINF / av) + (0.8 * soma / self.WVI)
        VTSUPI = (VPINF / av) + (0.8 * soma / self.WVS)

        return vtinpt, vtsupt, VTINPI, VTSUPI

    def tensoes_limites(self):
        # Cálculo das tensões limites
        LTJV = (
            1.5 * 0.7 * 0.3 * ((0.7 * self.FCKPM[self.PM]) ** (2 / 3))
        )  # Limite tração (Retangular)
        LTkV = 1.5 * 0.7 * 0.3 * (self.FCKPM[self.PM] ** (2 / 3))  # Limite tração (ELS)
        return LTJV, LTkV

    # Tensoes ELS

    def tensoes_els(self):
        TVI, TVS, TVPPI, TVPPS, TVGI, TVQ = self.momentos_tensoes()
        vtinpt, vtsupt, vtinpi, vtsupi = self.protensao_vigas()
        # Cálculo das tensões ELS (MPa)
        DESCOMPV = TVI + TVGI + 0.3 * TVQ + vtinpi  # vtinpi
        FFISSV = TVI + TVGI + 0.4 * TVQ + vtinpi  # vtinpi

        return DESCOMPV, FFISSV

    def tensoes_transitorias(self):
        # Recupera tensões protensão
        TVI, TVS, TVPPI, TVPPS, TVGI, TVQ = self.momentos_tensoes()
        vtinpt, vtsupt, vtinpi, vtsupi = self.protensao_vigas()
        av, PPV, ygv, iv = self.propriedades_geometrica_viga_isolada()

        # Tensões atuantes nas fases transitórias
        tdiv = vtinpt + TVPPI  # Desmoldagem Inferior
        tdsv = vtsupt + TVPPS  # Desmoldagem Superior
        ttiv = vtinpt + 0.8 * TVPPI  # Transporte Inferior
        ttsv = vtsupt + 0.8 * TVPPS  # Transporte Superior
        ttiiv = vtinpt + 1.3 * TVPPI  # Transporte Inferior 1.3
        ttssv = vtsupt + 1.3 * TVPPS  # Transporte Superior 1.3
        tmiv = vtinpi + TVI  # Montagem Inferior
        tmsv = vtsupi + TVS  # Montagem Superior

        return tdiv, tdsv, ttiv, ttsv, ttiiv, ttssv, tmiv, tmsv

    # PROTENSÃO SUPERIOR

    def calcular_protensao_superior(self, TTSV, TMSV, TDSV, LTJV):
        av, PPV, ygv, iv = self.propriedades_geometrica_viga_isolada()
        avc, mec, ygcv, ppvc, ivc = self.propriedades_secao_composta()

        PATS = 0.85 * (-0.5716)  # 4 cabos, considerando 85% (MN)
        EPCV = ygv - (self.HV[self.VV] - 0.05)
        EPCCV = self.YGCV - (self.HV[self.VV] - 0.05)
        PROTSUP = (PATS / av) + (PATS * EPCV / self.WVS)

        if TTSV > (2 * LTJV):
            TTSV += PROTSUP
        if TMSV > (2 * LTJV):
            TMSV += PROTSUP
        if TDSV > (2 * LTJV):
            TDSV += PROTSUP

        return TTSV, TMSV, TDSV

    def calcular_altura_total(self):
        self.HT = self.HV[self.VV] + self.HL[self.VL] + 0.05

    def braco_alavanca(self):
        self.DA = self.HT - 0.05
        self.DB = self.HT - 0.10

    def calcular_momento_resistente(self):
        # Cálculo de áreas
        APA = self.NA[self.ANA] * 0.0001014  # Área da armadura A
        APB = self.NB[self.ANB] * 0.0001014  # Área da armadura B
        AS = self.NPT[self.ANPT] * self.BP[self.ABP]  # Área da protensão

        # Cálculo de X (Linha-Neutra)
        XV = (1486.9 * (APA + APB) + 434.8 * AS) / (
            0.4857 * self.FCKPM[self.PM] * self.BV[self.VV]
        )

        # Braços de alavanca
        ZA = self.HT - 0.05 - 0.4 * XV  # Braço de alavanca camada A
        ZB = ZA - 0.05  # Braço de alavanca camada B

        # Momento resistido pela seção (MN.m)
        MRESV = 1486.9 * (APA * ZA + APB * ZB)
        return XV, MRESV

    # FLECHAS DE VIGAS

    def calcular_flechas(self):
        av, PPV, ygv, iv = self.propriedades_geometrica_viga_isolada()
        avc, mec, ygcv, ppvc, ivc = self.propriedades_secao_composta()

        cfiv = (self.PAT * self.EPA * self.LLV) / (
            8 * 4760 * (self.FCKPM[self.PM] ** 0.5) * iv
        )
        self.CFTV = cfiv * 2.5

        # Cálculo de fiv e ftv
        fiv = (
            3
            * ((np.sum(self.RL[:4]) + 0.3 * self.RL[4]) * (2 / 1.2) + PPV)
            * (self.LLV**4)
        ) / (100 * 384 * 4760 * (self.FCKPM[self.PM] ** 0.5) * ivc)
        self.FTV = fiv * 2.5

        # Cálculo das restrições
        self.calcular_restricoes()

    def calcular_restricoes(self):
        tdiv, tdsv, ttiv, ttsv, ttiiv, ttssv, tmiv, tmsv = self.tensoes_transitorias()
        DESCOMPV, FFISSV = self.tensoes_els()
        LTJV, LTkV = self.tensoes_limites()
        XV, MRESV = self.calcular_momento_resistente()
        MVD = self.momento_calculo()
        # Condição para TDIV
        if abs(tdiv) <= self.LCJ:
            self.GV[0] = 0
        else:
            self.GV[0] = abs(tdiv / self.LCJ) - 1

        # Condição para TTIV
        if abs(ttiv) <= self.LCJ:
            self.GV[1] = 0
        else:
            self.GV[1] = abs(ttiv / self.LCJ) - 1

        # Condição para TTIIV
        if abs(ttiiv) <= self.LCJ:
            self.GV[2] = 0
        else:
            self.GV[2] = abs(ttiiv / self.LCJ) - 1

        # Condição para TMIV
        if abs(tmiv) <= self.LCJ:
            self.GV[3] = 0
        else:
            self.GV[3] = abs(tmiv / self.LCJ) - 1

        # ZONA SUPERIOR - TRACIONADA
        fckpm_sqrt = (0.7 * self.FCKPM[self.PM]) ** 0.5

        # Condição para TDSV
        if tdsv <= fckpm_sqrt:
            self.GV[4] = 0
        else:
            self.GV[4] = abs(tdsv / fckpm_sqrt) - 1

        # Condição para TTSV
        if ttsv <= fckpm_sqrt:
            self.GV[5] = 0
        else:
            self.GV[5] = abs(ttsv / fckpm_sqrt) - 1

        # Condição para TTSSV
        if ttssv <= fckpm_sqrt:
            self.GV[6] = 0
        else:
            self.GV[6] = abs(ttssv / fckpm_sqrt) - 1

        # Condição para TMSV
        if tmsv <= fckpm_sqrt:
            self.GV[7] = 0
        else:
            self.GV[7] = abs(tmsv / fckpm_sqrt) - 1

        # ELS

        # Descompressão
        if DESCOMPV <= 0.05:
            self.GV[8] = 0
        else:
            self.GV[8] = (DESCOMPV / 0.05) - 1

        # Formação de fissura
        if FFISSV <= (2 * LTkV):
            self.GV[9] = 0
        else:
            self.GV[9] = (FFISSV / (2 * LTkV)) - 1

        # Restrição de momento
        if MRESV >= (0.98 * MVD):
            self.GV[10] = 0
        else:
            self.GV[10] = (
                abs((0.98 * MVD) / MRESV) - 1
                if MRESV > 0
                else 1 - (MRESV / (0.98 * MVD))
            )

        # Beta X
        BXV = XV / self.DA
        self.GV[11] = 0 if BXV > 0 else abs(BXV)
        self.GV[12] = 0 if BXV <= (1.02 * 0.6) else (BXV / (1.02 * 0.6)) - 1
        # Geometria
        self.GV[13] = (
            0
            if self.NA[self.ANA] <= self.NMAX[self.VV]
            else (self.NA[self.ANA] / self.NMAX[self.VV]) - 1
        )
        self.GV[14] = (
            0
            if self.NB[self.ANB] <= self.NMAX[self.VV]
            else (self.NB[self.ANB] / self.NMAX[self.VV]) - 1
        )
        self.GV[15] = 0 if self.HT <= self.hmax else (self.HT / self.hmax) - 1
        self.GV[16] = (
            0
            if self.BV[self.VV] <= self.bmax
            else ((100 * self.BV[self.VV]) / self.bmax) - 1
        )

        # Distância mínima entre pilares
        if self.LLV >= (self.DMINX * self.DL + self.DMINY * (1 - self.DL)):
            self.GV[17] = 0
        else:
            self.GV[17] = (
                (self.DMINX * self.DL + self.DMINY * (1 - self.DL)) / self.LLV
            ) - 1
        if self.NA[self.ANA] <= self.NB[self.ANB]:
            self.GV[18] = 0
        else:
            self.GV[18] = self.NB[self.ANB] / self.NA[self.ANA] - 1

        # Verificação de flechas
        if (self.CFTV + self.FTV) <= (1.05 * self.LLV / 250):
            self.GV[19] = 0
        else:
            self.GV[19] = ((self.CFTV + self.FTV) / (1.05 * self.LLV / 250)) - 1

        self.PENV = np.sum(self.GV[:20])

    def penalidade_total(self):
        self.PENTOTAL = 1 + 15 * (self.PENV + self.PENL)  # Intensidade penalização K=10

    def conta_elementos(self):
        # Quantidade de vigas, lajes e pilares por pavimento
        QDV = self.NX * (self.NY + 1) * self.DL + self.NY * (self.NX + 1) * (
            1 - self.DL
        )
        QDL = (self.NX * self.LLV / 1.2) * self.NY * self.DL + (
            self.NY * self.LLV / 1.2
        ) * self.NX * (1 - self.DL)
        QDP = (self.NX + 1) * (self.NY + 1)
        # Ajuste pela quantidade de pavimentos
        return QDV, QDL, QDP

    # CALCULO DA FUNCAO APTIDAO

    def calcula_volumes(self):
        QDV, QDL, QDP = self.conta_elementos()
        # Volume Vigas
        VPMV = (
            (self.BV[self.VV] + 0.3) * self.HV[self.VV]
            + self.BV[self.VV] * (self.HL[self.VL] - 0.05)
        ) * (self.LLV - self.LP)

        # Volume Lajes
        VPML = self.A[self.VL] * (self.LLJ - self.BV[self.VV])

        # Volume Capa + Complemento Viga
        VML = (self.LX * self.LY - QDP * self.SP) * 0.05 + self.BV[self.VV] * 0.05 * (
            self.LLV - self.LP
        ) * QDV

        # Volume Pilares
        VPMP = self.SP * 3.5 * 1.15  # Volume Pilar com ajuste para console
        return VPMV, VPML, VML, VPMP

    def calcula_taxa_aco_pilar(self):
        # Cálculo da taxa de aço no pilar
        if self.PM > 1:
            if self.PM == 2:
                RO = 120
            elif self.PM == 3:
                RO = 90
            else:
                RO = 60
        else:
            RO = 150

        self.RO = RO

    def calcula_volume_aco(self):
        # Cálculo do volume de aço para os diferentes elementos

        # Volume de aço protensão da viga
        VAPV = (
            (self.NA[self.ANA] + self.NB[self.ANB]) * 0.0001014 * (self.LLV - self.LP)
        )

        # Volume de aço protensão da laje
        VAPL = self.APL[self.VL] * (self.LLJ - self.BV[self.VV])

        # Volume de aço doce da viga
        VADV = self.NPT[self.ANPT] * self.BP[self.ABP] * (self.LLV - self.LP)

        return VAPV, VAPL, VADV

    def calcula_custo_concreto(self):
        VAPV, VAPL, VADV = self.calcula_volume_aco()
        VPMV, VPML, VML, VPMP = self.calcula_volumes()
        QDV, QDL, QDP = self.conta_elementos()
        CUSTOCONC = (
            (VPMV * self.cpm[self.PM] * QDV) * 1.5
            + (VPML * self.cpm[self.PM] * QDL)
            + (VPMP * self.cpm[self.PM] * QDP * 1.5)
        ) * self.numpav
        return CUSTOCONC

    def calcula_custo_concreto_lajes(self):
        VPMV, VPML, VML, VPMP = self.calcula_volumes()
        CUSTOCONCML = VML * self.CML * 1.3 * self.numpav
        return CUSTOCONCML

    def calcula_custo_operacional(self):
        QDV, QDL, QDP = self.conta_elementos()

        DOP = 24 if self.VL < 28 else 36
        CDOP = QDL * (self.LLJ - self.BV[self.VV]) * 1.2 * DOP * self.numpav
        return CDOP

    def calcula_custo_transporte(self):
        VPMV, VPML, VML, VPMP = self.calcula_volumes()
        QDV, QDL, QDP = self.conta_elementos()

        CTV = 1600 if (self.LLV - self.LP) > 12 else 1000
        CTL = 1600 if (self.LLJ - self.BV[self.VV]) > 12 else 1000
        CTP = 1600 if self.numpav > 3 else 1000
        CTT = (
            ((VPMV * QDV * CTV) / 10)
            + ((VPML * QDL * CTL) / 10)
            + ((VPMP * QDP * CTP) / 10)
        ) * self.numpav
        return CTT

    def calcula_custo_montagem(self):
        QDV, QDL, QDP = self.conta_elementos()
        CTMV = np.ceil((QDV / 16) + (QDL / 24))
        CTMP = (QDP / 8) * 1500
        CTMT = 1500 * CTMV * self.numpav + CTMP
        return CTMT

    def calcula_custo_acos(self):
        VPMV, VPML, VML, VPMP = self.calcula_volumes()
        VAPV, VAPL, VADV = self.calcula_volume_aco()

        QDV, QDL, QDP = self.conta_elementos()

        CUSTOPROT = (
            (1.085 * VAPV * 7810.65 * QDV + VAPL * 7857 * QDL) * self.cap * self.numpav
        )
        CUSTOAD = (
            VADV * 7760 * QDV * self.cad + VPMP * self.RO * QDP * self.cad
        ) * self.numpav
        CUSTOCIS = (
            5.6
            * (((self.BV[self.VV] - 0.05) + (self.HV[self.VV] - 0.05)) * 2 + 0.12)
            * self.BV[self.VV]
            * (self.LLV - self.LP)
            * QDV
            * self.cad
            * self.numpav
        )
        CUSTOPE = 0.86912 * (self.LLV - self.LP) * QDV * self.numpav * self.cad
        CUSTOLIG = 12.125 * QDP * self.numpav * self.cad
        CUSTONEO = QDP * 2 * self.numpav * 22.5
        return CUSTOPROT, CUSTOAD, CUSTOCIS, CUSTOPE, CUSTOLIG, CUSTONEO

    def calcula_custo_fabricacao(self):
        CUSTOCONC = self.calcula_custo_concreto()
        CDOP = self.calcula_custo_operacional()
        CUSTOPROT, CUSTOAD, CUSTOCIS, CUSTOPE, _, _ = self.calcula_custo_acos()
        CUSTOFAB = (CUSTOCONC + CUSTOPROT + CUSTOAD + CDOP + CUSTOCIS + CUSTOPE) * 1.33
        return CUSTOFAB

    def calcula_custo_total(self):
        CUSTOFAB = self.calcula_custo_fabricacao()
        CUSTOCONCML = self.calcula_custo_concreto_lajes()
        CTT = self.calcula_custo_transporte()
        CTMT = self.calcula_custo_montagem()
        _, _, _, _, CUSTOLIG, CUSTONEO = self.calcula_custo_acos()
        CUSTOTAL = (
            CUSTOFAB + CUSTOCONCML + CTT + CTMT + CUSTONEO + CUSTOLIG
        ) / self.numpav
        F = CUSTOTAL * self.PENTOTAL
        return F
