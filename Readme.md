<b>Assignment:</b> Crossword Puzzle Generator  
<b>Author:</b> Deepak Sharma
<b>Roll_No:</b> B14107

<b>Build the Program:</b>

	Simply run the following commands in terminal
	$ sudo make 

<b>How to run:</b>

Simply run the following lines in terminal:
	
    $ python crossword_gui.py

It will open a Interface to guide the user to generate the crossword

<b>Input:</b>

The input consists of a simple Json file (A sample can be found as Sample.json file). 

I had provided a input file named as 'result.json' that contains the words from "2000_comwords_ENG.txt" file from which the crossword has to be generated and "excluded_words.txt" as constraints (words to be excluded)

If the user wants to input his own Json file then rename it to 'result.json'
		
If the user wants to generate his own crossword file the refer to 'Generate Json file from word lists' section below 	


<b>Interface Walkthrough:</b>

The Interface comes up with a pre-generated crossword puzzle. It has four buttons:

1. 	Compute Crossword: This buttons is used to generate another crossword puzzle

2.	Set Clues: This button finalizes the Crossword Shown and opens another 			Interface named 'Clue Setter' containing the words
						that are in the crossword and a text field in front of them for typing the clues against each word. Once Clues have been set up
						for each and every word then click on the export button to generate the crossword in 'pdf' format with the output file automatically saved 
						as 'out.pdf' in the folder.

3. Clear Ansmwer: This buttons clears the grid.

4. Try these words:	This buttons is active only when the grid is clear that is first click on the Clear Answer button and then this will become active
							This button is used to manually specify some words in the grid and then generate crossword on top of these words


<b>Assignment Tasks:</b>

<b>1.	Avoid repeating words from recent puzzles:</b>

For the completion of this task the user has to specify the words in the constraints section of json file (look at the Json Sample file or either to json explainer section)

<b>2.	Allow the user to ask for another puzzle:</b>

For this the Compute Crossword button has been provided. This button computes another crossword puzzle

<b>3.	Allow the user to specify words in specific locations:</b>
				
 To specify certain words in the crossword according to the choice of user follow the steps:
			
  	(a) First click on the Clear Answer button. This will clear the grid.
	(b)	Then select any cell by clicking on it. Selection can be confirmed when a red border appears on the cell
	(c)	once the cell is selected then type the letter which you want to appear in the crossword
	(d) Repeat the above two steps until the user has specified the location of word/words
	(e) Then click on 'Try these words' button to generate the crossword.
	(f) Once the crossword is generated then Click on the 'Set clues' to set the clues for each and every word in the puzzle
	(e) Finally click on the Export button to save the crossword in the 'out.pdf' file in the program folder
	

<b>4.	(Optional) Provide an interface using which the setter 	can set the clues:-</b>
				
   To set the clues for a certain crossword puzzle, simply click on the 'Set Clue' button. This will provide the user with a new interface 
				where the user can specify the clue for the corresponding puzzles

<b>Json Files Input Data:</b>

To specify your own Json file, rename it to 'result.json'


I had provided a json file named 'result.json' or a sample of json Input can be found in the 'Sample.json'.

The Json file contains the following variables:

1. 	"name"	It contains the name of the program. 

2.	"variables": It agains contains two variables:
	
    (a) "grid_specification" It has three variable namely "row", "columns", "grid_size" respectively for the number of rows, columns and the size of one cell 							in the grid
	
    (b) "words_allowed": It contains the list of words from which the crossword has to be generated
	

3.	"constraints": The list of the words which are to be exluded from the puzzle

<b>Generate Json file from word lists:</b>
	
The user can also generate his own json file.For this I had provided the user with a parserfile that tooks two files one containing the words from which the crossword has to be generated and another containing the words from the previous year crosswords puzzle that are to be exclude.

To build your own Json file simple run the following commands
	
	$ python parse_files.py infile -r [] -c [] -s [] exfile

For Example:
	
    $ python parse_files.py "2000_comwords_ENG.txt" -r 13 -c 13 -s 30 "excluded_words.txt"

Here 2000_comwords_ENG.txt / infile is a file containing the words from which the crossword has to be generated
and 

excluded_words.txt / exfile contains the words to be excluded

-r flag tells the program about the number of rows of crossword grid (Default: 9)

-c flag tells the program about the number of columns of crossword grid	 (Default: 9)

-s specifies the size of each cell of the grid (Default: 30)


<b>References:</b>
	[1]	http://newcoder.io/gui/part-3/		For Creating the Interface 