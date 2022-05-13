class Square:
	def __init__(self, board, row, column):
		"""
		Initializes square class, which holds information about the position of a square for rendering the board properly, neighbors with whom it cannot share value, and the possible values of the square.
		"""
		self.board = board
		self.row = row
		self.column = column
		#Neighbors of all sorts, against which uniqueness is checked
		self.row_squares = set([]) 
		self.column_squares = set([])
		self.box_squares = set([])
		self.number = None #The actual value in the square
		self.possibilities = set(range(9)) #Possible numbers it could be
		self.box = None # Box starts at 0 in top left and increases right, so (0,0) = 0, (4,0) = 1, (0,4) = 3
		self.box = int((row)/3)+int((column)/3)*3
	def initialize(self):
		"""
		Passes itself to connect to row, column, and box neighbors
		"""
		#This is highly inefficient at the moment, but, as initialization is run once, inefficiencies do not highly contribute to slow run-time.
		for square in self.board.squares: #Checks through all squares to check shared attributes
			if square != self:
				if square.row == self.row:
					self.row_squares.add(square)
				if square.column == self.column:
					self.column_squares.add(square)
				if square.box == self.box:
					self.box_squares.add(square)
	def unique_check(self, comparison_set):
		"""
		Returns true if the number in this square is unique among the set, false otherwise.
		"""
		for square in comparison_set: #Some set to compare it to, always rows, columns, or boxes
			if square.number == self.number: #There is a match within the set
				return False
		return True
	def valid_square(self):
		"""
		Runs unique_check on all neighbor sets.
		"""
		return self.unique_check(self.row_squares) and self.unique_check(self.column_squares) and self.unique_check(self.box_squares)
	def deduce_number(self):
		"""
		If there is one possibility, convert self.number to the possibility and call deduce possible values on all other neighboring squares.
		"""
		if len(self.possibilities) == 1: #This is then the only number
			self.number = list(self.possibilities)[0]
			for square in self.row_squares: #This is the only information possible that will change the possiblities of neighbors, and thus they must be checked again
				if square not in self.board.deduce_queue and square.number == None:
					self.board.deduce_queue.append(square)
			for square in self.column_squares:
				if square not in self.board.deduce_queue and square.number == None:
					self.board.deduce_queue.append(square)
			for square in self.box_squares:
				if square not in self.board.deduce_queue and square.number == None:
					self.board.deduce_queue.append(square)
	def deduce_possible_values(self):
		"""
		Updates possibilities.
		"""
		if len(self.possibilities) == 1: #Don't check if there's only one possibility.
			return
		invalid_possibilities = set([])
		for pos_val in self.possibilities: #Check to see whether every possibility still leads to a valid board
			self.number = pos_val
			if not self.valid_square(): #Check whether the board is valid given that number.
				invalid_possibilities.add(pos_val) #Add the invalid number to the set to be removed
		for invalid_val in invalid_possibilities: #Subtract impossible numbers from possibilities.
			self.possibilities.remove(invalid_val)
		if len(self.possibilities) < 1: #Debug
			print("ERROR, no valid possibilities for square.  Output of program is necessarily incorrect.")
		self.number = None #Make sure to revert number
		self.deduce_number() #See if number can be deduced.




class Sudoku:
	def __init__(self):
		"""
		The container for squares.  Contains main functions to assign values to squares, to print the board, and to iterate over deduce_queue
		"""
		self.squares = set([])
		for row in range(9):
			for column in range(9):
				self.squares.add(Square(self, row, column))
		for square in self.squares: #Note this is O(n^2) in and of itself.  As these are generated predictably there is room for further improvement at this step.
			square.initialize() #Initialize connects squares to neighbors
		self.deduce_queue = list(self.squares.copy()) #Queue containing the next squares to deduce possible values

	def assign_initial_values(self, values):
		"""
		Assigns initial puzzle values to proper squares, inputted in the form of tuples ((row, column), number).
		"""
		for val in values:
			for square in self.squares:
				if square.row == val[0][0] and square.column == val[0][1]: #First element of value tuple is row column
					square.possibilities = set([val[1]]) #No other possiblities of course
					square.number = val[1] #Assign number
	def represent(self):
		"""
		Returns string representation of board.
		"""
		#This is horribly inefficient but is a debug function and thus is not run repeated times.
		ar = []
		for row in range(9):
			ar.append([])
			for column in range(9):
				ar[row].append("?")
		for square in self.squares:
			if square.number != None:
				ar[square.row][square.column] = str(square.number)
		s = ""
		for row in ar:
			s += "\n"
			for column in row:
				s += " | " + column + " | "
		return s[1:]
	def tick(self):
		"""
		Deduces the possible values for the next item in deduce_queue.
		"""
		sq = self.deduce_queue.pop(0) 
		sq.deduce_possible_values()
	def solve(self):
		"""
		Keeps running tick until the deduce queue is exahausted, either happening when a solution has been found or a point exists with multiple possible entries which this algorithm cannot handle.
		"""
		while len(self.deduce_queue) > 0:
			self.tick()
"""
sudoku_set_up_1 = [
((0,1),5),
((0,3),2),
((0,4),8),
((0,6),3),
((0,7),1),
((1,0),3),
((1,2),8),
((1,4),5),
((1,5),0),
((1,8),2),
((2,0),2),
((2,1),7),
((2,3),3),
((2,7),8),
((2,8),5),
((3,1),2),
((3,2),3),
((3,3),5),
((3,4),7),
((3,7),6),
((4,0),5),
((4,4),4),
((4,5),8),
((4,6),7),
((4,8),3),
((5,1),4),
((5,2),7),
((5,3),6),
((5,6),1),
((5,8),8),
((6,2),5),
((6,3),4),
((6,5),7),
((6,6),2),
((6,7),3),
((7,0),4),
((7,1),0),
((7,2),6),
((7,5),2),
((7,8),1),
((8,0),7),
((8,4),6),
((8,5),5),
((8,6),8),
((8,7),0),
]
s = Sudoku()
s.assign_initial_values(sudoku_set_up_1)
print(s.represent())
s.solve()
print(s.represent())"""
