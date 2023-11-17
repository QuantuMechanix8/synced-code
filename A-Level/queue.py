class Q:
	'''This is a docstring for the Q class'''
	def __init__(self, maxLen):
		self.q, self.start, self.end, self.maxlen  = [], 0, 0, maxLen
	
	def returnSize(self):
		return len(self.q)
	
	def NQ(self, NQData):
		if self.isfull() == False:
			self.q.insert(NQData)
		elif self.isfull() == True:
			print("queue is full")

	def DQ(self):
		self.q.pop(0)

	def isfull(self):
		if self.returnSize() < self.maxlen:
			return False
		elif self.returnSize() == self.maxlen:
			return True
	
	def isMT(self):
		if self.returnSize == 0:
			return True
		else:
			return False
	
	def print(self):
		print(self.q)

PS5Q = Q(10)
PS5Q.NQ("Colin")
PS5Q.NQ("MINGE")
PS5Q.NQ("Uvuvuevuevueenetuevenyeobvwevueosas")
PS5Q.print


