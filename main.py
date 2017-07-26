
'''

Author: Tim Ming Da Li, Ginny JI
Last Modified: July 6, 2017

This is where the main code of the simulator starts, different scheduler classes
are instantiated inside "placement_schedulers" before the simulation strats running.

For a detailed break-down of the structure of the simulator, go to "FirstFit_wrong.py"
and "Placement.py" and follow the comments there.



'''



from Machine import Machine
from Task import Task
import matplotlib.pyplot as plt


from FirstFit import FirstFit
from First_Fit_Discard import FirstFit_discard
from Multi_Resource_Packing import Multi_resource_alignment
from Multi_Resource_Packing_Discard import Multi_resource_alignment_discard
from TBF import TBF
from TBF_Discard import TBF_Discard
from EAGLE import EAGLE
from EAGLE_MOD import EAGLE_MOD
from Multi_Resource_Packing_MOD import Multi_resource_alignment_mod

from Sim import Sim
from random import randrange
from workload_generator import getWorkload


def getKey(task):
    return task.arrival_time

def getClusterFromFile(filename):  # This method reads the "machines" from the given file and output a "cluster"
    cluster = []  # that is a list which includes all information of these machines
    with open(filename, 'r') as f:
        for line in f:
            config = line.rstrip('\n').split('\t')
            machineID = int(config[0])
            cpu = float(config[1])
            mem = float(config[2])
            # cpu = 40
            # mem = 128
            m = Machine(machineID, cpu, mem)
            cluster.append(m)
    return cluster

def getTaskSubmissionEventsFromFile(filename):  # This method reads the "tasks" from the given file and output "events", which is
    events = []  # a list of classes (TaskSubmissionEvent). A second dictionary of "jobs" is also returned, which
    with open(filename, 'r') as f:
        for line in f:
            workload = line.rstrip('\n').split('\t')
            # time = int(workload[0])

            arrival_time = int(workload[0])
            task_duration = int(workload[1])
            cpu_string = (workload[2])
            mem_string = (workload[3])
            cpu = float(cpu_string)
            mem = float(mem_string)
            task = Task(arrival_time, task_duration, cpu, mem)
            events.append(task)

    events.sort(key=getKey, reverse = False)                            #all tasks are organized in increasing arrival time manner

    return events

# def plotResults():
#     prefix = setting.ResultsDirectory
#
#     filename = prefix + "placementResults"
#     algorithms = []
#     resourceFraction, unusedMachine, loadBalance = {}, {}, {}
#
#     with open(filename, 'r') as f:
#         for line in f:
#             result = line.rstrip('\n').split('\t')
#             if result[0] not in algorithms:
#                 algorithms.append(result[0])
#                 rscFract = []
#                 unusedMach = []
#                 ldBaln = []
#                 rscFract.append(float(result[1]))
#                 unusedMach.append(int(result[2]))
#                 ldBaln.append(float(result[3]))
#                 resourceFraction[result[0]] = rscFract
#                 unusedMachine[result[0]] = unusedMach
#                 loadBalance[result[0]] = ldBaln
#             else:
#                 resourceFraction[result[0]].append(float(result[1]))
#                 unusedMachine[result[0]].append(int(result[2]))
#                 loadBalance[result[0]].append(float(result[3]))
#
#     colors = ['r','b','g','w','k','c']
#
#     plt.figure(1)
#     plt.subplot(311)
#     for element in algorithms:
#         plt.plot(resourceFraction.get(element),label = "%s" %element)
#
#     plt.xlabel('Tests')
#     plt.ylabel('Resource Fraction')
#     plt.legend()
# #    plt.show()
#
#     plt.subplot(312)
#     for element in algorithms:
#         plt.plot(unusedMachine.get(element),label = "%s" %element)
#
#     plt.xlabel('Tests')
#     plt.ylabel('Unused Machines')
#     plt.legend()
# #    plt.show()
#
#     plt.subplot(313)
#     for element in algorithms:
#         plt.plot(loadBalance.get(element),label = "%s" %element)
#
#     plt.xlabel('Tests')
#     plt.ylabel('Load Balance Error')
#     plt.legend()
#     plt.show()




############################# Main Code Starts Here #############################



cluster = getClusterFromFile("Cluster_test")
# cluster = getClusterFromFile("Cluster_test_light")
# cluster = getClusterFromFile("Cluster")


# VM requests from the traces are received inside taskEvents
# for task_requst in range(200, 210, 10):    # #VM request varying from 100 to 2000 in increment of 200
#     getWorkload(task_requst)

# task_request = 100
# getWorkload(task_request)

placement_schedulers = [FirstFit(),Multi_resource_alignment(),TBF(),EAGLE(),EAGLE_MOD()]
# placement_schedulers = [EAGLE(), Multi_resource_alignment()]
# placement_schedulers = [FirstFit()]
# placement_schedulers = [Multi_resource_alignment()]
# placement_schedulers = [EAGLE_MOD()]
# placement_schedulers = [FirstFit_disc rd(),Multi_resource_alignment_discard()]

for placement in placement_schedulers:
    # taskEvents = getTaskSubmissionEventsFromFile("Workloads/Workload_Traces_test")
    # taskEvents = getTaskSubmissionEventsFromFile("Workloads/Actual_Workload_Traces")
    taskEvents = getTaskSubmissionEventsFromFile("Workloads/Workload_Traces_Backlogged")
    # taskEvents = getTaskSubmissionEventsFromFile("Workloads/Workload_Traces_OnebyOne")
    # taskEvents = getTaskSubmissionEventsFromFile("Workloads/Workload_Traces_Small")

    print("Now using %s ..." % placement)
    placement.cluster = cluster
    placement.tasks = taskEvents[:]
    sim = Sim(placement)

    sim.placeTasks()

    for machine in cluster:
        machine.cleanMachine()

    print("simulation finished...")

