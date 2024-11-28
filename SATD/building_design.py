import numpy as np


class BuildingDesignParameters:
    """
    Class to calculate and store building design parameters based on user-provided inputs.

    The class also includes fixed costs for materials like concrete and steel
    to be used in structural cost calculations.

    Attributes:
        CONCRETE_COSTS_CCML (np.ndarray): Array containing the cost of concrete for CCML type.
        CONCRETE_COSTS_CPM (np.ndarray): Array containing the cost of concrete for CPM type.
        STEEL_COST_PRESTRESSED (float): Cost of prestressed steel per unit.
        STEEL_COST_PASSIVE (float): Cost of passive steel per unit.
        arqout (str): Output file name for the results.
        numpav (int): Number of floors in the building.
        dminx (float): Minimum distance in the X dimension.
        dminy (float): Minimum distance in the Y dimension.
        lx (float): Length of the floor in the X dimension.
        ly (float): Length of the floor in the Y dimension.
        hmax (float): Maximum height.
        bmax (float): Maximum beam width.
        q (float): Load per square meter (Tf/m²).
        gpr (float): Permanent load for floors (Tf/m²).
        gpl (float): Permanent load for walls (Tf/m²).
        numind (int): Number of individuals in the genetic algorithm population.
        elit (int): Number of elite individuals to keep unchanged during selection.
        maxger (int): Maximum number of generations in the genetic algorithm.
        cruz_taxa (float): Crossover rate for the genetic algorithm.
        pmut (float): Mutation rate for the genetic algorithm.
        cruz (int): Calculated number of crossovers based on the crossover rate.
        nxmax (int): Calculated maximum number of X dimension divisions.
        nymax (int): Calculated maximum number of Y dimension divisions.
        nvv (int): Number of verticals based on the maximum beam width.
        numgen (int): Total number of generations for the genetic algorithm.

    """

    CONCRETE_COSTS_CCML = np.array([147, 158, 171, 185])
    CONCRETE_COSTS_CPM = np.array([185, 200, 216, 233])
    STEEL_COST_PRESTRESSED = 7
    STEEL_COST_PASSIVE = 4

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
        numind,
        elit,
        maxger,
        cruz_taxa,
        pmut,
    ):
        """
        Initializes the building design parameters with user inputs and calculates additional values.

        :param arqout: Output file name for the results.
        :param numpav: Number of floors in the building.
        :param dminx: Minimum distance in the X dimension.
        :param dminy: Minimum distance in the Y dimension.
        :param lx: Length of the floor in the X dimension.
        :param ly: Length of the floor in the Y dimension.
        :param hmax: Maximum height.
        :param bmax: Maximum beam width.
        :param q: Load per square meter (Tf/m²).
        :param gpr: Permanent load for floors (Tf/m²).
        :param gpl: Permanent load for walls (Tf/m²).
        :param numind: Number of individuals in the genetic algorithm population.
        :param elit: Number of elite individuals to keep unchanged during selection.
        :param maxger: Maximum number of generations in the genetic algorithm.
        :param cruz_taxa: Crossover rate for the genetic algorithm.
        :param mutation_taxa: Mutation rate for the genetic algorithm.
        """

        self.numpav = numpav
        self.dminx = dminx
        self.dminy = dminy
        self.lx = lx
        self.ly = ly
        self.hmax = hmax
        self.bmax = bmax
        self.q = q
        self.gpr = gpr
        self.gpl = gpl
        self.numind = numind
        self.elit = elit
        self.maxger = maxger
        self.cruz_taxa = cruz_taxa / 100
        self.mutation_taxa = pmut / 100

        # Calculando parâmetros
        self.cruz = self.calculate_cruzamento(numind, cruz_taxa)
        self.nxmax = self.calculate_max_dimension(lx, dminx)
        self.nymax = self.calculate_max_dimension(ly, dminy)
        self.nvv = 5 if bmax > 0.60 else 4
        self.numgen = 21 + self.nxmax + self.nymax + self.nvv

    def calculate_cruzamento(self, numind, cruz_taxa):
        """
        Calculates the number of crossovers based on the population size and crossover rate.

        :param numind: Number of individuals in the genetic algorithm population.
        :param cruz_taxa: Crossover rate (percentage) for the genetic algorithm.
        :return: int: The number of crossovers (even number).
        """
        cruz = (cruz_taxa * numind) // 100
        return cruz if cruz % 2 == 0 else cruz + 1

    def calculate_max_dimension(self, dimension, dmin):
        """
        Calculates the maximum division based on the dimension and minimum distance.

        :param dimension: The dimension (either lx or ly).
        :param dmin: The minimum distance (either dminx or dminy).
        :return: int: The maximum number of divisions (3 or 4).
        """
        aj = dimension / dmin
        if aj < 9:
            return 3
        elif aj >= 9:
            return 4
        return 2

    def get_parameters(self):
        """
        Returns all input parameters and calculated values in a dictionary.

        :return: dict: A dictionary containing all input parameters and calculated values.
        """
        return {
            "numpav": self.numpav,
            "dminx": self.dminx,
            "dminy": self.dminy,
            "lx": self.lx,
            "ly": self.ly,
            "hmax": self.hmax,
            "bmax": self.bmax,
            "q": self.q,
            "gpr": self.gpr,
            "gpl": self.gpl,
            "numind": self.numind,
            "elit": self.elit,
            "maxger": self.maxger,
            "cruz_taxa": self.cruz_taxa,
            "pmut": self.mutation_taxa,
            "nxmax": self.nxmax,
            "nymax": self.nymax,
            "nvv": self.nvv,
            "numgen": self.numgen,
            "ccml": self.CONCRETE_COSTS_CCML.tolist(),
            "cpm": self.CONCRETE_COSTS_CPM.tolist(),
            "cap": self.STEEL_COST_PRESTRESSED,
            "cad": self.STEEL_COST_PASSIVE,
        }


def main():
    print("Bem-vindo ao sistema de cálculo de parâmetros de design de edifícios!")

    # Solicitando entrada do usuário
    numpav = int(input("Número de pavimentos: "))
    dminx = float(input("Distância mínima entre pilares X (m): "))
    dminy = float(input("Distância mínima entre pilares X (m): "))
    lx = float(input("Dimensão do pavimento X (m): "))
    ly = float(input("Dimensão do pavimento Y (m): "))
    hmax = float(input("Altura máxima (m): "))
    bmax = float(input("Largura máxima da viga (m): "))
    q = float(input("Sobre-carga (Tf/m²): "))
    gpr = float(input("Carga permanente - Pavimento (Tf/m²): "))
    gpl = float(input("Carga permanente - Paredes (Tf/m²): "))
    numind = int(input("Número de indivíduos: "))
    elit = int(input("Número para elitismo: "))
    maxger = int(input("Número de gerações: "))
    cruz_taxa = int(input("Taxa de cruzamento (%): "))
    pmut = float(input("Taxa de mutação (%): "))

    # Criando a instância e obtendo os parâmetros
    try:
        params = BuildingDesignParameters(
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
            numind,
            elit,
            maxger,
            cruz_taxa,
            pmut,
        )
        result = params.get_parameters()

        print("\nParâmetros calculados:")
        for key, value in result.items():
            print(f"{key}: {value}")
    except ValueError as e:
        print(f"Erro ao calcular parâmetros: {e}")


if __name__ == "__main__":
    main()
