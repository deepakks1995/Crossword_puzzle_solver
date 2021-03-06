
from crossword import Crossword
from word import Word
from export import ExportCrossword
from matplotlib.backends.backend_pdf import PdfPages
try:
	from Tkinter import *
except ImportError:
	raise ImportError, "The Tkinter module is required to run this package" 

'''
Class: Clue_Setter
This class is used to create a new Interface named 'ClueSetter'
which allows the user to set the clues corresponding to each 
and every word in the puzzle
'''
class Clue_Setter(object):
	def __init__(self, parent, game, width, side = 25):
		super(Clue_Setter, self).__init__()
		self.parent = parent
		self.game = game
		self.SIDE = side
		self.WIDTH = width
		self.HEIGHT = side * len(self.game.current_word_list) + 40
		self.MARGIN = 20
		self.font_size = 5
		self.__INITUI()

	'''
	Function to initaiate the UI of Interfacce
	'''
	def __INITUI(self):
		self.parent.title("Clue Setter")
		self.entry = []
		Label(self.parent, text="Enter Clues for the words").grid(row=0)
		Label(self.parent, text="").grid(row=1)
		for i in range(len(self.game.current_word_list)):
			Label(self.parent, text=self.game.current_word_list[i].word).grid(row=i+2, column=0)
			entryfields = Entry(self.parent)
			entryfields.grid(row=i+2, column = 1)
			self.entry.append(entryfields)

		export = Button(self.parent, 
							text="Export ",
								command=self.__export).grid(row=len(self.game.current_word_list)+3)

	'''
	Function to print the crossword puzzle
	'''	
	def __export(self):
		for i in range(len(self.game.current_word_list)):
			self.game.current_word_list[i].clue = str(self.entry[i].get())
		export = ExportCrossword(self.game.row, 
									self.game.col, 
										self.SIDE, 
											self.MARGIN, 
												self.game.empty, 
													self.game.grid, 
														self.game.current_word_list, 
															self.font_size)
		export.__draw_grid__()
		with PdfPages("out.pdf") as pdf:
			export.__draw_puzzle__(pdf)
			export.__draw__legend__(pdf)

if __name__=='__main__':
	print "You are in the wrong file" 