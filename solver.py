import common
import numpy as np

class Solver:
	def __init__(self, size=3):
		"""
		Initialize a solver instance.
		Args:
			size(int) - Specifies the size of the sudoku puzzle by inner length.
				   That is to say by the length of the sides of the small squares of the puzzle.
		"""
		# Save size for later reference
		self.size = size
		# Get the list of all units from common.unit_list()
		self.unitlist = common.unit_list(size)
		# Get the peers dictionary from common.unit_list()
		self.peers = common.peers(size)
		# Initialize assignments to blank list
		self.assignments = []
		# Initialize the values reference to 1 to size * size inclusive range
		self.values = [v for v in range(1, size*size + 1)]
		# Initialize the coordinates reference for the 0 to size * size - 1 exclusive range.
		# Used to iterate through all rows/columns in self.display()
		self.coordinates = [c for c in range(0, size*size)]
		# Get a list of all boxes
		self.boxes = common.get_grid(size)


	def grid_values(self, grid):
		"""
		Convert string input into a new puzzle grid. Store puzzle grid as
			self.assignmens.
		Args:
			grid(string) - String for initial puzzle with blanks as '0' or '.'
		Returns:
			Dictionary representing the puzzle with real and possible values.
		"""

		values = []
		assert len(grid) == np.power(self.size, 4), \
			"Grid is not long enough. Returns length: %r" % len(grid)
		# For each character in the grid string: fill values with self.values if
		# the character is '.' or '0', else just use the character
		for box in grid:
			if box == '0' or box == '.':
				values.append(self.values.copy())
			elif int(box) in self.values:
				values.append([int(box)])

		self.assignments = dict(zip(self.boxes, values))
		return self.assignments


	def search(self, values=None):
		"""
		Search for a puzzle solution by trial and error.
		Args:
			values(dict) - The puzzle dictionary to search with.
					 Will default to self.assignments if left as None
		Returns:
			A solved puzzle dictionary.
		"""
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
			puzzle = values.copy()
			puzzle[box] = puzzle[box].remove(value)
			if run:
				return run


	def solve_to_length(self, length=1, values=None):
		"""
		Returns the number of values of specified length.
		Args:
			length(int) - The length to check against
			values(dict) - The puzzle we wish to check the length in.
					 Will default to self.assignments if left as None.
		Returns:
			The number of boxes of the specified length.
		"""
		if values == None:
			values = self.assignments
		# Return number of boxes with number of possibilities == length
		out = []
		for box in values.keys():
			if len(values[box]) == length:
				out.append(box)
		return len(out)


	def reduce_puzzle(self, values=None):
		"""
		Apply our constraint functions to the puzzle.
		Args:
			values(dict) - The puzzle to apply constraint functions to. Will default
					 to self.assignments if left as None.
		Returns:
			values with the constraint funcitons applied or False if our
				constraint functions deleted a box completely.
		"""


		if isinstance(values, str):
			values = self.grid_values(values)

		stalled = False

		while not stalled:
			solved_before = self.solve_to_length(values)
			print("Solved before: ", solved_before)

			values = self.eliminate(values)
			values = self.only_choice(values)
			values = self.naked_twins(values)

			solved_after = self.solve_to_length(values)
			print("Solved after: ", solved_after)

			stalled = solved_before == solved_after
			if self.solve_to_length(values, 0) > 0:
				return False

		return values


	def eliminate(self, values=None):
		"""
		Remove values from a box's peers if the box is solved (i.e. of length 1)
		Args:
			values(dict) - The puzzle to apply the function to.
			 			   Will default to self.assignments if left as None.
		Returns:
			values with legal possibilites (all solved values are unique within
				their unit).
		"""
		if values == None:
			values = self.assignments

		solved = [key for key in values.keys() if len(values[key]) == 1]
		for slv in solved:
			for peer in self.peers[slv]:
				assert len(values[slv]) != 0
				assert len(values[slv]) == 1
				for v in values[slv]:
					if v in values[peer]:
						length_before = len(values[peer])
						values[peer].remove(v)
						assert len(values[peer]) < length_before
						assert not isinstance(values[peer], int)

		return values

	def only_choice(self, values=None):
		"""
		Assign a value to a box if that box is the only place the value appears
			within its unit.
		Args:
			values(dict) - The puzzle to apply the functions to.
						   Will default to self.assignments if left as None.
		Returns:
			values with unique values assigned if they are unique to their unit.
		"""
		if values == None:
			values = self.assignments

		for unit in self.unitlist:
			for val in self.values:
				# For each possible value, record each place the value occurs in a
				# unit. If the value only appears once, finalize the value
				place = [box for box in unit if val in values[box]]
				if len(place) == 1 and len(values[place[0]]) > 1:
					length_before = len(values[place[0]])
					values[place[0]] = [val]
					assert len(values[place[0]]) < length_before
					assert not isinstance(values[peer], int)

		return values

	def find_twins(self, values):
		"""
		Collect a list of unique twin pairs within values.
		Args:
			values(dict) - The puzzle to find twins in.
		Returns:
			A list of tuples of unique twin pairs within values.
		"""
		pairlist = [box for box in values.keys() if len(values[box]) == 2]
		twinlist = []
		for pair in pairlist:
			for peer in self.peers[pair]:
				# If the sets are equivalent and the reverse tuple is not already
				# in the twinlist add the tuple
				if set(values[pair]) == set(values[peer]) and (peer, pair) not in twinlist:
					twinlist.append((pair, peer))
					print("Twinlist: ", twinlist)

		return twinlist


	def naked_twins(self, values=None):
		"""
		Remove twin values from the mutual peers of naked twins.
		Args:
			values(dict) - The puzzle to apply the function to. Will default
					 to self.assignments if left as None.
		Returns:
			values with legal possibilites (all solved values are unique within
				their unit).
		"""
		if values == None:
			values = self.assignments

		# Find all instances of naked twins
		twinlist = self.find_twins(values)

		# Eliminate the naked twins as possibilities for their peers
		for twins in twinlist:
			# get only mutual peers
			mutual = set(self.peers[twins[0]]) & set(self.peers[twins[1]])

			# Since we know twins[0] and twins[1] are equal
			twin = twins[0]
			print('Twins')

			# For each mutual peer: if the peer box contians more than one value, and
			# the peer box is not in our twinlist then remove the values
			# of our naked twins from that peer
			for peer in mutual:
				if len(values[peer]) > 1 and peer not in twinlist:
					for val in values[twin]:
						if val in values[peer]:
							values[peer].remove(val)
							assert len(values[peer]) < length_before
							assert not isinstance(values[peer], int)

		return values

	# Returns the indexs of square units
	def sqr_coordinates(self, size=None):
		if size == None:
			size = self.size
		return range(size - 1, size*size - size, size)

	def display(self, values=None):
		"""
		Display the solved puzzle (or any puzzle really).
		Args:
			values(dict) - The puzzle to display.
		Returns:
			None
		"""
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

	diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
	s.search(diag_sudoku_grid)
