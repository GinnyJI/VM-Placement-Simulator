class Task:
	def __init__(self, arrival_time, duration, cpu ,mem ):
		# self.time = time

		self.arrival_time = arrival_time
		self.duration = duration
		self.cpu = cpu
		self.mem = mem
		self.hostMachine = None												# The machine on which the task is executed
		self.placement_time = -1

	def __str__(self):
		return "[arrival time = %d ]" % (self.arrival_time)