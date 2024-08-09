import pygame,time
import math
from queue import PriorityQueue


pygame.init()
clock = pygame.time.Clock()
width = 1000

slow = False
screen = pygame.display.set_mode((width,width))
pygame.display.set_caption("ai pathfiding")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (30, 30, 30)
BLACK = (255, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (50, 50, 50)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col *  width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    def get_pos(self):
        return(self.row, self.col)
    
    def is_closed(self):
        return self.color == RED
    def is_open(self):
        return self.color == GREEN
    def is_air(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == TURQUOISE
    def is_path(self):
        return self.color == PURPLE
    def is_none(self):
        return self.color == WHITE
    def reset(self):
        self.color = WHITE
    ##MAKES
    def make_closed(self):
        self.color = RED
    def make_open(self):
        self.color = GREEN
    def make_barrier(self):
        self.color = BLACK
    def make_start(self):
       self.color = ORANGE
    def make_end(self):
       self.color = TURQUOISE
    def make_path(self):
        self.color = PURPLE
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.width))
    
    
    def update_neighbors(self, grid):
            self.neighbors = []
            if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_air(): # DOWN
                self.neighbors.append(grid[self.row + 1][self.col])

            if self.row > 0 and not grid[self.row - 1][self.col].is_air(): # UP
                self.neighbors.append(grid[self.row - 1][self.col])

            if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_air(): # RIGHT
                self.neighbors.append(grid[self.row][self.col + 1])

            if self.col > 0 and not grid[self.row][self.col - 1].is_air(): # LEFT
                self.neighbors.append(grid[self.row][self.col - 1])



    def __lt__(self, other):
        return False
    

def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def  reconstruct_path(came_from, current ,draw):

    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()



def algorithm(draw, grid, start, end,):
   
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
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
            print('path found')
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        
        if current != start:
            current.make_closed()

    return False
    

def save_grid(grid, start, end):
    grid_2 = []
    saved = []
    rows = len(grid[0])
    for i in range(rows):
        grid_2.append([])
        for j in range(rows):
            grid_2[i].append(grid[i][j].is_air())
    saved.append(start)
    saved.append(end)
    return grid_2

    
def load_grid(grid, saved_grid):
    grid_2 = []
    rows = len(grid[0])
    for i in range(rows):
        grid_2.append([])
        for j in range(rows):
            if saved_grid[i][j]:
                grid[i][j].make_barrier()
     

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows): 
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows): 
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
            



def draw(screen, grid, rows, width):
    screen.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(screen)

    draw_grid(screen, rows, width)
    pygame.display.update()
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col



def clean(grid):
                    
                    for row in grid:
                        for node in row:
                            if  node.is_path() or node.is_closed() or node.is_open() :
                                node.reset()

def main(screen, width):
    ROWS = 25
    grid = make_grid(ROWS, width)
    start = None
    end = None
    saved_grid = None
    run = True
    started = False
    saved = None
    while run:
        draw(screen, grid ,ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if started:
                continue
            if pygame.mouse.get_pressed()[0]: #LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    node.make_end()
                elif node != end and node != start:  node.make_barrier()
				           

            elif pygame.mouse.get_pressed()[2]: #RIGHT
                 pos = pygame.mouse.get_pos()
                 row, col = get_clicked_pos(pos, ROWS, width)
                 node = grid[row][col]
                 node.reset()
                 if node == start:
                     start = None
                 elif node == end:
                     end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and  not started and start and end:
                    clean(grid)
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    if not algorithm(lambda: draw(screen, grid ,ROWS, width), grid, start, end):  #added for comical propouses you can put only algorithm(lambda: draw(screen, grid ,ROWS, width), grid, start, end): and it will work
                        print('path__not__found')
                if event.key == pygame.K_r:
                    saved_grid = save_grid(grid, start, end) #saves map
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                if event.key == pygame.K_c :
                    clean(grid)
                if event.key == pygame.K_UP:
                   pass
                    
                if event.key == pygame.K_DOWN:
                    pass

                if event.key == pygame.K_l and saved_grid != None: # loads map
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    load_grid(grid, saved_grid)

                if event.key == pygame.K_i:
                    olds = start
                    olde = end
                    start = olde
                    end = olds
                    end.make_end()
                    start.make_start()
                    clean(grid)
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    if not algorithm(lambda: draw(screen, grid ,ROWS, width), grid, start, end):  #added for comical propouses you can put only algorithm(lambda: draw(screen, grid ,ROWS, width), grid, start, end): and it will work
                        print('path__not__found')

                          

                          


                if event.key == pygame.K_f and end != None and start != None:
                    for row in grid:
                        for node in row:
                            if node.is_air():
                                node.reset() 
                            elif  node.is_none():
                                node.make_barrier()
                            
                                

                            
                    start.make_start()
                    end.make_end()
                
            
                    
                           

               

            
    pygame.quit()


main(screen, width)