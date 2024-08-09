import pygame, random, math
import numpy as np



pygame.init()
clock = pygame.time.Clock()



width = 1000
height = 1000
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Soft bodies")
clock = pygame.time.Clock()


BLACK = (25, 25, 25)
GREY = (40, 40, 40)
WHITE = (255, 255, 255)
RED = (255,0,0)
BLUE = (7, 178, 245)

FPS = 60
G = (0,0)

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def get_angle(p1, p2):
   return  math.atan2(p2[1] - p1[1] , p2[0] - p1[0])


class Shell:
    def __init__(self, points,influence):
        self.points = points
        self.center = self.calculate_center()
        self.influence  = influence
        self.shadow_point_lenght = 5
        self.shadow_points, self.internal_springs = self.create_shadow()

    def calculate_center(self):
        x_sum = 0
        y_sum = 0

        for p in self.points:
            for particle in p:
                x_sum += particle.pos[0]
                y_sum += particle.pos[1]

        return x_sum / (len(self.points)*len(self.points)), y_sum / (len(self.points)*len(self.points))

    def update(self):
        #new_center = self.calculate_center()
        #dx = new_center[0] - self.center[0]
        #dy = new_center[1] - self.center[1]

        #for shadow_point in self.shadow_points:
        #    shadow_point.pos[0] += dx
        #    shadow_point.pos[1] += dy

        #self.center = new_center

        #angle = self.get_average_angle()
        #self.rotate_shadow(angle)
        #print(angle)
     

        for spring in self.internal_springs:
            spring.update()
            spring.draw()
        


    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.center[0]), int(self.center[1])), 7)
        for shadow_point in self.shadow_points:
            pygame.draw.circle(screen, WHITE, (int(shadow_point.pos[0]), int(shadow_point.pos[1])), 7)



    def rotate_shadow(self, angle):
        for point in self.shadow_points:
            vector = point.pos
            center_point = self.center

            angle_radians = math.radians(angle)

            relative_x = vector[0] - center_point[0]
            relative_y = vector[1] - center_point[1]

            rotated_x = relative_x * math.cos(angle_radians) - relative_y * math.sin(angle_radians)
            rotated_y = relative_x * math.sin(angle_radians) + relative_y * math.cos(angle_radians)

            final_x = rotated_x + center_point[0]
            final_y = rotated_y + center_point[1]

            point.pos = [final_x, final_y]

            


    def get_average_angle(self):
        angle = 0
        
        for point in range(len(self.points)):
            
            A = self.shadow_points[point].pos
            B = self.points[point].pos
            C = self.center
            

            V1 = [A[0] - C[0], A[1] - C[1]]
            V2 = [B[0] - C[0], B[1] - C[1]]
            
            theta_radians = np.arctan2(V2[1], V2[0]) - np.arctan2(V1[1], V1[0])
            


            theta_degrees = np.degrees(theta_radians)


           #pygame.draw.line(screen, WHITE, A, B, 4)
            angle += theta_degrees

        angle = angle//len(self.points)
        
            


        return angle//3






    def create_shadow(self):
        s_p = []
        internal_springs = []
        for p in self.points:
            for point in p:
                dx = point.pos[0] - self.center[0]
                dy = point.pos[1] - self.center[1]
                shadow_x = self.center[0] + dx
                shadow_y = self.center[1] + dy
                particle = Particle(shadow_x, shadow_y, 10)
                particle.lock()
                s_p.append(particle)
                spring = Spring(self.influence, self.shadow_point_lenght, point, particle)
                internal_springs.append(spring)
                spring.make_shell()


        return s_p, internal_springs

        


class Spring:
    def __init__(self, k, rest_lenght, a, b):
        self.x = False
        self.shell = False
        self.k = k
        self.len = 100
        self.rl = rest_lenght
        self.a = a
        self.b = b
        self.vector = [0,0]
        self.color = False
     
    def make_shell(self):
        self.shell = True
    def update(self):
   
        x = np.array(self.b.pos) - np.array(self.a.pos)
        
        self.len = np.linalg.norm(x)
 

        

        if self.len != 0 :
            direction = x / self.len
            spring_force = self.k * (self.len - self.rl) * direction
            
            
            self.a.apply_force(spring_force)
            self.b.apply_force(-spring_force)
          

        
        
    def draw(self):
       if not self.x:
            if self.len > 255:
                self.len = 255
            if self.color == False:
                color = (140, self.len, 252)
            else:
                color = RED
            if not self.shell:
                pygame.draw.line(screen, color,self.b.pos,self.a.pos,3)
            
            self.a.len,  self.b.len  = self.len, self.len

    def calculate_dist_to_point(self):
        vector = ( self.b.pos[0] - self.a.pos[0], self.b.pos[1] - self.a.pos[1] )
        distance = math.sqrt(vector[0]**2 + vector[1] **2 )
       
        return distance
    
  

                
               
               
               
                
             
          


class Particle:
    def __init__(self, x, y, rl):
        self.color = None
        self.rest_lenght = rl
        self.locked = False
        self.radious = self.rest_lenght // 2.4
        self.pos = [x, y]  # Use a list for position
        self.velocity = [0, 0]  # Use a list for velocity
        self.mass = 1
        self.origin = self.pos
        self.len = 20
        
    def draw(self):
        if self.color == None:
            self.color = (120, self.len, 252)


        pygame.draw.circle(screen,self.color,(self.pos[0],self.pos[1]),5)
        pygame.draw.circle(screen,self.color,(self.pos[0],self.pos[1]),self.radious,1)


        if self.color == (120, self.len, 252):
            self.color = None
       

    def update(self):
         bounce_back = 0.5
         self.velocity  += G
         self.pos += self.velocity
         self.velocity *= 0.95
         
        
    def apply_force(self, Force):
        if not self.locked:
            self.velocity  += Force
            self.update()
    def lock(self):
        self.locked = True
        self.color = BLUE
    def unlock(self):
        self.locked = False
        self.color = None
    def is_locked(self):
        return self.locked == True


def make_grid(g_numx,gnumy,k,spacing):
    particles = []
    springs = []
    for i in range (g_numx):
        particles.append([])
        for j in range(gnumy):
            particles[i].append(Particle(i*spacing,j*spacing,spacing))

    #vertical
    for i in range(g_numx):
        for j in range(gnumy-1):
            springs.append(Spring(k,spacing,particles[i][j],particles[i][j+1]))


    for i in range(g_numx-1):
        for j in range(gnumy):
                springs.append(Spring(k,spacing,particles[i][j],particles[i+1][j]))

    
  
    for i in range(g_numx - 1):
        for j in range(gnumy - 1):
            p1 = particles[i][j]
            p2 = particles[i + 1][j + 1]
            s = Spring(k, spacing, p1, p2)
            springs.append(s)
            s.x = True

            p1 = particles[i][j + 1]
            p2 = particles[i + 1][j]
            s = Spring(k, spacing, p1, p2)
            springs.append(s)
            s.x = True



    for i in particles[0]:
        i.lock()
    for i in particles[g_numx-1]:
        i.lock()
    
    for i in range(g_numx):
        particles[i][0].lock()  # Lock the bottom row
        particles[i][gnumy - 1].lock()  # Lock the top row
    
            


    return springs, particles
            
            
            


def find_closest_point(points, point):
    closest = None
    min_distance = float('inf')
    for po in points:
          for p in po:
            distance = np.linalg.norm(np.array(p.pos) - np.array(point))

            if distance < min_distance:
                        min_distance = distance
                        closest = p
    return closest

def main(screen, width):
    print('selfcolllision still does not work help and add collision detection with other objects')
    run = True
    grabbed = None
    grabbed2 = None
    run = True
    k = 0.05
    spacing = 25
    g_numy = int(height/spacing)  + 1
    g_numx = int(width/spacing)  + 1
    springs, particles = make_grid(g_numx, g_numy,k,spacing)
 
    
  
       


    while run:
        clock.tick(FPS)
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_SPACE:
                    for i in particles:
                        for p in i:
                             #p.unlock()
                             pass
                if event.key == pygame.K_r:
                    for i in particles:
                        springs, particles = make_grid(g_numx, g_numy,k,spacing)
                    
                        

        if pygame.mouse.get_pressed()[0]: 
                mouse_pos = pygame.mouse.get_pos()
           
                if not grabbed:
                    grabbed = find_closest_point(particles,mouse_pos)
                if not grabbed.locked:
                    grabbed.pos = mouse_pos
                    grabbed.velocity = [0,0]
        else:
            grabbed = None
        if pygame.mouse.get_pressed()[2]: 
            mouse_pos = pygame.mouse.get_pos()
           
            if not grabbed2:
                    grabbed2 = find_closest_point(particles,mouse_pos)
            if not grabbed2.locked:
                    dir_vec = grabbed2.origin[0] - mouse_pos[0], grabbed2.origin[1] - mouse_pos[1]
                    print(dir_vec)
                    grabbed2.pos = mouse_pos
                    grabbed2.velocity = [-dir_vec[0],-dir_vec[1]]
        else:
                grabbed2 = None
       

        
        for spring in springs: 
            spring.draw()
            spring.update()
        for particle in particles:
            for p in particle:
                pass
            
      
        
       
            

        pygame.display.update()
                

            
    pygame.quit()



main(screen, width)