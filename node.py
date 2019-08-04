import field

class Node(object):
	"""description of class"""

	id = None
	fieldPoint = None
	fieldPointType = None
	edges = None
	inEdges = None
	outEdges = None
	lastOutEdges = None
	hashIndex = None
	canvas = None
	graphic = None
	belongToPlayerID = None
	numberOfPaths = None

	def __init__(self):
		self.edges = list()
		self.inEdges = list()
		self.outEdges = list()

	#def __eq__(self, other):
	#	return id(self)==id(other)

	def addEdge(self, edge):
		self.edges.append(edge)

	def getFirstNotUsedEdge(self):
		E = next((E    for E in self.edges    if not E.used), None)
		return(E)

	def onlyOneUsedEdge(self):
		mE = self.getAllUsedEdges()
		if len(mE)==1:
			return True
		else:
			return False

	def getAllUsedEdges(self):
		mE = [E   for E in self.edges    if E.used]
		return(mE)

	def getAllUsedOrTracedEdges(self):
		mE = [E     for E in self.edges     if E.used or E.traced]
		return(mE)

	def noUsedOrTracedEdges(self):
		mE = [E     for E in self.edges     if E.used or E.traced]
		if len(mE)==0:
			return(True)
		else:
			return(False)



	def setInEdge(self, E): 
		self.inEdges.append(E)

	def untraceInEdge(self):
		self.inEdges[-1].traced = False

	def deleteInEdge(self):
		self.inEdges.pop()



	def setOutEdgesToScan(self):
		mE = [E     for E in self.edges     if (not E.used) and (not E.traced)]
		self.outEdges.append(mE)

	def deleteOutEdgesToScan(self):
		self.outEdges.pop()

	def getOutEdgeToScan(self):
		if len(self.outEdges[-1])==0:
			return(None)
		E = self.outEdges[-1].pop()
		return(E)



	def isGoal(self):
		if self.fieldPointType==field.FieldPointType.Goal:
			return(True)
		else:
			return(False)


	def isNoOutEdges(self):
		if len(self.outEdges[-1])==0:
			return(True)
		else:
			return(False)


	def isOnlyOneUsedOrTracedEdge(self):
		mE = [E     for E in self.edges     if E.used or E.traced]
		if len(mE)==1:
			return(True)
		else:
			return(False)



if __name__ == '__main__':

	N1 = Node()
	N2 = Node()
	a = N1==N2
	a = N1 in [N1, N2]
	debug = 1