
# Written by Siqi
# 2017-06-30
#Modified by Ginny

from Placement import Placement
import time


def getKey(task):
    return task.arrival_time

class FirstFit (Placement):
    def __init__(self):
        super(FirstFit, self).__init__()
        self.requestLatency = []

    # def find_best_PM(self, task):


    def VMplacement(self):
        self.clearResults()  # clear results directory

        start_time = time.time()
        print start_time

        current_time = 0
        unplaced_tasks = self.tasks[:]
        backlogged_tasks = []
        firstFailureAlready = False

        machine_empty = False
        enough_resource = True

        self.update_ratio()

        while unplaced_tasks:
            machine_empty = self.updateMachines(current_time)
            enough_resource = True
            task_end_time = 0

            while unplaced_tasks:
                if unplaced_tasks[0].arrival_time > task_end_time:
                    task_end_time = unplaced_tasks[0].arrival_time

                if unplaced_tasks[0].arrival_time <= current_time:
                    backlogged_tasks.append(unplaced_tasks.pop(0))
                else:
                    break
            if backlogged_tasks:
                for task in backlogged_tasks:
                    for m in self.cluster:
                        if m.availMem >= task.mem and m.availCPU >= task.cpu:
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
                    unplaced_tasks.append(task)
                    enough_resource = False

            backlogged_tasks = []

            if not enough_resource:
                print "First Fit: not enough resource for all tasks, time", current_time
                unplaced_tasks.sort(key=getKey, reverse=False)
                if not firstFailureAlready:
                    self.getFirstFailureResult()                  #First Failure Utilization Check
                    firstFailureAlready = True

            if current_time % 1 == 0 or (len(unplaced_tasks) == 0):
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
        super(FirstFit, self).getResults(current_round)

    def __str__(self):
        return "First Fit"
