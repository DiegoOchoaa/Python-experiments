import pygame, random, math




pygame.init()
clock = pygame.time.Clock()


ROWS = 20
width = 900
width = int(width/ROWS)*ROWS
slow = False
screen = pygame.display.set_mode((width,width))
pygame.display.set_caption("FABRIK")
font = pygame.font.Font('/Users/diegoochoa/Documents/python/soduko/Vercetti-Regular.ttf', int(width/70))

BLACK = (25, 25, 25)
GREY = (33, 33, 33)
WHITE = (255, 255, 255)
def display_text(text, x2, y2, color):
    text_surface = font.render(str(text), False, color)
    rect = text_surface.get_rect(center=(x2, y2))
    screen.blit(text_surface, rect)
def reverse(list):
    for i in range(len(list)):
      last_item = list.pop()
      list.insert(i, last_item)
    return list


def setMag(vector, target_magnitude):
    current_magnitude = math.sqrt(sum(x**2 for x in vector))
    
    if current_magnitude == 0:
        return [0.0] * len(vector)
    
    scaling_factor = target_magnitude / current_magnitude
    scaled_vector = [x * scaling_factor for x in vector]
    
    return scaled_vector


class Rig:
    def __init__(self, origin, number_of_segments, seg_lenght, iterations, Show_angle):
        self.origin = origin
        self.show_angle = Show_angle
        self.iterations = iterations
        self.seg_num = number_of_segments
        self.points = []
        self.lenght = seg_lenght
        self.segments = self.create_segments()
        self.r_segments = reverse(self.segments)
        total_lenght = 0
        self.target = None
        for i in self.segments:
            total_lenght += i.lenght
        self.total_lenght = total_lenght

    def create_segments(self):
        segs = []
        for seg in range(self.seg_num):
            segs.append(Segment((self.origin), 0, self.lenght))
        return segs
    
    def show(self):
        #pygame.draw.circle(screen, (50,50,50), self.origin, self.total_lenght, 5)
        for seg in self.segments:
            seg.draw()
            seg.update()
    def update(self, target):
        for seg in range(len(self.segments) - 1):
            self.segments[seg + 1].a = self.segments[seg].b
        ## conects segments
        self.target = target

        d =  math.sqrt(( target[0] - self.segments[0].a[0])**2 + ( target[1] -self.segments[0].a[1])**2)



        
        if  d > self.total_lenght:
            dir = (target[1] - self.origin[1], target[0] - self.origin[0])
            angle = math.atan2(dir[0],dir[1])
            angle  = math.degrees(angle)
            for seg in self.segments:
                seg.set_angle(angle)
        else:
            self.initialize_points()
            dist = 100
            cycles = 0
            while dist > 0.00000001 and cycles < 300:
                self.solve_FABRIK()
                self.solve_FABRIK_back()
                cycles += 1
                

                angle = get_angle(target, self.points[0])
                b = calc_st(self.points[0], self.segments[0].lenght, angle)
                dist =  math.sqrt(( target[0] - b[0])**2 + ( target[1] - b[1])**2)
            print(cycles)
       
                

            # setting new posicions
            self.points = reverse(self.points)
            self.points.append(target)
            for i in range(len(self.points)-1):
                
                
                segment = self.segments[i]

                segment.a = self.points[i]

               
                angle = get_angle(self.points[i+1], self.points[i])

                segment.set_angle(angle)
                if self.show_angle:
                        display_text(str(int(angle)), self.points[i][0],  self.points[i][1] - 15, WHITE)
               
            b = self.segments[len(self.segments)-1]
            
            
            
            
            
            
            
        
            

    def initialize_points(self):
        self.points = []
        for i in range(len(self.segments)):
                    total = len(self.segments)-1
                    self.points.append(self.segments[total - i].a)


    def solve_FABRIK(self):
                
                new_heuristic_points = [self.target]

                for seg in range(len(self.segments)):
                    point = new_heuristic_points[seg]
                    seg_point = self.points[seg]

                    angle = get_angle(seg_point , point)
                    b = calc_st(point, self.lenght, angle)
            
                    #pygame.draw.circle(screen, (255,50,50), b, 5)
                    #pygame.draw.line(screen, (80,80,80), b,point, 3)

                    new_heuristic_points.append(b)

                self.points = new_heuristic_points 
                self.points.pop(len(self.points)-1)
    


    def solve_FABRIK_back(self):
        
        new_heuristic_points = [self.origin]

        for seg in range(len(self.segments)):
            point = new_heuristic_points[seg]
            
            seg_point = self.points[len(self.points)-1 - seg]

            angle = get_angle(seg_point , point)
            b = calc_st(point, self.lenght, angle)
                
            #pygame.draw.circle(screen, (255, 255,50), b, 5)
            #pygame.draw.line(screen, (100,100,100), b,point, 3)

            new_heuristic_points.append(b)
        

        self.points = reverse(new_heuristic_points)
        self.points.pop(0)
       


                
                
   
       


class Segment:
    def __init__(self, initial_pos, angle, lenght):
        self.a = initial_pos
        self.angle = 0
        self.set_angle(angle)
        self.lenght = lenght
        self.b = []
        self.update()
    def calculate_b(self):
        dx =  self.lenght * math.cos(self.angle)
        dy =  self.lenght * math.sin(self.angle)
        self.b = [self.a[0] + dx, self.a[1] + dy]
    def update(self):
        self.calculate_b()
        

    def draw(self):
        pygame.draw.line(screen, WHITE, self.a, self.b, 3)
        pygame.draw.circle(screen, WHITE, self.a, 5)
        pygame.draw.circle(screen, WHITE, self.b, 5)
        

    def set_angle(self, angle):
        angle = math.radians(angle)
        self.angle = angle

    def follow(self, target):
        dir = (target[1] - self.a[1], target[0] - self.a[0])
        self.angle = math.atan2(dir[0],dir[1])
    def get_point(self, target):
        dir = (target[1] - self.a[1], target[0] - self.a[0])
        a = math.atan2(dir[0],dir[1])
        return math.degrees(a)

def calc_st(a, length, angle):
    angle = math.radians(angle)
    dx =  length * math.cos(angle)
    dy =  length * math.sin(angle)
    b = [a[0] + dx, a[1] + dy]
    return b
def get_angle(a, b):
    dir = (a[1] - b[1], a[0] - b[0])
    angle = math.atan2(dir[0],dir[1])
    angle  = math.degrees(angle)
    return angle




def calculate_closest_point(point, a, b):
    distance_a =  math.sqrt(( point[0] - a[0])**2 + ( point[1] - a[1])**2)
    distance_b =  math.sqrt(( point[0] - b[0])**2 + ( point[1] - b[1])**2)
    if distance_a < distance_b:
        return a
    else: 
        return b


def main(screen, width):
    print('grid min')
    anchor = [width//2,width//4]
    trail = []
    showangle = True
    main_rig = Rig((width//2, width//2),4,100,20, showangle)


    
    
   
    run = True
    cx = 0
    while run:
        clock.tick(60)
        screen.fill(GREY)
        mouse_pos = pygame.mouse.get_pos()
     
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
       
        all_keys = pygame.key.get_pressed()

        speed = 3
        if  all_keys[pygame.K_DOWN] == True :
                trail.append([anchor[0], anchor[1]])
                anchor[1] += speed
        if  all_keys[pygame.K_UP] == True :
                trail.append([anchor[0], anchor[1]])
                anchor[1] -= speed
        if  all_keys[pygame.K_LEFT] == True:
                trail.append([anchor[0], anchor[1]])
                anchor[0] -= speed
        if  all_keys[pygame.K_RIGHT] == True:
                trail.append([anchor[0], anchor[1]])
                anchor[0] += speed
        
        if pygame.mouse.get_pressed()[0]: #LEFT
             anchor = [mouse_pos[0], mouse_pos[1]]
        
      
        if len(trail) > 200:
            trail.pop(0)
        for i in trail:
            pygame.draw.circle(screen, (50,50,50), i, 5)
       
        
        pygame.draw.circle(screen, (50,50,50), anchor, 10)
        
        
        main_rig.update(anchor)
        main_rig.show()

        

       
        
       
    
        
        
        pygame.display.update()
                

            
    pygame.quit()



main(screen, width)