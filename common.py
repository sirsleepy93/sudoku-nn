import numpy as np
import itertools as it

# Return a list of all indices
def get_grid(size=3):
	enum = range(np.square(size))
	return [g for g in it.product(enum, enum)]


# Yield a list of all rows
def row_units(size=3):
	grid = get_grid(size)
	for i in range(np.square(size)):
		yield([idx for idx in grid if idx[0] == i])


# Yield a list of all columns
def column_units(size=3):
	grid = get_grid(size)
	for i in range(np.square(size)):
		yield([idx for idx in grid if idx[1] == i])


# Yield a list of all squares
def square_units(size=3):
	enum = range(size)
	key_grid = [g for g in it.product(enum, enum)]

	# Make first column of boxes
	cols = [[(kg1 + i, kg2) for (kg1, kg2) in key_grid]
	 		for i in range(0, np.square(size), size)]

	# Yield each grid adding appropriate numbers to the rows as necessary.
	# Note we start from zero in the loop to yield the originally generated
	# columns in cols[].
	for i in range(0, np.square(size), size):
		# For each col in column: return a list of coordinate tuples with value
		# i appended to the row.
		grids = [[(c1, c2 + i) for (c1, c2) in col] for col in cols]
		for grid in grids:
			yield(grid)


# Return a list of all rows, cols, and sqrs
def unit_list(size=3):
	units = []
	units += [unit for unit in row_units(size)]
	units += [unit for unit in column_units(size)]
	units += [unit for unit in square_units(size)]
	return units

# Return a list of tuples representing all peers of an index
def peers(size=3):
	grid = get_grid(size)

	units = dict((idx, [unit for unit in unit_list(size) if idx in unit])
				  for idx in grid)
	assert len(units) == np.power(size, 4)

	peers = dict((idx, set(sum(units[idx],[])) - set([idx])) for idx in grid)
	assert len(peers[(0,0)]) == 2 * (np.square(size) - 1) + \
	 							np.square(size) - (2 * size - 1)

	return peers
"""
#print(peers(3)[(0,0)])
for g in square_units():
	print(g)
"""
