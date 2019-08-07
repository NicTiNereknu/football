import arrayManipulation as arrMan
import csv
import threading
import random
#from typing import *
from enum import Enum
from node import Node
from edge import Edge


class PlayerType():
	Human = 0
	AI = 1


class Field(object):
	"""class for creation of field"""

	edgeTypes = ('horz', 'vert', 'diag')
	deltaRC = ((0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (1,1))
	deltaRCtext = ('horz', 'diag', 'vert', 'diag', 'horz', 'diag', 'vert', 'diag')

	nodeRadius = 5
	nodeWidth = 2 * nodeRadius
	horzNodeDistance = 20
	vertNodeDistance = 20

	colorNodeDefault = 'antique white'
	colorNodeActual = 'cornflower blue'
	colorEdgeDefault = 'antique white'
	colorEdgePlayer1 = 'cornflower blue'
	colorEdgePlayer2 = 'red'
	colorEdgePlayers = [colorEdgePlayer1, colorEdgePlayer2]
	colorEdgeBorder = 'black'
	colorEdgeSelected = 'green yellow'
	widthEdgeDefault = 1
	widthEdgeUsed = 2
	widthEdgeSelected = 4


	dictFieldPointsType_canCreate = None
	dictFieldPointsTypeCombinaction_edgeType = None
	dictBorderFieldPointsTypeCombinaction_edgeType = None
	dictNodeFieldPoint_node = None
	dictGraphicID_node = None

	numberOfGoalCells = None
	numberOfHorzCells = None
	numberOfVertCells = None
	numberOfGoalPoints = None
	numberOfHorzPoints = None
	numberOfVertPoints = None

	rowGoalPoints = None
	rowGoalLinePoints = None
	rowsInnerFieldPoints = None
	mFieldPointsType = None

	nodes = None
	edges = None

	canvas = None
	label = None
	trvPath = None
	canvasArrowUP = None
	canvasArrowDOWN = None
	actualNode : Node = None
	actualPlayerID = 0	# 0 or 1 (False or True)
	playersName = list()
	#playersType = [PlayerType.Human, PlayerType.AI]
	playersType = list()
	players = list()

	isNodeClicked = False

	def __init__(self):
		self.readAndCreateFieldPointsTypeCanCreateDictionary()
		self.readAndCreateFieldPointsTypeCombinationDictionary()
		self.readAndCreateBorderFieldPointsTypeCombinationDictionary()

	def readAndCreateFieldPointsTypeCanCreateDictionary(self):
		self.dictFieldPointsType_canCreate = dict()

		with open('FieldPointsType.csv', newline='') as csvfile:
			csvReader = csv.reader(csvfile, delimiter=';')
			for ind, row in enumerate(csvReader):
				if ind == 0: continue
				# get fields
				typ = int(row[0])
				canCreate = bool(int(row[1]))

				# save to dictionay
				self.dictFieldPointsType_canCreate[typ] = canCreate

	def readAndCreateFieldPointsTypeCombinationDictionary(self):
		self.dictFieldPointsTypeCombinaction_edgeType = dict()

		with open('FieldPointsTypeCombination.csv', newline='') as csvfile:
			csvReader = csv.reader(csvfile, delimiter=';')
			for ind, row in enumerate(csvReader):
				if ind == 0: continue
				# get fields
				typ1 = int(row[0])
				typ2 = int(row[1])
				#
				csvEdgeTypeAllowed = [int(x)   for x in row[2:]]
				connection = [self.edgeTypes[ind] 
							  for ind, allowed in enumerate(csvEdgeTypeAllowed)
							  if allowed]

				# save to dictionay
				key = (typ1, typ2)
				self.dictFieldPointsTypeCombinaction_edgeType[key] = connection

	def readAndCreateBorderFieldPointsTypeCombinationDictionary(self):
		self.dictBorderFieldPointsTypeCombinaction_edgeType = dict()

		with open('BorderTypeCombination.csv', newline='') as csvfile:
			csvReader = csv.reader(csvfile, delimiter=';')
			for ind, row in enumerate(csvReader):
				if ind == 0: continue
				# get fields
				typ1 = int(row[0])
				typ2 = int(row[1])
				#
				csvEdgeTypeAllowed = [int(x)   for x in row[2:]]
				connection = [self.edgeTypes[ind] 
							  for ind, allowed in enumerate(csvEdgeTypeAllowed)
							  if allowed]

				# save to dictionay
				key = (typ1, typ2)
				self.dictBorderFieldPointsTypeCombinaction_edgeType[key] = connection


	def setWidgets(self, canvas, label, trvPath, canvasArrowUP, canvasArrowDOWN):
		self.canvas = canvas
		self.label = label
		self.trvPath = trvPath
		self.canvasArrowUP = canvasArrowUP
		self.canvasArrowDOWN = canvasArrowDOWN


	def createFieldPointsTypeMatrix(self, numberOfGoalCells, numberOfHorzCells, numberOfVertCells):
		self.numberOfGoalCells = numberOfGoalCells
		self.numberOfHorzCells = numberOfHorzCells
		self.numberOfVertCells = numberOfVertCells

		self.numberOfGoalPoints = self.numberOfGoalCells + 1
		self.numberOfHorzPoints = self.numberOfHorzCells + 1
		self.numberOfVertPoints = self.numberOfVertCells + 1

		self.createRowGoalPoints()
		self.createRowGoalLinePoints()
		self.createRowsInnerFieldPoints()
		self.completeField()

	def createRowGoalPoints(self):
		#hlp1 = FieldPointType.Nothing * numpy.ones((1, int((self.numberOfHorzPoints - self.numberOfGoalPoints) / 2)))
		#hlp2 = FieldPointType.Goal * numpy.ones((1, self.numberOfGoalPoints))
		#self.rowGoalPoints = numpy.hstack((hlp1, hlp2, hlp1))
		hlp1 = arrMan.ones(FieldPointType.Nothing, 1, int((self.numberOfHorzPoints - self.numberOfGoalPoints) / 2))
		hlp2 = arrMan.ones(FieldPointType.Goal, 1, self.numberOfGoalPoints)
		self.rowGoalPoints = arrMan.hstack((hlp1, hlp2, hlp1))

	def createRowGoalLinePoints(self):
		hlp1 = arrMan.ones(FieldPointType.FieldEdge, 1, int((self.numberOfHorzPoints - self.numberOfGoalPoints) / 2))
		hlp2 = arrMan.ones(FieldPointType.Goalpost, 1, 1)
		hlp3 = arrMan.ones(FieldPointType.InnerField, 1, int(self.numberOfGoalPoints - 2))
		self.rowGoalLinePoints = arrMan.hstack((hlp1, hlp2, hlp3, hlp2, hlp1))

	def createRowsInnerFieldPoints(self):
		hlp1 = arrMan.ones(FieldPointType.FieldEdge, 1, 1)
		hlp2 = arrMan.ones(FieldPointType.InnerField, 1, self.numberOfHorzPoints - 2)
		rowFieldPoints = arrMan.hstack((hlp1, hlp2, hlp1))
		self.rowsInnerFieldPoints = arrMan.repeat(rowFieldPoints[0], self.numberOfVertPoints - 1, axis=0)

	def completeField(self):
		# join previously created rows
		mFieldPointsType = arrMan.vstack((self.rowGoalPoints, self.rowGoalLinePoints,
							   self.rowsInnerFieldPoints, self.rowGoalLinePoints, self.rowGoalPoints))
		# create zero roundings (zeros rows)
		hlp = arrMan.ones(FieldPointType.Nothing, 1, arrMan.size(mFieldPointsType, 1))
		mFieldPointsType = arrMan.vstack((hlp, mFieldPointsType, hlp))
		#   (zeros columns)
		hlp = arrMan.ones(FieldPointType.Nothing, arrMan.size(mFieldPointsType, 0), 1)
		mFieldPointsType = arrMan.hstack((hlp, mFieldPointsType, hlp))

		self.mFieldPointsType = mFieldPointsType




	def createNodesAndEdges(self):
		self.nodes = list()
		self.edges = list()

		self.createNodes()
		self.dictNodeRowCol_node = { (N.fieldPoint.row, N.fieldPoint.col):N     for N in self.nodes}

		for N1, p1, p1_type in self.genNode_andNodePoint_AndNodeType():
			for N2, p2, p2_type, dRCtext in self.genNeighbourNode_andFieldPoint_andType_andDeltaRCtext(p1):
				if self.isEdgeBetweenFieldPointsTypeAllowed(p1_type, p2_type, dRCtext):
					#print((p1, p1_type, p2, p2_type, dRCtext))
					self.createEdge(N1, N2)

		self.setGoalNodesToPlayers()
		self.setNodesAndEdgesHashIndex()
		# randomize path order by shuffeling edges
		self.shuffleEdgesInNodes()

	def createNodes(self):
		for p1, p1_type in self.genRCandType_ofFieldPoints():
			if not self.dictFieldPointsType_canCreate[p1_type]:
				continue
			self.createNode(p1, p1_type)

	def genRCandType_ofFieldPoints(self):
		for iR in range(0, arrMan.size(self.mFieldPointsType, 0)):
			for iC in range(0, arrMan.size(self.mFieldPointsType, 1)):
				yield (FieldPoint(row = iR, col = iC),  self.mFieldPointsType[iR][iC])

	def createNode(self, p, p_type):
		N = Node()
		N.fieldPoint = p
		N.fieldPointType = p_type
		N.id = ''.join(('node_', str(len(self.nodes))))
		# and save
		self.nodes.append(N)


	def genNode_andNodePoint_AndNodeType(self):
		for N in self.nodes:
			yield (N, N.fieldPoint, N.fieldPointType)

	def genNeighbourNode_andFieldPoint_andType_andDeltaRCtext(self, fieldPoint):
		for n in range(len(self.deltaRC)):
			dRC = self.deltaRC[n]
			r = fieldPoint.row + dRC[0]
			c = fieldPoint.col + dRC[1]
			try:
				N = self.dictNodeRowCol_node[(r, c)]
			except:
				continue
			yield (N, FieldPoint(row = r, col = c), N.fieldPointType, self.deltaRCtext[n])

	def isEdgeBetweenFieldPointsTypeAllowed(self, p1_type, p2_type, dRCtext):
		key = tuple(sorted([p1_type, p2_type]))
		allowedEdgeType = self.dictFieldPointsTypeCombinaction_edgeType[key]
		if dRCtext in allowedEdgeType:
			return True
		else:
			return False

	def createEdge(self, N1, N2):
		# create edge id
		ind1 = int(N1.id.replace('node_', ''))
		ind2 = int(N2.id.replace('node_', ''))
		hlp = sorted([ind1, ind2])
		id = ''.join(('edge_', str(hlp[0]), '-', str(hlp[1])))

		# check edge id if exist in e.g.  first node
		if self.isEdgeIdInNodeEdges(N1, id):
			return

		E = Edge()
		E.id = id
		E.used = False
		E.nodes.extend((N1, N2))
		# and save
		self.edges.append(E)

		# add edge to nodes
		N1.edges.append(E)
		N2.edges.append(E)

	def isEdgeIdInNodeEdges(self, N, Eid):
		hlp = [True    for E in N.edges    if E.id == Eid]
		if len(hlp) == 0:
			return False
		else:
			return True

	def setGoalNodesToPlayers(self):
		mN = [N    for N in self.nodes    if N.fieldPointType==FieldPointType.Goal]
		uniqRowNumber = sorted({N.fieldPoint.row    for N in mN})
		for playerID in [0, 1]:
			goalN = [N    for N in mN    if N.fieldPoint.row==uniqRowNumber[playerID]]
			for N in goalN:
				N.belongToPlayerID = playerID

	def setNodesAndEdgesHashIndex(self):
		for ind, N in enumerate(self.nodes):
			N.hashIndex = ind
		for ind, E in enumerate(self.edges):
			E.hashIndex = ind

	def shuffleEdgesInNodes(self):
		for N in self.nodes:
			random.shuffle(N.edges)



	def createGraphicNodesAndEdges(self):
		canvas = self.canvas
		canvas.delete('all')
		self.createGraphicNodes()
		self.createGraphicEdges()
		self.setBorderGraphicEdges()
		self.dictGraphicID_node = {N.graphic:N    for N in self.nodes}

	def createGraphicNodes(self):
		canvas = self.canvas
		for N in self.nodes:
			c = N.fieldPoint.col
			r = N.fieldPoint.row
			centerX = c * self.horzNodeDistance + self.nodeWidth
			centerY = r * self.vertNodeDistance + self.nodeWidth
			x0 = centerX - self.nodeRadius
			y0 = centerY - self.nodeRadius
			x1 = centerX + self.nodeRadius
			y1 = centerY + self.nodeRadius
			id = canvas.create_oval(x0, y0, x1, y1)
			canvas.itemconfig(id, fill=self.colorNodeDefault)
			canvas.tag_bind(id, '<Button-1>', self.nodeGraphic_Click)
			# and save
			N.canvas = canvas
			N.graphic = id

	def createGraphicEdges(self):
		canvas = self.canvas
		for E in self.edges:
			x = []
			y = []
			for N in E.nodes:
				#hlp = canvas.itemcget(N.graphic, 'bbox')
				(x0, y0, x1, y1) = canvas.bbox(N.graphic)
				centerX = x0 + int((x1 - x0) / 2)
				centerY = y0 + int((y1 - y0) / 2)
				x.append(centerX)
				y.append(centerY)

			id = canvas.create_line(x[0], y[0], x[1], y[1],
						   fill=self.colorEdgeDefault, width=self.widthEdgeDefault)
			canvas.tag_lower(id)
			E.canvas = canvas
			E.graphic = id

	def setBorderGraphicEdges(self):
		for N1, p1, p1_type in self.genNode_andNodePoint_AndNodeType():
			for N2, p2, p2_type, dRCtext in self.genNeighbourNode_andFieldPoint_andType_andDeltaRCtext(p1):
				if self.isBorderEdge(p1_type, p2_type, dRCtext):
					E = Edge.getEdgeBetweenNodes(N1, N2)
					E.used = True
					self.canvas.itemconfig(E.graphic, fill=self.colorEdgeBorder, width=self.widthEdgeUsed)

	def isBorderEdge(self, p1_type, p2_type, dRCtext):
		key = tuple(sorted([p1_type, p2_type]))
		allowedEdgeType = self.dictBorderFieldPointsTypeCombinaction_edgeType[key]
		if dRCtext in allowedEdgeType:
			return True
		else:
			return False

	def nodeGraphic_Click(self, e):
		if self.playersType[self.actualPlayerID]==PlayerType.AI:
			return
		canvas = self.canvas
		id = canvas.find_withtag('current')[0]
		N = self.dictGraphicID_node[id]
		print(''.join((   'graphicID=', str(id), ', node=', N.id  )))
		self.isNodeClicked = True

		if not self.canMakeMoveToNode(N):
			#self.callWinner(not self.actualPlayerID)
			return
		self.makeMoveToNode(N)
		state = self.evaluteCurrentState()
		if state=='game over':
			return
		elif state=='same player':
			pass
		elif state=='player change':
			timer = threading.Timer(0.1, self.letPlayerPlay)
			timer.start()


	def letPlayerPlay(self):
		if self.playersType[self.actualPlayerID]==PlayerType.Human:
			# "nodeGraphic_Click" takes care of human players
			pass
		elif self.playersType[self.actualPlayerID]==PlayerType.AI:
			origEdgesUsed = self.getEdgesUsed()

			AI = self.players[self.actualPlayerID]
			AI.actualNode = self.actualNode
			#AI.numberOfPathsToEndNodes = 10
			#AI.threadTimeout = 20
			AI.play()
			nodePath = AI.selectedNodePath

			self.setEdgesUsed(origEdgesUsed)
			for N in nodePath:
				if not self.canMakeMoveToNode(N):
					self.callWinner(not self.actualPlayerID)
					return
				self.makeMoveToNode(N)
				state = self.evaluteCurrentState()
				if state=='game over':
					return
				elif state=='same player':
					pass
				elif state=='player change':
					break

			self.canvas.update_idletasks()
			# call this function from new thread(Timer)
			timer = threading.Timer(0.1, self.letPlayerPlay)
			timer.start()

	def canMakeMoveToNode(self, N):
		# this function must be called for every player kind (human/AI/???)
		#---
		E = Edge.getEdgeBetweenNodes(N, self.actualNode)
		if E is None: return(False)
		if E.used: return(False)
		return(True)

	def makeMoveToNode(self, N):
		# this function must be called for every player kind (human/AI/???)
		#---
		E = Edge.getEdgeBetweenNodes(N, self.actualNode)
		if E is None: return
		if E.used: return

		self.setNodeGraphicAsDefault(self.actualNode)
		self.setNodeAndGraphicAsActual(N)
		self.setEdgeAndGraphicAsUsed(E)


	def evaluteCurrentState(self):
		# this function must be called for every player kind (human/AI/???)
		#---
		if self.actualNode.isGoal():
			self.callWinner(not self.actualNode.belongToPlayerID)
			return('game over')

		E = self.actualNode.getFirstNotUsedEdge()
		if E is None:
			self.callWinner(not self.actualPlayerID)
			return('game over')

		if self.actualNode.onlyOneUsedEdge():
			self.setActualPlayer(not self.actualPlayerID)
			return('player change')

		return('same player')




	def setNodeGraphicAsDefault(self, N):
		self.canvas.itemconfig(N.graphic, fill=self.colorNodeDefault)

	def setNodeAndGraphicAsActual(self, N):
		self.actualNode = N
		self.canvas.itemconfig(N.graphic, fill=self.colorNodeActual)

	def setEdgeAndGraphicAsUsed(self, E):
		E.used = True
		color = self.colorEdgePlayers[self.actualPlayerID]
		self.canvas.itemconfig(E.graphic, fill=color, width=self.widthEdgeUsed)

	def setEdgeAndGraphicAsSelected(self, E):
		E.used = True
		color = self.colorEdgeSelected
		self.canvas.itemconfig(E.graphic, fill=color, width=self.widthEdgeSelected)

	def setEdgeAndGraphicAsSelected_customColor(self, E, color):
		E.used = True
		self.canvas.itemconfig(E.graphic, fill=color, width=self.widthEdgeSelected)

	def setEdgeAndGraphicAsDefault(self, E):
		E.used = False
		color = self.colorEdgeDefault
		self.canvas.itemconfig(E.graphic, fill=color, width=self.widthEdgeDefault)

	def callWinner(self, playerID):
		from tkinter import messagebox
		messagebox.showinfo('We have a winner', ''.join(('Player ', self.playersName[playerID], ' wins the game.')))


	def setStartNode(self):
		c = int(self.numberOfHorzPoints/2)
		r = int(self.numberOfVertPoints/2) + 2 # +2 row =goal points, goal-line points
		N = next((N   for N in self.nodes     if ((N.fieldPoint.row==r) and (N.fieldPoint.col==c))))
		self.setNodeAndGraphicAsActual(N)

	def setActualPlayer(self, playerID):
		self.actualPlayerID = playerID
		self.label.config(text=self.playersName[playerID])
		if playerID==0:
			#self.canvasArrowUP.place(self.canvasArrowUP.pi)
			self.canvasArrowUP.place_forget()
			self.canvasArrowDOWN.place(self.canvasArrowDOWN.pi)
			#self.canvasArrowDOWN.place_forget()
		else:
			self.canvasArrowDOWN.place_forget()
			self.canvasArrowUP.place(self.canvasArrowUP.pi)
			#self.canvasArrowDOWN.place(self.canvasArrowDOWN.pi)
			#self.canvasArrowUP.place_forget()
		
	def RGBtoHEX(rgb):
		return '#%02x%02x%02x' % rgb

	def HEXtoRGB(hex):
		hex = hex.lstrip('#')
		return(  tuple(  int(hex[i:i+2], 16) for i in (0, 2, 4)  )  )
			


	# TODO: nezapomen tyto dve funkce volat, pred volanim AI, kdyby to nahodou trasovanim prepsala
	def getEdgesUsed(self):
		edgesUsed = tuple([E.used    for E in self.edges])
		return(edgesUsed)
	def setEdgesUsed(self, edgesUsed):
		for ind, E in enumerate(self.edges):
			E.used = edgesUsed[ind]

	def clearPlayersData(self):
		self.playersName = list()
		self.playersType = list()
		self.players = list()

	def createHumanPlayer(self):
		self.players.append('human')
		self.playersName.append(''.join(['human', str(len(self.players))]))
		self.playersType.append(PlayerType.Human)

	def createAIplayer(self, AI, numberOfContraTurns, numberOfPathsToEndNodes, threadTimeout):
		playerID = len(self.players)
		ai = AI(self.actualNode, self.nodes, self.edges, playerID, numberOfContraTurns, self.trvPath)
		ai.numberOfPathsToEndNodes = numberOfPathsToEndNodes
		ai.threadTimeout = threadTimeout
		self.players.append(ai)
		self.playersName.append(''.join(('AI', str(playerID))))
		self.playersType.append(PlayerType.AI)


class FieldPoint:
	def __init__(self, row:int = 0, col: int = 0):
		self.row = row
		self.col = col

	def __repr__(self):
		return "".join(['Point(', str(self.row), ',', str(self.col), ')'])



class FieldPointType():
	Nothing = 0
	InnerField = 1
	FieldEdge = 2
	Goal = 3
	Goalpost = 4








if __name__ == '__main__':

	field = Field()

	field.readAndCreateFieldPointsTypeCanCreateDictionary()
	field.readAndCreateFieldPointsTypeCombinationDictionary()


	# pro fotbalove hriste by melo byt minimalne (sirkaBrany + 2) ctvercu
	# horizontalne a zvetsovat se po 2 (5:2:?)
	#    a pocet ctvercu horizontalne minimálne 4 a taky se zvetsovat po 2 (4:2:?)
	field.createFieldPointsTypeMatrix(numberOfGoalCells=3, numberOfHorzCells=5, numberOfVertCells=7)

	# create Nodes
	field.createNodesAndEdges()


	H = Edge()
	U = Node()

	debug = 1
