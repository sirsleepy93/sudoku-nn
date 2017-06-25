import numpy as np
import itertools as it

"""
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
"""

# Return a list of all indices
def get_grid(size=3):
	enum = range(np.square(size))
	return [g for g in it.product(enum, enum)]

# Return a list of all rows
def row_units(size=3):
	grid = get_grid(size)
	#row_units = []
	for i in range(np.square(size)):
		#row_units.append([idx for idx in grid if idx[1] == i])
		yield([idx for idx in grid if idx[0] == i])

	#assert len(row_units) == np.square(size)
	#return row_units

# Return a list of all columns
def column_units(size=3):
	grid = get_grid(size)
	#col_units = []
	for i in range(np.square(size)):
		#col_units.append([idx for idx in grid if idx[1] == i])
		yield([idx for idx in grid if idx[1] == i])

	#assert len(col_units) == np.square(size)
	#return col_units

# Return a list of all squares
def square_units(size=3):
	enum = range(size)
	key_grid = [g for g in it.product(enum, enum)]

	# Make first column of boxes
	col = [[(kg1 + i, kg2) for (kg1, kg2) in key_grid]
	 		for i in range(0, np.square(size), size)]

	# Fill out the rest
	#sqr_units = []
	for i in range(0, np.square(size), size):
		grid = [[(c1, c2 + i) for (c1, c2) in c] for c in col]
		for g in grid:
			#sqr_units.append(g)
			yield(g)

	#assert len(sqr_units) == np.square(size)
	#return sqr_units

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
