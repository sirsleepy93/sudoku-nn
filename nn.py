import numpy

class sudoku_nn:
	def __init__():
		self.rows = 'ABCDEFGHI'
		self.cols = '123456789'

		grid = [r + c for r in self.rows for c in self.cols]
		self.grid = {[(g, 0) for g in grid]}
