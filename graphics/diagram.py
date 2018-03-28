import random

class Diagram :
    def __init__(self, draw, width, height, weight) :
        self.draw = draw
        self.width = width
        self.height = height
        self.weight = weight
    
    def draw_triangle(self) :
        x = int(0.1 * self.width + (self.width * 0.4 * random.random()))
        left = (x, self.height)
        right = (self.width - left[0],self.height)
        top = (int(random.random() * self.width),0)
        points = [left, top, right, left]
        
        self.draw.draw_line(points, self.weight)
        
    def draw_circle(self) :
        center = (self.width / 2, self.height / 2)
        min_dim = min(self.width, self.height)
        radius = random.randint(min_dim // 4, min_dim // 3)
        self.draw.draw_circle(center, radius)
        
    def draw_quadrilateral(self) :
        points = []
        zone_x = self.width / 3
        zone_y = self.height / 3
        
        rnd = random.random
        
        points.append((zone_x * rnd(), zone_y * rnd()))
        points.append((self.width - zone_x * rnd(), zone_y * rnd()))
        points.append((self.width - zone_x * rnd(), self.height - zone_y * rnd()))
        points.append((zone_x * rnd(), self.height - zone_y * rnd()))
        
        triangle_line = random.randint(0, 3)
        line = [points[triangle_line], points[(triangle_line + 2) % 4]] 
        
        self.draw.draw_line(line, self.weight)
        
        points.append(points[0])
        self.draw.draw_line(points, self.weight)
        
    
    def draw_cross(self) :
        x_axis = ((0, self.height // 2), (self.width, self.height // 2))
        self.draw.draw_line(x_axis, self.weight)
        
        y_axis = ((self.width // 2, 0), (self.width // 2, self.height))
        self.draw.draw_line(y_axis, self.weight)
        