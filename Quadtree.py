import pygame, random, math




pygame.init()
clock = pygame.time.Clock()



width = 900
height = 900
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Quad_tree")

BLACK = (17, 17, 17)
GREY = (40, 40, 40)
WHITE = (255, 255, 255)

def distance(a,b):
    

    dist = math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return(dist)

class Point:
    def __init__(self, x, y, User_data):
        self.x = x
        self.y = y
        self.User_data = User_data
        self.pos = [self.x,self.y]
    def show(self):
        pygame.draw.circle(screen, WHITE, [self.x, self.y], 2)


class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.rsquared = self.r*self.r
    def contains(self, point):
        d = distance([self.x, self.y], [point.x, point.y])
        return d <= self.rsquared
    def intersects(self, rangee):
        x_d = math.abs(rangee.x - self.x)
        y_d = math.abs(rangee.y - self.y)

        r = self.r
        w = rangee.w
        h = rangee.h

        edges = math.pow((x_d - w), 2) + math.pow((y_d - h), 2)

        if x_d > (r+w) or y_d > (r+h):
            return False
        if x_d <= w or y_d <= h:
            return True
        
        return edges <= self.rsquared
        

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def contains(self, point):
        a = point.x >= self.x - self.w
        b = point.x <= self.x + self.w
        c = point.y >= self.y - self.h
        d = point.y <= self.y + self.h
        return a and b and c and d
    
    def intersect(self, range):
        a = self.x - self.w > range.x + range.w
        b = self.x + self.w < range.x - range.w
        c = self.y - self.h > range.y + range.h
        d = self.y + self.h < range.y - range.h
        return not (a or b or c or d)


class QuadTree:
    def __init__(self, boundary, n):
        self.boundary = boundary
        self.capacity = n
        self.points = []
        self.subdivided = False

    def query(self, range):
        found = []
        if not self.boundary.intersect(range):
            # empty list
            return found
        else:
            for p in self.points:
                if range.contains(p):
                    found.append(p)
        
        if self.subdivided:
            found = found + (self.northwest.query(range))
            found = found + (self.northeast.query(range))
            found = found + (self.southwest.query(range))
            found = found + (self.southeast.query(range))
        return found

            

    def show(self, color):

        pygame.draw.rect(screen, color, [self.boundary.x - self.boundary.w, self.boundary.y - self.boundary.h, self.boundary.w*2, self.boundary.h*2], 1)
        if self.subdivided:
            self.northwest.show(color)
            self.northeast.show(color)
            self.southwest.show(color)
            self.southeast.show(color)
        

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.subdivided:
                self.subdivide()

            if  self.northwest.insert(point):
                return True
            elif self.northeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True
            elif self.southeast.insert(point):
                return True

    def subdivide(self):
        self.subdivided = True
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        ne = Rectangle(x + w/2, y - h/2, w/2, h/2)
        self.northeast = QuadTree(ne, self.capacity)
        nw = Rectangle(x - w/2, y - h/2, w/2, h/2)
        self.northwest = QuadTree(nw, self.capacity)
        se = Rectangle(x + w/2, y + h/2, w/2, h/2)
        self.southeast = QuadTree(se, self.capacity)
        sw = Rectangle(x - w/2, y + h/2, w/2, h/2)
        self.southwest = QuadTree(sw, self.capacity)



def main(screen, width, height):
    run = True
    
    boundary = Rectangle (0,0,width,height) 
    qt = QuadTree(boundary, 1)  

    for i in range(1000):
            p = Point(random.randint(0,width), random.randint(0,height), None)
            qt.insert(p)
            
    size = 100
    search  =  Rectangle(200, 100, size, size)

    while run:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)
        
        

        qt.show((100,100,100))
        
        points = qt.query(search)
        
        pygame.draw.rect(screen, (len(points),10,240), [search.x - size , search.y - size, size*2, size*2], 2)

        
        for p in points:
            pygame.draw.circle(screen, (len(points),10,240), [p.x,p.y],3)


        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
        
        search.x = mouse_pos[0]
        search.y = mouse_pos[1]

        if pygame.mouse.get_pressed()[0]:
            

            for i in range(1):
                sp = 10
                m = Point(mouse_pos[0] + random.randint(-sp, sp), mouse_pos[1]+  random.randint(-sp, sp), None)
                qt.insert(m)
            

      
        pygame.display.update()
                

            
    pygame.quit()



#main(screen, width, height)