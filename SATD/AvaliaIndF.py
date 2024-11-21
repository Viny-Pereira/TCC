import numpy as np


class StructuralEvaluation:
    """
    Classe para realizar a avaliação estrutural de indivíduos em uma população.

    Esta classe calcula parâmetros estruturais, como aptidão, propriedades de lajes
    e vigas, baseando-se em uma população inicial de indivíduos e diversas restrições
    e propriedades fornecidas.

    Atributos:
    ----------
    subpop : np.ndarray
        Matriz contendo as informações dos indivíduos da população.
    fitness : np.ndarray
        Array para armazenar os valores de aptidão de cada indivíduo.
    numpav : int
        Número de pavimentos do edifício.
    dminx, dminy : float
        Distâncias mínimas permitidas em X e Y, respectivamente.
    LX, LY : float
        Comprimentos das dimensões do pavimento em X e Y.
    hmax, bmax : float
        Altura máxima e largura máxima permitidas para as vigas.
    Q : float
        Sobrecarga aplicada (Tf/m²).
    GPR : float
        Carga permanente do pavimento (Tf/m²).
    GPL : float
        Carga permanente das paredes (Tf/m²).
    ccml : np.ndarray
        Custos unitários de concreto para diferentes resistências à compressão.
    cpm : np.ndarray
        Custos unitários de concreto para diferentes classes de pilares.
    cap : float
        Custo unitário do aço protendido (R$/kg).
    cad : float
        Custo unitário do aço passivo (R$/kg).
    numind : int
        Número de indivíduos na população.
    nxmax, nymax : int
        Número máximo de divisões permitidas nas dimensões X e Y.
    nvv : int
        Número de variáveis vinculadas ao projeto de vigas.
    numgen : int
        Número de gerações a serem simuladas.

    Propriedades das Lajes:
    ------------------------
    HL : np.ndarray
        Altura das lajes (m).
    A : np.ndarray
        Área das lajes (m²).
    YG : np.ndarray
        Centro de gravidade das lajes (m).
    II : np.ndarray
        Momento de inércia das lajes (m⁴).
    XMAX : np.ndarray
        Máxima compressão em X das lajes.

    Propriedades de Protensão:
    --------------------------
    PA : np.ndarray
        Força de protensão aplicada às lajes (MN).
    APL : np.ndarray
        Área total de protensão nos painéis das lajes (m²).

    Propriedades das Vigas:
    ------------------------
    NPT : np.ndarray
        Quantidade de barras passivas de tração.
    BP : np.ndarray
        Área das bitolas passivas disponíveis.
    NA : np.ndarray
        Quantidade de cabos na camada "A".
    NB : np.ndarray
        Quantidade de cabos na camada "B".
    HV : np.ndarray
        Altura das vigas (m).
    BV : np.ndarray
        Base das vigas (m).
    NMAX : np.ndarray
        Quantidade máxima de cordoalhas permitidas por base de viga.
    GL : np.ndarray
        Quantidade máxima de cordoalhas por seção longitudinal.
    GV : np.ndarray
        Quantidade máxima de cordoalhas por seção transversal.
    """

    def __init__(
        self,
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
    ):
        """
        Inicializa uma instância da classe StructuralEvaluation com os parâmetros fornecidos.

        Parâmetros:
        -----------
        numpav : int
            Número total de pavimentos do edifício.
        dminx : float
            Distância mínima permitida entre elementos estruturais na direção X (m).
        dminy : float
            Distância mínima permitida entre elementos estruturais na direção Y (m).
        lx : float
            Comprimento total do edifício na direção X (m).
        ly : float
            Comprimento total do edifício na direção Y (m).
        hmax : float
            Altura máxima permitida para as vigas (m).
        bmax : float
            Largura máxima permitida para as vigas (m).
        q : float
            Sobrecarga aplicada sobre os pavimentos (kN/m²).
        gpr : float
            Carga permanente devido ao peso próprio das lajes e acabamentos (kN/m²).
        gpl : float
            Carga permanente devido às paredes (kN/m²).
        ccml : np.ndarray
            Custos unitários do concreto por diferentes resistências à compressão (R$/m³).
        cpm : np.ndarray
            Custos unitários do concreto em diferentes categorias de pilares (R$/m³).
        cap : float
            Custo unitário do aço protendido (R$/kg).
        cad : float
            Custo unitário do aço passivo (R$/kg).
        numind : int
            Número total de indivíduos na população inicial.
        nxmax : int
            Máximo número de divisões permitidas na direção X.
        nymax : int
            Máximo número de divisões permitidas na direção Y.
        nvv : int
            Número de variáveis relacionadas ao projeto de vigas.
        numgen : int
            Número de gerações para as simulações.
        """
        self.numpav = numpav
        self.dminx = dminx
        self.dminy = dminy
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
        self.nxmax = nxmax
        self.nymax = nymax
        self.nvv = nvv
        self.numgen = numgen
        # Propriedades da LAJE
        self.HL = np.zeros(32)  # Altura da Laje (m)
        self.A = np.zeros(32)  # Área da Laje (m²)
        self.YG = np.zeros(32)  # Centro de Gravidade da Laje (m)
        self.II = np.zeros(32)  # Momento de Inércia da Laje (m^4)
        self.XMAX = np.zeros(32)  # Máximo X (compressão)

        self.PA = np.zeros(32)  # Força de Protensão (MN)
        self.APL = np.zeros(32)  # Área de Protensão Total no painel da Laje (m²)

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

        # Inicializa as propriedades
        self.initialize_properties()

    def initialize_properties(self):
        self.initialize_material_properties()
        self.initialize_panel_properties()
        self.initialize_beam_properties()
        self.initialize_prestressing_forces()

    def initialize_individual(self, subpop):
        """
        Initializes an individual with a given subpopulation, decodes its genetic representation,
        calculates spans, and evaluates structural components and costs.

        This method performs the following steps for the given individual:
        1. Decodes the genetic representation of the subpopulation.
        2. Calculates the longitudinal and vertical spans.
        3. Evaluates the hollow slab design.
        4. Computes the properties of inverted T-beams.
        5. Calculates the structural cost.

        Args:
            subpop (np.ndarray): A binary array representing the genetic representation of the individual.
                                Each gene encodes a design parameter.

        Returns:
            None. Updates the instance attributes based on the evaluated individual.
        """
        self.subpop = subpop
        self.decode()
        self.LLJ, self.LLV, self.LLJC = self.calculate_spans()
        self.hollow_slab()
        self.inverted_t_beam()
        self.custo_estrutura()

    def initialize_material_properties(self):
        """
        Inicializa as propriedades dos materiais de concreto.

        Este método define os valores de resistência característica à compressão (fck)
        para os concretos pré-moldado e moldado in loco, em MPa.

        - `FCKPM`: Resistências características para concreto pré-moldado.
        Valores gerados: [35, 40, 45, 50] MPa.
        - `FCKML`: Resistências características para concreto moldado in loco.
        Valores gerados: [20, 25, 30, 35] MPa.

        Os valores são definidos em incrementos de 5 MPa a partir de um limite inferior.
        """
        self.FCKPM = 35 + np.arange(4) * 5  # fck para pré-moldado
        self.FCKML = 20 + np.arange(4) * 5  # fck para moldado in loco

    def initialize_panel_properties(self):
        """
        Inicializa as propriedades das lajes estruturais do painel.

        Este método atribui valores fixos a várias propriedades das lajes,
        organizadas em intervalos predefinidos, para os seguintes parâmetros:

        - `HL`: Altura da laje (m).
        - `A`: Área da laje (m²).
        - `YG`: Centro de gravidade da laje em relação à base (m).
        - `II`: Momento de inércia da laje em relação ao eixo neutro (m⁴).
        - `XMAX`: Distância máxima permitida em x para a laje (compressão).

        Os valores são definidos em diferentes faixas de índices:
        - Intervalos [0:4], [4:9], [9:15], [15:21], [21:27], [27:32] representam
        diferentes tipos de lajes, com parâmetros específicos.

        Valores atribuídos:
        -------------------
        - Índices [0:4]:
            HL = 0.09 m, A = 0.0669983 m², YG = 0.045 m, II = 0.000063 m⁴, XMAX = 0.065 m.
        - Índices [4:9]:
            HL = 0.13 m, A = 0.0918954 m², YG = 0.06784 m, II = 0.00018 m⁴, XMAX = 0.07 m.
        - Índices [9:15]:
            HL = 0.17 m, A = 0.1136454 m², YG = 0.08847 m, II = 0.000396 m⁴, XMAX = 0.075 m.
        - Índices [15:21]:
            HL = 0.2 m, A = 0.1267849 m², YG = 0.1 m, II = 0.00063 m⁴, XMAX = 0.0725 m.
        - Índices [21:27]:
            HL = 0.21 m, A = 0.135401 m², YG = 0.108 m, II = 0.000734 m⁴, XMAX = 0.08 m.
        - Índices [27:32]:
            HL = 0.26 m, A = 0.1816019 m², YG = 0.129 m, II = 0.00144 m⁴, XMAX = 0.085 m.

        Este método facilita o uso de lajes padronizadas em análises estruturais,
        permitindo fácil acesso e manipulação de suas propriedades.
        """
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

    def initialize_prestressing_forces(self):
        """
        Inicializa os valores das forças de protensão (PA) e áreas de protensão (APL) para os painéis das lajes.

        Este método define:
        - `PA`: Vetor contendo as forças de protensão aplicadas a cada painel das lajes.
        Os valores são negativos, indicando forças de compressão (kN).
        - `APL`: Vetor contendo as áreas totais de protensão associadas a cada painel (m²).

        Os valores definidos para `PA` e `APL` correspondem a diferentes painéis,
        permitindo realizar análises estruturais considerando as condições de protensão

        Detalhes:
        ---------
        - `PA` (kN):
        Forças negativas, representando compressões, variando em magnitude conforme o painel.
        - `APL` (m²):
        Áreas de protensão para cada painel, definidas em correspondência com as forças de protensão.


        Observação:
        - O vetor `PA` possui 32 valores, representando as forças de protensão para 32 painéis.
        - O vetor `APL` possui 32 valores, representando as áreas associadas às forças aplicadas.

        Este método organiza os dados essenciais para cálculos relacionados à protensão,
        permitindo sua integração direta nas análises de engenharia.
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
                0.000444,
                0.000306,
                0.000372,
                0.000532,
                0.000811,
            ]
        )

    def initialize_beam_properties(self):
        """
        Inicializa as propriedades das vigas.

        Este método define os parâmetros relacionados às vigas, incluindo:
        - Quantidade de barras passivas de tração.
        - Áreas das bitolas passivas disponíveis.
        - Quantidade de cabos nas camadas "A" e "B".
        - Características geométricas da viga (altura, base e NMAX).

        Propriedades Definidas:
        -----------------------
        - `NPT` (int): Quantidade de barras passivas de tração.
            Valores disponíveis: [0, 2, 4, 6].
        - `BP` (m²): Áreas das bitolas passivas disponíveis.
            Valores disponíveis correspondem a diâmetros típicos:
            [6mm, 8mm, 10mm, 12.5mm].
        - `NA` (int): Quantidade de cabos na camada "A".
            Valores disponíveis: [3, 5, ..., 23].
        - `NB` (int): Quantidade de cabos na camada "B".
            Valores disponíveis: [0, 2, ..., 14].
        - `HV` (m): Altura das vigas.
            Calculada para cinco valores-base repetidos em seis intervalos, com ajustes finais.
        - `BV` (m): Base das vigas.
            Valores pré-definidos em faixas de 0.40m a 0.90m.
        - `NMAX` (int): Máximo de cabos suportados por camada.
            Valores definidos em faixas, de 13 a 23.

        Observação:
        -----------
        Os vetores `HV`, `BV` e `NMAX` são ajustados para incluir dois valores extras no final,
        replicando valores próximos para garantir a consistência dos dados.
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

    def get_beam_properties(self):
        """
        Retorna as propriedades das vigas em um formato de dicionário.
        """
        return {
            "Barras Passivas de Tração": self.NPT,
            "Bitolas Passivas": self.BP,
            "Cabos Camada A": self.NA,
            "Cabos Camada B": self.NB,
            "Altura Viga": self.HV,
            "Base Viga": self.BV,
            "Máxima Cordoalhas": self.NMAX,
        }

    # ROTINA DE DECODIFICAÇÂO

    def decode(self):
        """
        Realiza a decodificação das variáveis a partir dos valores binários da subpopulação.

        Este método converte os valores binários contidos na subpopulação (`subpop`)
        em parâmetros numéricos utilizados para caracterizar a solução.

        Decodificações:
        ---------------
        - DL: Valor direto (já decodificado).
        - PM, CML, VL: Parâmetros auxiliares, obtidos a partir de combinações binárias.
        - ANPT, ABP, ANA, ANB: Índices para listas específicas, decodificados por pesos binários.
        - NX, NY, VV: Variáveis dependentes calculadas com base nas funções auxiliares.
        - NA, NB: Ajustados para respeitar restrições geométricas.
        - Penalidades: Aplicadas para evitar configurações inválidas.

        Observação:
        -----------
        As funções auxiliares `calculate_nx`, `calculate_ny`, e `calculate_vv` são chamadas
        para determinar valores específicos.
        """
        self.DL = self.subpop[0]  # Já é o próprio valor

        self.PM = int(2 * self.subpop[1] + self.subpop[2])  # Auxiliar
        self.CML = int(2 * self.subpop[3] + self.subpop[4])  # Auxiliar

        self.VL = int(
            +16 * self.subpop[5]
            + 8 * self.subpop[6]
            + 4 * self.subpop[7]
            + 2 * self.subpop[8]
            + 1 * self.subpop[9]
        )  # Auxiliar

        self.ANPT = int(2 * self.subpop[10] + 1 * self.subpop[11])  # Auxiliar Lista NPT
        self.ABP = int(
            2 * self.subpop[12] + 1 * self.subpop[13]
        )  # Auxiliar p a lista BP
        self.ANA = int(
            8 * self.subpop[14]
            + 4 * self.subpop[15]
            + 2 * self.subpop[16]
            + 1 * self.subpop[17]
        )  # Auxiliar
        self.ANB = int(
            4 * self.subpop[18] + 2 * self.subpop[19] + 1 * self.subpop[20]
        )  # Auxiliar

        # NX decodificação
        self.NX = self.calculate_nx()
        # NY decodificação
        self.NY = self.calculate_ny()
        # VV decodificação
        VV = self.calculate_vv()

        # Redução do domínio da base
        self.VV = int(self.reduce_domain(VV))

        # Ajuste do NA para não ultrapassar o NMAX
        if self.NA[self.ANA] > self.NMAX[self.VV]:
            self.NA[self.ANA] = self.NMAX[self.VV]

        # Morfogênese (NA x NB)
        if self.NB[self.ANB] > self.NA[self.ANA]:
            self.NB[self.ANB], self.NA[self.ANA] = self.NA[self.ANA], self.NB[self.ANB]

        # Penalizar o vao minimo
        AJX = self.LX / self.dminx
        AJY = self.LY / self.dminy
        if self.NX > AJX:
            self.NX *= 100
        if self.NY > AJY:
            self.NY *= 100

    def calculate_nx(self):
        """
        Calcula o valor de NX com base nos bits da subpopulação.

        NX é determinado pela combinação binária dos bits subsequentes,
        a partir de 20 + 1 até 20 + self.nxmax.
        """
        NX = 0
        for i in range(1, self.nxmax + 1):
            NX += self.subpop[20 + i] * (2 ** (self.nxmax - i))
        return NX + 1

    def calculate_ny(self):
        """
        Calcula o valor de NY com base nos bits da subpopulação.

        NY é calculado similarmente ao NX, mas com deslocamento após NX.
        """
        NY = 0
        for i in range(1, self.nymax + 1):

            NY += self.subpop[20 + self.nxmax + i] * (2 ** (self.nymax - i))
        return NY + 1

    def calculate_vv(self):
        """
        Calcula o valor de VV com base nos bits da subpopulação.

        VV é calculado após os bits utilizados para NX e NY.
        """
        VV = 0
        for i in range(1, self.nvv + 1):
            VV += self.subpop[20 + self.nxmax + self.nymax + i] * (2 ** (self.nvv - i))
        return VV

    def reduce_domain(self, VV):
        """
        Reduz o domínio do valor de VV com base nas regras do domínio bmax.

        O ajuste é feito de acordo com a base máxima (bmax), garantindo
        que o valor de VV permaneça dentro de limites aceitáveis para cada faixa de bmax.
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

    def display_results(self):
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
        print(f"ANPT: {2 * self.subpop[10] + 1 * self.subpop[11] + 1}")
        print(f"ABP: {2 * self.subpop[12] + 1 * self.subpop[13] + 1}")

    def calculate_spans(self):
        """
        Calcula os vãos corrigidos com base em NX, NY e a direção da carga.

        Este método utiliza as divisões do eixo X (NX) e do eixo Y (NY),
        bem como o fator de distribuição de carga (DL), para calcular os
        vãos da laje em duas direções e aplicar uma correção com base na base
        da viga correspondente (BV).

        Retorna:
            tuple: Contém os seguintes valores:
                - LLJ (float): Vão da laje na direção principal.
                - LLV (float): Vão da laje na direção secundária.
                - LLJC (float): Vão corrigido da laje na direção principal.
        """
        LLJ = (self.LX / self.NX) * (1 - self.DL) + (self.LY / self.NY) * self.DL  # (m)
        LLV = (self.LX / self.NX) * self.DL + (self.LY / self.NY) * (1 - self.DL)  # (m)

        LLJC = LLJ - self.BV[self.VV]  # Supondo que BV é um array ou lista

        return LLJ, LLV, LLJC

    # LAJES ALVEOLARES

    def hollow_slab(self):
        """
        Realiza os cálculos principais para a análise de uma laje nervurada.

        Este método executa uma sequência de cálculos organizados em etapas, desde a
        definição de propriedades geométricas e materiais até as verificações de tensões
        e deslocamentos, respeitando os estados limites de serviço (ELS) e últimos (ELU).
        """
        # Etapa 1: Cálculo das propriedades da laje
        self.M, self.AC, self.YGC, self.IC = self.calculate_hollow_slab_properties()

        # Etapa 2: Determinação dos módulos de excentricidade
        (
            self.EP,
            self.EPC,
            self.WINF,
            self.WSUP,
            self.WCINF,
            self.WCSUP,
        ) = self.calculate_excentricity_modulus()

        # Etapa 3: Cálculo dos carregamentos aplicados na laje
        self.loads = self.calculate_slab_loads()

        # Etapa 4: Momentos fletores e esforços cortantes
        self.ML, self.RL, self.MLD, self.VLD = self.calculate_moments_and_stresses()

        # Etapa 5: Tensões na fase de concretagem
        self.TINF, self.TSUP = self.calculate_stresses_concreting_phase()

        # Etapa 6: Tensões após a concretagem
        self.TCINF, self.TCSUP = self.calculate_stresses_after_concreting()

        # Etapa 7: Perda de protensão após a transferência
        self.PT = self.calculate_prestress_after_transfer()

        # Etapa 8: Perda de protensão ao longo do tempo
        self.PINF = self.calculate_infinite_time_prestress()

        # Etapa 9: Tensões devido à protensão
        (
            self.TINPT,
            self.TSUPT,
            self.TINPI,
            self.TSUPI,
        ) = self.calculate_stresses_due_to_prestress()

        # Etapa 10: Tensões nos vazios
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

        # Etapa 11: Limites de tensões
        self.LCJ, self.LTJ, self.LCK, self.LTK = self.calculate_stress_limits()

        # Etapa 12: Tensões para verificação do ELS
        self.DES, self.FF = self.calculate_els_stresses_slab()

        # Etapa 13: Solicitações para o ELU
        self.XL, self.DDL, self.MRESL = self.calculate_elu_solicitations()

        # Etapa 14: Flechas na laje
        self.CFI, self.CFT = self.calculate_deflection_slab()

        # Etapa 15: Flechas devido ao carregamento
        self.fi, self.ft = self.calculate_deflection_loading()

    def calculate_hollow_slab_properties(self):
        """
        Calcula as propriedades da seção da laje composta (Laje).

        Retorna:
            M (float): Momento de inércia da seção.
            AC (float): Área equivalente da laje.
            YGC (float): Distância do centroide da seção composta.
            IC (float): Momento de inércia total da seção composta.
        """
        M = (self.FCKML[self.CML] / self.FCKPM[self.PM]) ** 0.5
        AC = M * 1.2 * 0.05
        YGC = (
            +self.A[self.VL] * self.YG[self.VL] + AC * (self.HL[self.VL] + 0.025)
        ) / (self.A[self.VL] + AC)

        IC = (
            self.II[self.VL]
            + self.A[self.VL] * ((YGC - self.YG[self.VL]) ** 2)
            + (M * 1.2 * (0.05**3)) / 12
            + AC * (self.HL[self.VL] + 0.025 - YGC) ** 2
        )
        return M, AC, YGC, IC

    def calculate_excentricity_modulus(self):
        """
        Calcula as excentricidades e os módulos resistentes das lajes.

        Parâmetros:
        YGC (float): Centro de gravidade da seção composta.
        IC (float): Momento de inércia da seção composta.
        """
        EP = self.YG[self.VL] - 0.012 - 0.006  # Section isolated, adopted CL = 1.2 cm
        EPC = self.YGC - 0.012 - 0.006  # Composite section

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
        MLD = (1.3 * ML[0] + 1.4 * np.sum(ML[1:])) / 100  # Design moment in MN.m
        VLD = (1.3 * RL[0] + 1.4 * np.sum(RL[1:])) / 100  # Design shear force in MN

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
        TINPT = (self.PT / self.A[self.VL]) + self.PT * (self.EP / self.WINF)  # MPa
        TSUPT = (self.PT / self.A[self.VL]) + self.PT * (self.EP / self.WSUP)  # MPa
        TINPI = (self.PINF / self.A[self.VL]) + self.PINF * (self.EP / self.WINF)  # MPa
        TSUPI = (self.PINF / self.A[self.VL]) + self.PINF * (self.EP / self.WSUP)  # MPa
        return TINPT, TSUPT, TINPI, TSUPI

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

    def calculate_hollow_slab_penalties(self):
        # Restrições
        GL = np.zeros(17)
        # Verificar restrições de tensões, compressões e fissuras
        GL[0] = 0 if abs(self.TDESI) <= self.LCJ else abs(self.TDESI / self.LCJ) - 1
        GL[1] = 0 if abs(self.TTI) <= self.LCJ else abs(self.TTI / self.LCJ) - 1
        GL[2] = 0 if abs(self.TTII) <= self.LCJ else abs(self.TTII / self.LCJ) - 1
        GL[3] = 0 if abs(self.TMI) <= self.LCJ else abs(self.TMI / self.LCJ) - 1
        GL[4] = (
            0 if self.TDESS <= 2 * self.LTJ else abs(self.TDESS / (2 * self.LTJ)) - 1
        )
        GL[5] = (
            0
            if self.TTS <= (0.7 * self.FCKPM[self.PM]) ** 0.5
            else abs(self.TTS / ((0.7 * self.FCKPM[self.PM]) ** 0.5)) - 1
        )
        GL[6] = 0 if self.TTSS <= 2 * self.LTJ else abs(self.TTSS / (2 * self.LTJ)) - 1
        GL[7] = 0 if self.TMS <= 2 * self.LTJ else abs(self.TMS / (2 * self.LTJ)) - 1
        GL[8] = 0 if self.DES <= 0 else self.DES
        GL[9] = 0 if self.FF <= 2 * self.LTK else (self.FF / (2 * self.LTK)) - 1
        GL[10] = (
            0 if self.XL <= self.XMAX[self.VL] else (self.XL / self.XMAX[self.VL]) - 1
        )

        # Verificar momento resistido e Beta X
        GL[11] = 0 if self.MRESL >= self.MLD else (self.MLD / self.MRESL) - 1
        bxl = self.XL / self.DDL
        GL[12] = 0 if bxl >= 0 else abs(bxl)
        GL[13] = 0 if bxl <= 0.6 else (bxl / 0.6) - 1

        # Verificar relação vão/altura da laje
        GL[14] = (
            0
            if self.LLJ >= (self.dminx * (1 - self.DL) + self.dminy * self.DL)
            else ((self.dminx * (1 - self.DL) + self.dminy * self.DL) / self.LLJ) - 1
        )

        # Verificar flechas (ELU)
        GL[15] = (
            0
            if (self.ft + self.CFT) <= (1.05 * self.LLJ / 250)
            else (self.ft + self.CFT) / (1.05 * self.LLJ / 250) - 1
        )

        # Verificar restrição de relação vão/altura da laje
        GL[16] = (
            0
            if (self.LLJ / (self.HL[self.VL] + 0.05)) <= 45
            else ((self.LLJ / (self.HL[self.VL] + 0.05)) / 45) - 1
        )
        self.GL = GL
        # Somatório das penalidades
        PENL = np.sum(GL)
        return PENL

    # NOVA CLASSE

    def inverted_t_beam(self):
        # Constantes pré-calculadas
        self.pp_concrete = 2.5  # Peso específico do concreto tf/m³

        # Propriedades geométricas
        self.AV = self.calculate_area_isolated_beam()
        self.PPV = self.calcuate_ppv()
        self.PPVC = self.calculate_ppvc()
        self.YGV, self.IV = self.calculate_inertia_isolated_beam()
        self.AVC, self.YGCV, self.IVC = self.calculate_composite_section_properties()
        self.EPA, self.EPCA, self.EPB, self.EPCB = self.calculate_layer_eccentricity()
        self.WVI, self.WVS, self.WCVI, self.WCVS = self.calculate_resistant_modulus()
        self.MVT, self.TVI, self.TVS, self.MVPP, self.TVPPI, self.TVPPS = (
            self.calculate_moments_and_stresses_assembly_phase()
        )
        self.SP, self.LP = self.calculate_pillar_reactions()
        self.MVG, self.MVQ, self.TVGI, self.TVQ, self.MVD = (
            self.calculate_moments_and_stresses_useful_life()
        )
        (
            self.PAV,
            self.PAT,
            self.SPTV,
            self.VTINPT,
            self.VTSUPT,
            self.VPINF,
            self.VTINPI,
            self.VTSUPI,
        ) = self.calculate_prestress_forces_and_stresses()
        self.LTJV, self.LTKV = self.calculate_limit_stresses()
        self.DESCOMPV, self.FFISSV = self.calculate_els_stresses()
        (
            self.TDIV,
            self.TDSV,
            self.TTIV,
            self.TTIIV,
            self.TTSV,
            self.TTSSV,
            self.TMIV,
            self.TMSV,
        ) = self.calculate_transient_stresses()
        self.adjust_stresses_due_to_prestressing()
        self.HT, self.DA, self.DB, self.XV, self.MRESV = (
            self.calculate_ultimate_limit_state()
        )
        self.CFTV, self.FTV = self.calculate_beam_deflection()
        self.calculate_restrictions()
        self.PENTOTAL = self.calculate_total_penalty()
        self.QDV, self.QDL, self.QDP = self.count_elements()

    def calculate_area_isolated_beam(self):
        """
        Calcula a área da seção transversal da viga isolada.

        Returns:
            float: Área da seção transversal da viga isolada.
        """
        return (self.BV[self.VV] + 0.3) * self.HV[self.VV] + self.BV[self.VV] * (
            self.HL[self.VL] - 0.05
        )

    def calcuate_ppv(self):
        """
        Calcula o peso próprio da viga isolada.

        Returns:
            float: Peso próprio da viga (tf/m).
        """
        return self.AV * self.pp_concrete

    def calculate_inertia_isolated_beam(self):
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

    def calculate_composite_section_properties(self):
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

    def calculate_ppvc(self):
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
        wvs = self.IV / (self.YGV - (self.HV[self.VV] + self.HL[self.VL] - 0.05))

        wcvi = self.IVC / self.YGCV
        wcvs = self.IVC / (self.YGCV - (self.HV[self.VV] + self.HL[self.VL] + 0.05))

        return wvi, wvs, wcvi, wcvs

    def calculate_moments_and_stresses_assembly_phase(self):
        """
        Calculate the moments and stresses in the assembly phase for a slab structure.

        :return: Tuple containing:
            - MVT (float): Transient moment during assembly phase
            - TVI (float): Stress at the isolated section (bottom)
            - TVS (float): Stress at the isolated section (top)
            - MVPP (float): Moment due to self-weight of the beam
            - TVPPI (float): Stress from self-weight at the isolated section (bottom)
            - TVPPS (float): Stress from self-weight at the isolated section (top)
        """
        # Calculate the transient moment (MVT)
        mvt = (((self.RL[0] + self.RL[1]) / 1.2) * 2 + self.PPV) * (self.LLV**2) / 8

        # Calculate stresses in the isolated section (TVI and TVS)
        tvi = mvt / (100 * self.WVI)
        tvs = mvt / (100 * self.WVS)

        # Calculate the moment due to the self-weight of the beam (MVPP)
        mvpp = (self.PPV * (self.LLV**2)) / 8

        # Calculate stresses due to the self-weight of the beam (TVPPI and TVPPS)
        tvppi = mvpp / (100 * self.WVI)
        tvpps = mvpp / (100 * self.WVS)

        return mvt, tvi, tvs, mvpp, tvppi, tvpps

    def calculate_pillar_reactions(self):
        """
        Calculate the reaction force on a pillar and determine the required steel area and lap length.

        :return: Tuple containing:
            - SP (float): Steel area required for the pillar
            - LP (float): Lap length based on the reaction force
        """
        # Calculate the reaction force on the pillar (RPILAR)
        rpilar = (
            ((np.sum(self.RL[:5]) * (2 / 1.2)) + self.PPV)
            * self.LLV
            * self.numpav
            * 1.02
        )

        # Determine the steel area (SP) and lap length (LP) based on the reaction force
        if rpilar <= 380:
            sp = 0.16
            lp = 0.4
        elif rpilar <= 600:
            sp = 0.25
            lp = 0.5
        else:
            sp = 0.36
            lp = 0.6

        return sp, lp

    def calculate_moments_and_stresses_useful_life(self):
        """
        Calculate moments and stresses for the slab during its useful life, based on permanent and live loads.

        :return: Tuple containing:
            - MVG (float): Moment due to permanent loads, revenues, and walls on the slab
            - MVQ (float): Moment due to live load on the slab
            - TVGI (float): Stress due to permanent loads, revenues, and walls on the slab
            - TVQ (float): Stress due to live load on the slab
            - MVD (float): Design moment for the slab
        """
        # Moment due to permanent loads plus revenues and walls on the slab (MVG)
        mvg = ((self.RL[2] + self.RL[3]) / 1.2) * 2 * (self.LLV**2) / 16

        # Moment due to live load on the slab (MVQ)
        mvq = (self.RL[4] / 1.2) * 2 * (self.LLV**2) / 16

        # Stress due to permanent loads plus revenues and walls on the slab (TVGI)
        tvgi = mvg / (self.WCVI * 100)

        # Stress due to live load on the slab (TVQ)
        tvq = mvq / (self.WCVI * 100)

        # Design moment (MVD), combining various loads
        mvd = (
            (
                (
                    1.3 * self.RL[0]
                    + 1.4 * self.RL[1]
                    + 1.4 * (self.RL[2] / 2)
                    + 1.4 * (self.RL[3] / 2)
                    + 1.4 * (self.RL[4] / 2)
                )
                * (2 / 1.2)
                + 1.3 * self.PPV
            )
            * ((self.LLV - self.LP) ** 2)
            / 8
        ) / 100

        return mvg, mvq, tvgi, tvq, mvd

    def calculate_prestress_forces_and_stresses(self):
        """
        Calculate prestress forces and stresses for the slab, including initial prestress force,
        stresses after transfer, and stresses at infinite time.

        :return: Tuple containing:
            - PAV (float): Initial prestress force
            - PAT (float): Prestress force after transfer
            - SPTV (float): Stress after transfer
            - VTINPT (float): Stress at bottom fiber after transfer
            - VTSUPT (float): Stress at top fiber after transfer
            - VPINF (float): Prestress force at infinite time
            - VTINPI (float): Stress at bottom fiber at infinite time
            - VTSUPI (float): Stress at top fiber at infinite time
        """
        # Calculate the initial prestress force (PAV)
        pav = -0.97 * (self.NA[self.ANA] + self.NB[self.ANB]) * 0.0001014 * 1453

        # Calculate the sum of prestress forces (SOMA)
        soma = (
            (self.NA[self.ANA] * self.EPA + self.NB[self.ANB] * self.EPB)
            * 0.97
            * 0.0001014
            * 1453
            * -1
        )

        # Calculate the sum of squared prestress forces (SOMA2)
        soma2 = (
            (self.NA[self.ANA] * (self.EPA**2) + self.NB[self.ANB] * (self.EPB**2))
            * 0.97
            * 0.0001014
            * 1453
            * -1
        )

        # Calculate the stress after transfer (SPTV)
        sptv = -1 * ((pav / self.AV) + (soma / self.WVI)) + (
            (40.966 / (self.FCKPM[self.PM] ** 0.5))
            * ((pav / self.AV) + (soma2 / self.IV))
        )

        # Calculate the prestress force after transfer (PAT)
        pat = pav - (self.NA[self.ANA] + self.NB[self.ANB]) * 0.0001014 * sptv

        # Calculate the sum of prestress forces after transfer (SOMA3)
        soma3 = pat * (
            self.NA[self.ANA] * self.EPA / (self.NA[self.ANA] + self.NB[self.ANB])
        ) + pat * (
            self.NB[self.ANB] * self.EPB / (self.NA[self.ANA] + self.NB[self.ANB])
        )

        # Calculate stresses at the bottom and top fibers after transfer (VTINPT, VTSUPT)
        vtinpt = (pat / self.AV) + (soma3 / self.WVI)
        vtsupt = (pat / self.AV) + (soma3 / self.WVS)

        # Calculate the prestress force at infinite time (VPINF), assuming a 20% loss
        vpinf = 0.8 * pav

        # Calculate stresses at the bottom and top fibers at infinite time (VTINPI, VTSUPI)
        vtinpi = (vpinf / self.AV) + (0.8 * soma / self.WVI)
        vtsupi = (vpinf / self.AV) + (0.8 * soma / self.WVS)

        return pav, pat, sptv, vtinpt, vtsupt, vpinf, vtinpi, vtsupi

    def calculate_limit_stresses(self):
        """
        Calculate the limit tensile stresses for the slab in both transient and service life conditions.

        :return: Tuple containing:
            - LTJV (float): Limit tensile stress for transient conditions
            - LTkV (float): Limit tensile stress for service life conditions
        """
        # Limit tensile stress for transient conditions (LTJV)
        ltjv = 1.5 * 0.7 * 0.3 * ((0.7 * self.FCKPM[self.PM]) ** (2 / 3))

        # Limit tensile stress for service life conditions (LTkV)
        ltkv = 1.5 * 0.7 * 0.3 * (self.FCKPM[self.PM] ** (2 / 3))

        return ltjv, ltkv

    def calculate_els_stresses(self):
        """
        Calculate decompression stresses for the slab in the Serviceability Limit State (ELS).

        :return: Tuple containing:
            - DESCOMPV (float): Decompression stress at the bottom fiber
            - FFISSV (float): Decompression stress at the top fiber
        """
        # Decompression stress at the bottom fiber (DESCOMPV)
        descompv = self.TVI + self.TVGI + 0.3 * self.TVQ + self.VTINPI

        # Decompression stress at the top fiber (FFISSV)
        ffissv = self.TVI + self.TVGI + 0.4 * self.TVQ + self.VTINPI

        return descompv, ffissv

    def calculate_transient_stresses(self):
        """
        Calculate transient stresses in the slab at various construction phases: demolding, transport, and assembly.

        :return: Tuple containing:
            - TDIV (float): Stress at the bottom fiber during demolding
            - TDSV (float): Stress at the top fiber during demolding
            - TTIV (float): Stress at the bottom fiber during initial transport phase
            - TTIIV (float): Stress at the bottom fiber during intermediate transport phase
            - TTSV (float): Stress at the top fiber during initial transport phase
            - TTSSV (float): Stress at the top fiber during intermediate transport phase
            - TMIV (float): Stress at the bottom fiber during assembly phase
            - TMSV (float): Stress at the top fiber during assembly phase
        """
        # Demolding stresses at the bottom and top fibers
        tdiv = self.VTINPT + self.TVPPI  # Bottom fiber
        tdsv = self.VTSUPT + self.TVPPS  # Top fiber

        # Transport stresses at the bottom fiber (initial and intermediate phases)
        ttiv = self.VTINPT + 0.8 * self.TVPPI  # Initial transport
        ttiiv = self.VTINPT + 1.3 * self.TVPPI  # Intermediate transport

        # Transport stresses at the top fiber (initial and intermediate phases)
        ttsv = self.VTSUPT + 0.8 * self.TVPPS  # Initial transport
        ttssv = self.VTSUPT + 1.3 * self.TVPPS  # Intermediate transport

        # Assembly stresses at the bottom and top fibers
        tmiv = self.VTINPI + self.TVI  # Bottom fiber
        tmsv = self.VTSUPI + self.TVS  # Top fiber

        return tdiv, tdsv, ttiv, ttiiv, ttsv, ttssv, tmiv, tmsv

    def adjust_stresses_due_to_prestressing(self):
        """
        Adjust stresses at specific points in the slab due to prestressing effects.

        :return: Tuple containing:
            - EPCV (float): Eccentricity at the bottom fiber of the slab section
            - EPCCV (float): Eccentricity at the composite section's bottom fiber
        """
        # Define the initial prestress adjustment factor (PATS)
        pats = 0.85 * (-0.5716)

        # Calculate eccentricities at the bottom fiber of slab (EPCV) and composite section (EPCCV)
        epcv = self.YGV - (self.HV[self.VV] - 0.05)
        epccv = self.YGCV - (self.HV[self.VV] - 0.05)

        # Calculate the adjusted prestress for the top fiber (PROTSUP)
        protsup = (pats / self.AV) + (pats * epcv / self.WVS)

        # Update stresses at critical points if they exceed twice the tensile limit (2 * LTJV)
        if self.TTSV > (2 * self.LTJV):
            self.TTSV += protsup

        if self.TMSV > (2 * self.LTJV):
            self.TMSV += protsup

        if self.TDSV > (2 * self.LTJV):
            self.TDSV += protsup

        return epcv, epccv

    def calculate_ultimate_limit_state(self):
        """
        Calculate the Ultimate Limit State for the slab section.

        :return: Tuple containing:
            - HT (float): Total height of the floor for the current index VV
            - DA (float): Lever arm for area A
            - DB (float): Lever arm for area B
            - XV (float): Neutral axis location
            - MRESV (float): Resisting moment of the section
        """
        # Total floor height (HT) for the index VV
        ht = self.HV[self.VV] + self.HL[self.VL] + 0.05

        # Lever arms for areas A and B
        da = ht - 0.05
        db = ht - 0.10

        # Calculation of areas APA and APB
        apa = self.NA[self.ANA] * 0.0001014
        apb = self.NB[self.ANB] * 0.0001014

        # Non-prestressed steel area (AS)
        as_ = self.NPT[self.ANPT] * self.BP[self.ABP]

        # Calculate the neutral axis (XV)
        xv = (1486.9 * (apa + apb) + 434.8 * as_) / (
            0.4857 * self.FCKPM[self.PM] * self.BV[self.VV]
        )

        # Calculate the lever arms for APA and APB (ZA and ZB)
        za = ht - 0.05 - 0.4 * xv
        zb = za - 0.05

        # Resisting moment of the section (MRESV)
        mresv = 1486.9 * (apa * za + apb * zb)

        return ht, da, db, xv, mresv

    def calculate_beam_deflection(self):
        """
        Calculates the initial camber and total deflection for beams.

        Returns:
            tuple: CFTV (initial camber) and FTV (total deflection).

        Variables:
            - CFIV: Initial camber countermeasure, calculated using the prestress force, eccentricity,
                    span length, and concrete strength.
            - CFTV: Total camber countermeasure, estimated as 2.5 times CFIV.

            - FIV: Initial deflection under load, calculated using the weighted sum of reactions, self-weight,
                span length, and concrete properties.
            - FTV: Total deflection during service, estimated as 2.5 times FIV.
        """
        CFIV = (self.PAT * self.EPA * self.LLV) / (
            8 * 4760 * self.FCKPM[self.PM] ** 0.5 * self.IV
        )
        CFTV = CFIV * 2.5

        # Weighted sum of reactions for FIV calculation
        summed_reactions = np.sum(self.RL[:4]) + 0.3 * self.RL[4]

        # Calculate FIV
        FIV = (3 * ((summed_reactions * (2 / 1.2)) + self.PPV) * (self.LLV**4)) / (
            100 * 384 * 4760 * self.FCKPM[self.PM] ** 0.5 * self.IVC
        )

        # Calculate FTV
        FTV = FIV * 2.5
        return CFTV, FTV

    def calculate_restrictions(self):
        """
        Calculates the various restrictions based on the structural conditions and updates the GV array.

        The function checks several conditions and updates the GV array based on these checks:
        1. Verifies whether the stresses during different phases (e.g., TDIV, TTIV, TTIIV) are within the limits.
        2. Checks the decompression stress (DESCOMPV) and formation of cracks (FFISSV).
        3. Assesses the ultimate limit state (MRESV) and checks if the bending ratio (BXV) is within limits.
        4. Verifies the geometry parameters such as the maximum steel area (NA, NB) and beam dimensions (HT, BV, LLV).
        5. Checks the cable distribution between layers A and B.
        6. Verifies deflection limits based on the beam span.

        Updates the GV array with restriction values for each condition. A value of 0 means no restriction, and values greater than 0 indicate a violation of the limit.

        Returns:
            None: The GV array is updated in place with restriction values.
        """
        # Verification and calculation for different stress conditions
        self.GV[0] = 0 if abs(self.TDIV) <= self.LCJ else abs(self.TDIV / self.LCJ) - 1
        self.GV[1] = 0 if abs(self.TTIV) <= self.LCJ else abs(self.TTIV / self.LCJ) - 1
        self.GV[2] = (
            0 if abs(self.TTIIV) <= self.LCJ else abs(self.TTIIV / self.LCJ) - 1
        )
        self.GV[3] = 0 if abs(self.TMIV) <= self.LCJ else abs(self.TMIV / self.LCJ) - 1

        # Limite de resistência para tensões
        limit = (0.7 * self.FCKPM[self.PM]) ** 0.5

        # Verificação para tensões de serviço
        self.GV[4] = 0 if self.TDSV <= limit else abs(self.TDSV / limit) - 1
        self.GV[5] = 0 if self.TTSV <= limit else abs(self.TTSV / limit) - 1
        self.GV[6] = 0 if self.TTSSV <= limit else abs(self.TTSSV / limit) - 1
        self.GV[7] = 0 if self.TMSV <= limit else abs(self.TMSV / limit) - 1

        # Verificação de decompression (descompressão)
        self.GV[8] = 0 if self.DESCOMPV <= 0.05 else (self.DESCOMPV / 0.05) - 1

        # Verificação para fissuração
        self.GV[9] = (
            0 if self.FFISSV <= (2 * self.LTKV) else (self.FFISSV / (2 * self.LTKV)) - 1
        )

        # Verificação para o estado limite último (ELU) e beta X
        if self.MRESV >= (0.98 * self.MVD):
            self.GV[10] = 0
        elif self.MRESV <= 0:
            self.GV[10] = 1 - (self.MRESV / (0.98 * self.MVD))
        else:
            self.GV[10] = abs((0.98 * self.MVD) / self.MRESV) - 1

        # Cálculo de Beta X viga
        BXV = self.XV / self.DA
        self.GV[11] = 0 if BXV > 0 else abs(BXV)
        self.GV[12] = 0 if BXV <= (1.02 * 0.6) else (BXV / (1.02 * 0.6)) - 1

        # Verificação de dimensões geométricas
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
            else (100 * self.BV[self.VV] / self.bmax) - 1
        )
        self.GV[17] = (
            0
            if self.LLV >= (self.dminx * self.DL + self.dminy * (1 - self.DL))
            else (self.dminx * self.DL + self.dminy * (1 - self.DL)) / self.LLV - 1
        )

        # Verificação da quantidade de cabos entre camadas A e B
        self.GV[18] = (
            0
            if self.NA[self.ANA] >= self.NB[self.ANB]
            else (self.NB[self.ANB] / self.NA[self.ANA]) - 1
        )

        # Verificação das flechas
        self.GV[19] = (
            0
            if (self.CFTV + self.FTV) <= (1.05 * self.LLV / 250)
            else (self.CFTV + self.FTV) / (1.05 * self.LLV / 250) - 1
        )

    def calculate_beam_penalty(self):
        """
        Calculates the beam penalty (PENV).

        This function sums the restriction values (GV) from index 0 to 18 to compute the beam penalty.

        Returns:
            float: The beam penalty value (PENV).
        """
        PENV = np.sum(self.GV)  # Sum of the first 19 restriction values
        return PENV

    def calculate_total_penalty(self):
        """
        Calculates the total penalty (PENTOTAL).

        This function uses the penalty factor (PENL) and the beam penalty (PENV) to calculate the total penalty value.
        The formula used is:

        PENTOTAL = 1 + 15 * (PENL + PENV)

        Returns:
            float: The total penalty value (PENTOTAL).
        """
        PENV = self.calculate_beam_penalty()  # Reuse the beam penalty calculation
        PENL = (
            self.calculate_hollow_slab_penalties()
        )  # Reuse the hollow slab penalty calculation

        PENTOTAL = 1 + 15 * (PENL + PENV)  # Total penalty calculation
        return PENTOTAL

    def count_elements(self):
        """
        Calculates the number of beams, slabs, and columns per floor.

        The function computes the following quantities:
        - QDV: The number of beams per floor.
        - QDL: The number of slabs per floor.
        - QDP: The number of columns per floor.

        The formulas used are:
        - QDV = Number of beams (based on NX, NY, and DL)
        - QDL = Number of slabs (based on NX, NY, LLV, and DL)
        - QDP = Number of columns (based on NX and NY)

        Returns:
            tuple: A tuple containing:
                - QDV (int): The number of beams per floor.
                - QDL (int): The number of slabs per floor.
                - QDP (int): The number of columns per floor.
        """
        # Calculate number of beams per floor
        QDV = int(
            self.NX * (self.NY + 1) * self.DL + self.NY * (self.NX + 1) * (1 - self.DL)
        )

        # Calculate number of slabs per floor
        QDL = int(
            ((self.NX) * self.LLV / 1.2) * self.NY * self.DL
            + ((self.NY) * self.LLV / 1.2) * self.NX * (1 - self.DL)
        )

        # Calculate number of columns per floor
        QDP = int((self.NX + 1) * (self.NY + 1))

        return QDV, QDL, QDP

        # Custos da Estrutura - NOVA CLASSE

    # Criar Classe

    # CLASSE CUSTOS

    def custo_estrutura(self):
        self.VPMV, self.VPML, self.VML, self.VPMP, self.VAPV, self.VAPL, self.VADV = (
            self.calculate_volumes()
        )
        self.RO = self.calculate_steel_ratio_pillar()
        self.CUSTOCONC, self.CUSTOCONCML = self.calculate_concrete_cost()
        self.CDOP = self.calculate_operational_cost_slabs()
        self.CTT = self.calculate_transportation_costs()
        self.CTMT = self.calculate_assembly_cost()
        (
            self.CUSTOPROT,
            self.CUSTOAD,
            self.CUSTOCIS,
            self.CUSTOPE,
            self.CUSTOLIG,
            self.CUSTONEO,
        ) = self.prestressing_cost()
        (
            self.CUSTOFAB,
            self.CUSTOTAL,
            self.CUSTOTAL_POR_PAVIMENTO,
            self.CUSTOEST,
            self.F,
        ) = self.calculate_total_cost()

    def calculate_volumes(self):
        """
        Calculates the volumes of beams, slabs, pillars, and steel reinforcement.

        The function computes the following volumes:
        - VPMV: The volume of beams.
        - VPML: The volume of slabs.
        - VML: The volume of the beam's cover and additional components.
        - VPMP: The volume of the pillar (with a 1.15 multiplier for the cantilever).
        - VAPV: The volume of prestressing steel in beams.
        - VAPL: The volume of prestressing steel in slabs.
        - VADV: The volume of non-prestressed steel in beams.

        Returns:
            tuple: A tuple containing:
                - VPMV (float): The volume of beams.
                - VPML (float): The volume of slabs.
                - VML (float): The volume of the beam's cover and additional components.
                - VPMP (float): The volume of pillars.
                - VAPV (float): The volume of prestressing steel in beams.
                - VAPL (float): The volume of prestressing steel in slabs.
                - VADV (float): The volume of non-prestressed steel in beams.
        """
        # Volume of beams

        VPMV = (
            (self.BV[self.VV] + 0.3) * self.HV[self.VV]
            + self.BV[self.VV] * (self.HL[self.VL] - 0.05)
        ) * (self.LLV - self.LP)

        # Volume of slabs
        VPML = self.A[self.VL] * (self.LLJ - self.BV[self.VV])

        # Volume of beam cover and additional components
        VML = (self.LX * self.LY - self.QDP * self.SP) * 0.05 + self.BV[
            self.VV
        ] * 0.05 * (self.LLV - self.LP) * self.QDV

        # Volume of pillars (considering 1.15 for cantilever)
        VPMP = self.SP * 3.5 * 1.15

        # Calculation of steel volumes
        VAPV = (
            (self.NA[self.ANA] + self.NB[self.ANB]) * 0.0001014 * (self.LLV - self.LP)
        )  # Volume of prestressing steel in beams
        VAPL = self.APL[self.VL] * (
            self.LLJ - self.BV[self.VV]
        )  # Volume of prestressing steel in slabs
        VADV = (
            self.NPT[self.ANPT] * self.BP[self.ABP] * (self.LLV - self.LP)
        )  # Volume of non-prestressed steel in beams

        return VPMV, VPML, VML, VPMP, VAPV, VAPL, VADV

    def calculate_steel_ratio_pillar(self):
        """
        Calculates the steel ratio for pillars based on the type of material.

        The function calculates the steel ratio (RO) for the pillar based on the value of `PM`.
        - If `PM` is greater than 1, it uses different values for RO depending on whether `PM` is 2, 3, or greater than 3.
        - If `PM` is 1 or less, it sets RO to 150.

        Returns:
            float: The steel ratio (RO) for the pillar based on the material type.
        """
        # Calculation of steel ratio for pillars
        if self.PM > 1:
            if self.PM == 2:
                RO = 120
            elif self.PM == 3:
                RO = 90
            else:
                RO = 60
        else:
            RO = 150

        return RO

    def calculate_concrete_cost(self):
        """
        Calculates the total concrete cost for beams, slabs, and complements.

        The function calculates the concrete cost for beams (CUSTOCONC) and slabs and complements (CUSTOCONCML) based on
        various factors such as the volume of the materials, the cost per material unit (`cpm`), and the number of floors (`numpav`).
        The concrete cost for beams is calculated with a multiplier of 1.5, and for the pillars, it's calculated with a multiplier of 1.5 as well.
        The cost for the complement volume is calculated with a factor of 1.3.

        Returns:
            tuple:
                - CUSTOCONC (float): The total concrete cost for beams, slabs, and pillars.
                - CUSTOCONCML (float): The concrete cost for complements.
        """
        # Concrete cost for beams, slabs, and complements
        CUSTOCONC = (
            (self.VPMV * self.cpm[self.PM] * self.QDV) * 1.5
            + self.VPML * self.cpm[self.PM] * self.QDL
            + (self.VPMP * self.cpm[self.PM] * self.QDP * 1.5)
        ) * self.numpav

        CUSTOCONCML = self.VML * self.ccml[self.CML] * 1.3 * self.numpav

        return CUSTOCONC, CUSTOCONCML

    def calculate_operational_cost_slabs(self):
        """
        Calculates the operational cost for slabs.

        This function calculates the operational cost for slabs (CDOP) based on the slab area (`QDL`), slab length (`LLJ`),
        beam width (`BV`), and a unit cost (`DOP`) that depends on the slab type (below or above a certain threshold of 28).
        The operational cost is adjusted by a factor of 1.2 and the number of floors (`numpav`).

        Returns:
            float: The total operational cost for the slabs (CDOP).
        """
        if self.VL < 28:
            DOP = 24  # Operational cost per unit for slabs with VL less than 28
        else:
            DOP = 36  # Operational cost per unit for slabs with VL 28 or greater

        # Calculating the operational cost for slabs
        CDOP = self.QDL * (self.LLJ - self.BV[self.VV]) * 1.2 * DOP * self.numpav
        return CDOP

    def calculate_transportation_costs(self):
        """
        Calculates the transportation costs for beams, slabs, and pillars.

        This function calculates the transportation cost for beams (CTV), slabs (CTL), and pillars (CTP)
        based on the dimensions of the elements and the number of floors (`numpav`).
        - CTV is based on the difference between `LLV` (length of the beam) and `LP` (width of the beam).
        - CTL is based on the difference between `LLJ` (length of the slab) and the beam width (`BV`).
        - CTP depends on the number of floors.

        The total transportation cost (`CTT`) is the sum of the individual costs for beams, slabs, and pillars,
        adjusted by the number of floors (`numpav`).

        Returns:
            float: The total transportation cost (`CTT`).
        """
        if (self.LLV - self.LP) > 12:
            CTV = 1600  # Transportation cost for beams if length difference exceeds 12
        else:
            CTV = 1000  # Transportation cost for beams if length difference is less than or equal to 12

        if (self.LLJ - self.BV[self.VV]) > 12:
            CTL = 1600  # Transportation cost for slabs if length difference exceeds 12
        else:
            CTL = 1000  # Transportation cost for slabs if length difference is less than or equal to 12

        if self.numpav > 3:
            CTP = 1600  # Transportation cost for pillars if number of floors exceeds 3
        else:
            CTP = 1000  # Transportation cost for pillars if number of floors is less than or equal to 3

        # Calculating the total transportation cost
        CTT = (
            ((self.VPMV * self.QDV * CTV) / 10)
            + ((self.VPML * self.QDL * CTL) / 10)
            + ((self.VPMP * self.QDP * CTP) / 10)
        ) * self.numpav
        return CTT

    def calculate_assembly_cost(self):
        """
        Função para calcular o custo de montagem com base nas fórmulas fornecidas.

        Parâmetros:
        QDV (float): Quantidade de algum valor relacionado a guindaste (por exemplo).
        QDL (float): Quantidade de outro valor (provavelmente relacionada a algum material ou processo).
        QDP (float): Quantidade relacionada a algum processo adicional.
        NUMPAV (int): Número de pavimentos da estrutura.

        Retorna:
        float: O custo total de montagem (CTMT).
        """
        # Calculando CTMV com a fórmula fornecida
        CTMV = np.ceil((self.QDV / 16) + (self.QDL / 24))  # arredondado para cima

        # Calculando CTMP com a fórmula fornecida
        CTMP = (self.QDP / 8) * 1500  # Cálculo do custo de montagem de material

        # Calculando o custo total de montagem (CTMT)
        CTMT = 1500 * CTMV * self.numpav + CTMP

        return CTMT

    def prestressing_cost(self):
        """
        Calcula os custos de protensão, aço passivo, cisalhamento, estribo, ligação e neoprene
        para vigas e pilares, com base em parâmetros como volumes de aço, custos unitários e
        o número de pavimentos.

        Retorna:
            tuple: Uma tupla contendo os seguintes valores:
                - CUSTOPROT: Custo do aço de protensão
                - CUSTOAD: Custo do aço passivo
                - CUSTOCIS: Custo de cisalhamento
                - CUSTOPE: Custo da porta estribo
                - CUSTOLIG: Custo de ligação
                - CUSTONEO: Custo do neoprene
        """
        # Custo do aço de protensão
        CUSTOPROT = (
            (1.085 * self.VAPV * 7810.65 * self.QDV + self.VAPL * 7857 * self.QDL)
            * self.cap
            * self.numpav
        )

        # Custo do aço passivo
        CUSTOAD = (
            self.VADV * 7760 * self.QDV * self.cad
            + self.VPMP * self.RO * self.QDP * self.cad
        ) * self.numpav

        # Custo de cisalhamento
        CUSTOCIS = (
            5.6
            * (((self.BV[self.VV] - 0.05) + (self.HV[self.VV] - 0.05)) * 2 + 0.12)
            * self.BV[self.VV]
            * (self.LLV - self.LP)
            * self.QDV
            * self.cad
            * self.numpav
        )

        # Custo da porta estribo
        CUSTOPE = 0.86912 * (self.LLV - self.LP) * self.QDV * self.numpav * self.cad

        # Custo de ligação
        CUSTOLIG = (
            12.125 * self.QDP * self.numpav * self.cad
        )  # Custo arm ligação 5 12.5mm (C=2,5 m)

        # Custo neoprene
        CUSTONEO = self.QDP * 2 * self.numpav * 22.5  # Custo neoprene R$ 22,50

        return CUSTOPROT, CUSTOAD, CUSTOCIS, CUSTOPE, CUSTOLIG, CUSTONEO

    def calculate_total_cost(self):
        """
        Calculates the total project cost, considering material, operational, and other costs
        such as prestressing steel, shear, neoprene, and connections. This method also adjusts the
        costs to consider only the structure and calculates the cost per floor and the final cost
        multiplied by the total price.

        Returns:
            tuple: A tuple containing the following values:
                - CUSTOFAB: Manufacturing cost of materials (adjusted).
                - CUSTOTAL: Total cost of materials (includes manufacturing, operational costs, and other costs).
                - CUSTOTAL_PER_FLOOR: Total cost per floor.
                - STRUCTURE_COST: Cost considering only the structure, excluding complementary costs.
                - F: Final cost, multiplied by the total price of the structure.
        """
        # Manufacturing cost calculation
        CUSTOFAB = (
            self.CUSTOCONC
            + self.CUSTOPROT
            + self.CUSTOAD
            + self.CDOP
            + self.CUSTOCIS
            + self.CUSTOPE
        ) * 1.33  # Adjusted material costs

        # Total material cost calculation
        CUSTOTAL = (
            CUSTOFAB
            + self.CUSTOCONCML
            + self.CTT
            + self.CTMT
            + self.CUSTONEO
            + self.CUSTOLIG
        )  # Total material cost

        # Adjusted cost to consider only the structure (excluding complementary costs)
        STRUCTURE_COST = CUSTOTAL - self.CUSTOCONCML  # Structure cost (PM)

        # Total cost per floor
        CUSTOTAL_PER_FLOOR = CUSTOTAL / self.numpav  # Cost per floor

        # Final cost calculation multiplied by the total price
        F = (
            CUSTOTAL_PER_FLOOR * self.PENTOTAL
        )  # Final cost multiplied by the total price

        return CUSTOFAB, CUSTOTAL, CUSTOTAL_PER_FLOOR, STRUCTURE_COST, F

    def get_fitness(self):
        return self.F

    def calcular_vtc(self):
        # Cálculo do volume de concreto total
        self.vtc = (
            self.VPMV * self.QDV
            + self.VPML * self.QDL
            + self.VPMP * self.QDP
            + self.VML
        )
        return self.vtc

    def mostrar_resultados(self, arquivo=None):
        """
        Exibe os resultados do cálculo estrutural.
        Se um arquivo for fornecido, grava os resultados no arquivo.

        :param arquivo: Instância de ArquivoSaida para gravação (opcional).
        """
        self.calcular_vtc()

        # Buffer para os resultados
        resultados = []

        # Variáveis de projeto
        resultados.append("--- Variáveis Projeto Indivíduo ---")
        resultados.append(f"NumGen= {self.numgen}")
        resultados.append(f"NX= {self.NX}")
        resultados.append(f"NY= {self.NY}")
        resultados.append(f"DL= {self.DL}")
        resultados.append(f"FCKCML= {self.FCKML[self.CML]}")
        resultados.append(f"FCKCPM= {self.FCKPM[self.PM]}")
        resultados.append(f"HL= {self.HL[self.VL]}")
        resultados.append(f"LLJ= {self.LLJ}")
        resultados.append(f"HV= {self.HV[self.VV]:.2f}")
        resultados.append(f"BV= {self.BV[self.VV]:.2f}")
        resultados.append(f"LLV= {self.LLV}")
        resultados.append(f"NA= {self.NA[self.ANA]}")
        resultados.append(f"NB= {self.NB[self.ANB]}")
        resultados.append(f"NPT= {self.NPT[self.ANPT]}")

        # Custos
        resultados.append(f"Custo Concreto= {self.CUSTOCONC:.2f}")
        resultados.append(f"Volume Concreto= {self.vtc:.2f}")
        resultados.append(f"Custo Protensão= {self.CUSTOPROT:.2f}")
        resultados.append(f"Custo Aço Passivo= {self.CUSTOAD:.2f}")
        resultados.append(f"Custo Transporte= {self.CTT:.2f}")
        resultados.append(f"Custo Montagem= {self.CTMT:.2f}")
        resultados.append(f"Custo Desp Operacional= {self.CDOP:.2f}")
        resultados.append(
            f"Custo %Fabricacao= {(self.CUSTOFAB / self.CUSTOEST) * 100:.2f}%"
        )
        resultados.append(f"Custo %Transporte= {(self.CTT / self.CUSTOEST) * 100:.2f}%")
        resultados.append(f"Custo %Montagem= {(self.CTMT / self.CUSTOEST) * 100:.2f}%")
        resultados.append(f"Custo Total= {self.CUSTOTAL:.2f}")
        resultados.append(f"Pentotal= {self.PENTOTAL:.2f}")
        resultados.append(f"Apt= {self.F:.2f}")
        resultados.append(
            f"Custo Estrutura/m2= {(self.CUSTOEST * 1.33) / (self.LX * self.LY * self.numpav):.2f}"
        )

        # Dados da laje
        resultados.append("--- DADOS DA LAJE INDIVÍDUO ---")
        resultados.append(f"VL= {self.VL}")
        resultados.append(f"flecha (Laje)= {self.fi}")
        resultados.append(f"f-Total (Laje)= {self.ft}")
        resultados.append(f"LP= {self.LP}")

        # Dados da viga
        resultados.append("--- DADOS DA VIGA INDIVÍDUO ---")
        resultados.append(f"VV= {self.VV}")
        resultados.append(f"cf-Total (Viga)= {self.CFTV}")
        resultados.append(f"f-Total (Viga)= {self.FTV}")
        resultados.append(f"qdv= {self.QDV}")
        resultados.append(f"QDP= {self.QDP}")
        resultados.append(f"QDL= {self.QDL}")

        # Escrever no arquivo ou exibir no console
        if arquivo:
            for linha in resultados:
                arquivo.file_handler.write(linha + "\n")
        else:
            for linha in resultados:
                print(linha)

    def calculate_restrictions_final(self):
        # Verificação das restrições
        for i in range(17):
            if self.GL[i] != 0:
                print(f"GL{i}= {self.GL[i]}")

        for i in range(20):
            if self.GV[i] != 0:
                print(f"GV{i}= {self.GV[i]}")


def main():
    # Parâmetros de entrada
    numind = 50
    numgen = 50
    subpop = np.random.randint(0, 2, size=(numind, numgen))  # População de indivíduos
    numpav = 8  # Número de pavimentos
    dminx, dminy = 3.0, 3.0  # Distâncias mínimas em x e y
    lx, ly = 20.0, 15.0  # Dimensões da estrutura
    hmax, bmax = 2.5, 0.3  # Altura e largura máximas
    q = 2.0  # Carga total na estrutura
    gpr, gpl = 1.5, 1.2  # Peso próprio
    ccml = np.array([147, 158, 171, 185])  # Custos por metro cúbico (exemplo)
    cpm = np.array([185, 200, 216, 233])  # Custos por metro linear (exemplo)
    cap, cad = 7, 4  # Capacidades diversas
    nxmax, nymax = 3, 3  # Limites de subdivisões
    nvv = 4  # Parâmetro adicional

    # Instanciando a classe
    evaluation = StructuralEvaluation(
        numpav=numpav,
        dminx=dminx,
        dminy=dminy,
        lx=lx,
        ly=ly,
        hmax=hmax,
        bmax=bmax,
        q=q,
        gpr=gpr,
        gpl=gpl,
        ccml=ccml,
        cpm=cpm,
        cap=cap,
        cad=cad,
        numind=numind,
        nxmax=nxmax,
        nymax=nymax,
        nvv=nvv,
        numgen=numgen,
    )
    evaluation.initialize_individual(subpop[0])

    aptidao = evaluation.get_fitness()
    # print(evaluation.mostrar_resultados())

    # Exibindo os resultados
    print(f"Aptidao: {aptidao}")


# Executa o main se o script for executado diretamente
if __name__ == "__main__":
    main()
