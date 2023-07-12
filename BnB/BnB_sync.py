import os
import time
import bisect
import numpy as np
import copy
import xlsxwriter


XLSX_FILE_NAME_WITH_PATH = os.path.dirname(__file__) + r'/' + 'inputs_results_temp.xlsx'
FILE_WITH_INPUTS = os.path.dirname(__file__) + r'/' + '8_inputs_final.txt'
FILE_NAME_WITH_PATH_SAVE = None
BEST_CURRENT_SOLUTION = None
NUMBER_OF_NODES_VISITED = 0
NUMBER_OF_MACHINES = None
K_NUMBER = None


def getJobsObj(jobs_as_string):
    jobsObj = getJobsObjAsListFromString(jobs_as_string)
    return jobsObj

def updateXLSXFileWithResults(results):
    workbook = xlsxwriter.Workbook(XLSX_FILE_NAME_WITH_PATH)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Input Index')
    worksheet.write('B1', 'OPT maxspan (if possible)')
    worksheet.write('C1', 'Maxspan')
    worksheet.write('D1', 'Number of nodes visited')
    worksheet.write('E1', 'Excecution time')
    for result in results:
        input_index = int(result['input_index'])
        row = input_index + 1
        worksheet.write('A' + str(row), input_index)
        worksheet.write('B' + str(row), result['opt_maxspan'])
        worksheet.write('C' + str(row), result['maxspan'])
        worksheet.write('D' + str(row), result['number_of_nodes'])
        worksheet.write('E' + str(row), result['excecution_time'])
    workbook.close()

def createXLSXFileWithPropertiesOfInputs(inputs):
    workbook = xlsxwriter.Workbook(XLSX_FILE_NAME_WITH_PATH)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Input Index')
    worksheet.write('B1', 'Number of machines')
    worksheet.write('C1', 'K number')
    for input_index, input in enumerate(inputs):
        row = input_index + 2
        worksheet.write('A' + str(row), input_index+2)
        worksheet.write('B' + str(row), input['number_of_machines'])
        worksheet.write('C' + str(row), input['K'])
    workbook.close()

def getJobsObjAsListFromString(jobsAsString: str):
    jobsForReturn = []
    jobsAsString = jobsAsString.replace('[', '')
    jobsAsString = jobsAsString.replace(']', '')
    jobsAsList = jobsAsString.split(',')
    sumOfAllJobs = 0
    for jobAsString in jobsAsList:
        job_index = int(jobAsString.split('(')[1].replace(')', ''))
        job_time = int(jobAsString.split('(')[0])
        bisect.insort(jobsForReturn, {'index': job_index, 'time': job_time}, key=lambda job: -1 * job['time'])
        sumOfAllJobs += job_time
    jobsObjForReturn = {'jobs': jobsForReturn, 'current_sum_of_all_jobs_times': sumOfAllJobs, 'sum_of_all_jobs_times': sumOfAllJobs}
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
        k_number = int(input_text.split('K number (allowed number of jobs on machine, except #1):')[1].strip())
        input_obj = {'jobs_string' : jobs_string, 'K' : k_number, 'number_of_machines' : number_of_machines}
        inputs_objects.append(input_obj)
    return inputs, inputs_objects

def makeLPTSolution(system, jobs):
    # LPT
    while True:
        if len(jobs) == 0:
            break
        for machine in reversed(system['machines']):
            if isMachineHaveFreeSpace(machine):
                addJobToMachine(jobs[0], machine)
                jobs.remove(jobs[0])
                break
        sortMachinesInSystemViaSpan(system, isReversed=True)
    system['maxspan'] = getMaxspan(system)
    return system

def sortMachinesInSystemViaSpan(system, isReversed = False):
        system['machines'].sort(key=lambda machine: machine.get('span'), reverse = isReversed)

def getNewFreeSystem():
    system = {'machines' : [], 'maxspan' : 0, 'free_space_in_other_machines': K_NUMBER*(NUMBER_OF_MACHINES-1)}
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

def isMachineHaveFreeSpace(machine):
    if machine['jobs_count'] < K_NUMBER or machine['index'] == 1:
        return True
    else:
        return False

def sortMachinesInSystemViaIndex(system, isReversed = False):
        system['machines'].sort(key=lambda machine: machine.get('index'), reverse = isReversed)

def addJobToMachine(job, machine):
    bisect.insort(machine['jobs'], job, key=lambda job: -1 * job['time'])
    machine['span'] += job['time']
    machine['jobs_count'] += 1

def removeJobFromMachine(job, machine):
    machine['jobs'].remove(job)
    machine['span'] -= job['time']
    machine['jobs_count'] -= 1

def getBeautifullPrint(system):
    sortMachinesInSystemViaIndex(system)
    text = '################################\nMaxspan: ' + str(system['maxspan']) + '\n' + \
           '********************************\n'
    for machine in system['machines']:
        text += ('Machine #' + str(machine['index']) + ': ' + getJobsAsString(machine['jobs']) + '; Jobs: ' + str(machine['jobs_count']) + '; Time: ' + str(machine['span'])) + '\n'
    text += '################################\n'
    return text

def getMin(system, jobs_obj):
    min = system['opt_solution']
    if min < system['maxspan']:
        min = system['maxspan']
    if len(jobs_obj['jobs']) > 0:
        if min < jobs_obj['jobs'][0]['time']:
            min = jobs_obj['jobs'][0]['time']

    possible_maximum_sum_of_jobs_in_other_machines = 0
    for i in range(system['free_space_in_other_machines']):
        try:
            possible_maximum_sum_of_jobs_in_other_machines += jobs_obj['jobs'][i]['time']
        except:
            break
    final_value = jobs_obj['current_sum_of_all_jobs_times'] - possible_maximum_sum_of_jobs_in_other_machines
    if min < final_value:
        min = final_value
    return min

def getJobFromJobsObj(jobs_obj):
    job_to_move = jobs_obj['jobs'][0]
    jobs_obj['jobs'].remove(job_to_move)
    jobs_obj['current_sum_of_all_jobs_times'] -= job_to_move['time']
    return job_to_move

def returnJobToJobsObj(job, jobs_obj):
    bisect.insort(jobs_obj['jobs'], job, key=lambda job: -1 * job['time'])
    jobs_obj['current_sum_of_all_jobs_times'] += job['time']

def addOneJobToMachine(node, job_to_add, machine):
    addJobToMachine(job_to_add, machine)
    node['maxspan'] = getMaxspan(node)
    if machine['index'] != 1:
        node['free_space_in_other_machines'] -= 1

def removeOneJobFromMachine(node, job_to_remove, machine):
    removeJobFromMachine(job_to_remove, machine)
    node['maxspan'] = getMaxspan(node)
    if machine['index'] != 1:
        node['free_space_in_other_machines'] += 1

def checkForSymmetry(machines):
    list_of_machines_to_skip = []
    for machine_1 in machines:
        for machine_2 in machines:
            if machine_1['index'] == 1 or machine_2['index'] == 1 or machine_1['index'] == machine_2['index']:
                continue
            if machine_1['span'] == machine_2['span'] and machine_1['jobs_count'] == machine_2['jobs_count']:
                if machine_1['index'] not in list_of_machines_to_skip and machine_2['index'] not in list_of_machines_to_skip:
                    list_of_machines_to_skip.append(machine_2['index'])
    return list_of_machines_to_skip

def getMaxAndCheckBestSolution(system, jobs_obj, node_index):
    global BEST_CURRENT_SOLUTION
    current_lpt_solution_system = makeLPTSolution(copy.deepcopy(system), copy.deepcopy(jobs_obj['jobs']))
    if current_lpt_solution_system['maxspan'] < BEST_CURRENT_SOLUTION['maxspan']:
        BEST_CURRENT_SOLUTION = current_lpt_solution_system
        print(getBeautifullPrint(BEST_CURRENT_SOLUTION))
    return current_lpt_solution_system['maxspan']

def BnB_findSolution(node: dict, jobs_obj):
    global BEST_CURRENT_SOLUTION, NUMBER_OF_NODES_VISITED
    NUMBER_OF_NODES_VISITED += 1
    node_index = NUMBER_OF_NODES_VISITED
    min = getMin(node, jobs_obj)
    if min >= BEST_CURRENT_SOLUTION['maxspan']:
        return
    max = getMaxAndCheckBestSolution(node, jobs_obj, node_index)
    if BEST_CURRENT_SOLUTION['maxspan'] == node['opt_solution']:
        raise Exception('Optimal solution found!')
    if min == max:
        return
    if len(jobs_obj['jobs']) == 0:
        return
    job = getJobFromJobsObj(jobs_obj)
    machine_indexes_to_pass = checkForSymmetry(node['machines'])
    for machine in node['machines']:
        if machine['index'] in machine_indexes_to_pass:
            continue
        if isMachineHaveFreeSpace(machine):
            addOneJobToMachine(node, job, machine)
            BnB_findSolution(node, jobs_obj)
            removeOneJobFromMachine(node, job, machine)
    returnJobToJobsObj(job, jobs_obj)

def main(input):
    global BEST_CURRENT_SOLUTION, NUMBER_OF_MACHINES, K_NUMBER
    NUMBER_OF_MACHINES = input['number_of_machines']
    K_NUMBER = input['K']
    jobs_obj = getJobsObj(input['jobs_string'])
    root = getNewFreeSystem()
    root['opt_solution'] = int(np.ceil(jobs_obj['sum_of_all_jobs_times']/NUMBER_OF_MACHINES))
    root['is_K_limits'] = K_NUMBER < int(np.ceil(len(jobs_obj['jobs'])/NUMBER_OF_MACHINES))
    initial_solution = makeLPTSolution(copy.deepcopy(root), copy.deepcopy(jobs_obj['jobs']))
    BEST_CURRENT_SOLUTION = initial_solution
    try:
        BnB_findSolution(root, jobs_obj)
    except Exception as e:
        if 'Optimal solution found!' not in str(e):
            print(str(e))

    system_best_solution = BEST_CURRENT_SOLUTION

    return system_best_solution['opt_solution'], system_best_solution['maxspan'], NUMBER_OF_NODES_VISITED

def getJobsString(j):
    jobs = []
    index = 1
    sumOfAllJobs = 0
    for i in range(1, j+1):
        time = 1
        bisect.insort(jobs, {'index': index, 'time': time}, key=lambda job: -1 * job['time'])
        sumOfAllJobs += time
        index += 1
    return getJobsAsString(jobs)
    
if __name__ == '__main__':
    results = []
    inputs, inputs_objects = getInputsFromFile()
    for input_number, input in enumerate(inputs_objects):
        start_time = time.time()
        opt_maxspan, maxspan, number_of_nodes = main(input)
        executuon_time = str(time.time() - start_time)
        if executuon_time == '0.0':
            executuon_time = '<0.0001'
        results.append({'opt_maxspan': opt_maxspan, 'maxspan': maxspan, 'number_of_nodes': number_of_nodes, 'excecution_time': executuon_time, 'input_index': input_number+1})
        FILE_NAME_WITH_PATH_SAVE = None
        BEST_CURRENT_SOLUTION = None
        NUMBER_OF_NODES_VISITED = 0
        NUMBER_OF_MACHINES = None
        K_NUMBER = None
    updateXLSXFileWithResults(results)