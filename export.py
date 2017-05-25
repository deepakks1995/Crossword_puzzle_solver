import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from crossword import Crossword
from word import Word
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
            if not [word.row-1, word.col-1] in cell_taken:
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
        plt.axis((x0,x1, 0, len(self.word_list)* 15*20))
        x0, x1, y0, y1 = plt.axis()
        for i in xrange(len(self.word_list)):
            x = (len(self.word_list) * i) * 10 
            if self.word_list[i].vertical == 1:
                text = "Vertical"
            else:
                text = "Horizontal"
            self.sub.text(0, (y1 - x), "[" + str(self.word_list[i].number) + "] (" + text + ")  " + self.word_list[i].clue, fontsize = self.font_size)
        pdf.savefig()

if __name__=='__main__':
    print "You are in the wrong file"