import numpy as np
from AvaliaIndF import StructuralEvaluation
from CruzUniforme import UniformCrossover
from building_design import BuildingDesignParameters
import matplotlib.pyplot as plt


class GeneticAlgorithm:
    """
    A genetic algorithm to optimize building design parameters based on structural evaluation.

    This class implements a genetic algorithm that evolves a population of individuals over
    generations to optimize building design parameters. Each individual represents a potential
    design solution, and the fitness of each individual is evaluated using the StructuralEvaluation
    class. The algorithm includes selection, crossover, and mutation operators to evolve the population.

    Attributes:
        num_individuals (int): Number of individuals in the population.
        num_genes (int): Number of genes (design parameters) per individual.
        max_generations (int): Maximum number of generations to run the algorithm.
        crossover_rate (float): Probability of performing a crossover.
        mutation_rate (float): Probability of performing a mutation.
        elitism_rate (float): Fraction of the population to keep unchanged through elitism.
        structural_params (dict): A dictionary of parameters required for structural evaluation.
        population (np.ndarray): A numpy array representing the population of individuals.
        fitness (np.ndarray): A numpy array containing the fitness values of each individual.
        fitness_history (list): A list to store the average fitness values of each generation.

    """

    def __init__(self, building_params):
        """
        Initializes the genetic algorithm with the given parameters.

        :param building_params: An instance of the BuildingDesignParameters class containing the design parameters.
        """
        self.params = building_params.get_parameters()
        self.num_individuals = self.params["numind"]
        self.num_genes = self.params["numgen"]
        self.max_generations = self.params["maxger"]
        self.crossover_rate = self.params["cruz_taxa"]
        self.mutation_rate = self.params["pmut"]
        self.elitism_rate = self.params["elit"] / self.num_individuals

        # Assuming structural_params contains necessary parameters for evaluation
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
        self.population = self._initialize_population()
        self.fitness = np.zeros(self.num_individuals)
        self.fitness_history = []

    def _initialize_population(self):
        """
        Initializes the population with random binary values (0 or 1).

        :return: np.ndarray representing the initial population of individuals.
        """
        return np.random.randint(0, 2, size=(self.num_individuals, self.num_genes))

    def _calculate_fitness(self):
        """
        Calculates the fitness of each individual using the StructuralEvaluation class.

        :return: None. The fitness values are stored in the self.fitness attribute.
        """
        self.fitness = np.zeros(self.num_individuals)

        for i, individual in enumerate(self.population):
            self.evaluation.initialize_individual(individual)
            self.fitness[i] = self.evaluation.get_fitness()

    def _selection(self):
        """
        Selects individuals based on fitness and applies elitism.

        Elitism ensures that a portion of the best individuals are kept unchanged for the next generation.

        :return: A tuple (elite, remaining) where:
            - elite: The elite individuals based on fitness.
            - remaining: The remaining individuals selected for crossover.
        """
        # Validate elitism_rate
        if not (0 <= self.elitism_rate <= 1):
            raise ValueError("Elitism rate must be between 0 and 1.")

        # Calculate elite size (at least one elite individual if rate > 0)
        elite_size = max(1, int(round(self.num_individuals * self.elitism_rate)))

        # Sort population based on fitness
        sorted_indices = np.argsort(self.fitness)  # Ascending order for minimization
        selected_individuals = self.population[sorted_indices]
        # Keep elite and separate remaining
        elite = selected_individuals[:elite_size]
        remaining = selected_individuals[elite_size:]

        return elite, remaining

    def _crossover(self, parents):
        """
        Performs uniform crossover on the selected parents to generate offspring.

        :param parents: A numpy array of selected parents for crossover.
        :return: np.ndarray of offspring generated by crossover.
        """
        eliminated = None
        if len(parents) % 2 != 0:
            eliminated = parents[-1]
            parents = parents[:-1]  # Ensure even number of parents for pairing
        num_crossover = int(self.crossover_rate * self.num_individuals)

        crossover_operator = UniformCrossover(parents, self.num_genes, num_crossover)
        offspring = crossover_operator.perform_crossover()
        if eliminated is not None:
            offspring = np.vstack(
                (offspring, eliminated)
            )  # Add the eliminated parent to offspring
        return offspring

    def _mutation(self, population):
        """
        Applies mutation on the population by flipping genes (0 or 1) based on mutation rate.

        Mutation introduces random changes to the population to maintain diversity.

        :param population: The current population of individuals (represented as binary arrays).
        :return: np.ndarray: The mutated population.
        """
        # Cria uma cópia da população para garantir que a original não seja alterada
        mutated_population = population.copy()

        # Itera sobre cada indivíduo na população
        for i in range(mutated_population.shape[0]):  # Percorre cada indivíduo
            for j in range(mutated_population.shape[1]):  # Percorre cada gene
                # Aplica mutação com base na taxa de mutação
                if np.random.rand() < self.mutation_rate:
                    mutated_population[i, j] = (
                        1 - mutated_population[i, j]
                    )  # Inverte o gene

        return mutated_population

    def evolve(self):
        """
        Runs the genetic algorithm for the specified number of generations.

        During each generation, the fitness of the population is calculated, elitism is applied,
        crossover and mutation are performed on the remaining individuals, and the new population
        is updated.

        :return: None
        """
        for generation in range(self.max_generations):
            self._calculate_fitness()

            # Selection: get elite and remaining individuals
            elite, remaining = self._selection()

            # Perform crossover on the remaining population
            offspring = self._crossover(remaining)
            # Perform mutation on the offspring
            offspring = self._mutation(offspring)
            # Combine elite and offspring to form the new population
            self.population = np.vstack((elite, offspring))

            self._calculate_fitness()

            # Track average fitness for each generation
            average_fitness = np.mean(self.fitness)

            self.fitness_history.append(average_fitness)
            print(f"Geração {generation + 1}, Aptidão Média: {average_fitness:.2f}")

    def get_best_individual(self):
        """
        Returns the best individual (the one with the highest fitness) and its fitness value.

        :return: tuple: (best_individual, best_fitness)
            - best_individual: The individual with the highest fitness.
            - best_fitness: The fitness value of the best individual.
        """
        best_index = np.argmin(self.fitness)
        return self.population[best_index], self.fitness[best_index]

    def sort_population_by_fitness(self):
        """
        Sorts the population and fitness values in ascending order of fitness.

        :return: tuple: (sorted_population, sorted_fitness)
            - sorted_population: Population sorted by fitness (lower is better).
            - sorted_fitness: Fitness corresponding to the sorted population.
        """
        sorted_indices = np.argsort(self.fitness)  # Ascending order
        sorted_population = self.population[sorted_indices]
        return sorted_population


def main():
    print("Bem-vindo ao sistema de cálculo de parâmetros de design de edifícios!")

    # Criando a instância de BuildingDesignParameters
    building_params = BuildingDesignParameters(
        numpav=2,
        dminx=7.0,
        dminy=7.0,
        lx=46.5,
        ly=48.0,
        hmax=0.50,
        bmax=0.40,
        q=0.3,
        gpr=0.1,
        gpl=0.2,
        numind=700,
        elit=3,
        maxger=50,
        cruz_taxa=80,
        pmut=1,
    )

    # Criando a instância do algoritmo genético com os parâmetros do edifício
    ga = GeneticAlgorithm(building_params)

    # Executando o algoritmo genético por um número de gerações
    ga.evolve()

    # Obtendo o melhor indivíduo após a execução
    best_individual, best_fitness = ga.get_best_individual()

    # Imprimindo o melhor indivíduo e sua aptidão
    print("Melhor Indivíduo:", best_individual)
    print("Aptidão do Melhor Indivíduo:", best_fitness)
    t = ga.fitness_history
    fig, ax = plt.subplots()
    ax.plot(t)

    ax.grid()
    plt.show()


if __name__ == "__main__":
    main()
