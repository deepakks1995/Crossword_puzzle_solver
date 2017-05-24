import random, time
from word import Word
import sys
from copy import copy as duplicate

class Crossword(object):
	"""docstring for Crossword"""
	def __init__(self, row, col, empty = '-', maxloops = 2000, available_words = [], current_word_list = [], grid = []):
		super(Crossword, self).__init__()
		self.row = row
		self.col = col
		self.empty = empty
		self.maxloops = maxloops
		self.available_words = available_words
		self.current_word_list = current_word_list
		self.grid = grid
		# This flag is used when user specifies some word and its location before computation
		self.flag = False
		self.sort_list()
		self.clear_grid()

	def clear_grid(self):
		self.grid = []
		for i in range(self.row):
			row_list = []
			for j in range(self.col):
				row_list.append(self.empty)
			self.grid.append(row_list)

	def sort_list(self):
		temp_list = []
		for word in self.available_words:
			if isinstance (word, Word):
				temp_list.append(Word(word.word, word.clue))
			else:
				temp_list.append(Word(word[0], word[1]))
		# temp_list.sort(key=lambda i: len(i.word), reverse=True)
		random.shuffle(temp_list)
		self.available_words = temp_list

	def compute_crossword(self,spins=4,loops=50):
		self.clear_grid() if not self.flag else True	
		copy = self.grid	
		iterator = 0
		grid = []
		current_word_list = []
		while iterator < loops:
			if not self.flag:
				self.current_word_list = []
			# for word in self.current_word_list:
			# 	print word.word
			itr = 0
			while itr < spins:
				for word in self.available_words:
					if not word in self.current_word_list:
						self.add_to_grid(word)
				itr += 1
			# print len(self.current_word_list)
			if len(current_word_list) < len(self.current_word_list):
				grid = self.grid
				current_word_list = self.current_word_list
				self.grid = copy
				self.sort_list()
			iterator +=1
		return True

	def compute_coordinates(self, word):
		word_iterator = -1
		coordinates_list = []
		for letter in word.word:
			word_iterator += 1
			row_iterator = 0
			for row in self.grid:
				row_iterator += 1
				col_iterator = 0
				for cell in row:
					col_iterator += 1
					if letter == cell:
						# try Horizontal
						if col_iterator - word_iterator > 0:
							if word.length + col_iterator - word_iterator <= self.col:
								coordinates_list.append([row_iterator, col_iterator - word_iterator, 0, 0])
						# try Vertical 
						if row_iterator - word_iterator > 0:
							if word.length + row_iterator - word_iterator <= self.row:
								coordinates_list.append([row_iterator - word_iterator, col_iterator, 1, 0])
		
		if len(coordinates_list) >= 0:
			new_coordinates_list = []
			for coordinate in coordinates_list:
				
				row = coordinate[0]
				col = coordinate[1]
				Vertical = coordinate[2]
				coordinate[3] = self.compute_coordinates_score(row, col, Vertical, word)
				new_coordinates_list.append(coordinate)
			new_coordinates_list.sort(key=lambda i: i[3], reverse=True)
			return new_coordinates_list
		else:
			return -1

	def compute_coordinates_score(self, row, col, Vertical, word):
		
		if col < 1 or row < 1:
			return 0
		score = 1
		count = 1
		for letter in word.word:
			actual_letter = self.grid[row-1][col-1]
			
			if actual_letter == self.empty or letter == actual_letter:
				pass
			else:
				return 0
			if actual_letter == letter:
				score += 1
			if Vertical == 1:
				if actual_letter != letter:
					if not self.check_empty_cells(row, col+1):
						return 0
					if not self.check_empty_cells(row, col-1):
						return 0
				if count == 1:
					if not self.check_empty_cells(row-1, col):
						return 0
				if word.length == count:
					if not self.check_empty_cells(row+1, col):
						return 0
			else:
				if actual_letter != letter:
					if not self.check_empty_cells(row - 1 , col):
						return 0
					if not self.check_empty_cells(row + 1, col):
						return 0
				if count == 1:
					if not self.check_empty_cells(row, col - 1):
						return 0
				if word.length == count:
					if not self.check_empty_cells(row, col + 1):
						return 0
			if Vertical == 1:
				row += 1
			else:
				col += 1
			count += 1
		return score

	def add_to_grid(self, word):
		fit = False
		iterator = 0
		coordinates_list = self.compute_coordinates(word)
		while iterator < self.maxloops and not fit:
			if len(self.current_word_list) == 0:
				row, col , Vertical = 1 , 1, random.randrange(0, 2)
				if self.compute_coordinates_score(row, col, Vertical, word):
					fit = True
					self.set_word(row, col ,Vertical, word)
			else:
				try:
					row, col ,Vertical = coordinates_list[iterator][0], coordinates_list[iterator][1], coordinates_list[iterator][2]
				except IndexError :
					return
				if self.compute_coordinates_score(row, col, Vertical, word):
					fit = True
					self.set_word(row, col, Vertical, word)
			iterator += 1
		return True

	def set_word(self, row, col ,Vertical, word):
		word.col = col
		word.row = row
		word.vertical = Vertical
		self.current_word_list.append(word)

		for letter in word.word:
			self.grid[row-1][col-1] = letter
			if Vertical:
				row += 1
			else:
				col += 1
		return True

	def check_empty_cells(self, row, col):
		try:
			cell = self.grid[row-1][col-1]
			if cell == self.empty:
				return True
		except IndexError:
			return False
		return False

	def print_solution(self):
		for row in self.grid:
			for cell in row:
				if cell == self.empty:
					print " ",
				else: 
					print cell,
			print ""

	def set_locaion_word(self, row, col, Vertical,  word):
			for letter in word:
				self.grid[row-1][col-1] = letter
				if Vertical:
					row += 1
				else:
					col += 1
			self.current_word_list.append(Word(word,""))


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


if __name__ == "__main__": 
	a = Crossword(13, 13, '-', 1, word_list)
	word = raw_input("Enter word to input")
	row = int(raw_input("Enter row"))
	col = int(raw_input("Enter col"))
	vertical = int(raw_input("Vertical"))
	a.flag = True
	flag = True
	a.set_locaion_word(row, col ,vertical, word)
	while flag:
		a.compute_crossword()
		a.print_solution()
		var  = raw_input("Generate another puzzle! [y/n] ")
		if var == 'n':
			flag = False
		elif var == 'y':
			pass
		else: 
			print "Wrong Input...Exiting....."
