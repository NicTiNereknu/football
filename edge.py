

class Edge(object):
	"""description of class"""

	id = None
	traced = None	# topology tracing
	canTrace = None
	used = None		# drawing
	nodes = None
	hashIndex = None
	canvas = None
	graphic = None

	def __init__(self):
		self.nodes = list()

	def addNode(self, node):
		self.nodes.append(node)

	def getEdgeBetweenNodes(N1, N2):
		for E in N1.edges:
			if N2 in E.nodes:
				return E
		return None
	
	def getOtherNode(self, N1):
		N2 = [N    for N in self.nodes   if id(N)!=id(N1)]   [0]
		return(N2)


if __name__ == '__main__':
	pass

