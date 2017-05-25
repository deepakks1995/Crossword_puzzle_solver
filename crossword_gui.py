
from crossword import Crossword
from word import Word
from sideKicks import Json_Parser
from clue_setter import Clue_Setter
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
		# self.cell_selected = False
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
									text="Specify Location for word",
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
					# original = self.game.start_puzzle[i][j]
					# color = "black" if answer == original else "sea green"
					color = "black"
					self.canvas.create_text(
						x, y, text=answer, tags="texts", fill=color
						)

	def __compute_crossword(self):
		self.__clear_answers()
		self.grid_cleared = False
		game = Crossword(13, 13, '-', 1, word_list)
		game.compute_crossword()
		self.game = game
		self.__draw_puzzle()
		self.specify_location.config(state="disabled")

	def __specify_location(self):
		self.game.flag = True
		self.game.compute_crossword()
		self.__draw_puzzle()
		self.grid_cleared = False
		self.specify_location.config(state="disabled")

	def __clear_answers(self):
		self.canvas.delete("cursor")
		self.canvas.delete("texts")
		self.game.flag = False
		# self.cell_selected = False
		self.grid_cleared = True
		self.game.clear_grid()
		self.specify_location.config(state="normal")

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
			self.game.grid[self.current_row][self.current_col] = (event.char)
			self.current_col, self.current_row = -1, -1
			self.__draw_puzzle()
			self.__draw_cursor()

word_list = ['saffron', 'The dried, orange yellow plant used to as dye and as a cooking spice.'], \
    ['pumpernickel', 'Dark, sour bread made from coarse ground rye.'], \
    ['leaven', 'An agent, such as yeast, that cause batter or dough to rise..'], \
    ['coda', 'Musical conclusion of a movement or composition.'], \
    ['paladin', 'A heroic champion or paragon of chivalry.'], \
    ['syncopation', 'Shifting the emphasis of a beat to the normally weak beat.'], \
    ['albatross', 'A large bird of the ocean having a hooked beek and long, narrow wings.'], \
    ['harp', 'Musical instrument with 46 or more open strings played by plucking.'], \
    ['piston', 'A solid cylinder or disk that fits snugly in a larger cylinder and moves under pressure as in an engine.'], \
    ['caramel', 'A smooth chery candy made from suger, butter, cream or milk with flavoring.'], \
    ['coral', 'A rock-like deposit of organism skeletons that make up reefs.'], \
    ['dawn', 'The time of each morning at which daylight begins.'], \
    ['pitch', 'A resin derived from the sap of various pine trees.'], \
    ['fjord', 'A long, narrow, deep inlet of the sea between steep slopes.'], \
    ['lip', 'Either of two fleshy folds surrounding the mouth.'], \
    ['lime', 'The egg-shaped citrus fruit having a green coloring and acidic juice.'], \
    ['mist', 'A mass of fine water droplets in the air near or in contact with the ground.'], \
    ['plague', 'A widespread affliction or calamity.'], \
    ['yarn', 'A strand of twisted threads or a long elaborate narrative.'], \
    ['snicker', 'A snide, slightly stifled laugh.']

if __name__ == '__main__':
	words = Json_Parser()
	words.json_parse("input.json")
	game = Crossword(13, 13, 'X', 1, words.allowed_words)
	game.compute_crossword()
	root = Tk()
	self = CrosswordGui(root, game, 30)
	root.geometry("%dx%d" % (self.WIDTH, self.HEIGHT + 40))
	root.mainloop(), 