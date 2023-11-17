class STACK:
	def __init__(self, maxsize):
		self.maxsize, self.stack = maxsize, []
	
	def push(self, item):
		if not(self.isFull()):
			self.stack.append(item)
		else:
			print(f"stack is full, cannot add {item} to list")
	
	def remove(self):
		if not(self.isMT()):
			return self.stack.pop()
		else:
			print("stack is empty, cannot remove an item from list")

	def size(self):
		return len(self.stack)

	def isFull(self):
		if self.size() == self.maxsize:
			return True
		else:
			return False 
	
	def isMT(self):
		if (self.size()) == 0:
			print("is mt")
			return True
		else:
			return False
	
	def peep(self):
		return (self.stack[-1])

palindrome = str(input("enter a word to be tested: "))
list1 = STACK(len(palindrome))
RevList = STACK(len(palindrome))
for i in range(len(palindrome)):
	list1.push(palindrome[i])
	print(list1.isFull())
	print("run")
for item in list1.stack:
	RevList.push(list1.remove())

print(f"rev list {RevList.stack}, palendrome {palindrome}")

