import time
import numpy

class corre:

    def cal_pop_fitness(self,feedback):
        # Calculating the fitness value of each solution in the current population.
        # The fitness function caulcuates the sum of products between each input and its corresponding weight.
        # Since we look for the smallest Distance, lets put bellow 1 to get a higher value outside
        print("cal_pop_fitness {}".format(feedback))
        fitness = numpy.sum(feedback, axis=1)
        return fitness

    def select_mating_pool(self,pop, fitness, num_parents):
        # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
        parents = numpy.empty((num_parents, pop.shape[1]))
        print("select_mating_pool: {}".format(fitness))
        for parent_num in range(num_parents):
            max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
            max_fitness_idx = max_fitness_idx[0][0]
            parents[parent_num, :] = pop[max_fitness_idx, :]
            fitness[max_fitness_idx] = -99999999999
        return parents

    def crossover(self,parents, offspring_size):
        offspring = numpy.empty(offspring_size)
        # The point at which crossover takes place between two parents. Usually it is at the center.
        crossover_point = numpy.uint8(offspring_size[1]/2)

        for k in range(offspring_size[0]):
            # Index of the first parent to mate.
            parent1_idx = k%parents.shape[0]
            # Index of the second parent to mate.
            parent2_idx = (k+1)%parents.shape[0]
            # The new offspring will have its first half of its genes taken from the first parent.
            offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
            # The new offspring will have its second half of its genes taken from the second parent.
            offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
        return offspring

    def mutation(self,offspring_crossover):
        # Mutation changes a single gene in each offspring randomly.
        for idx in range(offspring_crossover.shape[0]):
            # The random value to be added to the gene.
            random_value = numpy.random.uniform(-1.0, 1.0, 1)
            offspring_crossover[idx, 4] = offspring_crossover[idx, 4] + random_value
        return offspring_crossover

    print("oi, sou o g.a.")

    # Number of the weights we are looking to optimize.
    # The last 4 are the sequence of priority
    num_weights = 8

    """
    Genetic algorithm parameters:
        Mating pool size
        Population size
    """
    sol_per_pop = 5
    num_parents_mating = 5

    # Defining the population size.
    pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
    #Creating the initial population.
    new_population = numpy.random.uniform(low=0, high=150, size=pop_size)
    #print("-Momento 0 da população-")
    #print(new_population)
    
    for ii in range(0,sol_per_pop):
        freeOptions = [0,1,2,3]
        for i in range(1,5):
            new_population[ii][-i] = freeOptions[numpy.random.randint(0,len(freeOptions))]
            #print("-Momento 1 da população-")
            #print(new_population[ii])
            #print("*Numero para ser removido: " + str(new_population[ii][-i]) + "*")
            freeOptions.remove(new_population[ii][-i])
    print("First pop")
    print(new_population)

    #Number of generations
    #num_generations = 200

    

    def createGeneration(self,generation, feedback):
        print("Generation : ", generation)
        # Measing the fitness of each chromosome in the population.
        fitness = self.cal_pop_fitness(feedback)

        # Selecting the best parents in the population for mating.
        parents = self.select_mating_pool(self.new_population, fitness, 
                                        self.num_parents_mating)

        # Generating next generation using crossover.
        offspring_crossover = crossover(parents,
                                        offspring_size=(pop_size[0]-parents.shape[0], num_weights))

        # Adding some variations to the offsrping using mutation.
        offspring_mutation = mutation(offspring_crossover)

        # Creating the new population based on the parents and offspring.
        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = offspring_mutation

        # The best result in the current iteration.
        print("Best result : ", numpy.max(numpy.sum(new_population, axis=1)))
        
    # Getting the best solution after iterating finishing all generations.
    #At first, the fitness is calculated for each solution in the final generation.
    ###fitness = cal_pop_fitness(equation_inputs, new_population)

    # Then return the index of that solution corresponding to the best fitness.
    ###best_match_idx = numpy.where(fitness == numpy.max(fitness))

    ###print("Best solution : ", new_population[best_match_idx, :])
    ###print("Best solution fitness : ", fitness[best_match_idx])