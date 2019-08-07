#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.22
#  in conjunction with Tcl version 8.6
#    Jun 11, 2019 11:58:47 AM CEST  platform: Windows NT
#    Jul 03, 2019 10:32:12 AM CEST  platform: Windows NT
#    Jul 03, 2019 08:19:10 PM CEST  platform: Windows NT
#    Jul 07, 2019 12:57:13 PM CEST  platform: Windows NT
#    Jul 07, 2019 08:44:09 PM CEST  platform: Windows NT
#    Jul 23, 2019 12:31:44 PM CEST  platform: Windows NT
#    Aug 07, 2019 09:15:59 AM CEST  platform: Windows NT

import sys
import field
import pokus
import pickle
import playerAI
import time
import gameSettings
import colorSettings

try:
	import Tkinter as tk
except ImportError:
	import tkinter as tk

try:
	import ttk
	py3 = False
except ImportError:
	import tkinter.ttk as ttk
	py3 = True

class MySave():
	edgesUsed = None
	actualNodeID = None

	def __init__(self):
		self.edgesUsed = w.Field.getEdgesUsed()
		self.actualNodeID = w.Field.actualNode.id


def btnSetColorProperties_OnClick(p1):
	colorSettings.create_Toplevel1(root, fcnSetColorProperties=setColorProperties)
	debug = 1

def setColorProperties():
	# nacti barvy ze souboru
	with open('colorSettings.pkl', 'rb') as f:
		mySave = pickle.load(f)

	w.Field.nodeRadius = mySave.nodeRadius
	w.Field.horzNodeDistance = mySave.horizontalNodeDistance
	w.Field.vertNodeDistance = mySave.verticalNodeDistance
	w.Field.widthEdgeDefault = mySave.edgeWidthDefault
	w.Field.widthEdgeUsed = mySave.edgeWidthUsed
	w.Field.colorNodeDefault = mySave.colorNodeDefault
	w.Field.colorNodeActual = mySave.colorNodeActual
	w.Field.colorEdgeDefault = mySave.colorEdgeDefault
	w.Field.colorEdgePlayer1 = mySave.colorEdgePlayer1
	w.Field.colorEdgePlayer2 = mySave.colorEdgePlayer2
	w.Field.colorEdgePlayers = [w.Field.colorEdgePlayer1, w.Field.colorEdgePlayer2]
	w.Field.colorEdgeBorder = mySave.colorEdgeBorder

def btnPlay_OnClick(p1):
	Field = w.Field
	prop = w.gameProperties

	if prop['size']=='small':
		(numberOfHorzCells, numberOfVertCells) = (5, 7)
	elif prop['size']=='medium':
		(numberOfHorzCells, numberOfVertCells) = (9, 13)
	elif prop['size']=='big':
		(numberOfHorzCells, numberOfVertCells) = (15, 21)
	else:
		raise Exception('Unknown field size')

	if prop['field']=='football':
		numberOfGoalCells = 3
	elif prop['field']=='hockey':
		numberOfGoalCells = 1
	elif prop['field']=='rugby':
		numberOfGoalCells = numberOfHorzCells
	else:
		raise Exception('Unknown field type')

	Field.createFieldPointsTypeMatrix(numberOfGoalCells, numberOfHorzCells, numberOfVertCells)
	Field.createNodesAndEdges()
	Field.createGraphicNodesAndEdges()
	changeToplevelAndCanvasSize()

	Field.setStartNode()

	Field.clearPlayersData()

	if prop['player1Type']=='human':
		Field.createHumanPlayer()
	elif prop['player1Type']=='AI':
		if prop['AI1difficulty']=='easy':
			Field.createAIplayer(playerAI.PlayerAI, 1, 1, 0.1)
		elif prop['AI1difficulty']=='medium':
			Field.createAIplayer(playerAI.PlayerAI, 1, 2, 1)
		elif prop['AI1difficulty']=='hard':
			Field.createAIplayer(playerAI.PlayerAI, 1, 1000, 20)
		else:
			raise Exception('Unknown AI difficulty')
	else:
		raise Exception('Unknown player type')

	if prop['player2Type']=='human':
		Field.createHumanPlayer()
	elif prop['player2Type']=='AI':
		if prop['AI2difficulty']=='easy':
			Field.createAIplayer(playerAI.PlayerAI, 1, 1, 0.1)
		elif prop['AI2difficulty']=='medium':
			Field.createAIplayer(playerAI.PlayerAI, 1, 2, 1)
		elif prop['AI2difficulty']=='hard':
			Field.createAIplayer(playerAI.PlayerAI, 1, 1000, 20)
		else:
			raise Exception('Unknown AI difficulty')
	else:
		raise Exception('Unknown player type')

	w.lblPlayer1Name.config(text=Field.playersName[0])
	w.lblPlayer2Name.config(text=Field.playersName[1])

	Field.setActualPlayer(0)
	Field.letPlayerPlay()

def changeToplevelAndCanvasSize():
	(bbox_x, bbox_y, bbox_width, bbox_height) = w.Canvas1.bbox(tk.ALL)
	canvas_newWidth = bbox_width + bbox_x
	canvas_newHeight = bbox_height + bbox_y
	canvas_pi = w.Canvas1.place_info()
	canvas_pi['width'] = str(canvas_newWidth)
	canvas_pi['height'] = str(canvas_newHeight)
	w.Canvas1.place(canvas_pi)

	(canvas_x, canvas_y) = (w.Canvas1.winfo_x(), w.Canvas1.winfo_y())
	top_newWidth = canvas_x + canvas_newWidth
	top_newHeight = canvas_y + canvas_newHeight
	top_level.geometry("%dx%d" % (top_newWidth, top_newHeight))

def btnSetGameProperties_OnClick(p1):
	gameSettings.create_Toplevel1(root, fcnSetGameProperties=setGameProperties,
							   gameProperties=w.gameProperties)

def trvPath_Select(p1):
	print('main_support.trvPath_Select')

	if w.selectedEdges_folder is not None:
		for E in w.selectedEdges_folder:
			w.Field.setEdgeAndGraphicAsDefault(E)

	if w.selectedEdges_item is not None:
		for E in w.selectedEdges_item:
			w.Field.setEdgeAndGraphicAsDefault(E)

	item_iid = w.trvPath.selection()[0]
	item = w.trvPath.item(item_iid)
	parent_iid = w.trvPath.parent(item_iid)
	parent = w.trvPath.item(parent_iid)

	if parent_iid=='':
		path = w.dictItemID_path[  item_iid  ]
		w.selectedEdges_folder = path.edgesTraced
		for E in w.selectedEdges_folder:
			w.Field.setEdgeAndGraphicAsSelected_customColor(E, 'green yellow')

		w.selectedEdges_item = None
	else:
		path = w.dictItemID_path[  parent_iid  ]
		w.selectedEdges_folder = path.edgesTraced
		for E in w.selectedEdges_folder:
			w.Field.setEdgeAndGraphicAsSelected_customColor(E, 'green yellow')

		path = w.dictItemID_path[  item_iid  ]
		w.selectedEdges_item = path.edgesTraced
		for E in w.selectedEdges_item:
			w.Field.setEdgeAndGraphicAsSelected_customColor(E, 'red2')

	sys.stdout.flush()

def btnPlayAI_Click(p1):
	print('main_support.btnPlayAI_Click')

	try:
		if w.selectedEdges_folder is not None:
			for E in w.selectedEdges_folder:
				w.Field.setEdgeAndGraphicAsDefault(E)
	except:
		pass

	AI = playerAI.PlayerAI(w.Field.actualNode, w.Field.nodes, w.Field.edges, w.Field.actualPlayerID, 0, w.trvPath)
	AI.activateMyTurn()
	AI.setAllEdgesCanTraceToTrue()

	# simple(fast) path search
	firstPaths = AI.getFirstPathsToAllEndsFromNode(w.Field.actualNode)
	AI.setAllEdgesCanTraceToTrue()
	firstPaths = sorted(firstPaths, key=lambda x: (x.goalDistance))

	# if goal path exists then return it
	goalPath = [P    for P in firstPaths    if P.goalDistance==0]
	if 0<len(goalPath):
		selectedPath = goalPath[0]
		return(selectedPath)

	# prepare for tracing, get all paths, remove short paths
	endNodes = [P.nodesTraced[-1]     for P in firstPaths]
	endNodes = AI.getNodesWithFarGoalDistance(endNodes)
	AI.setEdgesCanTraceOfNodesToFalse(endNodes)
	AI.setNodesNumberOfPathsToZero(AI.nodes)
	AI.numberOfPathsToEndNodes = int(w.txtNumberOfPathsToEndNodes.get())
	paths = AI.getAllPathsFromNode(w.Field.actualNode)
	AI.setAllEdgesCanTraceToTrue()
	paths = AI.removePathsWithLowerTotalNumber(paths)

	# simulate contra-move, only end nodes are enough
	AI.activateOpponentTurn()
	nearestGoalDistance = list()
	for P in paths:
		AI.setAllEdgesCanTraceToTrue()

		AI.setCanTraceForEdges(P.edgesTraced, False)

		firstPathsToEndNodes = AI.getFirstPathsToAllEndsFromNode(P.nodesTraced[-1])
		AI.setAllEdgesCanTraceToTrue()
		endNodes = [P.nodesTraced[-1]    for P in firstPathsToEndNodes]
		nearestGoalDistance.append(AI.getNearestGoalDistanceForNodes(endNodes))

	# create AItable and sort it
	AItable = list()
	for ind, P in enumerate(paths):
		AItable.append([P, P.totalNumber, nearestGoalDistance[ind]])
	AItable = sorted(AItable, key=lambda x: (-x[2], -x[1]))

	# first path is the best :)
	if 0<len(AItable):
		selectedPath = AItable[0][0]
	else:
		if 0<len(firstPaths):
			selectedPath = firstPaths[0]
		else:
			selectedPath = AI.getAnyFirstPath(w.Field.actualNode)

	# show in TreeView
	paths = [x[0]    for x in AItable]
	AI.setStyleToPathTreeView()
	w.trvPath.delete(*w.trvPath.get_children())
	AI.fillPathTreeView_folderItems_andAddItemIDtoPath('', paths)
	w.selectedEdges_folder = None
	w.selectedEdges_item = None

	# create path dictionary to highlight path on TreeView change event
	w.dictItemID_path = dict()
	for P in paths:
		w.dictItemID_path[P.treeviewItemID] = P

	sys.stdout.flush()

def btnLoadEdgesState_Click(p1):
	print('main_support.btnLoadEdgesState_Click')
	with open('mySave.pkl', 'rb') as f:
		mySave = pickle.load(f)

	w.Field.setEdgesUsed(mySave.edgesUsed)
	for E in w.Field.edges:
		if E.used:
			w.Field.setEdgeAndGraphicAsUsed(E)
		else:
			w.Field.setEdgeAndGraphicAsDefault(E)
	w.Field.setBorderGraphicEdges()

	w.Field.setNodeGraphicAsDefault(w.Field.actualNode)
	actualNode = [N   for N in w.Field.nodes   if N.id==mySave.actualNodeID]  [0]
	w.Field.setNodeAndGraphicAsActual(actualNode)

	sys.stdout.flush()

def btnSaveEdgesState_Click(p1):
	print('main_support.btnSaveEdgesState_Click')
	with open('mySave.pkl', 'wb') as f:
		mySave = MySave()
		pickle.dump(mySave, f)
	sys.stdout.flush()

def btnButton1_Click(p1):
	gameSettings.create_Toplevel1(root, fcnSetGameProperties=setGameProperties)

def setGameProperties(**kwargs):
	w.gameProperties = kwargs

def init(top, gui, *args, **kwargs):
	global w, top_level, root
	w = gui
	top_level = top
	root = top

	sv = tk.StringVar()
	sv.set('1')
	w.txtNumberOfPathsToEndNodes.config(textvariable=sv)

	setGameProperties(field = 'football',
						 size = 'small',
						 player1Type = 'human',
						 AI1difficulty = 'easy',
						 player2Type = 'AI',
						 AI2difficulty = 'easy')

	# for work comment this block
	w.Button1.place_forget()
	w.Label1.place_forget()
	w.btnLoadEdgesState.place_forget()
	w.btnPlayAI.place_forget()
	w.btnSaveEdgesState.place_forget()
	w.txtNumberOfPathsToEndNodes.place_forget()
	w.trvPath.place_forget()
	w.Label2.place_forget()

	w.imgUP = tk.PhotoImage(file='arrow-up-double-2.gif')
	w.canvasArrowUP.create_image(0, 0, anchor=tk.NW, image=w.imgUP)
	w.canvasArrowUP.pi = w.canvasArrowUP.place_info()
	w.canvasArrowUP.place_forget()

	w.imgDOWN = tk.PhotoImage(file='arrow-down-double-2.gif')
	w.canvasArrowDOWN.create_image(0, 0, anchor=tk.NW, image=w.imgDOWN)
	w.canvasArrowDOWN.pi = w.canvasArrowDOWN.place_info()
	w.canvasArrowDOWN.place_forget()

	Field = field.Field()
	Field.setWidgets(w.Canvas1, w.Label1, w.trvPath, w.canvasArrowUP, w.canvasArrowDOWN)
	w.Field = Field
	setColorProperties()

def destroy_window():
	# Function which closes the window.
	global top_level
	top_level.destroy()
	top_level = None

if __name__ == '__main__':
	import main
	main.vp_start_gui()




