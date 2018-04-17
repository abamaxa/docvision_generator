import random
from numpy import arange, sin, cos, pi, log10

class Diagram :
    def __init__(self, draw, bounds, weight) :
        self.draw = draw
        self.width = bounds.width
        self.height = bounds.height
        self.x = bounds.x
        self.y = bounds.y
        self.weight = weight
        self.min_x = self.width // 5
        self.max_x = self.width - self.min_x
        self.min_y = 0 #self.height // 5
        self.max_y = self.height - (self.height // 10)         
    
    def render_random(self) :
        for i in range(2) :
           self.__random_object() 
            
    def __random_object(self) :
        foo = random.choice([self.render_triangle, self.render_cross, 
                                     self.render_quadrilateral, self.render_circle])
        foo()
        
    def render_triangle(self) :
        width = self.max_x - self.min_x
        
        x = self.min_x + int(width * 0.2 * random.random())
        left = (x, self.max_y)
        right = (self.width - left[0], self.max_y)
        top = (random.randint(self.min_x, self.max_x),self.min_y)
        points = self.__offset_points([left, top, right, left])
        
        self.draw.draw_line(points, self.weight)
        
        if random.random() < 0.3 :
            self.__random_object()
        
    def render_circle(self) :
        center = [(self.width / 2, self.height / 2)]
        center = self.__offset_points(center)
        min_dim = min(self.width, self.height)
        radius = random.randint(min_dim // 3, min_dim // 2.4)
        self.draw.draw_circle(center[0], radius)
        
        if random.random() < 0.4 :
            self.__random_object()     
        else :
            self.__render_axis()
        
    def render_quadrilateral(self) :
        points = []
        width = self.max_x - self.min_x
        height = self.max_y - self.min_y
        zone_x = width / 3
        zone_y = height / 3
        
        rnd = random.random
        
        points.append((self.min_x + zone_x * rnd(), self.min_y + zone_y * rnd()))
        points.append((self.max_x - zone_x * rnd(), self.min_y + zone_y * rnd()))
        points.append((self.max_x - zone_x * rnd(), self.max_y - zone_y * rnd()))
        points.append((self.min_x + zone_x * rnd(), self.max_y - zone_y * rnd()))
        
        if rnd() > 0.5 :
            rectangle = (points[0], points[2])
            self.draw.draw_rectangle(self.__offset_points(rectangle))
            if rnd() < 0.5 :
                self.draw.draw_line(self.__offset_points(rectangle), self.weight)
            if rnd() < 0.5 :
                self.draw.draw_line(self.__offset_points((points[1], points[3])), self.weight)            
        else :
            triangle_line = random.randint(0, 3)
            line = [points[triangle_line], points[(triangle_line + 2) % 4]]     
            self.draw.draw_line(self.__offset_points(line), self.weight)
            
            points.append(points[0])
            self.draw.draw_line(self.__offset_points(points), self.weight)
        
        if random.random() < 0.3 :
            self.render_triangle()        
            
    def render_cross(self) :
        self.__render_axis()
        self.plot_random_points()
        
    def plot_random_points(self) :
        r = random.random()
        if r < 0.4 :
            self.__render_function(lambda x_points:sin((0.5 + random.random())*x_points*pi))
        elif r < 0.8 :
            self.__render_function(lambda x_points:((random.random() * -3) * x_points * x_points) + random.random())
        else :
            self.__render_diagonal()
            
    def __render_axis(self) :
        r = random.random()
        if r < 0.33 :
            x_axis = ((self.min_x, self.height // 2), (self.max_x, self.height // 2))
            y_axis = ((self.width // 2, self.min_y), (self.width // 2, self.max_y))
            
        elif r < 0.66 :
            x_axis = ((self.min_x, self.max_y), (self.max_x, self.max_y))
            y_axis = ((self.width // 2, self.min_y), (self.width // 2, self.max_y))
            
        else :
            x_axis = ((self.min_x, self.max_y), (self.max_x, self.max_y))
            y_axis = ((self.min_x, self.max_y), (self.min_x, self.min_y))
            
        self.draw.draw_line(self.__offset_points(y_axis), self.weight)
        self.draw.draw_line(self.__offset_points(x_axis), self.weight)        
            
    def __render_function(self, foo) :
        x_low = -1.0
        x_high = 1.0
        
        x_points = arange(x_low, x_high, 0.02)
        y_points = foo(x_points)
        
        xscale = (self.max_x - self.min_x)
        yscale = (self.max_y - self.min_y) * 0.4
        
        y_points *= yscale
        x_points *= (xscale / (x_high - x_low))
        
        y_points += self.min_y + ((self.max_y - self.min_y) / 2)
        x_points += self.min_x + (self.max_x - self.min_x) / (x_high - x_low)
                
        points = self.__points_on_diagram([(x,y) for x,y in zip(x_points, y_points)])
        self.draw.draw_line(self.__offset_points(points),  self.weight)
        
    def __points_on_diagram(self, points) :
        return [(x,y) for x,y in points if x >= self.min_x and x <= self.max_x
            and y >= self.min_y and y <= self.max_y]
        
    def __render_diagonal(self) :
        y1 = random.randint(2 * self.height // 3, self.max_y)
        y2 = random.randint(self.min_y, self.height // 3) 
        
        if random.random() < 0.5 :
            points = ((self.min_x, y1), (self.max_x, y2))
        else :
            points = ((self.min_x, y2), (self.max_x, y1))     
            
        self.draw.draw_line(self.__offset_points(points))
                            
    def __offset_points(self, points) :
        return [(p[0] + self.x, p[1] + self.y) for p in points]
        