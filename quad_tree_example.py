import pygame, random, math
import Quadtree
import numpy as np


pygame.init()
clock = pygame.time.Clock()



width = 900
height = 900
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Quad_tree")

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
    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.vel[0] += self.acce[0]
        self.vel[1] += self.acce[1]
            

            
    def draw(self):
        if not self.high:
            pygame.draw.circle(screen, (100,100,100),  self.pos, self.draw_r)
        else:
            pygame.draw.circle(screen, WHITE,  self.pos, self.draw_r)

        #pygame.draw.circle(screen, (40,40,40),  self.pos, self.per_radious, 1
        self.high = False
    
    def intersect(self,other):
        d = distance( self.pos, other.pos)
        return d <= self.per_radious + other.per_radious 
    def bounce(self, points):
        self.acce = [0,0]
        cohe = self.cohesion(points)
        separ = self.separation(points)
        align = self.align(points)
        walls = self.no_walls(points)

        #self.acce[0] += cohe[0]
        #self.acce[1] += cohe[1]

        self.acce[0] += separ[0]
        self.acce[1] += separ[1]

        self.acce[0] += walls[0]
        self.acce[1] += walls[1]

        #self.acce[0] += align[0]
        #self.acce[1] += align[1]

    def no_walls(self, boids):
        steering = [0, 0]
        total = 0

        sensibility = self.per_radious
        divide = 6

        if self.pos[0] < sensibility:
            steering[0] += self.pos[0]/divide
        if self.pos[1] < sensibility:
            steering[1] += self.pos[1]/divide
        if self.pos[0] > width - sensibility:
            steering[0] -= (width - self.pos[0])/divide
        if self.pos[1] > width - sensibility:
            steering[1] -= (width - self.pos[1])/divide
            
            


        if total > 0:
            steering[0] /= total
            steering[1] /= total

            steering = set_magnitude(steering, self.max_speed)
            steering = [steering[0] - self.vel[0], steering[1] - self.vel[1]]

            if magnitude(steering) > self.max_force:
                steering = set_magnitude(steering, self.max_force)

        return steering 
        
    
    def separation(self, boids):
        steering = [0, 0]
        total = 0
        for other in boids:
            d = distance(self.pos, other.pos)
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

    


    particles = []
    for n in range(500):
        p = Particle([random.randint(0,width),random.randint(0,height)])
        particles.append(p)
      
  

    while run:
        clock.tick(60)
        print(int(clock.get_fps()))
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)

        boundary = Quadtree.Rectangle (0,0,width,height) 
        qt = Quadtree.QuadTree(boundary, 1) 
        
        
        

        for p in particles:

            point = Quadtree.Point(p.pos[0], p.pos[1], p)
            qt.insert(point)

        qt.show((40,40,40))
            
        for p in particles:
            p.draw()
            p.move()
        
        
        for p in particles:
         
            rangee = Quadtree.Rectangle(p.pos[0],p.pos[1],p.per_radious*2,p.per_radious*2)
            #pygame.draw.rect(screen, (50,50,50), [rangee.x - rangee.w/2, rangee.y - rangee.h/2, rangee.w, rangee.h], 1)

            points = qt.query(rangee)
            p.bounce(points)
            if len(points) != 1:
                p.high = True
            
            
            

                
                    

        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_SPACE:
                    pass

        if pygame.mouse.get_pressed()[0]:
            p = Particle([mouse_pos[0], mouse_pos[1]])
            particles.append(p)
            
        

      
        pygame.display.update()
                

            
    pygame.quit()

main(screen, width, height)