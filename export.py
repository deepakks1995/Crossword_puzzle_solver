import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from crossword import Crossword
from word import Word
from sideKicks import Json_Parser
import os

class ExportCrossword(object):
    def __init__(self, row=0, col=0, grid_size=0,margin = 0, empty = '', grid=[], word_list=[], font_size = 20 ):
        super(ExportCrossword, self).__init__()
        self.row = row
        self.col = col
        self.grid = grid
        self.empty = empty
        self.MARGIN = margin
        self.grid_size =grid_size
        self.word_list = word_list
        self.font_size = font_size
        self.HEIGHT = self.MARGIN*2 + self.grid_size * self.row
        self.WIDTH = self.MARGIN*2 + self.grid_size * self.col
        

    def __draw_grid__(self):
        self.fig = plt.figure()
        self.sub = self.fig.add_subplot(111)
        for i in range(self.col+1):
            x0 = self.MARGIN + i * self.grid_size
            y0 = self.MARGIN
            x1 = self.MARGIN + i * self.grid_size
            y1 = self.HEIGHT - self.MARGIN
            self.sub.plot([x0, x1], [y0, y1], '-', color="black")
        for i in range(self.row+1):
            x0 = self.MARGIN
            y0 = self.MARGIN + i * self.grid_size
            x1 = self.WIDTH - self.MARGIN
            y1 = self.MARGIN + i * self.grid_size
            self.sub.plot([x0, x1], [y0, y1], '-', color="black")
        plt.axis("off")

    def __draw_puzzle__(self,pdf):
        computed_grid = []
        for i in range(self.row):
            rowc = [self.empty for itr in range(self.col)]
            computed_grid.append(rowc)
        count = 1
        cell_taken = []
        number_taken = []
        for word in self.word_list:
            if [word.row-1, word.col-1] not in cell_taken:
                computed_grid[word.row - 1][word.col - 1] = str(count)
                cell_taken.append([word.row-1, word.col-1])
                number_taken.append(count)
                word.number = count
            else:
                for i in range(len(cell_taken)):
                    if cell_taken[i] == [word.row-1, word.col-1]:
                        word.number = number_taken[i]
            count += 1
            for i in range(1,len(word.word)):
                if word.vertical:
                    computed_grid[word.row - 1 + i][word.col - 1] = ' '
                else:
                    computed_grid[word.row - 1 ][word.col - 1 + i] = ' '
        for i in xrange(self.row):
            for j in xrange(self.col):
                answer = computed_grid[i][j]
                x = self.MARGIN + (j) * self.grid_size + self.grid_size / 2
                y = self.MARGIN + (self.row - i-1) * self.grid_size + self.grid_size / 2
                if True:
                    color = "black"
                    self.sub.text(x,y, answer)
        pdf.savefig()
        plt.close()
    
    def __draw__legend__(self, pdf):
        self.fig = plt.figure()
        self.sub = self.fig.add_subplot(111)
        plt.axis("off")
        x0, x1, y0, y1 = plt.axis()
        plt.axis((x0,x1, 0, len(self.word_list)* self.font_size*self.font_size))
        x0, x1, y0, y1 = plt.axis()
        for i in xrange(len(self.word_list)):
            x = (len(self.word_list) * i) * 10 
            if self.word_list[i].vertical == 1:
                text = "Vertical"
            else:
                text = "Horizontal"
            self.sub.text(0, (y1 - x), "[" + str(self.word_list[i].number) + "] (" + text + ")  " + self.word_list[i].clue, fontsize = self.font_size)
        pdf.savefig()


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

if __name__=='__main__':
    game = Crossword(13, 13, 'X', 1, word_list)
    game.compute_crossword()
    self = ExportCrossword(game.row, game.col, 18,10, str(game.empty), game.grid, game.current_word_list, 10)
    self.__draw_grid__()
    with PdfPages("out.pdf") as pdf:
        self.__draw_puzzle__(pdf)
        self.__draw__legend__(pdf)
