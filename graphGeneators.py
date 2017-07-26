# Author: Tim, Ginny
# 2017-07-05


import matplotlib.pyplot as plt
import numpy as np
import setting

trace = 'Workload_Traces_test'

time_dir = "results/time_elapsed"
resourceUtilization_dir = "results/resourceUtilization/"
firstFailure_dir = "results/firstFailure/"
unused_dir = "results/unusedMachines/"
firstStageMachine_dir = setting.firstStageMachine_dir

Algorithms = ["First Fit", "Multi Resource Alignment", "Two Stage Best Fit", "EAGLE", "EAGLE MOD"]
# Algorithms = ["EAGLE", "EAGLE MOD"]

'''

THE CODE BELOW GENERATES A CDF FOR CPU UTILIZATION AFTER ALL REQUESTS ARE HANDLED

'''

for algorithm in Algorithms:
    filename = resourceUtilization_dir + algorithm + "/Resource Utilization"
    with open(filename, 'r') as f:
        list = []
        for line in f:
            value = line.rstrip('\n').split('\t')
            CPU_usage = float(value[1])
            list.append(CPU_usage)

    sorted_data = np.sort(list)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data))
    plt.plot(sorted_data, yvals, label=algorithm)
    plt.legend(loc=0)

plt.title('CPU Utilization CDF')
plt.xlabel('CPU Utilization')
plt.ylabel('CDF')

plt.show()

'''

THE CODE BELOW GENERATES A BAR GRAPH FOR AVERAGE CPU UTILIZATION AFTER ALL REQUESTS ARE HANDLED

'''
CPU_average = {}

for algorithm in Algorithms:
    filename = resourceUtilization_dir + algorithm + "/Mean"
    with open(filename, 'r') as f:
        for line in f:
            value = line.rstrip('\n').split('\t')
            CPU_average[value[0]] = float(value[1])

plt.bar(range(len(CPU_average)), CPU_average.values(), align='center')
plt.xticks(range(len(CPU_average)), CPU_average.keys(), rotation=10)

plt.title('Average CPU Utilization')
plt.xlabel('Algorithms')
plt.ylabel('Average CPU Utilization Percentage')

plt.show()

'''

THE CODE BELOW GENERATES A CDF FOR MEMORY UTILIZATION AFTER ALL REQUESTS ARE HANDLED

'''
for algorithm in Algorithms:
    filename = resourceUtilization_dir + algorithm + "/Resource Utilization"
    with open(filename, 'r') as f:
        list = []
        for line in f:
            value = line.rstrip('\n').split('\t')
            mem_usage = float(value[2])
            list.append(mem_usage)

    sorted_data = np.sort(list)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data))
    plt.plot(sorted_data, yvals, label=algorithm)
    plt.legend(loc=0)

plt.title('Memory Utilization CDF')
plt.xlabel('Memory Utilization')
plt.ylabel('CDF')

plt.show()

'''

THE CODE BELOW GENERATES A BAR GRAPH FOR AVERAGE MEMORY UTILIZATION AFTER ALL REQUESTS ARE HANDLED

'''
Mem_average = {}

for algorithm in Algorithms:
    filename = resourceUtilization_dir + algorithm + "/Mean"
    with open(filename, 'r') as f:
        for line in f:
            value = line.rstrip('\n').split('\t')
            Mem_average[value[0]] = float(value[2])

plt.bar(range(len(Mem_average)), Mem_average.values(), align='center')
plt.xticks(range(len(Mem_average)), Mem_average.keys(), rotation=10)

plt.title('Average Memory Utilization')
plt.xlabel('Algorithms')
plt.ylabel('Average Memory Utilization Percentage')

plt.show()

'''

THE CODE BELOW GENERATES A BAR GRAPH FOR CPU UTILIZATION VARIANCE AFTER ALL REQUESTS ARE HANDLED

'''
Variance = {}

for algorithm in Algorithms:
    filename = resourceUtilization_dir + algorithm + "/Variance"
    with open(filename, 'r') as f:
        for line in f:
            value = line.rstrip('\n').split('\t')
            Variance[value[0]] = float(value[1])

plt.bar(range(len(Variance)), Variance.values(), align='center')
plt.xticks(range(len(Variance)), Variance.keys(), rotation=10)

plt.title('CPU Utilization Variance')
plt.xlabel('Algorithms')
plt.ylabel('CPU Utilization Variance')

plt.show()

'''

THE CODE BELOW GENERATES A BAR GRAPH FOR MEMORY UTILIZATION VARIANCE AFTER ALL REQUESTS ARE HANDLED

'''
Variance = {}

for algorithm in Algorithms:
    filename = resourceUtilization_dir + algorithm + "/Variance"
    with open(filename, 'r') as f:
        for line in f:
            value = line.rstrip('\n').split('\t')
            Variance[value[0]] = float(value[2])

plt.bar(range(len(Variance)), Variance.values(), align='center')
plt.xticks(range(len(Variance)), Variance.keys(), rotation=10)

plt.title('Memory Utilization Variance')
plt.xlabel('Algorithms')
plt.ylabel('Memory Utilization Variance')

plt.show()

'''


THE CODE BELOW GENERATES GRAPH FOR UNUSED MACHINES AFTER ALL TASKS PLACED


'''
machine_num = {}
for algorithm in Algorithms:
    filename = unused_dir + algorithm
    with open(filename, 'r') as f:
        for line in f:
            value = line.rstrip('\n').split('\t')
            numberOfVM = int(value[2])
            machine_num[algorithm] = numberOfVM

plt.bar(range(len(machine_num)), machine_num.values(), align='center')
plt.xticks(range(len(machine_num)), machine_num.keys(), rotation=10)
plt.title('Unused Machines Number')
plt.ylabel('# of Un-used Machines')
plt.show()

'''


THE CODE BELOW GENERATES GRAPH FOR MACHINES IN FIRST STAGE AFTER ALL TASKS PLACED


'''
machine_num = {}
for algorithm in Algorithms:
    filename = firstStageMachine_dir + algorithm
    with open(filename, 'r') as f:
        for line in f:
            value = line.rstrip('\n').split('\t')
            machine_num[value[0]] = int(value[1])

plt.bar(range(len(machine_num)), machine_num.values(), align='center')
plt.xticks(range(len(machine_num)), machine_num.keys(), rotation=10)
plt.title('Machines in First Stage')
plt.ylabel('# of Machines')
plt.show()

#
# '''
#
#
# THE CODE BELOW GENERATES A GRAPH FOR ALGORITHM EFFICIENCY
#
#
# '''
# filename = time_dir
#
# with open (filename, 'r') as f:
#     algorithms = []
#     time = {}
#
#     with open(filename, 'r') as f:
#         for line in f:
#             result = line.rstrip('\n').split('\t')
#             if result[0] not in algorithms:
#                 time[result[0]] = result[1]
#
# plt.bar(range(len(time)), time.values(), align='center')
# plt.xticks(range(len(time)), time.keys())
#
# plt.title('Algorithm Efficiency')
# plt.xlabel('Algorithms')
# plt.ylabel('Time Elapsed(s)')
# plt.legend()
#
# plt.show()


# filename = time_dir
#
# with open (filename, 'r') as f:
#     algorithms = []
#     time = {}
#
#     with open(filename, 'r') as f:
#         for line in f:
#             result = line.rstrip('\n').split('\t')
#             if result[0] not in algorithms:
#                 algorithms.append(result[0])
#                 time_ = []
#                 time_.append(float(result[1]))
#                 time[result[0]] = time_
#             else:
#                 time[result[0]].append(float(result[1]))
#
# for element in algorithms:
#     plt.plot(time.get(element), label="%s" % element)
#
# plt.title('Algorithm Efficiency')
# plt.xticks(range(10), range(100, 2100, 200))
# plt.xlabel('Algorithms')
# plt.ylabel('Time Elapsed(s)')
# plt.legend()
#
# plt.show()
#
'''


THE CODE BELOW GENERATES A GRAPH FOR AVERAGE RESOURCE FRAGMENTATION


'''
res_fragmentation = {}
for algorithm in Algorithms:
    filename = setting.resource_fraction_dir + algorithm + "/Resource Fraction Mean"
    with open(filename, 'r') as f:
        for line in f:
            value = line.rstrip('\n').split('\t')
            res_fragmentation[algorithm] = float(value[1])

plt.bar(range(len(res_fragmentation)), res_fragmentation.values(), align='center')
plt.xticks(range(len(res_fragmentation)), res_fragmentation.keys(), rotation=10)

plt.title('Average Resource Fragmentation')
plt.xlabel('Algorithms')
plt.ylabel('Resource Fragmentation Ratio')
# plt.legend()

plt.show()

'''


THE CODE BELOW GENERATES A CDF FOR RESOURCE FRAGMENTATION


'''

for algorithm in Algorithms:
    filename = setting.resource_fraction_dir + algorithm + "/Resource Fraction"
    with open(filename, 'r') as f:
        list = []
        for line in f:
            value = line.rstrip('\n').split('\t')
            fragmentation = float(value[2])
            list.append(fragmentation)
    sorted_data = np.sort(list)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
    plt.plot(sorted_data, yvals, label=algorithm)
    plt.legend()

plt.title('Resource Fragmentation CDF')
plt.xlabel('Resource Fragmentation')
plt.ylabel('CDF')

plt.show()

'''


THE CODE BELOW GENERATES A GRAPH FOR FAILURE NUMBER


'''
failures = {}
for algorithm in Algorithms:
    filename = setting.failure_dir + algorithm
    with open(filename, 'r') as f:
        for line in f:
            value = line.rstrip('\n').split('\t')
            failures[algorithm] = float(value[1])

plt.bar(range(len(failures)), failures.values(), align='center')
plt.xticks(range(len(failures)), failures.keys(), rotation=10)

plt.title('Failure Tasks')
plt.xlabel('Algorithms')
plt.ylabel('Failure Tasks Number')
# plt.legend()

plt.show()
