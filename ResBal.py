
# Written by Ginny

from Placement import Placement
import sys
import time


def getKey(task):
    return task.arrival_time

class Res_Bal(Placement):
    def __init__(self):
        super(Res_Bal, self).__init__()
        self.requestLatency = []

    def VMplacement(self):
        self.clearResults()  # clear results directory

        start_time = time.time()
        print start_time

        current_time = 0
        unplaced_tasks = self.tasks[:]
        backlogged_tasks = []

        machine_empty = False
        enough_resource = True
        firstFailureAlready = False

        while unplaced_tasks:
            machine_empty = self.updateMachines(current_time)
            enough_resource = True

            while unplaced_tasks:
                if unplaced_tasks[0].arrival_time <= current_time:
                    backlogged_tasks.append(unplaced_tasks.pop(0))
                else:
                    break

            if backlogged_tasks:
                for index, task in enumerate(backlogged_tasks):
                    # while True:
                    min_wastage = sys.maxint
                    # used_machine_bonus = 1000
                    # task_index = index
                    # machine = None
                    # placed = False
                    # for m in self.cluster:
                    #     if m.availMem >= task.mem and m.availCPU >= task.cpu:
                    #         placed = True
                    #         task_score = (m.availMem / m.mem) * (task.mem / m.mem) \
                    #                       + (m.availCPU / m.CPU) * (task.cpu / m.CPU)
                    #         if m.beingUtilized:
                    #             task_score = task_score + used_machine_bonus
                    #         if task_score > alignment_score:
                    #             alignment_score = task_score
                    #             machine = m
                    #
                    # if placed:
                    #     backlogged_tasks[task_index].hostMachine = machine.machineID
                    #     backlogged_tasks[task_index].placement_time = current_time
                    #     machine.placeTask(backlogged_tasks[task_index])

                    machine_index = 0
                    placed_in_used = False
                    placed_in_empty = False
                    for index, m in enumerate(self.cluster):
                        if m.beingUtilized == True:
                            if m.availMem >= task.mem and m.availCPU >= task.cpu:
                                placed_in_used = True
                                wastage = (abs((m.availCPU - task.cpu) / m.CPU - (m.availMem - task.mem) / m.mem) + self.EPSILON) \
                                / (1 - (m.availCPU - task.cpu) / m.CPU + 1 - (
                                m.availMem - task.mem) / m.mem)  # resource wastage if placing current task
                                if wastage > min_wastage:
                                    min_wastage = wastage
                                    machine_index = index

                    if not placed_in_used:
                        for index, m in enumerate(self.cluster):
                            if m.beingUtilized == False:
                                if m.availMem >= task.mem and m.availCPU >= task.cpu:
                                    placed_in_used = True
                                    wastage = (abs((m.availCPU - task.cpu) / m.CPU - (m.availMem - task.mem) / m.mem) + self.EPSILON) \
                                              / (1 - (m.availCPU - task.cpu) / m.CPU + 1 - (
                                        m.availMem - task.mem) / m.mem)  # resource wastage if placing current task
                                    if wastage > min_wastage:
                                        min_wastage = wastage
                                        machine_index = index

                    if placed_in_used or placed_in_empty:
                        task.hostMachine = self.cluster[machine_index].machineID
                        task.placement_time = current_time
                        self.cluster[machine_index].placeTask(task)
                        self.requestLatency.append(current_time - task.arrival_time)
                        # print "place task", task.arrival_time, task.duration, \
                        #     task.cpu, task.mem, "in machine", \
                        #     task.hostMachine, "at time", current_time

                        # backlogged_tasks.pop(task_index)

                        # if not placed:
                        #     break

            else:
                if current_time % 1 == 0 or (len(unplaced_tasks) == 0):
                    self.getResults(current_time)
                current_time += 1
                continue

            for task in backlogged_tasks:
                if task.hostMachine == None:
                    unplaced_tasks.append(task)
                    enough_resource = False

            backlogged_tasks = []

            if enough_resource and not unplaced_tasks:           #VM placement finished
                end_time = time.time()
                print end_time
                self.getTimeResult(float(end_time - start_time))
                break

            if not enough_resource:
                print "Resource Balance: not enough resource for all tasks, time", current_time
                unplaced_tasks.sort(key=getKey, reverse=False)
                if not firstFailureAlready:
                    self.getFirstFailureResult()  # First Failure Utilization Check
                    firstFailureAlready = True

            if current_time % 10 == 0 or (len(unplaced_tasks) == 0):
                self.getResults(current_time)
            current_time += 1

        self.getResourceFragmentation()


    def getResults(self, current_round):
        super(Res_Bal, self).getResults(current_round)

    def __str__(self):
        return "Resource Balance Fit"
