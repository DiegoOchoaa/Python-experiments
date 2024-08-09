import pygame, random, math

import numpy as np

pygame.init()
clock = pygame.time.Clock()

unit = 65

width = 1500
height = 1000
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Flocking")
clock = pygame.time.Clock()




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
def angle(a, b):
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    return math.degrees(angle)
def calc_st(a, length, angle):
    angle = math.radians(angle)
    dx =  length * math.cos(angle)
    dy =  length * math.sin(angle)
    b = [a[0] + dx, a[1] + dy]
    return b


class Boid:
    def __init__(self, pos, vel, pers_rad, max_force, max_speed, color):
        self.pos = pos
        self.velocity = vel
        self.acceleration = [0,0]
        self.pers_rad = pers_rad
        self.max_force = max_force
        self.max_speed = max_speed
        self.facing_angl = 0
        self.color = color
        self.trail = []
        self.p1 = [0,0]
        self.p2 = [0,0]
        self.p3 = [0,0]
    def draw(self):

        #---- get facing angle ----- 
        next_pos = [self.pos[0] + self.velocity[0], self.pos[1] +  self.velocity[1]]
        self.facing_angl =  angle(next_pos, self.pos)
        self.p1 = calc_st(self.pos,18,self.facing_angl+15)
        self.p2 = calc_st(self.pos,18,self.facing_angl-15)
        self.p3 = calc_st(self.pos,13,self.facing_angl)
        pygame.draw.polygon(screen, self.color, [self.pos, self.p1,self.p3, self.p2])

    def draw_trail(self):
        self.trail.append(self.p3)
        for coord in range(len(self.trail)):
             h = coord*1.2
             if h < 17:
                 h = 17
             pygame.draw.circle(screen, (h,h,h), self.trail[coord], 1)
    
        if len(self.trail) > 70:
            self.trail.pop(0)
    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.edges()
        

        # ------ limit ------- 
        if self.velocity[0] > self.max_speed:
                self.velocity[0] = self.max_speed
        if self.velocity[0] < -self.max_speed:
                self.velocity[0] = -self.max_speed

        if self.velocity[1] > self.max_speed:
                self.velocity[1] = self.max_speed
        if self.velocity[1] < -self.max_speed:
                self.velocity[1] = -self.max_speed
    def edges(self):
    
        if self.pos[0] > width:
            self.pos[0] -= width
        if self.pos[0] < 0:
            self.pos[0] += width

        if self.pos[1] > height:
            self.pos[1] -= height
        if self.pos[1] < 0:
            self.pos[1] += height   
    def align(self,boids):

        steering = [0,0]
        total = 0
        for b in range(len(boids)):

            d = distance(self.pos, boids[b].pos)
            if d < self.pers_rad and d != 0:
                steering[0] += boids[b].velocity[0]
                steering[1] += boids[b].velocity[1]
                total += 1

        if total > 0:
            steering[0] = steering[0]/total
            steering[1] = steering[1]/total


            # -------- setting magnitude ----- 
           
            steering = set_magnitude(steering, self.max_speed)
            steering = [steering[0] - self.velocity[0], steering[1] - self.velocity[1]]


            # ------ limit ------- 
            if steering[0] > self.max_force:
                steering[0] = self.max_force
            if steering[0] < -self.max_force:
                steering[0] = -self.max_force

            if steering[1] > self.max_force:
                steering[1] = self.max_force
            if steering[1] < -self.max_force:
                steering[1] = -self.max_force
        
        return steering
    def cohesion(self, boids):
        steering = [0, 0]
        total = 0
        for b in boids:
            d = distance(self.pos, b.pos)
            if d < self.pers_rad and b != self:
                steering[0] += b.pos[0]
                steering[1] += b.pos[1]
                total += 1

        if total > 0:
            steering[0] /= total
            steering[1] /= total

            steering = [steering[0] - self.pos[0], steering[1] - self.pos[1]]
            steering = set_magnitude(steering, self.max_speed)
            steering = [steering[0] - self.velocity[0], steering[1] - self.velocity[1]]

            if magnitude(steering) > self.max_force:
                steering = set_magnitude(steering, self.max_force)

        return steering
    def separation(self, boids):
        steering = [0, 0]
        total = 0
        for other in boids:
            d = distance(self.pos, other.pos)
            if d < self.pers_rad and other != self and d != 0:
                diff = [self.pos[0] - other.pos[0], self.pos[1] - other.pos[1]]
                diff = [diff[0] /d, diff[1] /d]

                steering[0] += diff[0]
                steering[1] += diff[1]
                total += 1

        if total > 0:
            steering[0] /= total
            steering[1] /= total

            steering = set_magnitude(steering, self.max_speed)
            steering = [steering[0] - self.velocity[0], steering[1] - self.velocity[1]]

            if magnitude(steering) > self.max_force:
                steering = set_magnitude(steering, self.max_force)

        return steering  
    def avoid_coordinate(self,predators):
        total = 0
        steering = [0, 0]
        if predators != None:     
            for p in predators:   
                d = distance(self.pos, p)
                if d < 200:

                    diff = [self.pos[0] - p[0], self.pos[1] - p[1]]

                    diff = [diff[0] /d, diff[1] /d]

                    steering[0] += diff[0]
                    steering[1] += diff[1]
                    total += 1

            
            if total > 0:
                steering[0] /= total
                steering[1] /= total

                steering = set_magnitude(steering, self.max_speed)
                steering = [steering[0] - self.velocity[0], steering[1] - self.velocity[1]]

                if magnitude(steering) > self.max_force:
                        steering = set_magnitude(steering, self.max_force)

        return steering  
    def flock(self,boids, mouse):
            self.acceleration = [0,0]
            alignment = self.align(boids)
            cohesion = self.cohesion(boids)
            separation = self.separation(boids)
            avoid = self.avoid_coordinate(mouse)

            self.acceleration = [self.acceleration[0] + alignment[0], self.acceleration[1] + alignment[1]]
            self.acceleration = [self.acceleration[0] + cohesion[0], self.acceleration[1] + cohesion[1]]
            self.acceleration = [self.acceleration[0] + separation[0], self.acceleration[1] + separation[1]]
            #self.acceleration = [self.acceleration[0] + avoid[0], self.acceleration[1] + avoid[1]]
        
class Flock:
    def __init__(self, boids, radious, max_force, max_speed, color):
        self.total_boids = boids
        self.radious = radious
        self.max_force = max_force
        self.max_speed = max_speed
        self.flock_boids = []
        self.color = color
        self.initialize_()
    def initialize_(self):
        for b in range(self.total_boids):
             self.flock_boids.append(Boid([random.randint(0,width),random.randint(0,height)],[random.randint(-10,10),random.randint(-10,10)],self.radious,self.max_force,self.max_speed, self.color))
    
    def update(self, predators):
        for i in self.flock_boids:
            i.update()
            i.draw_trail()
            

        for i in self.flock_boids:
            i.flock(self.flock_boids, predators)
            i.draw()
    def add_boid(self, pos):
         self.flock_boids.append(Boid([pos[0],pos[1]],[random.randint(-10,10),random.randint(-10,10)],self.radious,self.max_force,self.max_speed, self.color))
    
    

            




def main(screen, width, height):
    run = True

    
    fish = Flock(120, 100, 1, 7,  (116,179,184))
   


   
  
    while run:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_SPACE:
                    fish = Flock(120, 100, 1, 7,  (116,179,184))

        
        
        
        fish.update([mouse_pos])

        if pygame.mouse.get_pressed()[0]:
            fish.add_boid(mouse_pos)
        

        
            

  
       

        
        

            
            
       

        pygame.display.update()
                

            
    pygame.quit()



main(screen, width, height)