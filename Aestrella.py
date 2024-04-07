"""De Tim: https://www.youtube.com/watch?v=JtiK0DOeI4A"""

import pygame
import math
from queue import PriorityQueue

WIDTH = 1000
WINDOW = pygame.display.set_mode((WIDTH, WIDTH)) #La pantalla es un cuadrado

pygame.display.set_caption("A* Path Finding Algortihm visualization")
pygame.init()

#Los colores a usar
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Square:
    """Cada cuadrado de la pantalla es un objeto con un color"""
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width #Para las coordenadas de cada cuadrado
        self.y = col * width #Cada cuadrado tiene una anchura y altura a tener en cuenta, por eso hay que hacer una especie de plantilla
        self.color = WHITE #Color inicial es blanco para todos
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows 

    def get_pos(self):
        return self.row, self.col
    
    #Comorbaciones de si los cuadrados son un color u otro
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, WINDOW):
        pygame.draw.rect(WINDOW, self.color,(self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {square: float("inf") for row in grid for square in row}
    g_score[start] = 0

    f_score = {square: float("inf") for row in grid for square in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1
        
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()
        if current != start:
            current.make_closed()

    return False
def make_grid(rows, width):
    """Grid creation"""
    grid =[]
    gap = width // rows #Anchura de los cuadrados en la grid

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            square = Square(i, j, gap, rows) #Se crea el objeto
            grid[i].append(square) #Y se añade a la grid
        
    return grid

def draw_grid(win, rows, width):
    """Dibuja las líneas grises"""
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i* gap), (width, i *gap))
        for j in range(rows):
                    pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    """Dibuja la plantilla entera"""
    win.fill(WHITE)

    for row in grid:
        for square in row:
            square.draw(win) #Dibuja cada cuadradito de forma individual

    draw_grid(win, rows, width) #Por encima se dibujan las líneas grises
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    """Simplemente devuelve la posición con respecto a filas y columnas
    a partir de la posición en la ventana"""
    gap = width // rows
    y,x = pos

    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    """Main function of the game"""
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]:
                """Si se presiona click izquierdo"""
                pos = pygame.mouse.get_pos() #Se obtiene la posición del ratón y se guarda en pos
                row, col = get_clicked_pos(pos, ROWS, width) # Así se obtiene la fila y columna que se ha pulsado con la función auxiliar
                square = grid[row][col]

                if not start and square != end:
                    """Si no hay inicio, se le asigna"""
                    start = square
                    start.make_start()

                elif not end and square != start:
                    """Si no hay final, se dibuja"""
                    end = square
                    end.make_end()
                
                elif square != start and square != end:
                    square.make_barrier()


            elif pygame.mouse.get_pressed()[2]:
                """Click derecho, el centro sería [1]"""
                pos = pygame.mouse.get_pos() #Se obtiene la posición del ratón y se guarda en pos
                row, col = get_clicked_pos(pos, ROWS, width) # Así se obtiene la fila y columna que se ha pulsado con la función auxiliar
                square = grid[row][col]
                square.reset()

                if square == start:
                    start = None

                elif square == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                """Did you press a key down on the keyboad?"""
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for square in row:
                            square.update_neighbours(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
            
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

    
main(WINDOW, WIDTH)

