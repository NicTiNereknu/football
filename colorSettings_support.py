#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.22
#  in conjunction with Tcl version 8.6
#    Aug 06, 2019 10:47:59 AM CEST  platform: Windows NT
#    Aug 06, 2019 10:53:45 AM CEST  platform: Windows NT
#    Aug 06, 2019 12:41:36 PM CEST  platform: Windows NT
#    Aug 06, 2019 04:57:00 PM CEST  platform: Windows NT
#    Aug 06, 2019 05:19:33 PM CEST  platform: Windows NT
#    Aug 06, 2019 05:28:15 PM CEST  platform: Windows NT
#    Aug 07, 2019 09:42:26 AM CEST  platform: Windows NT

import sys
import pickle

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
	nodeRadius = None
	horizontalNodeDistance = None
	verticalNodeDistance = None
	edgeWidthDefault = None
	edgeWidthUsed = None
	colorNodeDefault = None
	colorNodeActual = None
	colorEdgeDefault = None
	colorEdgePlayer1 = None
	colorEdgePlayer2 = None
	colorEdgeBorder = None

	def __init__(self):
		self.nodeRadius = int(varSpnNodeRadius.get())
		self.horizontalNodeDistance = int(varSpnHorizontalNodeDistance.get())
		self.verticalNodeDistance = int(varSpnVerticalNodeDistance.get())
		self.edgeWidthDefault = int(varSpnEdgeWidthDefault.get())
		self.edgeWidthUsed = int(varSpnEdgeWidthUsed.get())
		self.colorNodeDefault = w.lblColorNodeDefault.cget('bg')
		self.colorNodeActual = w.lblColorNodeActual.cget('bg')
		self.colorEdgeDefault = w.lblColorEdgeDefault.cget('bg')
		self.colorEdgePlayer1 = w.lblColorEdgePlayer1.cget('bg')
		self.colorEdgePlayer2 = w.lblColorEdgePlayer2.cget('bg')
		self.colorEdgeBorder = w.lblColorEdgeBorder.cget('bg')

def set_Tk_var():
	global varSpnNodeRadius
	varSpnNodeRadius = tk.StringVar()
	global varSpnHorizontalNodeDistance
	varSpnHorizontalNodeDistance = tk.StringVar()
	global varSpnVerticalNodeDistance
	varSpnVerticalNodeDistance = tk.StringVar()
	global varSpnEdgeWidthDefault
	varSpnEdgeWidthDefault = tk.StringVar()
	global varSpnEdgeWidthUsed
	varSpnEdgeWidthUsed = tk.StringVar()

def btnCancel_OnClick(p1):
	destroy_window()

def lblColorPicker_OnClick(p1):
	lbl = p1.widget
	lblColor = lbl.cget('bg')
	from tkinter.colorchooser import askcolor
	color = askcolor(lblColor)
	color = color[1]
	if color is None: return
	lbl.config(bg=color)

def btnSave_OnClick(p1):
	#w.fcnSetColorProperties()
	# uloz barvy do souboru
	with open('colorSettings.pkl', 'wb') as f:
		mySave = MySave()
		pickle.dump(mySave, f)
	w.fcnSetColorProperties()
	destroy_window()

def setWidgets():
	# nacti barvy ze souboru
	with open('colorSettings.pkl', 'rb') as f:
		mySave = pickle.load(f)

	varSpnNodeRadius.set(str(mySave.nodeRadius))
	varSpnHorizontalNodeDistance.set(str(mySave.horizontalNodeDistance))
	varSpnVerticalNodeDistance.set(str(mySave.verticalNodeDistance))
	varSpnEdgeWidthDefault.set(str(mySave.edgeWidthDefault))
	varSpnEdgeWidthUsed.set(str(mySave.edgeWidthUsed))
	w.lblColorNodeDefault.config(bg=mySave.colorNodeDefault)
	w.lblColorNodeActual.config(bg=mySave.colorNodeActual)
	w.lblColorEdgeDefault.config(bg=mySave.colorEdgeDefault)
	w.lblColorEdgePlayer1.config(bg=mySave.colorEdgePlayer1)
	w.lblColorEdgePlayer2.config(bg=mySave.colorEdgePlayer2)
	w.lblColorEdgeBorder.config(bg=mySave.colorEdgeBorder)

	pass

def init(top, gui, *args, **kwargs):
	global w, top_level, root
	w = gui
	top_level = top
	root = top

	w.fcnSetColorProperties = kwargs['fcnSetColorProperties']

	setWidgets()

def destroy_window():
	# Function which closes the window.
	global top_level
	top_level.destroy()
	top_level = None

if __name__ == '__main__':
	import colorSettings
	colorSettings.vp_start_gui()




