"""
This module was created, because Numpy takes after cx_freeze over 100 MB.
"""


def ones(const, numberOfRows, numberOfColumns):
	a = [[const]*numberOfColumns    for iR in range(numberOfRows)]
	return(a)


def vstack(args):
	# check for second dimension equality
	numberOfColumns = list()
	for arg in args:
		secondDim = [len(arg[iR])    for iR in range(len(arg))]
		numberOfColumns.extend(secondDim)

	uniqNumberOfColumns = set(numberOfColumns)
	if len(uniqNumberOfColumns)!=1:
		raise Exception('Non-consistent number of columns.')

	a = list()
	for arg in args:
		a.extend(arg)
	return(a)


def hstack(args):
	# check for first dimension equality
	numberOfRows = [len(arg)     for arg in args]
	uniqNumberOfRows = set(numberOfRows)
	if len(uniqNumberOfRows)!=1:
		raise Exception('Non-consistent number of rows.')

	uniqNumberOfRows = list(uniqNumberOfRows)[0]
	a = list()
	for iR in range(uniqNumberOfRows):
		row = list()
		for arg in args:
			row.extend(arg[iR])
		a.append(row)
	return(a)


def repeat(what, howManyTimes, axis):
	if axis==0:
		numberOfRows = howManyTimes
		numberOfColumns = 1
	elif axis==1:
		numberOfRows = 1
		numberOfColumns = howManyTimes
	else:
		raise Exception('Not allowed axis. Choose 0(rows) or 1(columns)')

	a = [what*numberOfColumns    for iR in range(numberOfRows)]
	return(a)

def size(a, axis):
	if axis==0:
		return(len(a))
	elif axis==1:
		return(len(a[0]))
	else:
		raise Exception('Not allowed axis. Choose 0(rows) or 1(columns)')

if __name__ == '__main__':
	a = ones(1, 5, 3)
	b = ones(2, 2, 3)
	c = vstack([a, b])

	a = ones(1, 3, 5)
	b = ones(2, 3, 2)
	c = hstack([a, b])

	a = [1, 2, 3]
	c = repeat(a, 4, 0)

	a = [1, 2, 3]
	c = repeat(a, 4, 1)

	a = ones(1, 3, 5)
	c = size(a, 0)
	c = size(a, 1)

	debug = 1
