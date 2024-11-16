import numpy as np


class UniformCrossover:
    def __init__(self, parents, num_genes, num_crossovers):
        """
        Initializes the uniform crossover object with the given parameters.

        :param parents: 2D array where each row is a parent and each column is a gene.
        :param num_genes: Number of genes per individual.
        :param num_crossovers: Number of crossover pairs to generate.
        """
        # Ensure number of parents is even for pairing
        if len(parents) % 2 != 0:
            raise ValueError("Number of parents must be even.")
        
        self.parents = parents
        self.num_genes = num_genes
        self.num_crossovers = num_crossovers
        self.offspring = np.zeros_like(parents)  # To store the offspring


    def generate_crossover_mask(self):
        """
        Generates a random mask for each gene in the population.

        :return: A 2D array representing crossover masks for each pair.
        """
        return np.random.randint(0, 2, size=(self.num_crossovers, self.num_genes))

    def perform_crossover(self):
        """
        Performs the uniform crossover by combining genes from pairs of parents
        based on the generated mask.

        :return: The matrix of offspring created by uniform crossover.
        """
        # Generate all crossover masks at once for efficiency
        masks = self.generate_crossover_mask()

        for i in range(0, self.num_crossovers, 2):
            mask = masks[i]  # Select a crossover mask for this pair

            for j in range(self.num_genes):
                # First child takes genes based on the mask
                if mask[j] == 0:
                    self.offspring[i, j] = self.parents[i, j]
                    self.offspring[i + 1, j] = self.parents[i + 1, j]
                else:
                    self.offspring[i, j] = self.parents[i + 1, j]
                    self.offspring[i + 1, j] = self.parents[i, j]

        return self.offspring

    def get_results(self):
        """
        Returns the generated offspring from the crossover process.

        :return: A 2D numpy array with the offspring.
        """
        return self.perform_crossover()


# Example usage:
if __name__ == "__main__":
    # Example: 6 individuals, each with 4 genes
    parents = np.array(
        [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
            [17, 18, 19, 20],
            [21, 22, 23, 24],
        ]
    )

    num_genes = 4
    num_crossovers = 6

    # Initialize the UniformCrossover object
    crossover = UniformCrossover(parents, num_genes, num_crossovers)

    # Perform the crossover and get the results
    offspring = crossover.get_results()

    # Display the results
    print("Parents:")
    print(parents)
    print("Offspring:")
    print(offspring)
