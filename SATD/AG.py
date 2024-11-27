import numpy as np
from AvaliaIndF import StructuralEvaluation
from CruzUniforme import UniformCrossover
from building_design import BuildingDesignParameters
from ImpressaoEmArquivo import FileWriter



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
        self.arqout = self.params["arqout"]
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
        elite_size = int(self.num_individuals * self.elitism_rate)
        sorted_indices = np.argsort(self.fitness)[::-1]
        selected_individuals = self.population[sorted_indices]

        # Keep elite individuals
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
        # Create a copy of the population to ensure the original remains unchanged
        mutated_population = population.copy()
        for i in range(len(mutated_population)):
            if np.random.rand() < self.mutation_rate:
                # Generate binary mutation vector (0 or 1)
                mutation_vector = np.random.randint(
                    0, 2, size=mutated_population[i].shape
                )
                # Apply mutation
                mutated_population[i] = mutation_vector

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
        best_index = np.argmax(self.fitness)
        return self.population[best_index], self.fitness[best_index]
    
    def sort_population_by_fitness(self):
        """
        Ordena a população e os valores de fitness em ordem decrescente de fitness.

        :return: tuple: (sorted_population, sorted_fitness)
            - sorted_population: População ordenada pela fitness.
            - sorted_fitness: Fitness correspondente à população ordenada.
        """
        sorted_indices = np.argsort(self.fitness)[::-1]
        sorted_population = self.population[sorted_indices]
        return sorted_population

    def write_population_to_file(self):
        """
        Writes information about the sorted population to a specified file.

        This method sorts the population by fitness, evaluates each individual, and saves their 
        detailed information to a file. Each individual is labeled with a sequential identifier.

        :raises AttributeError: If `self.evaluation` or `self.arqout` is not properly initialized.
        """
        try:
            # Sort the population by fitness
            sorted_population = self.sort_population_by_fitness()

            # Initialize the file writer
            file_writer = FileWriter(self.arqout)

            # Counter to track the individual index
            count = 0

            # Iterate over the sorted population and write their details to the file
            for individual in sorted_population:
                count += 1
                self.evaluation.initialize_individual(individual)

                # Get detailed information for the individual
                individual_info = self.evaluation.mostrar_resultados(count)

                # Write the individual's information to the file
                file_writer.write_list_to_file(individual_info)

        except AttributeError as error:
            print(f"Error: {error}. Ensure that `self.evaluation` and `self.arqout` are initialized.")



def main():
    print("Bem-vindo ao sistema de cálculo de parâmetros de design de edifícios!")

    # Criando a instância de BuildingDesignParameters
    building_params = BuildingDesignParameters(
        arqout="output.txt",
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
        numind=10,
        elit=5,
        maxger=1,
        cruz_taxa=80,
        pmut=1,
    )

    # Criando a instância do algoritmo genético com os parâmetros do edifício
    ga = GeneticAlgorithm(building_params)

    # Executando o algoritmo genético por um número de gerações
    ga.evolve()

    # Obtendo o melhor indivíduo após a execução
    best_individual, best_fitness = ga.get_best_individual()
    ga.write_population_to_file()
    # Imprimindo o melhor indivíduo e sua aptidão
    print("Melhor Indivíduo:", best_individual)
    print("Aptidão do Melhor Indivíduo:", best_fitness)


if __name__ == "__main__":
    main()
