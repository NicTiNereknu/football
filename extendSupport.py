#
# work on this was canceled
#

import re
import pathlib

mySupport = 'mySupport'
newLine = '\n'

def addMySupportToFile(filename, mySupportFilename):
	mySupportFilename = pathlib.Path(mySupportFilename).stem

	lines = readSupportFileLines(filename)

	#if linesAlreadyChanged(lines, mySupportFilename):
	#	print('File already changed.')
	#	return()

	lines = addImport(lines, mySupportFilename)




def readSupportFileLines(filename):
	with open(filename) as f:
		lines = f.readlines()
		return(lines)

def linesAlreadyChanged(lines, mySupportFilename):
	pattern = ''.join(('import.*', mySupportFilename))
	for s in lines:
		x = re.search(pattern, s)
		if x != None:
			return True
	return False


def addImport(lines, mySupportFilename):
	# find index of first import line
	pattern = '^import'
	for ind, s in enumerate(lines):
		x = re.search(pattern, s)
		if x != None:
			break
	# add my import to next line
	shlp = ''.join(('import ', mySupportFilename, ' as ', mySupport, newLine))
	a = lines.insert(ind+1, shlp)
	return lines






if __name__ == '__main__':
	addMySupportToFile('main_support.py', 'pokus.py')


	debug = 1


























