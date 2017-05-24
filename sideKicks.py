import json
from pprint import pprint

class Json_Parser(object):
	def __init__(self):
		super(Json_Parser, self).__init__()

	def json_parse(self, file):
		with open(file) as json_file:
			data = json.load(json_file)
		self.split_data(data)
	
	def split_data(self, data):
		self.allowed_words = []
		self.words_not_allowed = []
		self.row = data['variables']['grid_specification']['row']
		self.col = data['variables']['grid_specification']['column']
		self.grid_size = data['variables']['grid_specification']['grid_size']
		if len(data['constraints']) != 0 :
			if isinstance(data['constraints'][0], list):
				for _list in data['constraints']:
					self.words_not_allowed.append(str(_list[0]))
			else:
				self.words_not_allowed = [_ for _ in data['variables']['constraints']]
		for word in data['variables']['words_allowed']:
			if not word in self.words_not_allowed:
				self.allowed_words.append(str(word))

if __name__=='__main__':
	self = Json_Parser()
	self.json_parse("input.json")
	print self.allowed_words
	print self.words_not_allowed
 		 
