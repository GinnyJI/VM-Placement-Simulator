
# Written by Siqi
# 2017-06-30
# Modefied by Ginny

from Placement import Placement
import sys
import time


def getKey(task):
    return task.arrival_time

class Multi_resource_alignment(Placement):
    # Mem_Abv_Ratio = 0

    def __init__(self):
        super(Multi_resource_alignment, self).__init__()
        self.requestLatency = []
        return

    # def update_mem_abv_ratio(self):
    #     for task in self.tasks:
    #         if task.mem > self.Mem_Abv_Ratio:
    #             self.Mem_Abv_Ratio = task.mem
    #     return

    def find_best_PM(self, task):
        alignment_score_used = 0  # store the highest score in all used machines
        alignment_score_empty = 0  # store the highest score in all empty machines
        machine_used = 0  # store the best machine in all used machines
        machine_empty = 0  # store the best machine in all empty machine
        placed_in_used = False
        placed_in_empty = False
        for index, m in enumerate(self.cluster):
            if m.beingUtilized == True:  # if used machine, check if with highest score among all used machine
                if m.availMem >= task.mem and m.availCPU >= task.cpu:
                    placed_in_used = True
                    task_score = (m.availMem / m.mem) * (task.mem / m.mem) \
                                 + (m.availCPU / m.CPU) * (task.cpu / m.CPU)
                    if task_score > alignment_score_used:
                        alignment_score_used = task_score
                        machine_used = m
            else:  # if empty machine, check if with highest score among all empty machine
                if m.availMem >= task.mem and m.availCPU >= task.cpu:
                    placed_in_empty = True
                    task_score = (m.availMem / m.mem) * (task.mem / m.mem) \
                                 + (m.availCPU / m.CPU) * (task.cpu / m.CPU)
                    if task_score > alignment_score_empty:
                        alignment_score_empty = task_score
                        machine_empty = m

        # choose best machine from used machine first. If not, choose from empty machine
        if placed_in_used:
            return machine_used
        elif placed_in_empty:
            return machine_empty
        else:
            return None

    def find_best_PM_blw_ratio(self,task):
        alignment_score_used = 0  # store the highest score in all used machines
        alignment_score_empty = 0  # store the highest score in all empty machines
        machine_used = 0  # store the best machine in all used machines
        machine_empty = 0  # store the best machine in all empty machine
        placed_in_used = False
        placed_in_empty = False
        for index, m in enumerate(self.cluster):
            if m.availMem - self.Mem_Abv_Ratio >= task.mem and m.availCPU - self.CPU_Abv_Ratio >= task.cpu:
                m_mem = m.mem - self.Mem_Abv_Ratio
                m_cpu = m.CPU - self.CPU_Abv_Ratio
                m_avail_mem = m.availMem - self.Mem_Abv_Ratio
                m_avail_cpu = m.availCPU - self.CPU_Abv_Ratio
                task_score = (m_avail_mem / m_mem) * (task.mem / m_mem) + (m_avail_cpu / m_cpu) * (task.cpu / m_cpu)
                if m.beingUtilized is True:  # if used machine, check if with highest score among all used machine
                    placed_in_used = True
                    if task_score > alignment_score_used:
                        alignment_score_used = task_score
                        machine_used = m
                else:  # if empty machine, check if with highest score among all empty machine
                    placed_in_empty = True
                    if task_score > alignment_score_empty:
                        alignment_score_empty = task_score
                        machine_empty = m

        # choose best machine from used machine first. If not, choose from empty machine
        if placed_in_used:
            return machine_used
        elif placed_in_empty:
            return machine_empty
        else:
            return None

    def VMplacement(self):
        self.clearResults()  # clear results directory

        start_time = time.time()
        print start_time

        current_time = 0
        unplaced_tasks = self.tasks[:]
        backlogged_tasks = []

        firstFailureAlready = False

        self.update_ratio()

        while unplaced_tasks:
            machine_empty = self.updateMachines(current_time)
            enough_resource = True
            task_end_time = 0     #store the latest task coming time

            while unplaced_tasks:
                if unplaced_tasks[0].arrival_time > task_end_time:
                    task_end_time = unplaced_tasks[0].arrival_time
                if unplaced_tasks[0].arrival_time <= current_time:
                    backlogged_tasks.append(unplaced_tasks.pop(0))
                else:
                    break

            if backlogged_tasks:
                for task in backlogged_tasks:
                    # PM = self.find_best_PM_blw_ratio(task)
                    # if PM is not None:
                    #     self.place_task(task, PM, current_time)
                    #     continue
                    PM = self.find_best_PM(task)
                    if PM is not None:
                        self.place_task(task, PM, current_time)

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

            if not enough_resource:
                print "Multi-Resource Packing: not enough resource for all tasks, time", current_time
                unplaced_tasks.sort(key=getKey, reverse=False)
                if not firstFailureAlready:
                    self.getFirstFailureResult()  # First Failure Utilization Check
                    firstFailureAlready = True

            if current_time % 10 == 0 or (len(unplaced_tasks) == 0):
                self.getResults(current_time)
            current_time += 1

            # if enough_resource and not unplaced_tasks:           #VM placement finished
            # if not enough_resource:
            if current_time > task_end_time:
                end_time = time.time()
                print end_time
                self.getTimeResult(float(end_time - start_time))
                break

        self.getResourceFragmentation()
        self.getFailureNum()


    def getResults(self, current_round):
        super(Multi_resource_alignment, self).getResults(current_round)

    def __str__(self):
        return "Multi Resource Alignment"
