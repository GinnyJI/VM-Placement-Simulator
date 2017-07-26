
# Written by Ginny

from Placement import Placement
import time
from math import sqrt
import sys


class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

    def shift(self, x, y):
        self.x += x
        self.y += y

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

def distance(a, b):
    return sqrt((a.x-b.x)**2+(a.y-b.y)**2)

def getKey(task):
    return task.arrival_time

class EAGLE (Placement):
    # Mem_Abv_Ratio = 0
    r0 = 0.1 # Satisfaction factor
    R0 = 0.8 # Balance Factor
    O1 = Point(1-R0, R0) #center of quarter circle
    O2 = Point(R0, 1-R0)

    def __init__(self):
        super(EAGLE, self).__init__()
        self.requestLatency = []

    def is_in_SD(self,S): #return true if point is in safety domain
        if distance(S, self.O1) <= self.R0 and distance(S, self.O2) <= self.R0:
            return True
        elif S.x <= (1 - self.R0) and S.y <= (1- self.R0):
            return True
        elif S.x >= self.R0 and S.y >= self.R0:
            return True
        else:
            return False

    def is_in_AD(self,S): #return true if point is in acceptance domain
        E = Point(1,1)
        if distance(S, E) <= self.r0:
            return True
        else:
            return False

    def find_best_PM(self,task):
        R_max = 0 #store maximum utilization ratio
        best_PM_in_AD = None
        PM_found_in_AD = False
        D_min = sys.maxint  # store minimum variance distance
        best_PM_in_SD = None
        PM_found_in_SD = False
        for m in self.cluster:
            if m.beingUtilized == True:
                if m.availMem >= task.mem and m.availCPU >= task.cpu:
                    post_mem_ratio = 1-(m.availMem - task.mem)/m.mem
                    post_CPU_ratio = 1-(m.availCPU - task.cpu)/m.CPU
                    pus = Point(post_mem_ratio,post_CPU_ratio) #posterior usage state
                    if self.is_in_AD(pus):
                        R = ((1-m.availMem/m.mem)+(1-m.availCPU/m.CPU))*0.5 #avarage utilization ratio
                        if R > R_max:
                            best_PM_in_AD = m
                            R_max = R
                            PM_found_in_AD = True
                    elif self.is_in_SD(pus): #if m is in AD, no need to check SD
                        res_util_mean = (post_mem_ratio + post_CPU_ratio)*0.5
                        D = distance(pus, Point(res_util_mean,res_util_mean))
                        if D < D_min:
                            best_PM_in_SD = m
                            D_min = D
                            PM_found_in_SD = True
        if PM_found_in_AD:
            return best_PM_in_AD
        elif PM_found_in_SD:
            return best_PM_in_SD
        else:                                           # return an unused machine
            for m in self.cluster:
                if m.beingUtilized == False:
                    if m.availMem >= task.mem and m.availCPU >= task.cpu:
                        return m
            return None

    def find_best_PM_blw_ratio(self,task):
        R_max = 0 #store maximum utilization ratio
        best_PM_in_AD = None
        PM_found_in_AD = False
        D_min = sys.maxint  # store minimum variance distance
        best_PM_in_SD = None
        PM_found_in_SD = False
        for m in self.cluster:
            if m.availMem - self.Mem_Abv_Ratio >= task.mem and m.availCPU - self.CPU_Abv_Ratio >= task.cpu:
                if m.beingUtilized is True:
                    post_mem_ratio = 1-(m.availMem - task.mem)/m.mem
                    post_CPU_ratio = 1-(m.availCPU - task.cpu)/m.CPU
                    pus = Point(post_mem_ratio, post_CPU_ratio) #posterior usage state
                    if self.is_in_AD(pus):
                        R = ((1-m.availMem/m.mem)+(1-m.availCPU/m.CPU))*0.5 #avarage utilization ratio
                        if R > R_max:
                            best_PM_in_AD = m
                            R_max = R
                            PM_found_in_AD = True
                    elif self.is_in_SD(pus): #if m is in AD, no need to check SD
                        res_util_mean = (post_mem_ratio + post_CPU_ratio)*0.5
                        D = distance(pus, Point(res_util_mean,res_util_mean))
                        if D < D_min:
                            best_PM_in_SD = m
                            D_min = D
                            PM_found_in_SD = True
        if PM_found_in_AD:
            return best_PM_in_AD
        elif PM_found_in_SD:
            return best_PM_in_SD
        else:                                           # return an unused machine
            for m in self.cluster:
                if m.beingUtilized == False:
                    if m.availMem - self.Mem_Abv_Ratio>= task.mem and m.availCPU >= task.cpu:
                        return m
            return None

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

        # Fetch VM requests
        while unplaced_tasks:
            machine_empty = self.updateMachines(current_time)
            enough_resource = True
            task_end_time = 0  #store the latest task coming time

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
                print "EAGLE: not enough resource for all tasks, time", current_time
                unplaced_tasks.sort(key=getKey, reverse=False)
                if not firstFailureAlready:
                    self.getFirstFailureResult()                  #First Failure Utilization Check
                    firstFailureAlready = True

            if current_time % 1 == 0 or (len(unplaced_tasks) == 0):
                self.getResults(current_time)
            current_time += 1

            # if enough_resource and not unplaced_tasks:           #VM placement finished
            # if not enough_resource:
            if current_time > task_end_time:                       #heavy workload case VM placement finished
                end_time = time.time()
                print end_time
                self.getTimeResult(float(end_time - start_time))
                break

        self.getResourceFragmentation()
        self.getFailureNum()



    def getResults(self, current_round):
        super(EAGLE, self).getResults(current_round)

    def __str__(self):
        return "EAGLE"
