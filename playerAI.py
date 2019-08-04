import math
import threading
from field import FieldPointType

class PlayerAI(object):
	"""description of class"""
	"""sdfsd sfjslfjs fl lsdls dfls dlfsldf l gsdfsf"""
	actualNode = None
	nodes = None
	edges = None
	origEdgesUsed = None
	numberOfOpponentTurns = None	# 0=only one turn of this AI, 1=AI_turn -> opponent_turn -> AI_turn
	trvPath = None
	selectedNodePath = None
	dictPathID_path = dict()
	playerID = None
	myGoalNodes = None
	opponentGoalNodes = None
	myTurn = None
	numberOfPathsToEndNodes = None
	stopThread = None
	threadTimeout = None
	handleThread = None

	def __init__(self, actualNode, nodes, edges, playerID, numberOfContraTurns, trvPath):
		self.actualNode = actualNode
		self.nodes = nodes
		self.edges = edges
		self.playerID = playerID
		self.numberOfContraTurns = numberOfContraTurns
		self.trvPath = trvPath
		#self.setStyleToPathTreeView()
		self.origEdgesUsed = self.getEdgesUsed()
		self.myGoalNodes = [N    for N in self.nodes    if N.fieldPointType==FieldPointType.Goal \
			and N.belongToPlayerID==self.playerID]
		self.opponentGoalNodes = [N    for N in self.nodes    if N.fieldPointType==FieldPointType.Goal \
			and N.belongToPlayerID!=self.playerID]


	def getEdgesUsed(self):
		edgesUsed = tuple([E.used    for E in self.edges])
		return(edgesUsed)


	def setEdgesUsed(self, edgesUsed):
		for ind, E in enumerate(self.edges):
			E.used = edgesUsed[ind]

	def getEdgesCanTrace(self):
		edgesCanTrace = tuple([E.canTrace    for E in self.edges])
		return(edgesCanTrace)

	def setEdgesCanTrace(self, edgesCanTrace):
		for ind, E in enumerate(self.edges):
			E.canTrace = edgesCanTrace[ind]

	def setCanTraceForEdges(self, edges, canTrace):
		for E in edges:
			E.canTrace = canTrace

	def setAllEdgesCanTraceToTrue(self):
		for E in self.edges:
			E.canTrace = True

	def setEdgesCanTraceOfNodesToFalse(self, nodes):
		for N in nodes:
			for E in N.edges:
				E.canTrace = False

	def setEdgesCanTraceOfNodesToTrue(self, nodes):
		for N in nodes:
			for E in N.edges:
				E.canTrace = True


	def genMoveToNode(self):
		self.myTurn = True
		paths = self.getAllPathsFromNode(self.actualNode)
		self.fillPathTreeView(paths)

		return
		
	def removePathsWithFarGoalDistance(self, paths):
		uniqGoalDistances = list(  set([P.goalDistance   for P in paths])  )
		uniqGoalDistances = sorted(uniqGoalDistances)

		#if len(uniqGoalDistances)<=3:
		#	uniqGoalDistances = uniqGoalDistances[0]
		#else:
		#	uniqGoalDistances = uniqGoalDistances[0:2]
		uniqGoalDistances = [uniqGoalDistances[0]]

		paths = [P    for P in paths     if P.goalDistance in uniqGoalDistances]
		return(paths)

	def getNodesWithFarGoalDistance(self, nodes):
		goalDistance = [self.getGoalDistance(N)   for N in nodes]
		uniqGoalDistances = list(  set(goalDistance)  )
		uniqGoalDistances = sorted(uniqGoalDistances)

		#if len(uniqGoalDistances)<=3:
		#	uniqGoalDistances = [uniqGoalDistances[0]]
		#else:
		#	uniqGoalDistances = uniqGoalDistances[0:2]
		uniqGoalDistances = [uniqGoalDistances[0]]

		nodes = [N    for ind, N in enumerate(nodes)     if goalDistance[ind] not in uniqGoalDistances]
		return(nodes)

	def getNearestGoalDistanceForNodes(self, nodes):
		goalDistance = [self.getGoalDistance(N)   for N in nodes]
		uniqGoalDistances = list(  set(goalDistance)  )
		uniqGoalDistances = sorted(uniqGoalDistances)
		return(uniqGoalDistances[0])

	def removePathsWithLowerTotalNumber(self, paths):
		uniqTotal = list(  set([P.totalNumber   for P in paths])  )
		uniqTotal = sorted(uniqTotal, reverse=True)

		ind = int(len(uniqTotal)/4)
		if ind==0:
			ind = 1
		uniqTotal = uniqTotal[0:ind]

		paths = [P    for P in paths     if P.totalNumber in uniqTotal]
		return(paths)

	def getAllPathsFromNode(self, actualNode):

		def beginTracing():
			nonlocal nodeStack, sPath, actualNode
			nodeStack.append(actualNode)
			sPath.append(actualNode.id)
			actualNode.setInEdge(None)
			actualNode.setOutEdgesToScan()


		def goForward():
			nonlocal edgeStack, actualNode, E, nodeStack, sPath

			E.traced = True
			edgeStack.append(E)
			sPath.append(E.id)

			otherNode = E.getOtherNode(actualNode)
			otherNode.setInEdge(E)
			otherNode.setOutEdgesToScan()

			sPath.append(otherNode.id)
			nodeStack.append(otherNode)
			actualNode = otherNode


		def goBack():
			nonlocal nodeStack, actualNode, sPath, edgeStack

			actualNode.deleteOutEdgesToScan()
			actualNode.untraceInEdge()
			actualNode.deleteInEdge()

			nodeStack.pop()
			actualNode = nodeStack[-1]

			edgeStack.pop()

			sPath.pop()
			sPath.pop()


		def endTracing():
			nonlocal nodeStack, actualNode
			actualNode.deleteOutEdgesToScan()
			actualNode.deleteInEdge()
			actualNode = None
			nodeStack.pop()


		def isEndOfPath():
			nonlocal self, actualNode
			#if (actualNode.isGoal() and actualNode.belongToPlayerID!=self.playerID) or \
			#	actualNode.isOnlyOneUsedOrTracedEdge():
			if actualNode.isGoal() or actualNode.isOnlyOneUsedOrTracedEdge():
				return(True)
			else:
				return(False)

		def isActualNodeNumberOfPathsReached():
			nonlocal actualNode
			if self.numberOfPathsToEndNodes == actualNode.numberOfPaths:
				return(True)
			else:
				return(False)

		def goBackToFirstNodeInStack():
			nonlocal nodeStack
			while True:
				if len(nodeStack)==1:
					break
				goBack()

		def savePath():
			nonlocal pathCounter, actualNode, nodeStack, edgeStack, paths, uniqPathsEdges, \
				dictEndNode_numberOfPaths

			# check if edges in different order are used in previous paths
			hiEdges = sorted([E.hashIndex    for E in edgeStack])
			if hiEdges in uniqPathsEdges:
				return
			uniqPathsEdges.append(hiEdges)

			path = Path()
			path.id = pathCounter
			path.isGoal = actualNode.isGoal()
			path.goalDistance = self.getGoalDistance(actualNode)
			path.nodesTraced = nodeStack.copy()
			path.edgesTraced = edgeStack.copy()
			path.myTurn = self.myTurn
			path.numberOfTracedNodes = len(path.nodesTraced)
			path.numberOfTracedEdges = len(path.edgesTraced)
			path.totalNumber = path.numberOfTracedNodes + path.numberOfTracedEdges
			paths.append(path)
			pathCounter += 1



		paths = list()
		nodeStack = list()
		edgeStack = list()
		sPath = list()
		pathCounter = 1
		uniqPathsEdges = list()
		dictEndNode_numberOfPaths = dict()

		beginTracing()
		while True:
			if self.stopThread:
				goBackToFirstNodeInStack()
				endTracing()
				break

			sNode = [N.id   for N in nodeStack]
			sEdge = [(E.id, E.traced)   for E in edgeStack]

			E = actualNode.getOutEdgeToScan()
			if E is None:
				if len(nodeStack)==1:
					endTracing()
					break
				goBack()
				continue

			if not E.canTrace:
				continue
			

			goForward()
			if isEndOfPath():
				if isActualNodeNumberOfPathsReached():
					actualNode.numberOfPaths = 0
					savePath()
					goBackToFirstNodeInStack()
				else:
					actualNode.numberOfPaths += 1
					savePath()
					goBack()

		return(paths)

	def getAnyFirstPath(self, actualNode):

		def beginTracing():
			nonlocal nodeStack, sPath, actualNode
			nodeStack.append(actualNode)
			sPath.append(actualNode.id)
			actualNode.setInEdge(None)
			actualNode.setOutEdgesToScan()


		def goForward():
			nonlocal edgeStack, actualNode, E, nodeStack, sPath

			E.traced = True
			edgeStack.append(E)
			sPath.append(E.id)

			otherNode = E.getOtherNode(actualNode)
			otherNode.setInEdge(E)
			otherNode.setOutEdgesToScan()

			sPath.append(otherNode.id)
			nodeStack.append(otherNode)
			actualNode = otherNode


		def goBack():
			nonlocal nodeStack, actualNode, sPath, edgeStack

			actualNode.deleteOutEdgesToScan()
			actualNode.untraceInEdge()
			actualNode.deleteInEdge()

			nodeStack.pop()
			actualNode = nodeStack[-1]

			edgeStack.pop()

			sPath.pop()
			sPath.pop()


		def endTracing():
			nonlocal nodeStack, actualNode
			actualNode.deleteOutEdgesToScan()
			actualNode.deleteInEdge()
			actualNode = None
			nodeStack.pop()


		def isEndOfPath():
			nonlocal self, actualNode
			#if (actualNode.isGoal() and actualNode.belongToPlayerID!=self.playerID) or \
			#	actualNode.isOnlyOneUsedOrTracedEdge():
			if actualNode.isGoal() or actualNode.isOnlyOneUsedOrTracedEdge():
				return(True)
			else:
				return(False)

		def isActualNodeNumberOfPathsReached():
			nonlocal actualNode
			if self.numberOfPathsToEndNodes == actualNode.numberOfPaths:
				return(True)
			else:
				return(False)

		def goBackToFirstNodeInStack():
			nonlocal nodeStack
			while True:
				if len(nodeStack)==1:
					break
				goBack()

		def savePath():
			nonlocal pathCounter, actualNode, nodeStack, edgeStack, paths, uniqPathsEdges, \
				dictEndNode_numberOfPaths

			#endNode = nodeStack[-1]
			#if self.numberOfPathsToEndNodes == endNode.numberOfPaths:
			#	endNode.numberOfPaths = 0
			#	# return to first node
			#	while True:
			#		if len(nodeStack)==1:
			#			break
			#		goBack()
			#	return
			#else:
			#	endNode.numberOfPaths += 1

			# check if edges in different order are used in previous paths
			hiEdges = sorted([E.hashIndex    for E in edgeStack])
			if hiEdges in uniqPathsEdges:
				return
			uniqPathsEdges.append(hiEdges)

			path = Path()
			path.id = pathCounter
			path.isGoal = actualNode.isGoal()
			path.goalDistance = self.getGoalDistance(actualNode)
			path.nodesTraced = nodeStack.copy()
			path.edgesTraced = edgeStack.copy()
			path.myTurn = self.myTurn
			path.numberOfTracedNodes = len(path.nodesTraced)
			path.numberOfTracedEdges = len(path.edgesTraced)
			path.totalNumber = path.numberOfTracedNodes + path.numberOfTracedEdges
			paths.append(path)
			pathCounter += 1



		paths = list()
		nodeStack = list()
		edgeStack = list()
		sPath = list()
		pathCounter = 1
		uniqPathsEdges = list()
		dictEndNode_numberOfPaths = dict()

		beginTracing()
		while True:
			sNode = [N.id   for N in nodeStack]
			sEdge = [(E.id, E.traced)   for E in edgeStack]

			E = actualNode.getOutEdgeToScan()
			if E is None:
				savePath()
				goBackToFirstNodeInStack()
				endTracing()
				break

			if not E.canTrace:
				continue

			goForward()
			if isEndOfPath():
				savePath()
				goBackToFirstNodeInStack()
				break

		return(paths)


	def getFirstPathsToAllEndsFromNode(self, actualNode):

		def beginTracing():
			nonlocal nodeStack, sPath, actualNode
			nodeStack.append(actualNode)
			sPath.append(actualNode.id)
			actualNode.setInEdge(None)
			actualNode.setOutEdgesToScan()

		def canGoForward():
			nonlocal actualNode, nodeStack
			otherNode = E.getOtherNode(actualNode)
			if otherNode in nodeStack:
				return(False)
			else:
				return(True)

		def goForward():
			nonlocal edgeStack, actualNode, E, nodeStack, sPath

			E.traced = True
			edgeStack.append(E)
			sPath.append(E.id)

			otherNode = E.getOtherNode(actualNode)
			otherNode.setInEdge(E)
			otherNode.setOutEdgesToScan()

			sPath.append(otherNode.id)
			nodeStack.append(otherNode)
			actualNode = otherNode


		def goBack():
			nonlocal nodeStack, actualNode, sPath, edgeStack

			actualNode.deleteOutEdgesToScan()
			actualNode.untraceInEdge()
			actualNode.deleteInEdge()

			nodeStack.pop()
			actualNode = nodeStack[-1]

			edgeStack.pop()

			sPath.pop()
			sPath.pop()


		def endTracing():
			nonlocal nodeStack, actualNode
			actualNode.deleteOutEdgesToScan()
			actualNode.deleteInEdge()
			actualNode = None
			nodeStack.pop()


		def isEndOfPath():
			nonlocal self, actualNode
			#if (actualNode.isGoal() and actualNode.belongToPlayerID!=self.playerID) or \
			#	actualNode.isOnlyOneUsedOrTracedEdge():
			if actualNode.isGoal() or actualNode.isOnlyOneUsedOrTracedEdge():
				return(True)
			else:
				return(False)

		def savePath():
			nonlocal pathCounter, actualNode, nodeStack, edgeStack, paths, uniqPathsEdges
			# check if edges in different order are used in previous paths
			hiEdges = sorted([E.hashIndex    for E in edgeStack])
			if hiEdges in uniqPathsEdges:
				return
			uniqPathsEdges.append(hiEdges)

			path = Path()
			path.id = pathCounter
			path.isGoal = actualNode.isGoal()
			path.goalDistance = self.getGoalDistance(actualNode)
			path.nodesTraced = nodeStack.copy()
			path.edgesTraced = edgeStack.copy()
			path.myTurn = self.myTurn
			path.numberOfTracedNodes = len(path.nodesTraced)
			path.numberOfTracedEdges = len(path.edgesTraced)
			path.totalNumber = path.numberOfTracedNodes + path.numberOfTracedEdges
			paths.append(path)
			pathCounter += 1


		paths = list()
		nodeStack = list()
		edgeStack = list()
		sPath = list()
		pathCounter = 1
		uniqPathsEdges = list()
		endNodes = list()

		beginTracing()
		while True:
			sNode = [N.id   for N in nodeStack]
			sEdge = [(E.id, E.traced)   for E in edgeStack]

			E = actualNode.getOutEdgeToScan()
			if E is None:
				if len(nodeStack)==1:
					endTracing()
					break
				self.setEdgesCanTraceOfNodesToFalse([actualNode])
				goBack()
				continue

			if not E.canTrace:
				continue

			if not canGoForward():
				continue

			goForward()
			if isEndOfPath():
				savePath()
				self.setEdgesCanTraceOfNodesToFalse([actualNode])
				goBack()

		return(paths)


	def getGoalDistance(self, actualNode):
		if self.myTurn:
			goalNodes = self.opponentGoalNodes
		else:
			goalNodes = self.myGoalNodes

		prepony = list()
		for G in goalNodes:
			dx = abs(actualNode.fieldPoint.col - G.fieldPoint.col)
			dy = abs(actualNode.fieldPoint.row - G.fieldPoint.row)
			prepona = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
			prepony.append(prepona)
		return(min(prepony))


	def setStyleToPathTreeView(self):
		trvPath = self.trvPath
		trvPath.configure(columns=['PathID', 'IsGoal', 'GoalDistance', 'MyTurn',
							 'NumOfNodes', 'NumOfEdges', 'TotalNum'])
		trvPath.heading("#0",text="#")
		trvPath.heading("#0",anchor="center")
		trvPath.column("#0",width="30")
		trvPath.column("#0",minwidth="30")
		trvPath.column("#0",stretch="0")
		trvPath.column("#0",anchor="w")
		trvPath.heading("PathID",text="PathID")
		trvPath.heading("PathID",anchor="center")
		trvPath.column("PathID",width="100")
		trvPath.column("PathID",minwidth="100")
		trvPath.column("PathID",stretch="0")
		trvPath.column("PathID",anchor="w")
		trvPath.heading("IsGoal",text="IsGoal")
		trvPath.heading("IsGoal",anchor="center")
		trvPath.column("IsGoal",width="50")
		trvPath.column("IsGoal",minwidth="50")
		trvPath.column("IsGoal",stretch="0")
		trvPath.column("IsGoal",anchor="w")
		trvPath.heading("GoalDistance",text="GoalDistance")
		trvPath.heading("GoalDistance",anchor="center")
		trvPath.column("GoalDistance",width="50")
		trvPath.column("GoalDistance",minwidth="50")
		trvPath.column("GoalDistance",stretch="0")
		trvPath.column("GoalDistance",anchor="w")
		trvPath.heading("MyTurn",text="MyTurn")
		trvPath.heading("MyTurn",anchor="center")
		trvPath.column("MyTurn",width="50")
		trvPath.column("MyTurn",minwidth="50")
		trvPath.column("MyTurn",stretch="0")
		trvPath.column("MyTurn",anchor="w")
		trvPath.heading("NumOfNodes",text="NumOfNodes")
		trvPath.heading("NumOfNodes",anchor="center")
		trvPath.column("NumOfNodes",width="50")
		trvPath.column("NumOfNodes",minwidth="50")
		trvPath.column("NumOfNodes",stretch="0")
		trvPath.column("NumOfNodes",anchor="w")
		trvPath.heading("NumOfEdges",text="NumOfEdges")
		trvPath.heading("NumOfEdges",anchor="center")
		trvPath.column("NumOfEdges",width="50")
		trvPath.column("NumOfEdges",minwidth="50")
		trvPath.column("NumOfEdges",stretch="0")
		trvPath.column("NumOfEdges",anchor="w")
		trvPath.heading("TotalNum",text="TotalNum")
		trvPath.heading("TotalNum",anchor="center")
		trvPath.column("TotalNum",width="50")
		trvPath.column("TotalNum",minwidth="50")
		trvPath.column("TotalNum",stretch="0")
		trvPath.column("TotalNum",anchor="w")

			
	def fillPathTreeView_folderItems_andAddItemIDtoPath(self, folder, paths):
		trvPath = self.trvPath
		for ind, p in enumerate(paths):
			iid = trvPath.insert(folder, 'end', text=ind, values=(p.id, p.isGoal, 
											   p.goalDistance, p.myTurn,
											   p.numberOfTracedNodes, p.numberOfTracedEdges,
											   p.totalNumber))
			p.treeviewItemID = iid

			
	def activateMyTurn(self):
		self.myTurn = True

	def activateOpponentTurn(self):
		self.myTurn = False

	def setNodesNumberOfPathsToZero(self, nodes):
		for N in nodes:
			N.numberOfPaths = 0

	def play(self):
		self.activateMyTurn()
		self.setAllEdgesCanTraceToTrue()

		# simple(fast) path search
		firstPaths = self.getFirstPathsToAllEndsFromNode(self.actualNode)
		self.setAllEdgesCanTraceToTrue()
		firstPaths = sorted(firstPaths, key=lambda x: (x.goalDistance))

		if len(firstPaths)==0:
			p = self.getAnyFirstPath(self.actualNode)
			p = p[0]
			self.selectedNodePath = p.nodesTraced
			self.selectedNodePath = self.selectedNodePath[1:]
			return

		# if goal path exists then return it
		goalPath = [P    for P in firstPaths    if P.goalDistance==0]
		if 0<len(goalPath):
			self.selectedNodePath = goalPath[0].nodesTraced
			self.selectedNodePath = self.selectedNodePath[1:]
			return

		# prepare for tracing, get all paths, remove short paths
		endNodes = [P.nodesTraced[-1]     for P in firstPaths]
		#endNodes = self.getNodesWithFarGoalDistance(endNodes)
		#self.setEdgesCanTraceOfNodesToFalse(endNodes)
		self.setNodesNumberOfPathsToZero(self.nodes)

		# set timer to stop  time exhausted tracing "getAllPathsFromNode"
		self.stopThread = False
		def setStopThread():
			self.stopThread = True
		timer = threading.Timer(self.threadTimeout, setStopThread)
		timer.start()
		paths = self.getAllPathsFromNode(self.actualNode)
		timer.cancel()

		self.setAllEdgesCanTraceToTrue()
		#paths = self.removePathsWithLowerTotalNumber(paths)

		# simulate contra-move, only end nodes are enough
		self.activateOpponentTurn()
		nearestGoalDistance = list()
		for P in paths:
			self.setAllEdgesCanTraceToTrue()

			self.setCanTraceForEdges(P.edgesTraced, False)

			firstPathsToEndNodes = self.getFirstPathsToAllEndsFromNode(P.nodesTraced[-1])
			if len(firstPathsToEndNodes)==0:
				nearestGoalDistance.append(0)
			else:
				self.setAllEdgesCanTraceToTrue()
				endNodes = [P.nodesTraced[-1]    for P in firstPathsToEndNodes]
				nearestGoalDistance.append(self.getNearestGoalDistanceForNodes(endNodes))

		# create AItable and sort it
		AItable = list()
		for ind, P in enumerate(paths):
			AItable.append([P, P.totalNumber, nearestGoalDistance[ind]])
		AItable = sorted(AItable, key=lambda x: (-x[2], -x[1]))

		# first path is the best :)
		if 0<len(AItable):
			self.selectedNodePath = AItable[0][0].nodesTraced
		else:
			if 0<len(firstPaths):
				self.selectedNodePath = firstPaths[0].nodesTraced
			else:
				p = self.getAnyFirstPath(self.actualNode)
				p = p[0]
				self.selectedNodePath = p.nodesTraced

		self.selectedNodePath = self.selectedNodePath[1:]



	# TODO: tridu Path presun do field.py
class Path():
	id = None				# tuple of integers
	isGoal = None			# boolean
	goalDistance = None		# integer
	nodesTraced = None		# tuple of nodes
	edgesTraced = None		# tuple of edges
	myTurn = None			# False = opponent turn
	numberOfTracedNodes = None
	numberOfTracedEdges = None
	totalNumber = None
	treeviewItemID = None



if __name__ == '__main__':

	from field import Field, FieldPointType
	from node import Node
	from edge import Edge
	F = Field()

	N1 = Node(); N1.id = 'N1'
	N2 = Node(); N2.id = 'N2'
	N3 = Node(); N3.id = 'N3'
	N4 = Node(); N4.id = 'N4'; N4.fieldPointType = FieldPointType.Goal

	E1 = Edge(); E1.id = 'E1'
	E2 = Edge(); E2.id = 'E2'
	E3 = Edge(); E3.id = 'E3'
	E4 = Edge(); E4.id = 'E4'

	N1.addEdge(E1)
	N2.addEdge(E1); N2.addEdge(E2); N2.addEdge(E3); N2.addEdge(E4)
	N3.addEdge(E2); N3.addEdge(E3)
	N4.addEdge(E4)

	E1.addNode(N1); E1.addNode(N2)
	E2.addNode(N2); E2.addNode(N3)
	E3.addNode(N2); E3.addNode(N3)
	E4.addNode(N2); E4.addNode(N4)

	F.nodes = [N1, N2, N3, N4]
	F.edges = [E1, E2, E3, E4]
	F.actualNode = N1

	for N in F.nodes:
		N.fieldPoint.col = 0
		N.fieldPoint.row = 0

	AI = PlayerAI(F, 0)
	for N in AI.genMoveToNode():
		print(N.id)

	debug = 1
