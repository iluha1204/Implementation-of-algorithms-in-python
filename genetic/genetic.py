import os, shutil
import time
import numpy as np
import copy
import random
from tqdm import tqdm

FILE_WITH_INPUTS = os.path.dirname(__file__) + r'/' + '5000.txt'
NUMBER_OF_MACHINES = None
TEXT_TO_PRINT = ''

#Genetic algorithm properties
POPULATION_SIZE = 100
NUMBER_OF_CHROMOSOMES_FOR_MUTATION = int(POPULATION_SIZE*0.02)
GENERATIONS = 1000
MUTATION_RATE = 0.001
PRINT_EVERY_TH_POPULATION = GENERATIONS//10

def getJobsObj(jobs_as_string):
    jobsObj = getJobsObjAsListFromString(jobs_as_string)
    return jobsObj

def getJobsObjAsListFromString(jobsAsString: str):
    jobsForReturn = []
    jobsAsString = jobsAsString.replace('[', '')
    jobsAsString = jobsAsString.replace(']', '')
    jobsAsList = jobsAsString.split(',')
    sumOfAllJobs = 0
    for jobAsString in jobsAsList:
        job_index = int(jobAsString.split('(')[1].replace(')', ''))
        job_time = int(jobAsString.split('(')[0])
        jobsForReturn.append({'index': job_index, 'time': job_time})
        sumOfAllJobs += job_time
    jobsForReturn.sort(key=lambda job: job.get('index'), reverse = False)
    jobsObjForReturn = {'jobs': jobsForReturn, 'sum_of_all_jobs_times': sumOfAllJobs, 'number_of_jobs': len(jobsForReturn)}
    return jobsObjForReturn

def getInputsFromFile():
    inputs = []
    with open(FILE_WITH_INPUTS, 'r') as f:
        file_text = f.read()
        index = 1
        while True:
            try:
                input = file_text.split(str(index)+'.')[1].split(str(index + 1)+'.')[0]
                inputs.append(input.strip())
                file_text = file_text.split(input)[1].strip()
                index += 1
            except:
                break
    inputs_objects = []
    for input in inputs:
        input_text = copy.deepcopy(input)
        jobs_string = input_text.split('Jobs (time(index)):')[1].split('Number of machines:')[0].strip()
        input_text = input_text.split(jobs_string)[1]
        number_of_machines = int(input_text.split('Number of machines:')[1].split('K number')[0].strip())
        input_text = input_text.split(f'Number of machines: {str(number_of_machines)}')[1]
        input_obj = {'jobs_string' : jobs_string, 'number_of_machines' : number_of_machines}
        inputs_objects.append(input_obj)
    return inputs, inputs_objects

def getNewFreeSystem():
    system = {'machines' : [], 'maxspan' : 0}
    for j in range(1, NUMBER_OF_MACHINES+1):
        system['machines'].append({'jobs' : [], 'jobs_count': 0, "span" : 0, 'index': j})
    return system

def getMaxspan(system):
    maxspan = 0
    for machine in system['machines']:
        if maxspan < machine['span']:
            maxspan = machine['span']
    return maxspan

def getJobsAsString(jobs):
    jobs_as_string = '['
    is_first_job = True
    for job in jobs:
        if is_first_job:
            jobs_as_string += str(job['time']) + '(' + str(job['index']) + ')'
            is_first_job = False
        else:
            jobs_as_string += ', ' + str(job['time']) + '(' + str(job['index']) + ')'
    if jobs_as_string == '[':
        jobs_as_string += 'No jobs'
    jobs_as_string += ']'
    return jobs_as_string

def getJobsFromMachinesToArray(system):
    jobs = []
    for machine in system['machines']:
        for job in machine['jobs']:
            jobs.append(job)
    jobs.sort(key=lambda job: job.get('index'))
    return jobs

def sortMachinesInSystemViaIndex(system, isReversed = False):
        system['machines'].sort(key=lambda machine: machine.get('index'), reverse = isReversed)

def addJobToMachine(job, machine):
    machine['jobs'].append(job)
    machine['span'] += job['time']
    machine['jobs_count'] += 1

def systemToString(system):
    sortMachinesInSystemViaIndex(system)
    text = '################################\nMaxspan: ' + str(system['maxspan']) + '\n' + \
           'OPT MAXSPAN (if possible): ' + str(system['opt_solution']) + '\n' + \
           '********************************\n'
    for machine in system['machines']:
        text += ('Machine #' + str(machine['index']) + ': ' + getJobsAsString(machine['jobs']) + '; Jobs: ' + str(machine['jobs_count']) + '; Time: ' + str(machine['span'])) + '\n'
    text += '################################'
    return text

def addOneJobToMachine(system, job_to_add, machine):
    addJobToMachine(job_to_add, machine)
    system['maxspan'] = getMaxspan(system)

def getMachineIndexesString():
    indexes = ''
    for i in range(NUMBER_OF_MACHINES):
        indexes += str(i)
    return indexes

def getSystemToChromosomeString(system, number_of_jobs):
    indexes = [None]*number_of_jobs
    for machine in system['machines']:
        for job in machine['jobs']:
            indexes[job['index']-1] = str(machine['index']-1)
    chromosome_string = ''.join(indexes)
    return {'string': chromosome_string, 'fitness': system['opt_solution']/system['maxspan']}

def fitnessFucntion(system):
    # return 1/system['maxspan'] #1
    # return 1/(system['maxspan']**4) #2
    # return 1/((system['maxspan'] - system['opt_solution'] + 1)**2) #3
    return 1/(2**((system['maxspan'] - system['opt_solution'])**(1/4))) #4

def getChromosomeFitness(chromosome_string, jobs, free_system): 
    for job_index, char in enumerate(chromosome_string):
        addOneJobToMachine(free_system, jobs[job_index], free_system['machines'][int(char)])
    return fitnessFucntion(free_system), free_system['maxspan']

def initializePopulation(jobs_obj, free_system):
    population = []
    machines_indexes = getMachineIndexesString()
    interval_start = 0
    for _ in range(POPULATION_SIZE):
        chromosome_string = ''.join(random.choices(machines_indexes, k = jobs_obj['number_of_jobs'])) 
        chromosome_fitness, maxspan = getChromosomeFitness(chromosome_string, jobs_obj['jobs'], copy.deepcopy(free_system))
        interval_end = interval_start + chromosome_fitness
        chromosome_interval = (interval_start, interval_end)
        chromosome = {'string': chromosome_string, 'fitness': chromosome_fitness, 'maxspan': maxspan, 'interval': chromosome_interval, 'index': _+1}
        population.append(chromosome)
        interval_start = interval_end
    return population, interval_end

def mutate(chromosome, jobs, free_system):
    new_chromosome_string = ''
    for char in chromosome['string']:
        if random.random() < MUTATION_RATE:
            new_chromosome_string += str(random.randint(0, NUMBER_OF_MACHINES-1))
        else:
            new_chromosome_string += char
    chromosome_fitness, maxspan = getChromosomeFitness(new_chromosome_string, jobs, copy.deepcopy(free_system))
    return {'string': new_chromosome_string, 'fitness': chromosome_fitness, 'maxspan': maxspan}

def getMutatedCromosomes(population, jobs, free_system, sum_of_all_fitnesses):
    list_of_chromosomes = []
    while True:
        random_float = random.uniform(0, sum_of_all_fitnesses)
        random_chromosome = getRandomChromosomeFromPopulationViaBinarySearch(random_float, population)
        if random_chromosome not in list_of_chromosomes:
            list_of_chromosomes.append(random_chromosome)
            if len(list_of_chromosomes)==NUMBER_OF_CHROMOSOMES_FOR_MUTATION:
                break
    new_interval_start = 0
    list_of_mutated_chromosomes = []
    for index, chromosome in enumerate(list_of_chromosomes):
        mutaded_chromosome = mutate(chromosome, jobs, free_system)
        new_interval_end = new_interval_start + mutaded_chromosome['fitness']
        mutaded_chromosome['interval'] = (new_interval_start, new_interval_end)
        mutaded_chromosome['index'] = index + 1
        list_of_mutated_chromosomes.append(mutaded_chromosome)
        new_interval_start = new_interval_end
    return list_of_mutated_chromosomes, new_interval_end

def binarySearch(population, low, high, random_float):
    mid = (high + low) // 2
    if population[mid]['interval'][0] <= random_float and random_float < population[mid]['interval'][1]:
        return population[mid]
    elif population[mid]['interval'][0] > random_float:
        return binarySearch(population, low, mid - 1, random_float)
    elif population[mid]['interval'][1] <= random_float:
        return binarySearch(population, mid + 1, high, random_float)
    
def getRandomChromosomeFromPopulationViaBinarySearch(random_float, population):
    lower_index = 0
    higher_index = POPULATION_SIZE-1
    return binarySearch(population, lower_index, higher_index, random_float)
    
def selectParents(population, sum_of_all_fitnesses):
    selected_parents = []
    while True:
        random_float = random.uniform(0, sum_of_all_fitnesses)
        random_chromosome = getRandomChromosomeFromPopulationViaBinarySearch(random_float, population)
        if random_chromosome not in selected_parents:
            selected_parents.append(random_chromosome)
            if len(selected_parents)==2:
                break
    return selected_parents[0], selected_parents[1]

def crossover(parent1, parent2, jobs_obj, free_system):
    point1 = random.randint(0, jobs_obj['number_of_jobs'] - 1)
    point2 = random.randint(point1, jobs_obj['number_of_jobs'] - 1)
    child1_string = parent1['string'][:point1] + parent2['string'][point1:point2] + parent1['string'][point2:]
    child2_string = parent2['string'][:point1] + parent1['string'][point1:point2] + parent2['string'][point2:]
    child1_fitness, child1_maxspan = getChromosomeFitness(child1_string, jobs_obj['jobs'], copy.deepcopy(free_system))
    child2_fitness, child2_maxspan = getChromosomeFitness(child2_string, jobs_obj['jobs'], copy.deepcopy(free_system))                                                
    child1 = {'string': child1_string, 'fitness': child1_fitness, 'maxspan': child1_maxspan}
    child2 = {'string': child2_string, 'fitness': child2_fitness, 'maxspan': child2_maxspan}
    return child1, child2

def getOffspring(population, jobs_obj, free_system, sum_of_all_fitnesses, new_sum_of_all_fitnesses):
    offspring = []
    new_interval_start = new_sum_of_all_fitnesses
    index_start = NUMBER_OF_CHROMOSOMES_FOR_MUTATION+1
    for _ in range((POPULATION_SIZE-NUMBER_OF_CHROMOSOMES_FOR_MUTATION)//2):
        parent1, parent2 = selectParents(population, sum_of_all_fitnesses)
        child1, child2 = crossover(parent1, parent2, jobs_obj, free_system)
        new_interval_end = new_interval_start + child1['fitness']
        child1['interval'] = (new_interval_start, new_interval_end)
        child1['index'] = index_start
        offspring.append(child1)
        new_interval_start = new_interval_end
        new_interval_end = new_interval_start + child2['fitness']
        child2['interval'] = (new_interval_start, new_interval_end)
        child2['index'] = index_start+1
        offspring.append(child2)
        new_interval_start = new_interval_end
        index_start += 2
    return offspring, new_interval_end

def getSystemFromChromosome(chromosome_string,  free_system, jobs):
    for job_index, char in enumerate(chromosome_string):
        addOneJobToMachine(free_system, jobs[job_index], free_system['machines'][int(char)])
    return free_system

def chromosomeToString(chromosome, only_index=False):
    index_text = f'[{chromosome["index"]}]'
    if only_index:
        return index_text
    text = f'{index_text}[String: {chromosome["string"]}, Maxspan: {chromosome["maxspan"]}, Fitness: {chromosome["fitness"]}]'
    return text

def populationToString(population):
    text = ''
    for chromosome in population:
        text += chromosomeToString(chromosome) + '\n'
    return text

def getNumberOfDublicates(population):
    list_of_string = []
    for chromosome in population:
        if chromosome['string'] not in list_of_string:
            list_of_string.append(chromosome['string'])
    return len(list_of_string)

def doGeneticAlgorithm(free_system, jobs_obj):
    global TEXT_TO_PRINT
    if not os.path.isdir(os.path.dirname(__file__) + r'/' + 'population'):
        os.mkdir(os.path.dirname(__file__) + r'/' + 'population')
    else:
        shutil.rmtree(os.path.dirname(__file__) + r'/' + 'population')
        os.mkdir(os.path.dirname(__file__) + r'/' + 'population')
    if os.path.exists(os.path.dirname(__file__) + r'/' + 'unique_chromosomes.txt'):
        os.remove(os.path.dirname(__file__) + r'/'  + 'unique_chromosomes.txt')
    if os.path.exists(os.path.dirname(__file__) + r'/' + 'output.txt'):
        os.remove(os.path.dirname(__file__) + r'/'  + 'output.txt')

    population, sum_of_all_fitnesses = initializePopulation(jobs_obj, free_system)
    for generation_index in tqdm(range(GENERATIONS)):
        # if (generation_index+1)%PRINT_EVERY_TH_POPULATION==0:
        #     with open(os.path.dirname(__file__) + r'/population/' + str(generation_index+1) + '.txt', 'w') as file_save_population:
        #         file_save_population.write(f'Number of unique chromosomes is {getNumberOfDublicates(population)}\n\n{populationToString(population)}')
        # with open(os.path.dirname(__file__) + r'/' + 'unique_chromosomes' + '.txt', 'a') as file_save_uniq:
        #     file_save_uniq.write(f'Number of unique chromosomes in population {generation_index+1} is {getNumberOfDublicates(population)}.\n')
        list_of_mutated_chromosomes, new_sum_of_all_fitnesses = getMutatedCromosomes(population, jobs_obj['jobs'], free_system, sum_of_all_fitnesses)
        offspring, new_sum_of_all_fitnesses= getOffspring(population, jobs_obj, free_system, sum_of_all_fitnesses, new_sum_of_all_fitnesses)
        population = list_of_mutated_chromosomes + offspring
        sum_of_all_fitnesses = new_sum_of_all_fitnesses
    population.sort(key=lambda chromosome: chromosome.get('fitness'), reverse = True)
    best_chromosome = population[0]
    TEXT_TO_PRINT += f'Best chromosome is {chromosomeToString(best_chromosome)}.\n'
    return best_chromosome

def main(input):
    global NUMBER_OF_MACHINES, TEXT_TO_PRINT
    NUMBER_OF_MACHINES = input['number_of_machines']
    jobs_obj = getJobsObj(input['jobs_string'])
    free_system = getNewFreeSystem()
    free_system['opt_solution'] = int(np.ceil(jobs_obj['sum_of_all_jobs_times']/NUMBER_OF_MACHINES))
    best_chromosome = doGeneticAlgorithm(free_system, jobs_obj)
    best_found_solution = getSystemFromChromosome(best_chromosome['string'], free_system, jobs_obj['jobs'])
    TEXT_TO_PRINT += f'Best system found:\n{systemToString(best_found_solution)}\n'
    print(systemToString(best_found_solution))

def getAverageNumberOfChromosomes():
    values = []
    with open(os.path.dirname(__file__) + r'/' + 'unique_chromosomes.txt') as file:
        file_text = file.read()
        index = 1
        while True:
            value = int(file_text.split('.')[0].split(f'Number of unique chromosomes in population {index} is ')[1])
            values.append(value)
            file_text = file_text.replace(f'Number of unique chromosomes in population {index} is {value}.', '').strip()
            index += 1
            if index>GENERATIONS:
                break
    print(sum(values)/len(values))

if __name__ == '__main__':

    # getAverageNumberOfChromosomes()
    # quit()

    results = []
    inputs, inputs_objects = getInputsFromFile()
    for input_number, input in enumerate(inputs_objects):
        start_time = time.time()
        main(input)
        executuon_time = str(time.time() - start_time)
        TEXT_TO_PRINT += f'Execution time {executuon_time}\n'
        print(f'Execution time {executuon_time}\n')

    with open(os.path.dirname(__file__) + r'/' + 'output.txt', 'w') as file_save:
        file_save.write(TEXT_TO_PRINT)