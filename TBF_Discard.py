
# Written by Ginny
# 2017-07-06

from Placement import Placement
import time
import sys


def getKey(task):
    return task.arrival_time

class TBF_Discard (Placement):
    def __init__(self):
        super(TBF_Discard, self).__init__()
        self.requestLatency = []

    def VMplacement(self):
        self.clearResults()  # clear results directory

        start_time = time.time()

        current_time = 0
        unplaced_tasks = self.tasks[:]
        backlogged_tasks = []
        firstFailureAlready = False

        machine_empty = False
        enough_resource = True

        while unplaced_tasks or not machine_empty:
            machine_empty = self.updateMachines(current_time)
            enough_resource = True

            while unplaced_tasks:
                if unplaced_tasks[0].arrival_time <= current_time:
                    backlogged_tasks.append(unplaced_tasks.pop(0))
                else:
                    break
            if backlogged_tasks:
                for task in backlogged_tasks:
                    ram_balance_ratio = 0.34
                    memDifference = sys.float_info.max
                    memAbvRatio = 15 * (1 - ram_balance_ratio)
                    host_machine = -1
                    for m in self.cluster:
                        if m.availMem - memAbvRatio >= task.mem and m.availCPU >= task.cpu:
                            if (m.availMem - memAbvRatio - task.mem) < memDifference:
                                memDifference = m.availMem - memAbvRatio - task.mem
                                host_machine = m.machineID

                    if host_machine > 0:
                        for m in self.cluster:
                            if m.machineID == host_machine:
                                m.placeTask(task)
                                task.placement_time = current_time
                                task.place_latency = current_time - task.arrival_time
                                self.requestLatency.append(current_time - task.arrival_time)
                                task.hostMachine = m.machineID
                                print "place task", task.arrival_time, task.duration, \
                                    task.cpu, task.mem, "in machine", task.hostMachine, "at time", current_time
                    else:
                        break

                for task in backlogged_tasks:
                    memDifference = sys.float_info.max
                    host_machine = -1
                    for m in self.cluster:
                        if m.availMem >= task.mem and m.availCPU >= task.cpu:
                            if (m.availMem - task.mem) < memDifference:
                                memDifference = m.availMem - task.mem
                                host_machine = m.machineID

                    for m in self.cluster:
                        if m.machineID == host_machine:
                            m.placeTask(task)
                            task.placement_time = current_time
                            task.place_latency = current_time -task.arrival_time
                            self.requestLatency.append(current_time - task.arrival_time)
                            task.hostMachine = m.machineID
                            print "place task", task.arrival_time, task.duration, \
                                task.cpu, task.mem, "in machine", task.hostMachine, "at time", current_time
                            break

            else:
                if current_time % 10 == 0 or (len(unplaced_tasks) == 0):
                    self.getResults(current_time)
                current_time += 1
                continue

            for task in backlogged_tasks:
                if task.hostMachine == None:
                    # unplaced_tasks.append(task)
                    enough_resource = False

            backlogged_tasks = []

            if enough_resource and not unplaced_tasks:           #VM placement finished
                end_time = time.time()
                self.getTimeResult(float(end_time - start_time))

            if not enough_resource:
                print "Two Stage Best Fit Discard: not enough resource for all tasks, time", current_time
                unplaced_tasks.sort(key=getKey, reverse=False)
                if not firstFailureAlready:
                    self.getFirstFailureResult()                  #First Failure Utilization Check
                    firstFailureAlready = True

            if current_time % 1 == 0 or (len(unplaced_tasks) == 0):
                self.getResults(current_time)
            current_time += 1



    def getResults(self, current_round):
        super(TBF_Discard, self).getResults(current_round)

    def __str__(self):
        return "Two Stage Best Fit Discard"
