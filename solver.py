import common
import numpy as np

class Solver:
	def __init__(self, size=3):
		self.unitlist = common.unit_list(size)
		self.peers = common.peers(size)
		#self.assignments = []
		self.vals = [v for v in range(1, np.square(size) + 1)]
		self.boxes = common.get_grid(size)

	"""
	def assign_value(self, values, box, value):
		# Don't waste memory appending actions that don't actually change any values
		if values[box] == value:
			return values

		values[box] = value
		print(value)
		if len(value) == 1:
			self.assignments.append(values.copy())
		return values
	"""

	def grid_values(self, grid):
		values = []
		for box in grid:
			if box == '0' or box == '.':
				values.append(self.vals)
			elif int(box) in self.vals:
				#print(int(box))
				values.append([int(box)])

		assert len(values) == 81
		return dict(zip(self.boxes, values))

	def search(self, values):
		if isinstance(values, str):
			values = self.grid_values(values)
			values = self.reduce_puzzle(values)

		elif isinstance(values, dict):
			values = self.reduce_puzzle(values)

		if values is False: # value
			return False
		elif all(len(values[box]) == 1 for box in self.boxes): # is solved?
			return values

		_, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

		for value in values[box]:
			#print("SEARCHING")
			puzzle = values.copy()
			puzzle[box] = value
			run = self.search(puzzle)
			if run:
				return run

	def num_possible(self, values, length = 1):
		# Return number of boxes with number of possibilities == length
		return len([box for box in values.keys() if len(values[box]) == length])

	def reduce_puzzle(self, values):
		stalled = False
		#print("REDUCING")
		while not stalled:
			solved_before = self.num_possible(values)
			#print("Solved before: ", solved_before)

			values = self.eliminate(values)
			values = self.only_choice(values)
			values = self.naked_twins(values)

			solved_after = self.num_possible(values)
			#print("Solved after: ", solved_after)

			stalled = solved_before == solved_after

			if self.num_possible(values, 0):
				return False
		return values

	def eliminate(self, values):
		solved = [key for key in values.keys() if len(values[key]) == 1]
		for idx in solved:
			for peer in self.peers[idx]:
				for v in values[idx]:
					if v in values[peer] and len(values[peer]) > 1:
						print("eliminate")
						values[peer].remove(v)

		return values

	def only_choice(self, values):
		for unit in self.unitlist:
			for i in self.vals:
				place = [box for box in unit if i in values[box]]
				if len(place) == 1:
					print("only")
					values[place[0]] = i

		return values

	def naked_twins(self, values):
		# Find all instances of naked twins

		pairlist = [box for box in values.keys() if len(values[box]) == 2]

		twinlist = []
		for box1 in pairlist:
			for box2 in self.peers[box1]:
				if set(values[box1]) == set(values[box2]) and (box2, box1) not in twinlist:
					twinlist.append((box1, box2))

		# Eliminate the naked twins as possibilities for their peers
		for twins in twinlist:
			# get only mutual peers
			mutual = set(self.peers[twins[0]]) & set(self.peers[twins[1]])
			twin = twins[0]

			for peer in mutual:
				if len(values[peer]) > 2:
					for i in values[twin]:
						self.assign_value(values, peer, values[peer].replace(i, ''))
		#print(values)
		return values

"""
	def display(self, values):
		# Taken from Strategy 1: Elimination lesson
		width = 1 + max(len(values[box]) for box in self.boxes)
		line = '+'.join(['-' * (width * 3)] * 3)
		for row in rows:
			print(''.join(values[row+col].center(width)+('|' if col in '36' else '')
						  for col in self.vals))
			if row in 'CF':
				print(line)
		return
"""
if __name__ == '__main__':
	s = Solver(3)

	#set_diagonal_mode(True)
	"""
	diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
	s.search(diag_sudoku_grid)
	"""
	grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
	s.search(grid2)

	try:
		from visualize import visualize_assignments
		visualize_assignments(assignments)

	except SystemExit:
		pass
	except:
		print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
