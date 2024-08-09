import pygame, random, math
import numpy as np
pygame.init()
clock = pygame.time.Clock()

width = 1000
height = 1000

slow = False
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("raytracing GUI")
font = pygame.font.Font('/Users/diegoochoa/Documents/python/soduko/Vercetti-Regular.ttf', int(width/70))
pygame.mouse.set_visible(False)
GREEN = (0,255,0)
BLACK = (25, 25, 25)
GREY = (130, 130, 130)
WHITE = (255, 255, 255)
OFF_WHITE = (230, 230, 240)
BLUE = (100,255,200)
LIGHT_COLOR = (149, 191, 188)
LIGHT_COLOR = (252, 186, 3)

LINE_COLOR = WHITE

def convert_range(value_to_be_converted, start_orig, end_orgn, new_start, new_end):
 
    return new_start + (value_to_be_converted - start_orig) * (new_end - new_start) / (end_orgn - start_orig)

def get_angle(p1, p2):
   
   return  math.atan2(p2[1] - p1[1] , p2[0] - p1[0])


def convert_poligon_to_walls(poligon_points, walls):
    past_point = None
   

    for point in poligon_points:
        if past_point != None:
            walls.append(Boundary(past_point,point,False))
        past_point = point

    walls.append(Boundary(past_point,poligon_points[0], False))

class Boundary(pygame.sprite.Sprite):
    def __init__(self, a, b, iswall):
        self.a = a
        self.b = b
        self.is_wall = iswall
    def draw(self, wall_width):
         pygame.draw.line(screen,WHITE,self.a,self.b,wall_width)
    def collision_with_other_wall(self, pos, wall):
        x1 = wall.a[0]
        y1 = wall.a[1]
        x2 = wall.b[0]
        y2 = wall.b[1]



        x3 = self.a[0]
        y3 =  self.a[1]
        x4 = self.b[0]
        y4 = self.b[1]

        det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if det == 0:

            return None


        t = ((x1 - x3) * (y3 - y4) - (y1 -y3) * (x3  - x4))  / det

        u = -((x1  - x2) * (y1 -y3) - (y1 - y2) * (x1  - x3)) / det

        if 0 <= t  <= 1 and u >= 0 :
            x = x1  + t * (x2  - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)
        
        return None
class Ray(pygame.sprite.Sprite):
    def __init__(self,angle):
        self.angle = angle
        self.pos = None
        self.distance = None
     
    def draw(self, pos, color, line_width):
        dx = math.cos(self.angle) * 2000  # length of ray for drawing purposes, can adjust this value
        dy = math.sin(self.angle)  * 2000
        pygame.draw.line(screen, color, pos, (pos[0] + dx, pos[1]  + dy),line_width)
    def define_pos(self,pos):
        self.pos = pos
    
   
        
   
    
    def cast(self, pos, wall):
        x1 = wall.a[0]
        y1 = wall.a[1]
        x2 = wall.b[0]
        y2 = wall.b[1]



        x3 = pos[0]
        y3 = pos[1]
        x4 = pos[0] + math.cos(self.angle)
        y4 = pos[1] + math.sin(self.angle)

        det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if det == 0:

            return None


        t = ((x1 - x3) * (y3 - y4) - (y1 -y3) * (x3  - x4))  / det

        u = -((x1  - x2) * (y1 -y3) - (y1 - y2) * (x1  - x3)) / det

        if 0 <= t  <= 1 and u >= 0:
            x = x1  + t * (x2  - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)
        
        return None




def make_boundaries(height, width, ww):
    new_h = height + ww
    new_w = width + ww
    h0 = -ww
    w0 = -ww
    walls = []
    walls.append(Boundary((w0,h0), (w0,new_h), True)) #side
    walls.append(Boundary((new_w,new_h), (w0,new_h), True)) #bottom
    walls.append(Boundary((new_w,h0), (new_w,new_h), True)) #side
    walls.append(Boundary((w0,h0), (new_w,h0), True)) #top
    return walls


def draw_hits(list, screen):
    for i in range(len(list)):
        try:
           pygame.draw.circle(screen, list[i][0], list[i][1], list[i][2])
        except: pass
    return []

def draw_fill_poligons(rays,screen, pos, color):
    past_pos = None
    rays.sort(key=lambda x: x.angle)


    for ray in rays:

          if past_pos != None:
            pygame.draw.polygon(screen, color, (ray.pos, past_pos,pos))
        
          past_pos = ray.pos
    pygame.draw.polygon(screen, color, (rays[0].pos, past_pos,pos))



def draw_rays(rays_to_draw,screen,line_width):
    rtw = rays_to_draw
    for i in range(len(rtw)):
        pygame.draw.line(screen, LINE_COLOR, rtw[i][0], rtw[i][1], line_width)
    return []

def rays_fr_each_wall(walls,rays, pos):
            for wall in walls:
                dif =  0.00001
                
                angle = get_angle(pos, wall.a)
                rays.append(Ray(angle))
                rays.append(Ray(angle - dif))
                rays.append(Ray(angle + dif))
                

                angle = get_angle(pos, wall.b)
                rays.append(Ray(angle))
                rays.append(Ray(angle - dif))
                rays.append(Ray(angle + dif))
            
def main():
    print('up and down arrow keys to make more defined and less defined, r to reset, space to make new enviorment, h to hide dots and  v to see walls')
    pog_points = [[(700, 284), (612, 401), (850, 391)],
                 
[(1110, 70), (958, 289), (1385, 526), (1339, 241), (1329, 85)],

[(252, 463), (112, 717), (416, 752), (336, 279), (308, 299)],
[(936, 570), (685, 832), (1010, 857), (1143, 559), (1084, 533)],
[(1344, 607), (1351, 759), (1394, 725)]]
    

    vis = True
    hide_points = False
    time = 0
    ray_setup_num = 3

    poligon_points = []
    poligons = []
    hits = []
    rays_to_draw = []
   
    wall_width = 5
    line_width = 1
    walls =  make_boundaries(height,width, wall_width)
    rays = []
    for pog in pog_points:
         convert_poligon_to_walls(pog, walls)
    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
           
              
            
            if event.type == pygame.KEYDOWN:         
                
                if event.key == pygame.K_SPACE:
                    walls =  make_boundaries(height,width, wall_width)
                    poligons = []
                    for pog in pog_points:
                        convert_poligon_to_walls(pog, walls)
                    poligon_points = []
                if event.key == pygame.K_r:
                    walls =  make_boundaries(height,width, wall_width )
                    poligons = []
                    poligon_points = []
                if event.key == pygame.K_q:
                    running = False
               
                if event.key == pygame.K_v:
                    if vis:
                        vis = False
                    else:
                        vis = True
                if event.key == pygame.K_h:
                    if hide_points:
                        hide_points = False
                    else:
                        hide_points = True
                if event.key == pygame.K_z:
                    if poligon_points != []:
                        poligon_points.pop()
                if event.key == pygame.K_d:
                    if walls != []:
                          walls.pop()


       
            
        if event.type == pygame.MOUSEBUTTONDOWN and time == 0:
            time += 10
            if pygame.mouse.get_pressed()[2] and len(poligon_points) > 1:
                if len(poligon_points) == 2:
                    pass
                poligons.append(poligon_points)
                convert_poligon_to_walls(poligon_points, walls)
                poligon_points = []
                

            if pygame.mouse.get_pressed()[0] : #LEFT 
                    pos = pygame.mouse.get_pos()

                    poligon_points.append(pos)
            
            
                    

        elif time != 0 : time -= 1
        

        screen.fill(BLACK)

        pos = pygame.mouse.get_pos()

        
        rays = []
        rays_fr_each_wall(walls,rays,pos)
       

        for ray in rays:
            closest = None
            record = float('inf')
            for wall in walls:
                point = ray.cast(pos, wall)
                if point:
                    d = math.dist(pos, point)
                   
                    
                    
                    if d < record:
                        record = d
                        closest = point
                
            if closest:
                ray.distance = d
                rays_to_draw.append([pos,closest])

                
                if  hide_points:
                    if ray_setup_num != 1: size = convert_range(d,0,width,7,4)
                    else: size = 1
                    value = convert_range(d,0,width,250,0)
                    invrt_value = convert_range(d,0,width,0,250)
                    
                    
                    hits.append([(value,5,invrt_value), closest, size])
                   

                   
                ray.define_pos(closest)
        
                    
        
        draw_fill_poligons(rays, screen, pos, LIGHT_COLOR)
        for wall in walls:
            if vis:
               wall.draw(wall_width)
        
        
       
        

        if hide_points:
            rays_to_draw = draw_rays(rays_to_draw,screen, line_width)
            hits = draw_hits(hits, screen)

        #vis before drawing
        if len(poligon_points) > 2:
                pygame.draw.polygon(screen,WHITE,poligon_points,wall_width//2)
        if len(poligon_points) == 2:
            pygame.draw.line(screen,WHITE,poligon_points[0],poligon_points[1],wall_width//2)
        

        s = 6

        for point in poligon_points:
            pygame.draw.circle(screen, OFF_WHITE, point, s)

        seperation = 10
        pygame.draw.circle(screen, WHITE, pos, s)
        


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()