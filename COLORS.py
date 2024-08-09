import pygame, random, math
import Quadtree
import numpy as np


pygame.init()
clock = pygame.time.Clock()



width = 600
height = 1000
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Quad_tree")
sounds = []
sounds.append(pygame.mixer.Sound("/Users/diegoochoa/Documents/python/Quad_tree/mixkit-catching-a-basketball-ball-2081.wav"))
Load = pygame.mixer.Sound("/Users/diegoochoa/Documents/python/Quad_tree/mixkit-small-metallic-sci-fi-drop-888.wav")

BLACK = (17, 17, 17)
GREY = (40, 40, 40)
WHITE = (255, 255, 255)

def set_magnitude(vector, target_magnitude):
    current_magnitude = np.linalg.norm(vector)
    
    if current_magnitude == 0:
        # Handle the case where the vector is the zero vector
        return np.zeros_like(vector)
    
    normalized_vector = vector / current_magnitude
    scaled_vector = target_magnitude * normalized_vector
    
    return scaled_vector
def magnitude(vector): 
    return math.sqrt(sum(pow(element, 2) for element in vector))
def distance(a,b):
    

    dist = math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return(dist)

class Particle:
    def __init__(self, pos):
        self.pos = pos
        fact = 1
        self.vel = [random.randint(-fact,fact),random.randint(-fact,fact)]
        self.acce = [0,0]
        self.per_radious = 20
        self.draw_r = 4
        self.max_speed = 4
        self.max_force = 1
        self.high = False
        self.hue = 20
    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.vel[0] += self.acce[0]
        self.vel[1] += self.acce[1]
            

            
    def draw(self):
        lightest_blue = 150
        Red = 20

        color = [Red,self.hue, lightest_blue - self.vel[1]]
        for c in range(len(color)):
            if color[c] >= 255:
                color[c] = 255
            elif color[c] <= 0:
                color[c] = 0

        if not self.high:
            pygame.draw.circle(screen, color,  self.pos, self.draw_r)
        else:
            pygame.draw.circle(screen, (30,255,255),  self.pos, self.draw_r)

        
        self.high = False
    
    def intersect(self,other):
        d = distance( self.pos, other.pos)
        return d <= self.per_radious + other.per_radious 
    def active_forces(self, points):
        self.hue = len(points)*13+30


        self.acce = [0,0]
        separ = self.separation(points)
        align = self.align(points)
        self.no_walls()


        self.acce[0] += separ[0]
        self.acce[1] += separ[1]


        self.gravity()

    def gravity(self):
        pass
    
    def no_walls(self):

        

        return_coeficient = 0.97
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.vel[0] *= -return_coeficient
            pygame.mixer.Sound.play(random.choice(sounds))

        elif self.pos[1] < 0:
            self.pos[1] = 0
            self.vel[1] *= -return_coeficient
            pygame.mixer.Sound.play(random.choice(sounds))
            

        elif self.pos[0] > width:
            self.pos[0] = width
            self.vel[0] *= -return_coeficient
            pygame.mixer.Sound.play(random.choice(sounds))
        

        elif self.pos[1] > height:
            self.pos[1] = height
            self.vel[1] *= -return_coeficient
            pygame.mixer.Sound.play(random.choice(sounds))
          
            
            


        
    
    def separation(self, boids):
        steering = [0, 0]
        total = 0
        for other in boids:
            d = distance(self.pos, other.pos)
            if d < 3:
                self.high = True
            if d < self.per_radious and other != self and d != 0:
                diff = [self.pos[0] - other.pos[0], self.pos[1] - other.pos[1]]
                diff = [diff[0] /d, diff[1] /d]

                steering[0] += diff[0]
                steering[1] += diff[1]
                total += 1

        if total > 0:
            steering[0] /= total
            steering[1] /= total

            steering = set_magnitude(steering, self.max_speed)
            steering = [steering[0] - self.vel[0], steering[1] - self.vel[1]]

            if magnitude(steering) > self.max_force:
                steering = set_magnitude(steering, self.max_force)

        return steering 

    def cohesion(self, boids):
        steering = [0, 0]
        total = 0
        for b in boids:
            d = distance(self.pos, b.pos)
            if d < self.per_radious and b != self:
                steering[0] += b.pos[0]
                steering[1] += b.pos[1]
                total += 1

        if total > 0:
            steering[0] /= total
            steering[1] /= total

            steering = [steering[0] - self.pos[0], steering[1] - self.pos[1]]
            steering = set_magnitude(steering, self.max_speed)
            steering = [steering[0] - self.vel[0], steering[1] - self.vel[1]]

            if magnitude(steering) > self.max_force:
                steering = set_magnitude(steering, self.max_force)

        return steering 
    def align(self,boids):

        steering = [0,0]
        total = 0

        for b in range(len(boids)):
       
            d = distance(self.pos, boids[b].User_data.pos)
            if d <= self.per_radious and d != 0:
                steering[0] += boids[b].User_data.vel[0]
                steering[1] += boids[b].User_data.vel[1]
                total += 1

        if total > 0:
            steering[0] = steering[0]/total
            steering[1] = steering[1]/total


            # -------- setting magnitude ----- 
           
            steering = set_magnitude(steering, self.max_speed)
            steering = [steering[0] - self.vel[0], steering[1] - self.vel[1]]


        return steering

        







    


def main(screen, width, height):
    run = True
    speed = None

    


    particles = []
    for n in range(400):
        p = Particle([random.randint(0,width),random.randint(0,height)])
        particles.append(p)
      
  

    while run:
        clock.tick(60)
        print("FPS ",int(clock.get_fps()),"      particles" ,len(particles))
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)

        boundary = Quadtree.Rectangle (0,0,width,height) 
        qt = Quadtree.QuadTree(boundary, 1) 

        if speed != None:
            pygame.draw.line(screen, WHITE, speed, mouse_pos, 1)
        

        for p in particles:

            point = Quadtree.Point(p.pos[0], p.pos[1], p)
            qt.insert(point)
        #qt.show((23,23,23))
        for p in particles:
            p.draw()
            p.move()
        
        
        for p in particles:
            #### fix where they look for each other like look where it fails
            rangee = Quadtree.Rectangle(p.pos[0],p.pos[1],p.per_radious*2,p.per_radious*2)
            #pygame.draw.rect(screen, (50,50,50), [rangee.x - rangee.w/2, rangee.y - rangee.h/2, rangee.w, rangee.h], 1)

            points = qt.query(rangee)
            p.active_forces(points)
           
            
            
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: #MOUSEBUTTONDOWN event o
                if pygame.mouse.get_pressed()[0]:
                    if speed == None:
                        speed = mouse_pos
                    else:
                        p = Particle([mouse_pos[0], mouse_pos[1]])
                        velocity =  [mouse_pos[0] - speed[0],mouse_pos[1] - speed[1]]
                        p.vel = [velocity[0]/5,velocity[1]/5]
                        speed = None
                        particles.append(p)
        
            
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_SPACE:
                    particles = []
                    for n in range(0):
                        p = Particle([random.randint(0,width),random.randint(0,height)])
                        particles.append(p)
                if event.key == pygame.K_UP:
                    for i in range(10):
                        p = Particle([random.randint(0,width),random.randint(0,height)])
                        particles.append(p)
            
          

                    
            
            if pygame.mouse.get_pressed()[2]:
                    if speed == None:
                        speed = mouse_pos
                    else:
                        p = Particle([mouse_pos[0], mouse_pos[1]])
                        velocity =  [mouse_pos[0] - speed[0],mouse_pos[1] - speed[1]]
                        p.vel = [velocity[0],velocity[1]]
                        speed = None
                        particles.append(p)
        
        

        
            
        

      
        pygame.display.update()
                

            
    pygame.quit()

main(screen, width, height)