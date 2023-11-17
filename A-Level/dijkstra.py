import sys # so that we can use the max integer value to initialise "traversal difficulty" for each node
"""
The tree will be represented as an adjacency list (dictionary) with weights, where each item in the list is a tuple of the node and edge weight
i.e. node A may have an associated list of [(B, 2),(D, 5),(E, 1)]
e.g. tree = {'A' : [('B', 2),('D', 5),('E', 1)], 
						 'B' : [()]}
"""
def Dijkstra(tree, startNode, endNode):
	path = []
	priorityQueue = []
	visitedNodes = []
	nodeTraversalDifficulty = {}
	#the dictionary holding a value for the "traversal-difficulty" (total edge weights) to reach each node from the start node, i.e. A: 12, means that the weight traversed to reach node A is 12
	for node in tree:
		nodeTraversalDifficulty[node] = sys.maxsize # some equally large number can be used to represent an ∞ weight (large enough that when reached the weight is lower so it is updated)
	nodeTraversalDifficulty[startNode] = 0
	currentNode = startNode
	while not complete:
		currentWeight+=node.weight
		for node in currentNode.neighbors:
			if node not in visitedNodes:
				pass
				
class PriorityQueue:

	def __init__(self):
		self.data = []
	
	def addItem(self, newItem, newItemValue):
		for index, item in enumerate(self.data):
			if newItemValue>=item[1]:
				self.data.insert((newItem, newItemValue), index)
				return True
		return False
	
def removeItem(self):
	return self.data.pop(0)

class Node:
	
	def __init__(self, identifier, weight = 0):
		self.identifier, self.weight = identifier, weight
	
	def getWeight(self):
		return self.weight
	
	def getIdentifier(self):
		return self.identifier
	
	def setWeight(self, weight):
		self.weight = weight

