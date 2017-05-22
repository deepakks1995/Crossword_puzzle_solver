import re

class Word(object):
 	"""docstring for Word"""
 	def __init__(self, word=None, clue=None):
 		super(Word, self).__init__()
 		self.word = re.sub(r'\s', '', word.lower())
 		self.clue = clue
 		self.length = len(word)
 		self.row = None
 		self.col = None
 		self.vertical = None
 		self.number = None

 	def down_across(self):
 		if self.vertical:
 			return 'down'
 		else:
 			return 'across'
 		 
