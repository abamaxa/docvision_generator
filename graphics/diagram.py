import random

class Diagram :
    def __init__(self, draw, bounds, weight) :
        self.draw = draw
        self.width = bounds.width
        self.height = bounds.height
        self.x = bounds.x
        self.y = bounds.y
        self.weight = weight
    
    def render_triangle(self) :
        x = int((0.1 * self.width) + (self.width * 0.2 * random.random()))
        left = (x, self.height)
        right = (self.width - left[0],self.height)
        top = (int(random.random() * self.width),0)
        points = self.__offset_points([left, top, right, left])
        
        self.draw.draw_line(points, self.weight)
        
    def render_circle(self) :
        center = [(self.width / 2, self.height / 2)]
        center = self.__offset_points(center)
        min_dim = min(self.width, self.height)
        radius = random.randint(min_dim // 3, min_dim // 2.4)
        self.draw.draw_circle(center[0], radius)
        
    def render_quadrilateral(self) :
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
        
        self.draw.draw_line(self.__offset_points(line), self.weight)
        
        points.append(points[0])
        self.draw.draw_line(self.__offset_points(points), self.weight)
            
    def render_cross(self) :
        min_x = self.width // 5
        max_x = self.width - min_x
        min_y = self.height // 5
        max_y = self.height - min_y      
        
        x_axis = ((min_x, self.height // 2), (max_x, self.height // 2))
        self.draw.draw_line(self.__offset_points(x_axis), self.weight)
        
        y_axis = ((self.width // 2, min_y), (self.width // 2, max_y))
        self.draw.draw_line(self.__offset_points(y_axis), self.weight)
        
        y1 = random.randint(2 * self.height // 3, max_y)
        y2 = random.randint(min_y, self.height // 3) 
        
        if random.random() < 0.5 :
            points = ((min_x, y1), (max_x, y2))
        else :
            points = ((min_x, y2), (max_x, y1))
            
        self.draw.draw_line(self.__offset_points(points))
                            
    def __offset_points(self, points) :
        return [(p[0] + self.x, p[1] + self.y) for p in points]
        