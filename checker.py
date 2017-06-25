assignments = []
from common import *
"""
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B): # needed here
	"Cross product of elements in A and elements in B."
	return [a+n for a in A for n in B]

def generate_diagonals():
	A = []
	B = []
	for i in range(len(rows)):
		A.append(rows[i]+cols[i])
		B.append(rows[i]+cols[-i - 1])
	return [A, B]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = generate_diagonals()
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
"""

# Function Declarations
def assign_value(values, box, value):
	"""
	Please use this function to update your values dictionary!
	Assigns a value to a given box. If it updates the board record it.
	"""

	# Don't waste memory appending actions that don't actually change any values
	if values[box] == value:
		return values

	values[box] = value
	if len(value) == 1:
		assignments.append(values.copy())
	return values

def naked_twins(values):
	"""Eliminate values using the naked twins strategy.
	Args:
		values(dict): a dictionary of the form {'box_name': '123456789', ...}

	Returns:
		the values dictionary with the naked twins eliminated from peers.
	"""

	# Find all instances of naked twins
	pairlist = [box for box in values.keys() if len(values[box]) == 2]

	twinlist = []
	for box1 in pairlist:
		for box2 in peers[box1]:
			if set(values[box1]) == set(values[box2]) and (box2, box1) not in twinlist:
				twinlist.append((box1, box2))

	# Eliminate the naked twins as possibilities for their peers
	for twins in twinlist:
		# get only mutual peers
		mutual = set(peers[twins[0]]) & set(peers[twins[1]])
		twin = twins[0]

		for peer in mutual:
			if len(values[peer]) > 2:
				for i in values[twin]:
					assign_value(values, peer, values[peer].replace(i, ''))
	#print(values)
	return values

def grid_values(grid):
	"""
	Convert grid into a dict of {square: char} with '123456789' for empties.
	Args:
		grid(string) - A grid in string form.
	Returns:
		A grid in dictionary form
			Keys: The boxes, e.g., 'A1'
			Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
	"""
	# Taken from Strategy 1: Elimination lesson
	values = []
	for box in grid:
		if box == '.':
			values.append(cols) # cols being 1 - 9
		elif box in cols:
			values.append(box)
	assert len(values) == 81
	return dict(zip(boxes, values))

def display(values):
	"""
	Display the values as a 2-D grid.
	Args:
		values(dict): The sudoku in dictionary form
	"""
	# Taken from Strategy 1: Elimination lesson
	boxes = cross(rows, cols)
	width = 1 + max(len(values[box]) for box in boxes)
	line = '+'.join(['-'*(width*3)]*3)
	for row in rows:
		print(''.join(values[row+col].center(width)+('|' if col in '36' else '')
					  for col in cols))
		if row in 'CF': print(line)
	return

def eliminate(values):
	solved = [key for key in values.keys() if len(values[key]) == 1]
	for idx in solved:
		for peer in peers[idx]:
			assign_value(values, peer, values[peer].replace(values[idx], ''))
			#values[peer] = values[peer].replace(values[idx], '')
	return values

def only_choice(values):
	for unit in unitlist:
		for i in cols:
			place = [box for box in unit if i in values[box]]
			if len(place) == 1:
				assign_value(values, place[0], i)
				#values[place[0]] = i
	return values


def num_possible(values, length = 1):
	# Return number of boxes with number of possibilities == length
	return len([box for box in values.keys() if len(values[box]) == length])

def reduce_puzzle(values):
	stalled = False
	#print("REDUCING")
	while not stalled:
		solved_before = num_possible(values)
		#print("Solved before: ", solved_before)

		values = eliminate(values)
		values = only_choice(values)
		values = naked_twins(values)

		solved_after = num_possible(values)
		#print("Solved after: ", solved_after)

		stalled = solved_before == solved_after

		if num_possible(values, 0):
			return False
	return values

def search(values):
	values = reduce_puzzle(values)

	if values is False:
		return False
	elif all(len(values[box]) == 1 for box in boxes):
		return values

	_, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

	for value in values[box]:
		#print("SEARCHING")
		puzzle = values.copy()
		puzzle[box] = value
		run = search(puzzle)
		if run:
			return run

def solve(grid):
	"""
	Find the solution to a Sudoku grid.
	Args:
	grid(string): a string representing a sudoku grid.
	Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
	Returns:
	The dictionary representation of the final sudoku grid. False if no solution exists.
	"""
	return search(grid_values(grid))

def set_diagonal_mode(switch):
	unitlist = row_units + column_units + square_units
	if switch == True:
		unitlist += diagonal_units


if __name__ == '__main__':
	print(units)

	set_diagonal_mode(True)
	diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
	display(solve(diag_sudoku_grid))

	try:
		from visualize import visualize_assignments
		visualize_assignments(assignments)

	except SystemExit:
		pass
	except:
		print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
