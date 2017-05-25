import argparse
import json

if __name__=='__main__':
	parser = argparse.ArgumentParser(description=('Crossword generator.'), prog='Enigma')
	parser.add_argument('infile', help=('Name of word list file.'))
	parser.add_argument('-r', '--row', dest='row',default = 13, help=('Number of rows in grid. Example: -r 9 or --row 9'))
	parser.add_argument('-c', '--col', dest='col', default = 13, help=('Number of columns in grid. Example: -c 9 or --col 9'))
	parser.add_argument('-s', '--size', dest='size', default = 30, help=('Size of a cell. Example: -s 25 or --size 25'))
	parser.add_argument('exfile', help=('Name of the file containing the excluded words/puzzle from previous years'))
	args = parser.parse_args()
	dict = {}
	excluded_words = []
	grid_dict = {}
	word_list = []
	variables = {}
	with open(args.exfile, "r") as fp:
		for line in fp:
			word = str(line).split("\n")
			excluded_words.append(word[0])
	dict["constraints"] = excluded_words
	with open(args.infile, "r") as fp:
		for line in fp:
			word = str(line).split("\n")
			word_list.append(word[0])
	variables["words_allowed"] = word_list
	grid_dict["row"] = args.row
	grid_dict["column"] = args.col
	grid_dict["grid_size"] = args.size
	variables["grid_specification"] = grid_dict
	dict["variables"] =variables
	dict["name"] = "Enigma"
	
	with open("result.json", "w") as fp:
		json.dump(dict, fp)
