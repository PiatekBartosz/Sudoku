import pygame, sys
from pygame.locals import *
import numpy

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = LIGHT_GRAY
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                #toggle acivate
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    global matrix 
                    matrix = get_matrix(inputboxes)
                    print(numpy.matrix(matrix))
                    solve()
                    print("test")
                elif event.key == pygame.K_BACKSPACE:
                    self.text = ''
                elif event.key >= 49 and event.key <= 57:
                    self.text = event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, DISPLAYSURF):
        # Blit the text.
        DISPLAYSURF.blit(self.txt_surface, self.txt_surface.get_rect(center = (self.rect.x + self.rect.w/2, self.rect.y + self.rect.h/2)))
        # Blit the rect.
        pygame.draw.rect(DISPLAYSURF, self.color, self.rect, 2)
        


def main():
    global DISPLAYSURF, FPSCLOCK, width, height, WHITE, LIGHT_GRAY, GRAY
    global cell_size_x, cell_size_y, inputboxes
    global FONT, DISPLAYSURF, fontsize
    #window size
    width = 720
    height = 720
    #grid 
    cell_size_x = int(width/9)
    cell_size_y = int(width/9)
    FPS = 60
    #colours
    WHITE = (255, 255, 255)
    LIGHT_GRAY = (200, 200, 200)
    GRAY = (50, 50, 50)
    #font
    pygame.font.init()
    fontsize = 64
    FONT = pygame.font.Font(None, fontsize)
    #init pygame & screen
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sudoku solver")
    DISPLAYSURF.fill(GRAY)
    draw_grid()
    
    #input boxes
    inputboxes = []
    for i in range(0, height + cell_size_y, cell_size_y):
        for j in range(0, width, cell_size_x):  
            inputboxes.append(InputBox(j, i, cell_size_x, cell_size_y))

    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            for box in inputboxes:
                box.handle_event(event)

        #erease old
        DISPLAYSURF.fill(GRAY)
        draw_grid()
        for box in inputboxes:
            box.draw(DISPLAYSURF)

        pygame.display.flip()
        FPSCLOCK.tick(FPS)

def draw_grid():
    bolded_line = 6
    #vertical grid
    for x in range(0, width, 3*cell_size_x):
        pygame.draw.line(DISPLAYSURF, LIGHT_GRAY, (x, 0), (x , height), bolded_line)
    #horizontal grid
    for y in range(0, width, 3*cell_size_y):
        pygame.draw.line(DISPLAYSURF, LIGHT_GRAY, (0, y), (width, y), bolded_line)

def get_matrix(inputboxes):
    temp = []
    temp2 = []
    for box in inputboxes:
        if len(temp2) < 9:
            if box.text == '':
                temp2.append(0)
            else:
                temp2.append(int(box.text))
        else:
            temp.append(temp2)
            temp2 = []
            if box.text == '':
                temp2.append(0)
            else:
                temp2.append(int(box.text))
    return temp

def solve():
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                for n in range(1, 10):
                    if possible(i, j, n):
                        matrix[i][j] = n
                        solve()
                        matrix[i][j]  = 0
                return
    print(numpy.matrix(matrix))
    input("More?")
    return

def possible(y, x, n):
    #check for horizontal
    for i in range(0, 9):
        if matrix[y][i] == n:
            return False
    #check for vertical
    for i in range(0, 9):
        if matrix[i][x] == n:
            return False
    #check in square x0, y0 upper left of square
    x0 = (x//3) * 3
    y0 = (y//3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if matrix[y0 + i][x0 + j] == n:
                return False
    return True

if __name__ == "__main__":
    main()