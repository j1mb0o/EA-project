import numpy as np
# you need to install this package `ioh`. Please see documentations here: 
# https://iohprofiler.github.io/IOHexp/ and
# https://pypi.org/project/ioh/
from ioh import get_problem, logger, ProblemClass
import sys
from itertools import product
from GA_utils import one_point_crossover,n_point_crossover,uniform_crossover
from GA_utils import  bit_flip_mutation,swap_mutation
from GA_utils import proportional_seletion, tournament_seletion
np.random.seed(42)

dimension = 50

def grid_search(problem):
    param_grid = {
        "selection_mechanism": ["proportional_seletion","tournament_seletion"],
        "crossover_mechanism": ["one_point_crossover","n_point_crossover","uniform_crossover"],
        "mutation_mechanism": ["bit_flip_mutation","swap_mutation"],
        "population_size": [50, 100, 150],
        "mutation_rate": [0.01, 0.02, 0.05],
        "crossover_probability": [0.5, 0.7],
        "tournament_k": [10, 20]
    }

    for params in product(*param_grid.values()):
        param_dict = dict(zip(param_grid.keys(), params))
        mean_fitness = s3840220_s3841863_GA(problem, **param_dict)
        
        if mean_fitness > best_fitness:
            best_fitness = mean_fitness
            best_params = param_dict

    print("Best mean fitness:", best_fitness)
    print("Best parameters:", best_params)




def s3840220_s3841863_GA(problem, ):
    budget = 5000

    f_opt = problem.state.evaluations
    x_opt = None

    parent = []
    parent_f = []
    # initial_pop = ... make sure you randomly create the first population
    for i in range(pop_size):
        initial_pop = np.random.randint(2, size=(dimension))
        parent.append(initial_pop)
   
    # `problem.state.evaluations` counts the number of function evaluation automatically,
    # which is incremented by 1 whenever you call `problem(x)`.
    # You could also maintain a counter of function evaluations if you prefer.
        initial_pop_f = np.array(problem(initial_pop))
        parent_f.append(initial_pop_f)
        budget = budget - 1

    while problem.state.evaluations < budget:
        # please implement the mutation, crossover, selection here
        offspring = proportional_seletion(parent,parent_f)
        
        for i in range(0,pop_size - (pop_size%2),2) :
            uniform_crossover(offspring[i], offspring[i+1])


        for i in range(pop_size):
            bit_flip_mutation(offspring[i])

        parent = offspring.copy()
        for i in range(pop_size) : 
            parent_f[i] = problem(parent[i])
            budget = budget - 1
            if parent_f[i] > f_opt:
                    f_opt = parent_f[i]
                    x_opt = parent[i].copy()
        
        # this is how you evaluate one solution `x`
        # f = problem(x)
    # no return value needed 
    problem.reset()
    print(f_opt)
    # return f_opt, x_opt



def create_problem(fid: int):
    # Declaration of problems to be tested.
    problem = get_problem(fid, dimension=dimension, instance=1, problem_class=ProblemClass.PBO)

    # Create default logger compatible with IOHanalyzer
    # `root` indicates where the output files are stored.
    # `folder_name` is the name of the folder containing all output. You should compress the folder 'run' and upload it to IOHanalyzer.
    l = logger.Analyzer(
        root="data",  # the working directory in which a folder named `folder_name` (the next argument) will be created to store data
        folder_name="run",  # the folder name to which the raw performance data will be stored
        algorithm_name="genetic_algorithm",  # name of your algorithm
        algorithm_info="Practical assignment of the EA course",
    )
    # attach the logger to the problem
    problem.attach_logger(l)
    return problem, l


if __name__ == "__main__":
    # this how you run your algorithm with 20 repetitions/independent run
    F18, _logger = create_problem(18)
    for run in range(20): 
        s3840220_s3841863_GA(F18)
        F18.reset() # it is necessary to reset the problem after each independent run
    _logger.close() # after all runs, it is necessary to close the logger to make sure all data are written to the folder

    F19, _logger = create_problem(19)
    for run in range(20): 
        s3840220_s3841863_GA(F19)
        F19.reset()
    _logger.close()