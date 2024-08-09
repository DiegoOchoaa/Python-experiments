import pygame 
import math, random







###CHANGES

#make two balls go around each other

##draw a trace

pygame.init 

WIDTH, HEIGHT = 1000, 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption
clock = pygame.time.Clock()

WHITE = (255,255,255)
RED  = (255,0,0)

MASS = 100
SHIP_MASS = 1
FPS = 69
TAIL_LEN = 500
OBJ_SIZE = 5
VEL_SCALE = 300

class static_body:
     def __init__(self,x,y,mass):
        self.x = x 
        self.y = y
        self.mass = mass
     def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x),int(self.y)), self.mass*2)

class Body:
    def __init__(self,x,y,velx,vely,mass):
        self.x = x 
        self.y = y
        self.mass = mass
        self.velx = velx
        self.vely = vely
        self.tail = []
        self.tail_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    def move(self, otherbody,G):
        self.tail.append([self.x,self.y])
        distance = math.sqrt((self.x- otherbody.x)**2 + (self.y - otherbody.y)**2)
        if distance == 0:
            print(distance)
        force = (G *self.mass * otherbody.mass)/ distance
        acceleration = force/ self.mass
        angle = math.atan2(otherbody.y - self.y, otherbody.x - self.x)

        acceleration_x =  acceleration * math.cos(angle)
        acceleration_y =  acceleration * math.sin(angle)

        self.velx += acceleration_x
        self.vely += acceleration_y


        self.x += self.velx
        self.y += self.vely
    
    def draw(self):
        for mark in range(len(self.tail)-1):
            pygame.draw.line(screen,self.tail_color, self.tail[mark],self.tail[mark+1])

        pygame.draw.circle(screen, self.tail_color, (int(self.x),int(self.y)), OBJ_SIZE)
        while len(self.tail) >= TAIL_LEN:
            self.tail.remove(self.tail[0])


def cerate_ship(Location, Mouse):
    t_x, t_y = Location
    m_x, m_y = Mouse
    vel_x = (m_x - t_x)/VEL_SCALE
    vel_y = (m_y - t_y)/VEL_SCALE
    obj = Body(t_x,t_y,vel_x,vel_y, SHIP_MASS)
    return obj

def main():
    running = True
    g = 1
    

    initial_velocity = 0.1
    objects = []
    objects.append(Body(100,100,initial_velocity,initial_velocity,5))
    objects.append(Body(WIDTH-100,HEIGHT-100,-initial_velocity,-initial_velocity,5))
    temp_obj_pos = None
    static_bodys = []

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_SPACE:
                    static_bodys = []
                    objects = []
                
            if pygame.mouse.get_pressed()[2]: 
                static_bodys.append(static_body(mouse_pos[0],mouse_pos[1],5))
            if pygame.mouse.get_pressed()[0]: 
                if temp_obj_pos:
                    
                    obj = cerate_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                    
                else:
                    temp_obj_pos = mouse_pos
        screen.fill((30,30,30))

        if temp_obj_pos:
            pygame.draw.line(screen,WHITE,temp_obj_pos,mouse_pos,2)
            pygame.draw.circle(screen,(255,0,0),temp_obj_pos,OBJ_SIZE)
        
       
      
        for i in static_bodys:
            i.draw()
        
        for obj in range(len(objects)):


            
            objects[obj].draw()
            for obj2 in range(len(objects)):
                if obj != obj2:
                     objects[obj].move(objects[obj2],g)
            for static in static_bodys:
                 objects[obj].move(static,g)

            
       

            
        





        pygame.display.update()
        

    pygame.quit()



main()