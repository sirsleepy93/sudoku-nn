import common
import numpy as np

class Solver:
	def __init__(self, size=3):
		self.size = size
		self.unitlist = common.unit_list(size)
		self.peers = common.peers(size)
		self.assignments = []
		self.vals = [v for v in range(1, size*size + 1)]
		self.coordinates = [c for c in range(0, size*size)]
		self.boxes = common.get_grid(size)

	def grid_values(self, grid):
		values = []
		for box in grid:
			if box == '0' or box == '.':
				values.append(self.vals.copy())
			elif int(box) in self.vals:
				values.append([int(box)])

		assert len(values) == np.power(self.size, 4), \
										"len(values) = %r  size = %r" % (len(values), np.square(self.size))
		self.assignments = values
		return dict(zip(self.boxes, values))

	def search(self, values=None):
		if values == None:
			values = self.assignments

		if isinstance(values, str):
			values = self.grid_values(values)
			values = self.reduce_puzzle(values)
		elif isinstance(values, dict):
			values = self.reduce_puzzle(values)

		if values is False: # value
			return False
		elif all(len(values[box]) == 1 for box in self.boxes): # is solved?
			return values

		_, box = min((len(values[box]), box) for box in self.boxes
					  if len(values[box]) > 1)

		for value in values[box]:
			#print("SEARCHING")
			puzzle = values.copy()
			puzzle[box] = value
			run = self.search(puzzle)
			if run:
				return run

	def num_possible(self, values=None, length=1):
		if values == None:
			values = self.assignments
		# Return number of boxes with number of possibilities == length
		out = []
		for box in values.keys():
			if isinstance(values[box], int):
				print(box)
			if len(values[box]) == length:
				out.append(box)
		return len(out)

	def reduce_puzzle(self, values):
		stalled = False

		if isinstance(values, str):
			values = self.grid_values(values)

		while not stalled:
			solved_before = self.num_possible(values)
			print("Solved before: ", solved_before)

			values = self.eliminate(values)
			print([key for key in values.keys() if isinstance(values.keys(),int)])
			values = self.only_choice(values)
			print([key for key in values.keys() if isinstance(values.keys(),int)])
			values = self.naked_twins(values)
			print([key for key in values.keys() if isinstance(values.keys(),int)])

			solved_after = self.num_possible(values)
			print("Solved after: ", solved_after)

			stalled = solved_before == solved_after
			if self.num_possible(values, 0) > 0:
				return False

		return values

	def eliminate(self, values = None):
		if values == None:
			values = self.assignments
		solved = [key for key in values.keys() if len(values[key]) == 1]
		for slv in solved:
			for peer in self.peers[slv]:
				assert len(values[slv]) != 0
				assert len(values[slv]) == 1
				for v in values[slv]:
					if v in values[peer] and len(values[peer]) > 1:
						values[peer].remove(v)

		return values

	def only_choice(self, values = None):
		if values == None:
			values = self.assignments

		for unit in self.unitlist:
			for val in self.vals:
				place = []
				place = [box for box in unit if len(values[box]) > 1 and val in values[box]]
				if len(place) == 1:
					print("only")
					values[place[0]] = [val]

		return values

	def naked_twins(self, values=None):
		if values == None:
			values = self.assignments
		# Find all instances of naked twins
		pairlist = [box for box in values.keys() if len(values[box]) == 2]
		twinlist = []
		for box1 in pairlist:
			for box2 in self.peers[box1]:
				#print('Naked: {} {}'.format(box1, box2))
				#print('Twins: {} {}'.format(values[box1], values[box2]))
				if set(values[box1]) == set(values[box2]) and (box2, box1) not in twinlist:
					twinlist.append((box1, box2))
					print("Twinlist: {}".format(twinlist))

		# Eliminate the naked twins as possibilities for their peers
		for twins in twinlist:
			# get only mutual peers
			mutual = set(self.peers[twins[0]]) & set(self.peers[twins[1]])
			twin = twins[0]
			print('Twins')
			for peer in mutual:
				if len(values[peer]) > 2:
					for i in values[twin]:
						self.assign_value(values, peer, values[peer].replace(i, ''))
		#print(values)
		return values

	# Returns the indexs of square units
	def sqr_coordinates(self, size=None):
		if size == None:
			size = self.size
		return range(size - 1, size*size - size, size)

	def display(self, values=None):
		if values == None:
			values = self.assignments

		width = 1 + max(len(values[box]) for box in self.boxes)
		line = '+'.join(['-' * (width * self.size)] * self.size)

		for row in self.coordinates:
			output = ''
			for col in self.coordinates:
				output += str(values[row, col]).center(width)
				output += ('|' if col in self.sqr_coordinates() else '')

			print(output)

			if row in self.sqr_coordinates():
				print(line)

		return


if __name__ == '__main__':
	s = Solver(3)

	#set_diagonal_mode(True)
	"""
	diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
	s.search(diag_sudoku_grid)
	"""
	grid1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
	grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
	s.display(s.search(grid2))

	try:
		from visualize import visualize_assignments
		visualize_assignments(assignments)

	except SystemExit:
		pass
	except:
		print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
