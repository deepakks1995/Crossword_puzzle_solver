
from crossword import Crossword
from word import Word
from json_parser import Json_Parser
from clue_setter import Clue_Setter
from copy import deepcopy
try:
	from Tkinter import *
except ImportError:
	raise ImportError, "The Tkinter module is required to run this package" 

class CrosswordGui(Frame):
	"""docstring for CrosswordGui"""
	def __init__(self, parent, game, grid_size=25):
		Frame.__init__(self, parent)
		self.parent = parent
		self.game = game
		self.row = self.game.row
		self.col = self.game.col
		self.MARGIN = 20
		self.SIDE = grid_size
		self.HEIGHT = self.MARGIN*2 + self.SIDE * self.row
		self.WIDTH = self.MARGIN*2 + self.SIDE * self.col
		self.grid_cleared = False
		self.__initUI()

	def __initUI(self):

		self.parent.title("Crossword")
		self.pack( expand=0)
		self.canvas = Canvas(self,state="normal", width=self.WIDTH, height=self.HEIGHT)
		
		self.clear_button = Button(self,
								text="Clear answers",
                              		command=self.__clear_answers)
		self.compute_crossword = Button(self,
									text="Compute Crossword",
										command=self.__compute_crossword)
		self.specify_location = Button(self,
									text="Try these words",
										command=self.__specify_location,
											state=DISABLED)
		self.set_clues = Button(self, 
								text="Set Clues",
									command=self.__set_clues)
		self.canvas.pack(fill=BOTH, side=TOP)
		self.set_clues.pack(side=LEFT)
		self.clear_button.pack(side=LEFT)
		self.compute_crossword.pack(side=LEFT)
		self.specify_location.pack(side=LEFT)
		self.__draw_grid()
		self.__draw_puzzle()
		self.canvas.bind("<Button-1>", self.__cell_clicked)
		self.canvas.bind("<Key>", self.__key_pressed)
		self.canvas.config(state="disabled")

	def __set_clues(self):
		self.set_clues.config(state="disabled")
		self.compute_crossword.config(state="disabled")
		self.specify_location.config(state="disabled")
		self.clear_button.config(state="disabled")
		print "This Crossword Puzzle has been finalized. To try Another Puzzle please restart the Program"
		root = Tk()
		self = Clue_Setter(root, self.game, self.WIDTH, self.SIDE)
		root.geometry("%dx%d" % (self.WIDTH, self.HEIGHT + 40))
		root.mainloop(), 

	def __draw_grid(self):
		for i in range(self.col+1):
			color = "blue" 
			x0 = self.MARGIN + i * self.SIDE
			y0 = self.MARGIN
			x1 = self.MARGIN + i * self.SIDE
			y1 = self.HEIGHT - self.MARGIN
			self.canvas.create_line(x0, y0, x1, y1, fill=color)
		for i in range(self.row+1):
			x0 = self.MARGIN
			y0 = self.MARGIN + i * self.SIDE
			x1 = self.WIDTH - self.MARGIN
			y1 = self.MARGIN + i * self.SIDE
			self.canvas.create_line(x0, y0, x1, y1, fill=color)

	def __draw_puzzle(self):
		self.canvas.delete("texts")
		for i in xrange(self.row):
			for j in xrange(self.col):
				answer = self.game.grid[i][j]
				x = self.MARGIN + j * self.SIDE + self.SIDE / 2
				y = self.MARGIN + i * self.SIDE + self.SIDE / 2
				if answer != self.game.empty:
					color = "black"
					self.canvas.create_text(
						x, y, text=answer, tags="texts", fill=color
						)

	def __compute_crossword(self):
		self.__clear_answers()
		self.grid_cleared = False
		game = Crossword(self.row, self.col, self.game.empty, self.game.maxloops, self.game.available_words)
		game.compute_crossword(1,10)
		self.game = game
		self.__draw_puzzle()
		self.specify_location.config(state="disabled")
		self.set_clues.config(state="normal")
		print "Crossword Generated!......."

	def __find_vertical__(self, i, j, grid):
		if i < self.col - 1:
			if grid[i+1][j]!= self.game.empty:
				return 1
			else:
				return 0
		else:
			return -1

	def __find_horizontal__(self, i, j, grid):
		if j < self.col - 1:
			if grid[i][j+1]!= self.game.empty:
				return 1
			else:
				return 0
		else:
			return -1

	def __extract_words__(self):
		extracted_words = []
		current_word = ""
		grid = deepcopy(self.game.grid)
		i , j = 0 , 0
		while i < self.row:
			j = 0
			while j < self.col:
				if grid[i][j] != self.game.empty:
					horizontal = self.__find_horizontal__(i,j,grid)
					if horizontal != -1:
						if horizontal == 1:
							itr = j
							while itr < self.col and grid[i][itr] != self.game.empty:
								current_word += grid[i][itr]
								itr += 1
							word = Word("", "")
							word.row = i + 1
							word.col = j + 1
							word.vertical = 0
							word.word = current_word
							word.length = len(current_word)
							extracted_words.append(word)
							j = itr - 1
							current_word = ""
				j += 1
			i += 1
		j = 0
		while j < self.col:
			i = 0
			while i < self.row:
				if grid[i][j] != self.game.empty:
					vertical = self.__find_vertical__(i, j, grid)
					if vertical != -1:
						if vertical:
							itr = i
							while itr < self.row and grid[itr][j]!= self.game.empty:
								current_word += grid[itr][j]
								itr += 1
							word = Word("", "")
							word.word = current_word
							word.length = len(current_word)
							word.row = i + 1
							word.col = j + 1
							word.vertical = 1
							extracted_words.append(word)
							i = itr - 1
							current_word = ""
				i += 1
			j += 1
		return extracted_words

	def __specify_location(self):
		# self.game.current_word_list.append(Word(word, "") for word in self.entered_word_list)
		self.game.flag = True
		self.game.current_word_list  = self.__extract_words__()
		self.game.compute_crossword(1,10)
		self.__draw_puzzle()
		self.grid_cleared = False
		self.specify_location.config(state="disabled")
		# self.compute_crossword.config(state="normal")
		self.set_clues.config(state="normal")
		print "Crossword Generated! To try another press Compute Crossword button"

	def __clear_answers(self):
		self.canvas.delete("cursor")
		self.canvas.delete("texts")
		self.game.flag = False
		self.grid_cleared = True
		self.game.clear_grid()
		self.set_clues.config(state="disabled")

	def __cell_clicked(self, event):
		x, y = event.x, event.y
		self.current_row, self.current_col = -1, -1
		if (self.MARGIN < x < self.WIDTH - self.MARGIN and self.MARGIN < y < self.HEIGHT - self.MARGIN):
			self.canvas.focus_set()
			row, col = (y - self.MARGIN) / self.SIDE, (x - self.MARGIN) / self.SIDE
			if not self.game.grid[row][col] == self.game.empty:
				self.current_col, self.current_row = col, row
			if self.grid_cleared:
				self.current_col, self.current_row = col, row
		self.__draw_cursor()

	def __draw_cursor(self):
		self.canvas.delete("cursor")
		if self.current_row >= 0 and self.current_col >= 0:
			x0 = self.MARGIN + self.current_col * self.SIDE + 1
			y0 = self.MARGIN + self.current_row * self.SIDE + 1
			x1 = self.MARGIN + (self.current_col + 1) * self.SIDE - 1
			y1 = self.MARGIN + (self.current_row + 1) * self.SIDE - 1
			self.canvas.create_rectangle(
				x0, y0, x1, y1,
				outline="red", tags="cursor"
				)

	def __key_pressed(self, event):
		if self.current_row >= 0 and self.current_col >= 0 and self.grid_cleared:
			self.compute_crossword.config(state="disabled")
			self.set_clues.config(state="disabled")
			self.specify_location.config(state="normal")
			self.game.grid[self.current_row][self.current_col] = (event.char)
			self.previous_row, self.previous_col = self.current_row, self.current_col
			self.current_col, self.current_row = -1, -1
			self.__draw_puzzle()
			self.__draw_cursor()

if __name__ == '__main__':
	words = Json_Parser()
	words.json_parse("result.json")
	game = Crossword(int(words.row), int(words.col), 'X', 1, words.allowed_words)
	game.compute_crossword(1,10)
	root = Tk()
	self = CrosswordGui(root, game, int(words.grid_size))
	root.geometry("%dx%d" % (self.WIDTH, self.HEIGHT + 40))
	root.mainloop(), 