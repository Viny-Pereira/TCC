import numpy as np
from AvaliaIndF import StructuralEvaluation  # Certifique-se de importar a classe correta


class GeneticAlgorithm:
    def __init__(self, num_individuals, num_variables, max_generations, crossover_rate, mutation_rate, elitism_rate, structural_params):
        """
        Initializes the genetic algorithm with the given parameters.

        :param num_individuals: Number of individuals in the population.
        :param num_variables: Number of genes per individual.
        :param max_generations: Maximum number of generations to run the algorithm.
        :param crossover_rate: The probability of performing a crossover.
        :param mutation_rate: The probability of performing a mutation.
        :param elitism_rate: The percentage of the population to keep unchanged (elitism).
        :param structural_params: Parameters needed for structural evaluation (pass to StructuralEvaluation)
        """
        self.num_individuals = num_individuals
        self.num_variables = num_variables
        self.max_generations = max_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_rate = elitism_rate
        self.structural_params = structural_params  # Params for structural evaluation
        
        self.population = self._initialize_population()
        self.fitness = np.zeros(self.num_individuals)
        self.fitness_history = []

    def _initialize_population(self):
        """Initializes the population with random values."""
        return np.random.rand(self.num_individuals, self.num_variables)
    
    def _calculate_fitness(self):
        """Calculates the fitness of each individual using StructuralEvaluation."""
        self.fitness = np.zeros(self.num_individuals)

        for i, individual in enumerate(self.population):
            # Aqui estamos assumindo que StructuralEvaluation já possui um método para calcular aptidão
            # Substitua "individual" e "self.structural_params" conforme necessário para o seu contexto.
            evaluation = StructuralEvaluation(individual, **self.structural_params)
            self.fitness[i] = evaluation.calculate_fitness()  # Substitua conforme necessário
    
    def _selection(self):
        """Selects individuals based on fitness and elitism."""
        elite_size = int(self.num_individuals * self.elitism_rate)
        sorted_indices = np.argsort(self.fitness)[::-1]
        selected_individuals = self.population[sorted_indices]
        
        # Keep elite individuals
        elite = selected_individuals[:elite_size]
        
        return elite, selected_individuals[elite_size:]

    def _crossover(self, parents):
        """Performs crossover between pairs of individuals."""
        num_parents = len(parents)
        offspring = []
        
        for i in range(0, num_parents, 2):
            if np.random.rand() < self.crossover_rate:
                parent1, parent2 = parents[i], parents[i + 1]
                # Simple average crossover method
                child = (parent1 + parent2) / 2
                offspring.append(child)
        
        return np.array(offspring)
    
    def _mutation(self, population):
        """Performs mutation on each individual with the given mutation rate."""
        for i in range(len(population)):
            if np.random.rand() < self.mutation_rate:
                mutation_vector = np.random.normal(size=population[i].shape)
                population[i] += mutation_vector
        return population
    
    def evolve(self):
        """Runs the genetic algorithm for a given number of generations."""
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
        """Returns the best individual and its fitness."""
        best_index = np.argmax(self.fitness)
        return self.population[best_index], self.fitness[best_index]

# Example usage of the GeneticAlgorithm class:
if __name__ == "__main__":
    num_individuals = 100
    num_variables = 10
    max_generations = 50
    crossover_rate = 0.8
    mutation_rate = 0.05
    elitism_rate = 0.1
    
    # Parâmetros para a avaliação estrutural (ajuste conforme necessário)
    structural_params = {
        'param1': value1,
        'param2': value2,
        # Adicione todos os parâmetros necessários para StructuralEvaluation
    }

    ga = GeneticAlgorithm(num_individuals, num_variables, max_generations, crossover_rate, mutation_rate, elitism_rate, structural_params)
    ga.evolve()

    best_individual, best_fitness = ga.get_best_individual()
    print("Melhor Indivíduo:", best_individual)
    print("Aptidão do Melhor Indivíduo:", best_fitness)
