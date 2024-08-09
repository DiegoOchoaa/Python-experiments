import pygame, random
import sys
from queue import PriorityQueue
# make it so the farther away it is from the current cell the more transparent it is
sys.setrecursionlimit(1000000)
pygame.init()
clock = pygame.time.Clock()

stack = []
possible_rows = [20, 100,200,500, 700]
which = 2
ROWS  = possible_rows[which]
ROWS = ROWS +1
width = 1300
if which == 3:
     width = 1500
if which == 1 or which == 0 or  which == 2:
     width = 1000
width = int(width/ROWS)*ROWS
slow = False
screen = pygame.display.set_mode((width,width))
clock = pygame.time.Clock()
pygame.display.set_caption("depht first search maze generetor and solver w/ A*"  )

RED = (255, 0, 0)
PATH = (4, 200, 2)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
END = (255, 0, 0)
BLUE1 = (25,25,25)
START = (49, 173, 0)
GREY = (40, 40, 40)
BLACK =(250,250,250)
BACK = (250,250,250)
tone = [0, 0, 255]



class Cell:
    def __init__(self, row, col, width, total_rows):
        
        self.value = 0
        self.row = row
        self.col = col
        self.tone = None
        self.closed = False
        self.x = row * width
        self.y = col *  width
        self.color = BLUE1
        self.neighbors = []
        self.width = width
        self.back = False
        self.path = False
        self.total_rows = total_rows
        self.visited = False
    def get_pos(self):
        return(self.row, self.col)
    
    def is_closed(self):
        return  self.closed == True
    def is_open(self):
        return self.color == RED
    def is_air(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == START
    def is_end(self):
        return self.color == END
    def is_path(self):
        return self.color == PATH
    def is_path(self):
        return self.path == True
    def is_none(self):
        return self.color == BLACK
    def reset(self):
        self.color = BLACK

    
    def make_start(self):
       self.color = START
       self.closed = False
    def make_end(self):
       self.color = END
       self.closed = False
    def make_closed(self,qan):
        global tone
        red = tone[0]
        green = tone[1]
        blue = tone[2]
        if red < 250:
            red += qan
            if blue > 1:
                blue -= qan
        elif green < 250:
            green += qan
            red -= qan
            if blue > 1:
                blue -= qan
            
        elif blue < 250:
            blue += qan
            if green > 1:
                green -= qan
            if red > 1:
                red -= qan
        elif red < 240 and blue < 240 and green < 240:
             red = 0
             blue = 255
             green = 0

           
           
            

        tone[0] = red
        tone[1] = green
        tone[2] = blue
        
        self.tone = (tone[0],tone[1],tone[2])
        self.color = (tone[0],tone[1],tone[2])
        self.closed = True


    def make_open(self):
       self.color = RED
       self.closed = False
    def remake_color(self):
         self.color = self.tone
         self.path = True
         self.closed = True
    def make_path(self):
        self.tone = self.color
        self.closed = False
        self.color = PATH
        self.path = True

    def make_visited(self):
         self.color = BLACK
         self.visited = True
    def make_backtracked(self):
         self.color = BACK
         self.back = True
    def is_bactracked(self):
         return self.color == BACK
    def make_highlight(self):
         self.color = START
    def is_visited(self):
        return self.visited == True
    def make_end(self):
        #self.color = END
        pass
    def reset(self):
         self.path = False
         self.closed = False
         self.back = False
         self.color = BLUE1
         self.visited = False
        
    
  
         
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.width))

  
        
    def update_neighbors_1block(self, grid):
            self.neighbors = []
            if self.row < self.total_rows - 1 and  grid[self.row + 1][self.col].is_none(): # DOWN
                self.neighbors.append(grid[self.row + 1][self.col])

            if self.row > 0 and  grid[self.row - 1][self.col].is_none(): # UP
                self.neighbors.append(grid[self.row - 1][self.col])

            if self.col < self.total_rows - 1 and  grid[self.row][self.col + 1].is_none(): # RIGHT
                self.neighbors.append(grid[self.row][self.col + 1])

            if self.col > 0 and  grid[self.row][self.col - 1].is_none(): # LEFT
                self.neighbors.append(grid[self.row][self.col - 1])


    def update_neighbors(self, grid):
            self.neighbors = []
            if self.row > 0 and not grid[self.row - 2][self.col].is_visited() and self.row != 1 : # top
                self.neighbors.append(grid[self.row - 2][self.col])


            if self.col < self.total_rows - 2 and not grid[self.row][self.col + 2].is_visited(): # right
                self.neighbors.append(grid[self.row][self.col + 2])

            if self.row < self.total_rows - 2 and not grid[self.row + 2][self.col].is_visited() :  # bottom
                self.neighbors.append(grid[self.row + 2][self.col])
                


            if self.col > 0 and not grid[self.row][self.col - 2].is_visited() and self.col != 1: # left
                self.neighbors.append(grid[self.row][self.col - 2])
    
   
          
################### A***** ######

def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def  reconstruct_path(came_from, current ,draw, vis, frame_rate, delay):
    cn = 0
    while current in came_from:
        # loop to be able to change settings while runing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_SPACE:
                     if vis:
                          vis = False
                     else:
                          vis = True            
                if event.key == pygame.K_c:
                     frame_rate = 1000000
        ##############################
        current = came_from[current]
        current.make_path()
        cn += 1
        if vis or cn > frame_rate:
           draw()
           cn = 0
        
        if delay != 0 and  vis == True:
             pygame.time.delay(delay)
             
       
             
    


def clean(grid):
     for row in grid:
          for cell in row:
               if cell.is_open() or cell.is_closed():
                    cell.color = BLACK
    
  
def algorithm_Astar(draw, grid, start, end, vis, frame_rate, delay,qan):
    cn = 0
    count = 0
    old_framerate  = frame_rate
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
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_SPACE:
                     if vis:
                          vis = False
                     else:
                          vis = True
                if event.key == pygame.K_c:
                     frame_rate = 90000
                     vis = False 

                    

            
               
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        
        if current == end and False:
            
            reconstruct_path(came_from, end, draw, vis, old_framerate, delay)
            
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
        cn += 1
        
        if vis or cn > frame_rate :
                draw()
                cn = 0
        if delay != 0 and vis == True:
             pygame.time.delay(delay)
        
        if current != start:
            current.make_closed(qan)

    return came_from



def make_grid(rows, width):
    
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i,j, gap, rows)
            
            grid[i].append(cell)
    return grid

def connect(a,b, grid):
     
     a_val, b_val = a.get_pos()[0] - b.get_pos()[0],   a.get_pos()[1] - b.get_pos()[1]
   
     if a_val == 2: #lft
          grid[a.get_pos()[0]  - 1 ][a.get_pos()[1]].make_visited()
     elif a_val == -2: #down
          grid[a.get_pos()[0]  + 1 ][a.get_pos()[1]].make_visited()
     elif b_val == 2: #right
          grid[a.get_pos()[0]  ][a.get_pos()[1] - 1].make_visited()
     elif b_val == -2: #up
          grid[a.get_pos()[0]  ][a.get_pos()[1] + 1].make_visited()
     else: 
          return True
     return False
def connect_back(a,b, grid):
     a_val, b_val = a.get_pos()[0] - b.get_pos()[0],   a.get_pos()[1] - b.get_pos()[1]
   
     if a_val == 2: #lft
          grid[a.get_pos()[0]  - 1 ][a.get_pos()[1]].make_backtracked()
     elif a_val == -2: #down
          grid[a.get_pos()[0]  + 1 ][a.get_pos()[1]].make_backtracked()
     elif b_val == 2: #right
          grid[a.get_pos()[0]  ][a.get_pos()[1] - 1].make_backtracked()
     elif b_val == -2: #up
          grid[a.get_pos()[0]  ][a.get_pos()[1] + 1].make_backtracked()
     else: 
          return True
     return False





    

def algorythm(draw, grid, current_cell, delay, vizualize, old_d, frame_rate, time_variable, finish):  # top right bottom left
    
    time_variable += 1
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_c:
                    vizualize = False
                    frame_rate = 1000000
                    finish = True
                if event.key == pygame.K_SPACE:
                     if delay != 0:
                        old_d = delay
                        delay = 0
                        vizualize = False
                     else: 
                          delay = old_d
                          vizualize = True
              
                   
    current_cell.make_highlight()
    
    if vizualize:
         draw()
    elif not vizualize and not finish:
        if  time_variable > frame_rate :
                 draw()
                 time_variable = 0
      


    
    current_cell.make_backtracked()
    current_cell.update_neighbors(grid)
    if not current_cell.is_visited():
        current_cell.make_visited()
    
    
    if  current_cell.neighbors != []:
    
             
        random.shuffle(current_cell.neighbors)

        stack.append(current_cell)

        connect(current_cell,current_cell.neighbors[0], grid)
        if vizualize:
            pygame.time.delay(delay)
        algorythm(draw, grid, current_cell.neighbors[0], delay, vizualize, old_d, frame_rate, time_variable, finish)
       
    elif len(stack) > 1:
         if vizualize:
            pygame.time.delay(delay)
         old_cell = current_cell
         current_cell = stack.pop()
         current_cell.make_highlight()
         if vizualize:
                draw()
         elif not vizualize and not finish:
            if  time_variable > frame_rate :
                 draw()
                 time_variable = 0
      
         current_cell.make_backtracked()
         connect_back(current_cell,current_cell.neighbors[0], grid)
         
         algorythm(draw, grid, current_cell, delay, vizualize, old_d, frame_rate, time_variable, finish)
    else:
         return 0
    
   
         
       
         
         
     
         

   

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows): 
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows): 
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
def draw(screen, grid, rows, width):
    screen.fill(BLUE1)

    for row in grid:
        for cell in row:
            
            cell.draw(screen)
            if  cell.is_visited():
                 pass
                #cell.draw_walls(screen)
                

    

   
    pygame.display.update()
    clock.tick(12000)





def main(screen, width):
    global stack, tone
    print('SPACE to run, c to complete all map, r to reset, v to turn on and off vizualization, SPACE for fast in maze generation, c to clean after')
    grid = make_grid(ROWS, width)
    run = True
    vis = True
    came_from = None
    frame_rate = 3000
    color_change_q = 1
    delay = 20
    end = None
    olddelay = 0
    time_variable = 0
    start_pos = grid[ROWS//2][ROWS//2]
    if ROWS == 21:
         frame_rate = 1
         color_change_q = 5

    if ROWS == 101:
         frame_rate = 1
         color_change_q = 0.15
    elif ROWS == 701:
         frame_rate = 1500
         color_change_q = 0.003
         delay = 1
    elif ROWS == 501:
         frame_rate = 1000
         color_change_q = 0.006
         delay = 1
    elif ROWS == 201:
         frame_rate = 15
         color_change_q = 0.04
         delay = 1
    
    while run:
        draw( screen, grid ,ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_SPACE:
                     tone = [0, 0, 255]

                     for row in grid:
                          for cell in row:
                                 cell.reset()
                    
                     algorythm(lambda: draw(screen, grid ,ROWS, width), grid,  start_pos, delay, vis, 0, frame_rate, time_variable, False)
                     start_pos.make_highlight()
                     if end == None:
                        end = grid[ROWS-1][ROWS-1]
                        end.make_end()
                     for row in grid:
                        for cell in row:
                             cell.update_neighbors_1block(grid)
                     came_from = algorithm_Astar(lambda: draw(screen, grid ,ROWS, width), grid, start_pos, end, vis, frame_rate, delay, color_change_q)  #added for comical propouses you can put only algorithm(lambda: draw(screen, grid ,ROWS, width), grid, start, end): and it will work
                   
                     
                   
                if event.key == pygame.K_c:
                     clean(grid)

                if event.key == pygame.K_r:
                     for row in grid:
                          for cell in row:
                                 cell.reset()
                                 
                if event.key == pygame.K_v:
                     if vis:
                          vis = False
                          frame_rate += 60000
                          print('vizualization: ',vis)
                          olddelay = delay
                          delay = 0
                     else:
                          frame_rate -= 60000
                          vis = True
                          print('vizualization: ',vis)
                          delay = olddelay
                     
                    
            
        if pygame.mouse.get_pressed()[0] and came_from != None: #LEFT   # totally optional does not need to be here
                frame_rate += 8000
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)

                clicked_cell = grid[row][col] 
                if (row % 2) != 0 : row += 1
                if (col % 2) != 0 : col += 1
                     
                clicked_cell = grid[row][col] 
                     
                
                     
                     
               
                for row in grid:
                        for cell in row:
                                if cell.is_path():
                                    cell.remake_color()
                
                
                vis = False
                reconstruct_path(came_from,clicked_cell,lambda: draw(screen, grid ,ROWS, width),vis,frame_rate,delay)
                frame_rate -= 8000
                
                   
                
        
                             

            
    pygame.quit()



main(screen, width)
