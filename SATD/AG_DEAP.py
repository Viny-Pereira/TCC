import numpy as np
from deap import base, creator, tools, algorithms
import random
import matplotlib.pyplot as plt
from AvaliaIndF import StructuralEvaluation
from building_design import BuildingDesignParameters


class GeneticAlgorithm:
    """
    A genetic algorithm implementation using DEAP for optimizing building design parameters.
    """

    def __init__(self, building_params, selection_strategy="tournament"):
        self.params = building_params.get_parameters()
        self.num_individuals = self.params["numind"]
        self.num_genes = self.params["numgen"]
        self.max_generations = self.params["maxger"]
        self.crossover_rate = self.params["cruz_taxa"]
        self.mutation_rate = self.params["pmut"]
        self.elit = self.params["elit"]
        self.selection_strategy = selection_strategy

        # Initialize structural evaluation
        self.structural_params = {
            "numpav": self.params["numpav"],
            "dminx": self.params["dminx"],
            "dminy": self.params["dminy"],
            "lx": self.params["lx"],
            "ly": self.params["ly"],
            "hmax": self.params["hmax"],
            "bmax": self.params["bmax"],
            "q": self.params["q"],
            "gpr": self.params["gpr"],
            "gpl": self.params["gpl"],
            "ccml": self.params["ccml"],
            "cpm": self.params["cpm"],
            "cap": self.params["cap"],
            "cad": self.params["cad"],
            "numind": self.params["numind"],
            "nxmax": self.params["nxmax"],
            "nymax": self.params["nymax"],
            "nvv": self.params["nvv"],
            "numgen": self.params["numgen"],
        }
        self.evaluation = StructuralEvaluation(**self.structural_params)
        self.evaluation = StructuralEvaluation(**self.structural_params)

        # DEAP components
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()
        self.toolbox.register("bit", random.randint, 0, 1)
        self.toolbox.register(
            "individual",
            tools.initRepeat,
            creator.Individual,
            self.toolbox.bit,
            self.num_genes,
        )
        self.toolbox.register(
            "population", tools.initRepeat, list, self.toolbox.individual
        )

        self.toolbox.register("evaluate", self.evaluate)
        self.toolbox.register("mate", tools.cxUniform, indpb=self.crossover_rate)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=self.mutation_rate)
        self._register_selection_strategy()

    def _register_selection_strategy(self):
        strategies = {
            "rank": lambda: self.toolbox.register(
                "select", tools.selStochasticUniversalSampling
            ),
            "tournament": lambda: self.toolbox.register(
                "select", tools.selTournament, tournsize=self.elit
            ),
            "roulette": lambda: self.toolbox.register("select", tools.selRoulette),
            "random": lambda: self.toolbox.register("select", tools.selRandom),
        }
        strategy_func = strategies.get(
            self.selection_strategy, lambda: tools.selStochasticUniversalSampling
        )
        strategy_func()

    def evaluate(self, individual):
        self.evaluation.initialize_individual(individual)
        return (self.evaluation.get_fitness(),)

    def evolve(self):
        population = self.toolbox.population(n=self.num_individuals)

        # Statistics for tracking progress
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", np.min)
        stats.register("avg", np.mean)

        # Run the genetic algorithm with elitism
        population, logbook = algorithms.eaSimple(
            population,
            self.toolbox,
            cxpb=self.crossover_rate,
            mutpb=self.mutation_rate,
            ngen=self.max_generations,
            stats=stats,
            halloffame=None,
            verbose=True,
        )

        # Track the best individual
        self.population = population
        self._best_individual = tools.selBest(population, 1)[0]
        self._best_fitness = self._best_individual.fitness.values[0]
        self.logbook = logbook

    def get_best_individual(self):
        return self._best_individual, self._best_fitness

    def get_log(self):
        return self.logbook

    def get_population(self):
        return self.population[0]

    def sort_population_by_fitness(self):
        """
        Sorts the population by fitness values in ascending order and returns the list of individuals only.

        :return: list: A sorted list of individuals in ascending order of fitness.
        """
        # Ordena a população com base no valor de fitness (mas não inclui o fitness na lista retornada)
        sorted_population = sorted(
            self.population, key=lambda ind: ind.fitness.values[0]
        )

        # Retorna apenas os indivíduos, sem a aptidão
        return sorted_population


def main():
    print("Bem-vindo ao sistema de cálculo de parâmetros de design de edifícios!")
    maxgen = 3000
    # Initialize building design parameters
    building_params = BuildingDesignParameters(
        numpav=3,
        dminx=7.0,
        dminy=7.0,
        lx=46.5,
        ly=48.0,
        hmax=0.60,
        bmax=0.70,
        q=0.15,
        gpr=0.15,
        gpl=0.5,
        numind=700,
        elit=3,
        maxger=maxgen,
        cruz_taxa=80,
        pmut=1,
    )

    # Initialize and run the genetic algorithm
    ga = GeneticAlgorithm(building_params)
    ga.evolve()
    best_individual, best_fitness = ga.get_best_individual()
    logbook = ga.get_log()

    # Display the results
    print("Melhor Indivíduo:", best_individual)
    print("Aptidão do Melhor Indivíduo:", best_fitness)

    # Plot fitness history
    gen = logbook.select("gen")
    avg = logbook.select("avg")
    minimum = logbook.select("min")

    plt.figure(figsize=(10, 6))
    plt.plot(gen, avg, label="Aptidão Média")
    plt.plot(gen, minimum, label="Aptidão Mínima", color="red")
    plt.xlabel("Geração")
    plt.ylabel("Aptidão")
    plt.title("Progresso do Algoritmo Genético")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
