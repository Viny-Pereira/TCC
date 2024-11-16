import numpy as np

class Ag:

  # Variáveis
  # count = atribui à semente dos números aleatórios valor baseado no clock do sistema
  # Seed = semente para a geração de números aleatórios
  # R = número aleatório
  # numind = número de indivíduos da população
  # numgen = PARÂMETRO número de genes do cromossomo ou indivíduo
  # pop = matriz da população corrente
  # subpop = matriz da subpopulação ou população intermediária
  # AllocateStatus = usada pelo programa na alocação de memória (recebe 0 se a alocação tiver sucesso)
  # apt = (real) vetor das aptidões
  # elit = número de indivíduos que participarão do elitismo
  # ger = contador das gerações
  # maxger = número máximo de gerações
  # cruz = taxa de cruzamento
  # pmut = taxa de mutação
  # mut = matriz da mutação
  # rank = matriz dos indivíduos que participarão do cruzamento
  # subrank = matriz dos filhos resultantes do cruzamento
  # aptger = vetor contendo a melhor aptidão de cada de gerações
  # med = aptidão média de cada geração
  # aptmed = vetor com a aptidão média de cada geração

  def __init__(self) -> None:
    # Vãos e limites geométricos das peças
    dminx, dminy, lx, ly, hmax, bmax = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    # Fatores de ajuste
    AJX, AJY = 0.0, 0.0

    # Números máximos de pavimentos e vãos
    NXMAX, NYMAX, NVV = 0, 0, 0

    # Cargas
    q, gpr, gpl = 0.0, 0.0, 0.0

    # Modulações em X e Y
    mx, my = 0.0, 0.0

    # Custos do concreto por Fck em R$/m³
    cpm = np.zeros(4)
    ccml = np.zeros(4)

    # Custos do aço de protensão e passivo em R$/kg
    cap, cad = 0.0, 0.0

    # Número de pavimentos do prédio
    NUMPAV = 0

    # Variáveis para controle e cálculos
    R, F, pmut, med = 0.0, 0.0, 0.0, 0.0

    # Vetores e matrizes
    apt = None  # Vetor de aptidões
    subapt = None  # Vetor de aptidões da subpopulação
    aptger = None  # Vetor contendo a melhor aptidão de cada geração
    aptmed = None  # Vetor com a aptidão média de cada geração
    pop = None  # Matriz da população corrente
    subpop = None  # Matriz da subpopulação ou população intermediária
    rank = None  # Matriz dos indivíduos que participarão do cruzamento
    subrank = None  # Matriz dos filhos resultantes do cruzamento
    mut = None  # Matriz da mutação

    # Contadores e parâmetros
    count, numind, numgen, AllocateStatus = 0, 0, 0, 0
    i, j, k, elit, ger, maxger, cruz = 0, 0, 0, 0, 0, 0, 0
    indou, selcruz, teste = 0, 2, 0

    # Semente para a geração de números aleatórios
    Seed = np.zeros(1)

    # Arquivos de entrada e saída
    arqou, arqout = '', ''

