import argparse

if __name__=='__main__':
	parser = argparse.ArgumentParser(description=_('Crossword generator.'), prog='Enigma')
    parser.add_argument('infile', help=_('Name of word list file.'))
    parser.add_argument('-r', '--row', dest='row',default = 9, help=_('Number of rows in grid. Example: -r 9 or --row 9'))
    parser.add_argument('-c', '--col', dest='col', default = 9, help=_('Number of columns in grid. Example: -c 9 or --col 9'))
    parser.add_argument('excludefile', help=_('Name of the file containing the excluded words/puzzle from previous years'))
    args = parser.parse_args()
    print args.infile
    print args.row 
