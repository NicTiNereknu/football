import tkinter
import main
import importlib
import os
import field

def onObjectClick(e):
	print('klikl si na text')

def onLineClick(e):
	print('klikl si na caru')

def pokusHokus(canvas):
	obj1 = canvas.create_text(50, 30, text='Click me one')
	canvas.tag_bind(obj1, '<Button-1>', onObjectClick)
	obj1 = canvas.create_line(0, 0, 100, 100, fill="red")
	canvas.tag_bind(obj1, '<Button-1>', onLineClick)
	canvas.pack()


def getEdgeType(point1, point2):
	return 0









if __name__ == '__main__':

	import sys
	from threading import Thread
	import threading
	import time


	timer = threading.Timer(1, lambda: print('asdf'))
	timer.cancel()
	timer.cancel()
	timer.cancel()
	timer.cancel()
	timer.cancel()

	class classAI():
		counterSetActualPlayer = 0
		counterAImovement = 0

		def setActualPlayer(self):
			self.counterSetActualPlayer += 1
			print(''.join(('enter setActualPlayer  ', str(self.counterSetActualPlayer))))
			sys.stdout.flush()
			if 2<self.counterSetActualPlayer:
				print(''.join(('force return AImovement ', str(self.counterSetActualPlayer))))
				sys.stdout.flush()
				return()
			Thread(target=self.AImovement).start()
			print(''.join(('leave setActualPlayer ', str(self.counterSetActualPlayer))))
			sys.stdout.flush()


		def AImovement(self):
			self.counterAImovement += 1
			print(''.join(('enter AImovement ', str(self.counterAImovement))))
			sys.stdout.flush()
			time.sleep(self.counterAImovement*2)
			Thread(target=self.setActualPlayer).start()
			print(''.join(('leave AImovement ', str(self.counterAImovement))))
			sys.stdout.flush()

	print("enter main")
	sys.stdout.flush()
	AI = classAI()
	Thread(target=AI.setActualPlayer).start()
	print("leave main")
	sys.stdout.flush()


