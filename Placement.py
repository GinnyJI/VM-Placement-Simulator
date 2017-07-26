# Wriiten by Siqi
# 2017-06-30
# Modified by Ginny
# 2017-07-07

import setting

class Placement(object):
    EPSILON = 0.0001
    Mem_Abv_Ratio = 0
    CPU_Abv_Ratio = 0

    def __int__(self):
        self.resourceFraction = 0

    # def prePlacement(self):
    #     self.clearResults()  # clear results directory
    #
    #     start_time = time.time()
    #     print start_time
    #
    #     current_time = 0
    #     unplaced_tasks = self.tasks[:]
    #     backlogged_tasks = []
    #
    #     machine_empty = False
    #     enough_resource = True
    #     firstFailureAlready = False
    #
    #     while unplaced_tasks:
    #         machine_empty = self.updateMachines(current_time)
    #         enough_resource = True
    #
    #         while unplaced_tasks:
    #             if unplaced_tasks[0].arrival_time <= current_time:
    #                 backlogged_tasks.append(unplaced_tasks.pop(0))
    #             else:
    #                 break

    def update_ratio(self):
        for task in self.tasks:
            if task.mem > self.Mem_Abv_Ratio:
                self.Mem_Abv_Ratio = task.mem
            if task.cpu > self.CPU_Abv_Ratio:
                self.CPU_Abv_Ratio = task.cpu
        print "Mem_Abv_Ratio = ", self.Mem_Abv_Ratio
        print "CPU_Abv_Ratio = ", self.CPU_Abv_Ratio
        return

    def updateMachines(self, current_time):

        machine_empty = True

        for machine in self.cluster:
            if machine.beingUtilized:
                for task in list(machine.runningTasks):
                    if task.placement_time + task.duration <= current_time:
                        machine.removeTask(task, current_time)
                        machine.runningTasks.remove(task)
                        print "delete task", current_time, task.arrival_time, task.placement_time, task.duration, task.cpu, task.mem, "on machine", task.hostMachine

        for machine in self.cluster:
            if machine.beingUtilized:
                if not machine.runningTasks:
                    machine.beingUtilized = False

        for machine in self.cluster:
            if machine.beingUtilized:
                machine_empty = False

        return machine_empty

    def place_task(self, task, PM, current_time):
        PM.placeTask(task)
        task.placement_time = current_time
        task.place_latency = current_time - task.arrival_time
        self.requestLatency.append(current_time - task.arrival_time)
        task.hostMachine = PM.machineID
        print "place task", task.arrival_time, task.duration, \
            task.cpu, task.mem, "in machine", task.hostMachine, "at time", current_time

    def clearResults(self):
        unusedMachine_dir = setting.unusedMachine_dir + self.__str__()
        requestLatency_dir = setting.requestLatency_dir + self.__str__()
        cpu_dir = setting.resource_dir + self.__str__() + "/" + "CPU"
        memory_dir = setting.resource_dir + self.__str__() + "/" + "memory"
        time_path = "results/time_elapsed"
        resource_fraction_dir = setting.resource_fraction_dir + self.__str__() + "/Resource Fraction"
        resourceUtilization_dir = setting.resource_dir + self.__str__() + "/" + "Resource Utilization"

        open(unusedMachine_dir, "w").close()
        open(requestLatency_dir, "w").close()
        open(cpu_dir, "w").close()
        open(memory_dir, "w").close()
        open(resource_fraction_dir, "w").close()
        open(resourceUtilization_dir, "w").close()

    def getResults(self, currentRound):

        self.availMachine = 0
        for machine in self.cluster:
            if machine.beingUtilized == False:
                self.availMachine += 1

        unusedMachine_dir = setting.unusedMachine_dir + self.__str__()
        requestLatency_dir = setting.requestLatency_dir + self.__str__()
        cpu_dir = setting.resource_dir + self.__str__() + "/" + "CPU"
        memory_dir = setting.resource_dir + self.__str__() + "/" + "memory"



        with open(unusedMachine_dir, 'a') as f:
            f.write("%d\t%s\t%d\n" %(currentRound, self.__str__(), self.availMachine))


        with open(memory_dir, 'a') as f:
            for machine in self.cluster:
                if machine.beingUtilized == True:
                    f.write("%d\t%f" % (currentRound, (machine.mem - machine.availMem) / machine.mem))
                    f.write("\n")


        with open(cpu_dir, 'a') as f:
            for machine in self.cluster:
                if machine.beingUtilized == True:
                    f.write("%d\t%f" % (currentRound, (machine.CPU - machine.availCPU) / machine.CPU))
                    f.write("\n")

        with open(requestLatency_dir, 'a') as f:
            for latency in self.requestLatency:
                f.write("%d\n" % (latency))

        self.requestLatency = []


    def getFirstFailureResult(self):

        firstFailureUtil_dir = "results/firstFailure/" + self.__str__()

        with open(firstFailureUtil_dir, 'w') as f:
            for machine in self.cluster:
                f.write("%d\t%.2f\t%.2f\n" % (machine.machineID, (machine.CPU - machine.availCPU)/machine.CPU \
                                                  ,(machine.mem - machine.availMem)/machine.mem) )

    def getTimeResult(self, time_elapsed):
        path = "results/time_elapsed"

        print time_elapsed

        with open(path, 'a') as f:
            f.write("%s\t%f\n" % (self.__str__(), time_elapsed))

    def getFailureNum(self):
        dir = setting.failure_dir + self.__str__()

        unplaced_tasks = 0
        for task in self.tasks[:]:
            if task.hostMachine == None:
                unplaced_tasks += 1

        with open(dir, 'w') as f:
            f.write("%s\t%d\n" % (self.__str__(), unplaced_tasks))


    def getResourceFragmentation(self):
        resource_fraction_dir = setting.resource_fraction_dir + self.__str__() + "/Resource Fraction"
        avg_res_fraction_dir = setting.resource_fraction_dir + self.__str__() + "/Resource Fraction Mean"

        resourceUtilization_dir = setting.resource_dir + self.__str__() + "/Resource Utilization"
        avg_res_util_dir = setting.resource_dir + self.__str__() + "/Mean"
        variance_dir = setting.resource_dir + self.__str__() + "/Variance"

        firstStageMachine_dir = setting.firstStageMachine_dir + self.__str__()

        resource_wastage = []
        mem_Utilization = []
        cpu_Utilization = []
        mem_Used = []
        cpu_Used = []

        first_stage_mach = 0

        for machine in self.cluster:
            cpu_Used.append(machine.CPU - machine.availCPU)
            mem_Used.append(machine.mem - machine.availMem)

            if machine.beingUtilized == True:
                wastage = (abs(machine.availCPU / machine.CPU - machine.availMem / machine.mem) + self.EPSILON) \
                          / (1 - machine.availCPU / machine.CPU + 1 - machine.availMem / machine.mem)  # resource wastage modelling --Ginny
                # wastage = (machine.availCPU / machine.CPU + machine.availMem / machine.mem) #Mem left + CPU left
                resource_wastage.append(wastage)
                with open(resource_fraction_dir, 'a') as f:
                    f.write("%d\t%s\t%f\n" % (machine.machineID, self.__str__(), wastage))

                CPU_Util = (machine.CPU - machine.availCPU) / machine.CPU
                mem_Util = (machine.mem - machine.availMem) / machine.mem
                mem_Utilization.append(mem_Util)
                cpu_Utilization.append(CPU_Util)
                with open(resourceUtilization_dir, 'a') as f:
                    f.write("%d\t%.2f\t%.2f\n" % (machine.machineID, CPU_Util, mem_Util))

            if machine.availMem >= self.Mem_Abv_Ratio:
                first_stage_mach += 1

        if resource_wastage:
            self.resourceFraction = sum(resource_wastage) / len(resource_wastage)
        if mem_Utilization:
            mem_avg = sum(mem_Utilization) / len(mem_Utilization)
        if cpu_Utilization:
            cpu_avg = sum(cpu_Utilization) / len(cpu_Utilization)
        if cpu_Used:
            average = sum(cpu_Used) / len(cpu_Used)
            cpu_Variance = sum((average - value) ** 2 for value in cpu_Used) / len(cpu_Used)
        if mem_Used:
            average = sum(mem_Used) / len(mem_Used)
            mem_Variance = sum((average - value) ** 2 for value in mem_Used) / len(mem_Used)


        with open(avg_res_util_dir, 'w') as f:
            f.write("%s\t%.2f\t%.2f\n" % (self.__str__(), cpu_avg, mem_avg))

        with open(variance_dir, 'w') as f:
            f.write("%s\t%.2f\t%.2f\n" % (self.__str__(), cpu_Variance, mem_Variance))

        with open(avg_res_fraction_dir, 'w') as f:
            f.write("%s\t%f\n" %(self.__str__(), self.resourceFraction))

        with open(firstStageMachine_dir, 'w') as f:
            f.write("%s\t%d\n" %(self.__str__(), first_stage_mach))