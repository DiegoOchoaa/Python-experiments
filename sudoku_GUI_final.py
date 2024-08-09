import pygame, random




pygame.init()
clock = pygame.time.Clock()
width = 700
width = int(width/9)*9
slow = False
cycles = 0
screen = pygame.display.set_mode((width,width))
pygame.display.set_caption("sudoku vizualization")
font = pygame.font.Font('/Users/diegoochoa/Documents/python/soduko/Vercetti-Regular.ttf', int(width/10))
RED = (255, 0, 0)
RED_HIGHLIGHT = (102, 23, 20)
GREEN = (0, 255, 0)
BLUE = (35, 95, 168)
WHITE = (30, 30, 30)
HIGH = (60, 60, 60)
GREY = (50, 50, 50)


def display_text(text, x2, y2, color):
    text_surface = font.render(str(text), False, color)
    rect = text_surface.get_rect(center=(x2, y2))
    screen.blit(text_surface, rect)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.value = 0
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col *  width
        self.color = WHITE
        self.num_color = RED
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    def get_pos(self):
        return(self.row, self.col)
    
 
    def highlight(self, color):
         self.color = color


    def is_highlight(self, color):
         return self.color == color
    def reset(self):
         self.color = WHITE
  
         
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.width))



def generate_sudk_board(grid, delay, screen, removes, vizualization):
    solve_rnd(grid, delay, screen, vizualization)
   
   
    for x in range(len(grid)):
        for y in  range(len(grid[0])):
                rnd = random.randint(1, removes)
               
                if rnd != removes:
                    grid[x][y].value = 0


    



def solve_rnd(grid, delay, screen, vizualization):
    
    if vizualization:
        draw(screen, grid, 9, width)
        pygame.display.update()
        pygame.time.wait(delay)

    if not next_pos(grid):
        return True

    row, col = next_pos(grid)
    nums = [1,2,3,4,5,6,7,8,9]
    random.shuffle(nums)

    

    for num in nums:
        if legal_move( row, col, num, grid):
            grid[row][col].value = num
            grid[row][col].num_color = RED
            if solve_rnd(grid, delay, screen, vizualization):
                return True

            grid[row][col].value = 0
    return False
   
    
   

def solved(bo):
    solved = True
    for row in bo:
        for num in row:
            if num == 0:
                solved = False
    return solved
    

def make_grid(rows, width):
    
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j, gap, rows)
            grid[i].append(node)
    return grid



##SUDOKU###_____________--  ------


def legal_move(x, y, num, grid):
    global cycles
    cycles += 1
    emty_spaces_num = get_emty_spaces(grid)
    print('cycle_num: ', ('{:,}'.format(cycles)),'  ', 'emtpy_spaces_left:', emty_spaces_num)
    # Check row
    if num in [grid[x][i].value for i in range(9)]:
        return False
    
    # Check column
    if num in [grid[i][y].value for i in range(9)]:
        return False
    
    # Check 3x3 square
    box_x, box_y = 3 * (x // 3), 3 * (y // 3)
    for i in range(3):
        for j in range(3):
            if grid[box_x + i][box_y + j].value == num:
                return False
 
    return True
   


def get_emty_spaces(grid):
    emty_spaces = 0
    for row in grid: 
        for num in row:
           if num.value == 0:
               emty_spaces += 1


    return emty_spaces

def solve(grid, delay, screen, visualization):
   
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
          
    
    if visualization == True:
                 draw(screen, grid, 9, width)
                 pygame.display.update()
                 pygame.time.wait(delay)
                

    if not next_pos(grid):
        return True

    row, col = next_pos(grid)

    for num in range(1, 10):
        if legal_move( row, col, num, grid):
            grid[row][col].value = num
            grid[row][col].num_color = BLUE
            if solve(grid, delay, screen, visualization):
                
                return True

            grid[row][col].value = 0
   
   
    return False
    
   
def next_pos(grid):
   
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[y][x].value == 0:
                return y,x


    
    


def valid_sudoku_list(lst):
    nums = [x for x in lst if x != 0]  # Get all non-zero numbers
    return len(nums) == len(set(nums))  # Check if there are duplicates



def draw_grid(win, rows, width):
    
	gap = width // rows
	for i in range(rows):
            if i == 3 or  i == 6:
                 gap1 = 5
            else:
                 gap1 = 1
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap), gap1)
            for j in range(rows):
                if j == 3 or  j == 6:
                    gap2 = 5
                else:
                    gap2 = 1
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width), gap2)
           
def valid_sudoku_list(sudoku_board):
    re = True
    for row in sudoku_board:
       numbers = [1,2,3,4,5,6,7,8,9]
       for num in row:
           if num != 0:
               try:
                  numbers.remove(num)
               except:
                  re = False
    return re


def valid(suduko_board):
    #horizontal line check
    valid = True
    if valid_sudoku_list(suduko_board) == False:
        valid = False
     
    
    #vertical line check
    vertical_sodoku = []
    for y in range(len(suduko_board)):
       vertical_sodoku.append([])
       for x in range(len(suduko_board)):
           vertical_sodoku[y].append(suduko_board[x][y])
    if valid_sudoku_list(vertical_sodoku) == False:
        valid = False
    
    
    #squares check

    squares_3x3 = []
  
        
    for i in range(0,9,3):
        for j in range(0,9,3):
            square = [suduko_board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
            squares_3x3.append(square)

    if valid_sudoku_list(squares_3x3) == False:
        valid = False 
        
       

    return valid



def draw(screen, grid, rows, width):
    screen.fill(WHITE)

    for row in grid:
        for node in row:
            
            node.draw(screen)

    draw_grid(screen, rows, width)

    for row in grid:
        for square in row:
            if square.value != 0:
               display_text(square.value, square.x + square.width/2 , square.y + square.width/2 , square.num_color)

    pygame.display.update()
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col



def convert_sudoku_board(grid):
     sudoku_board = []
     for row in range(len(grid)):
          sudoku_board.append([])
          for col in range(len(grid)):
               sudoku_board[row].append(grid[row][col].value)
     return(sudoku_board)


def highlight(grid, row, col, color):
       grid[row][col].highlight(color)
       for rows in grid: 
                for node in rows:
                    if node != grid[row][col] and node.is_highlight(color):
                        
                        node.reset()



def clean(grid):
    for row in grid:
        for square in row:
            if square.num_color == BLUE:
                square.value = 0
                square.num_color = RED
            if square.is_highlight:
                square.reset()
def reset(grid):
    for row in grid:
        for square in row:
            square.value = 0
def get_number(grid, row, col, event):
   square = grid[row][col]
   if event.type == pygame.KEYDOWN:
     if event.key == pygame.K_1:
         square.value = 1
         square.num_color = RED
     if event.key == pygame.K_2:
          square.value = 2
          square.num_color = RED
     if event.key == pygame.K_3:
          square.value = 3
          square.num_color = RED
     if event.key == pygame.K_4:
          square.value = 4
          square.num_color = RED
     if event.key == pygame.K_5:
          square.value = 5
          square.num_color = RED
     if event.key == pygame.K_6:
          square.value = 6
          square.num_color = RED
     if event.key == pygame.K_7:
           square.value = 7
           square.num_color = RED
     if event.key == pygame.K_8:
          square.value = 8
          square.num_color = RED
     if event.key == pygame.K_9:
          square.value = 9
          square.num_color = RED
   if pygame.mouse.get_pressed()[0]: #RIGHT
          square.num_color = RED
          if square.value == 9:
               square.value = 0
          elif square.value != 9:
             square.value += 1
   if pygame.mouse.get_pressed()[2]: 
        square.value = 0
        square.num_color = RED



def main(screen, width):
    global cycles
    print('g to generate(up, down to change),v to turn off or on vizualization r to reset, space to run, up, numberical inputs')
    grid = make_grid(9, width)
    run = True
    started = False
    delay = 1
    sudoku_b_difficlty = 7
    visualization = False
    while run:
        draw(screen, grid ,9, width)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if started:
                continue
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, 9, width)
            
            val = valid(convert_sudoku_board(grid))
            get_number(grid, row, col, event)


            if started:
                continue
            
            if val == True:
                highlight(grid, row, col, HIGH)
             
            if val == False:
                 highlight(grid, row, col, RED_HIGHLIGHT)
            
                
               
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and  not started and val == True:
                     clean(grid)
                     cycles = 0
                     started = True
                     solve(grid, delay, screen, visualization)
                     print('final_cycle_count: ', ('{:,}'.format(cycles)))
                     if solved(grid):
                         started = False
                     if valid(grid):
                         print('board is valid')
                     else:
                         print('board is valid')
                elif event.key == pygame.K_r and  not started:
                    reset(grid)
                elif event.key == pygame.K_g and  not started:
                    reset(grid)
                    cycles = 0
                    print('generate_board')
                    generate_sudk_board(grid, 0, screen, sudoku_b_difficlty, visualization)
                elif event.key == pygame.K_UP:
                    sudoku_b_difficlty += 1
                    print('gen_dif = ', sudoku_b_difficlty)
                elif event.key == pygame.K_DOWN:
                    if sudoku_b_difficlty != 1:
                        sudoku_b_difficlty -= 1
                    print('gen_dif = ', sudoku_b_difficlty)
                elif event.key == pygame.K_v:
                    if visualization:
                        visualization = False
                        print('visualization: ', visualization)
                    else:
                        visualization = True
                        print('visualization: ', visualization)

                     
                     
            
           
            
            # press any number and it will put it int the cell you are above
            # and make the cell highlited

               
				           

            
            
                           

               

            
    pygame.quit()



main(screen, width)