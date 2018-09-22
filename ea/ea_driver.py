import copy
import ea.genotype as genotype_class
import ea.log as log_class
import math
import puzzle.light_up_puzzle as puzzle_class
import random
import util.seed as seed_class


class EADriver:
    def __init__(self, config):
        """Initializes the EADriver class.
        
        Where config is a Config object. 
        """

        self.config = config

        # Initialize the seed class
        self.seed = seed_class.Seed(self.config)

        self.population_size = int(self.config.settings['mu'])
        self.offspring_pool_size = int(self.config.settings['lambda'])
        
        self.run_count = 1
        self.best_fit_global_genotype = genotype_class.Genotype()

        self.init_run_variables()

        # Initialize the log file class
        self.log = log_class.Log(self.config, self.seed, self.phenotype, overwrite=True)


    def init_run_variables(self):
        """Initializes run specific variables.

        This function should be called before each run.
        """

        def force_adj_bulbs():
            """Places bulbs around black squares where there is only one valid
            bulb placement pattern.
            """
            bulbs = set([])

            # Determine where to place bulbs
            for black_square in self.phenotype.black_squares:
                # Get the adjacent coordinates to black_square that are not black
                adj_coords = [s for s in self.phenotype.get_adj_coords(black_square) if not s in self.phenotype.black_squares]

                if self.phenotype.black_squares[black_square] == len(adj_coords):
                    # There is only one way to place bulbs around this square
                    # Place those bulbs
                    for coord in adj_coords:
                        self.phenotype.place_bulb(coord, bulbs)
            
            # Save bulb placements to each genotype
            for genotype in self.population:
                genotype.bulbs = copy.deepcopy(bulbs)


        def init_puzzles_with_bulbs():
            """Randomly places bulbs on each puzzle in population in a uniform manner.
            
            The number of attempted bulb placement failures is determined by config.
            """
            for genotype_index in range(len(self.population)):
                # Place bulbs until num_bulb_placement_failures failures are reached
                failure_count = 0
                while failure_count < int(self.config.settings['num_bulb_placement_failures']):
                    if not self.phenotype.place_bulb_randomly(self.population[genotype_index].bulbs):
                        failure_count += 1


        self.max_run_fitness = 0
        self.eval_count = 0
        self.avg_fitness_ratio = 0.0
        self.total_fitnesses_seen = 0
        self.total_fitness_ratio_sum = 0
        self.stale_fitness_count = 0
        self.prev_avg_fitness_ratio = 0.0
        self.best_fit_local_genotype = genotype_class.Genotype()

        # Create/reset the base puzzle class (phenotype)
        self.phenotype = puzzle_class.LightUpPuzzle(self.config)

        # Create/reset the puzzle population: a list genotypes
        self.population = []
        for _ in range(self.population_size):
            self.population.append(genotype_class.Genotype())

        self.parents = []
        self.children = []

        if int(self.config.settings['force_validity']):
            # Use black square adjacency heuristic to force validity
            force_adj_bulbs()
        
        init_puzzles_with_bulbs()

    
    def evaluate(self, genotypes, log_run=True):
        """Evaluates all genotypes in the list genotypes, updating their fitness values, the average 
        fitness value, and the best fitness seen so far.

        If log_run is True, the state of the experiment is written to the log file.
        """ 
        for genotype in genotypes:
            self.phenotype.check_valid_solution(genotype.bulbs)
            genotype.fitness = self.phenotype.get_fitness()
            genotype.fitness_ratio = genotype.fitness / (self.phenotype.num_rows * self.phenotype.num_cols - len(self.phenotype.black_squares))

            # Calculate average fitness
            self.total_fitness_ratio_sum += genotype.fitness_ratio
            self.total_fitnesses_seen += 1
            self.avg_fitness_ratio = self.total_fitness_ratio_sum / self.total_fitnesses_seen

            # Determine if this fitness is the new best fitness (both locally and globally)
            if genotype.fitness_ratio > self.best_fit_local_genotype.fitness_ratio:
                self.best_fit_local_genotype = genotype

                if self.best_fit_local_genotype.fitness_ratio > self.best_fit_global_genotype.fitness_ratio:
                    self.best_fit_global_genotype = self.best_fit_local_genotype

                    # Write to solution file
                    self.phenotype.write_to_soln_file(self.best_fit_global_genotype.bulbs)
            
            # Determine if the population fitness is stagnating
            if math.isclose(self.avg_fitness_ratio, self.prev_avg_fitness_ratio, rel_tol=float(self.config.settings['termination_convergence_criterion_magnitude'])):
                self.stale_fitness_count += 1
            else:
                self.stale_fitness_count = 0
                self.prev_avg_fitness_ratio = self.avg_fitness_ratio
            
            self.eval_count += 1

        if log_run:
            self.log.write_run_data(self.eval_count, self.avg_fitness_ratio, self.best_fit_local_genotype.fitness_ratio)


    def select_parents(self):
        """Chooses which parents from the population will breed.

        Depending on the parent selection configuration, one of the two following methods
        is used to select parents:
            1. Fitness proportional selection
            2. k-tournament selection with replacement

        The resulting parents are stored in self.parents.
        """
        self.parents = []

        if int(self.config.settings['use_fitness_proportional_selection']):
            # Select parents for breeding using the fitness proportional "roulette wheel" method (with replacement)
            self.parents = random.choices(self.population, weights=[(g.fitness_ratio * 100) / float(len(self.population)) for g in self.population], k=int(self.config.settings['parent_population_size']))

        else:
            # Perform a k-tournament selection with replacement
            while len(self.parents) <= int(self.config.settings['parent_population_size']):
                self.parents.append(self.perform_tournament_selection(self.population, int(self.config.settings['k_parent_selection']), w_replacement=True))
            
            # Maintain the parent population size
            # This accounts for situations where the parent population size is not divisible by k
            self.parents = self.parents[:int(self.config.settings['parent_population_size'])]


    def recombine(self):
        """Breeds lambda (offspring_pool_size) children from the existing parent population.

        The resulting children are stored in self.children.
        """

        def breed(parent_a, parent_b):
            """Breeds two parent genotypes together to produce a child genotype using
            n-point crossover.

            Returns the child genotype.
            """
            a_bulbs = list(parent_a.bulbs)
            b_bulbs = list(parent_b.bulbs)

            # Perform a n-point crossover on the parent's bulbs
            n = int(self.config.settings['n_point_crossover'])

            min_crossover_index = 0
            max_crossover_index = min(len(a_bulbs) - 1, len(b_bulbs) - 1)

            if not max_crossover_index:
                if len(parent_a.bulbs):
                    return genotype_class.Genotype(parent_a.bulbs)
                else:
                    return genotype_class.Genotype(parent_b.bulbs)

            crossover_indices = []
            rand_start = min_crossover_index 
            for _ in range(n):
                if not rand_start == max_crossover_index and rand_start < max_crossover_index:
                    crossover_indices.append(random.randint(rand_start, max_crossover_index))
                    rand_start = crossover_indices[-1]
            
            # Ensure the entire parent is copied during crossover
            crossover_indices.append(max_crossover_index + 1)

            child_bulbs = set([])
            prev_crossover_index = 0
            for crossover_index in crossover_indices:
                if random.random() < float(self.config.settings['parent_selection_weight']):
                    # Choose parent_a's substring
                    for bulb in a_bulbs[prev_crossover_index:crossover_index]:
                        child_bulbs.add(bulb)

                else:
                    # Choose parent_b's substring
                    for bulb in b_bulbs[prev_crossover_index:crossover_index]:
                        child_bulbs.add(bulb)
                
                prev_crossover_index = crossover_index
            
            return genotype_class.Genotype(child_bulbs)


        self.children = []

        for _ in range(self.offspring_pool_size):
            # Select parents with replacement
            # Note: this implementation allows for parent_a and parent_b to be the same genotype
            parent_a = self.parents[random.randint(0, len(self.parents) - 1)]
            parent_b = self.parents[random.randint(0, len(self.parents) - 1)]

            # Produce a child
            self.children.append(breed(parent_a, parent_b))
        
    
    def mutate(self):
        """Probabilistically performs mutation on each child in the child population."""

        def shuffle_bulb(child):
            """Attempts to move the placement of a random bulb to a random position in a given
            child genotype.

            If this cannot be done in a valid way, the child's bulb is removed.
            """
            if len(child.bulbs):
                rand_bulb_index = random.randint(0, len(child.bulbs) - 1)
            else:
                rand_bulb_index = 0

            try:
                child.pop(rand_bulb_index)
            except:
                # No bulbs available to remove
                pass
            
            fail_count = 0
            while fail_count < int(self.config.settings['num_bulb_placement_failures_mutation']):
                if self.phenotype.place_bulb_randomly(child.bulbs):
                    break
                else:
                    fail_count += 1
            

        for child in self.children:
            if random.random() < float(self.config.settings['mutation_probability']):
                for i in range(random.randint(1, int(self.config.settings['rand_num_bulb_shuffles']))):
                    shuffle_bulb(child)


    def select_for_survival(self):
        """Integrates children from self.children into self.population while keeping mu (population
        size) constant.

        Depending on the survival selection configuration, one of the two following methods
        is used to select survivors:
            1. Truncation
            2. k-tournament selection without replacement
        """
        combined_generations = self.population + self.children
        self.population = []

        if int(self.config.settings['use_truncation']):
            # Use truncation for survival selection
            self.sort_genotypes(combined_generations)
            self.population = combined_generations[:self.population_size]
        
        else:
            # Use k-tournament for survival selection without replacement
            while len(self.population) <= self.population_size:
                self.population.append(self.perform_tournament_selection(combined_generations, int(self.config.settings['k_survival_selection']), w_replacement=False))

            # Maintain the population size
            # This accounts for situations where the population size is not divisible by k
            self.population = self.population[:self.population_size]


    def decide_termination(self):
        """Returns True if the program will terminate, False otherwise.

        The program will terminate if any of the following conditions are True:
            1. There has been no change in fitness (average fitness) for n evaluations.
            2. The number of evaluations specified in config has been reached.
        """
        if self.stale_fitness_count >= int(self.config.settings['n_termination_convergence_criterion']):
            # There has been no change in average fitness for too long
            return True

        if self.eval_count >= int(self.config.settings['num_fitness_evaluations']):
            # The number of desired evaluations has been reached
            return True

        return False


    def sort_genotypes(self, genotype_list):
        """Sorts the given genotype list from most fit to least fit by each
        element's fitness ratio.
        """
        genotype_list.sort(key=lambda x : x.fitness_ratio, reverse=True)


    def increment_run_count(self):
        """Increments the run count by one."""
        self.run_count += 1

    
    def perform_tournament_selection(self, genotypes, k, w_replacement=False):
        """Performs a k-tournament selection on genotypes, a list of genotype objects.

        Returns the winning genotype.
        """
        arena_genotypes = []
        forbidden_indices = set([])

        # Randomly select k elements from genotypes
        for _ in range(k):
            rand_index = random.randint(0, len(genotypes) - 1)

            # Don't allow replacement (if applicable)
            while rand_index in forbidden_indices:
                rand_index = random.randint(0, len(genotypes) - 1)

            arena_genotypes.append(genotypes[rand_index])

            if w_replacement == False:
                forbidden_indices.add(rand_index)

        # Make the genotypes fight, return the winner
        return max(arena_genotypes, key=lambda x : x.fitness_ratio)
