class Machine:
	def __init__(self, machineID, CPU, mem):
		self.machineID = machineID
		self.CPU = CPU
		self.mem = mem
		self.availCPU = CPU
		self.availMem = mem
		self.runningTasks = []	# number of tasks running for each job
		self.beingUtilized = False

	def placeTask (self, task):
		self.availCPU -= task.cpu
		self.availMem -= task.mem
		self.runningTasks.append(task)
		self.beingUtilized = True

	def removeTask (self, task, current_time):
		self.availCPU += task.cpu
		self.availMem += task.mem

	def cleanMachine(self):
		self.availCPU = self.CPU
		self.availMem = self.mem
		self.beingUtilized = False
		self.runningTasks = []

	def __cmp__(self, other):
		if hasattr(other, 'CPU'):
			return self.CPU.__cmp__(other.CPU)
