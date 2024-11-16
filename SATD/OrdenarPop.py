import numpy as np

class PopulationSorter:
    def __init__(self, population, fitness, ascending=True):
        """
        Initializes the class with the population matrix and the fitness vector, allowing sorting order.

        :param population: Population matrix (individuals x features)
        :param fitness: Fitness vector (one value per individual)
        :param ascending: Boolean to indicate whether sorting should be ascending or descending
        """
        if len(population) != len(fitness):
            raise ValueError("Population and fitness arrays must have the same number of individuals.")
        
        self.population = population
        self.fitness = fitness
        self.ascending = ascending

    def sort_population(self):
        """
        Sorts the population based on fitness and returns the sorted population and fitness vectors.
        """
        sorted_indices = np.argsort(self.fitness)
        if not self.ascending:
            sorted_indices = sorted_indices[::-1]  # Reverse order if descending

        sorted_population = self.population[sorted_indices]
        sorted_fitness = self.fitness[sorted_indices]

        return sorted_population, sorted_fitness
    
    def get_results(self):
        """
        Returns the sorted population and fitness as a dictionary.
        """
        sorted_population, sorted_fitness = self.sort_population()
        return {
            "sorted_population": sorted_population,
            "sorted_fitness": sorted_fitness
        }


# Example usage of the class:
if __name__ == "__main__":
    # Example population and fitness (matrix of 5 individuals and 3 features)
    population = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]])
    fitness = np.array([0.9, 0.1, 0.8, 0.4, 0.7])

    # Create the PopulationSorter object
    sorter = PopulationSorter(population, fitness, ascending=False)

    # Get sorted results
    results = sorter.get_results()

    # Displaying the results
    print("Sorted Population:")
    print(results["sorted_population"])
    print("Sorted Fitness:")
    print(results["sorted_fitness"])
