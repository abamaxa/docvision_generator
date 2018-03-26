from abc import abstractmethod

class Object(object) :
    def __init__(self) :
        self._counter = 0
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False    
        
    def __iter__(self):
        self._counter = 0
        return self    
    
    def __next__(self):
        return self.next()        
    
    @abstractmethod
    def next(self):
        raise StopIteration


class Size(Object) :
    def __init__(self, width = None, height = None) :
        super().__init__()
        self._width = width
        self._height = height
        
    @property
    def width(self) :
        return self._width
    
    @property
    def height(self) :
        return self._height
    
    def __repr__(self) :
        return "Width: {} Height: {}".format(self.width, self.height)
    
    def next(self):
        self._counter += 1
        if self._counter == 1 :
            return self._width
        elif self._counter == 2 :
            return self._height
        raise StopIteration    
    
class Origin(Object) :
    def __init__(self, x = None, y = None) :
        super().__init__()
        self._x = x
        self._y = y
        
    @property
    def x(self) :
        return self._x
    
    @property
    def y(self) :
        return self._y 
    
    def __repr__(self) :
        return "x: {} y: {}".format(self.x, self.y)    
    
    def next(self):
        self._counter += 1
        if self._counter == 1 :
            return self._x
        elif self._counter == 2 :
            return self._y
        raise StopIteration        
           
   
class Bounds(Object) :
    def __init__(self, x = None, y = None, width = None, height = None, x2 = None, y2 = None) :
        super().__init__()
        self._origin = Origin(x, y)
        if not width is None and not height is None :
            self._size = Size(width, height)
        elif not x2 is None and not y2 is None and not x is None and not y is None :
            self._size = Size(x2 - x, y2 - y)
        else :
            self._size = Size(0, 0)
            
    @property
    def size(self) :
        return self._size
    
    @property
    def origin(self) :
        return self._origin    
    
    @property
    def x(self) :
        return self._origin.x
    
    @property
    def y(self) :
        return self._origin.y     
    
    @property
    def x2(self) :
        return self.x + self.width
    
    @property
    def y2(self) :
        return self.y + self.height
    
    @property
    def width(self) :
        return self._size.width
    
    @property
    def height(self) :
        return self._size.height   
    
    #@property
    #def rectangle(self) :
    #    return (self.x, self.y, self.x2, self.y2)
    
    def inflate(self, inflate_by_x, inflate_by_y):
        return Bounds(self.x - inflate_by_x,
                      self.y - inflate_by_y,
                      self.width + inflate_by_x + inflate_by_x,
                      self.height + inflate_by_y + inflate_by_y)
    
    def scale(self, xscale, yscale):
        return Bounds(self.x * xscale,
                      self.y * yscale,
                      self.width * xscale,
                      self.height * yscale)
    
    def move_to(self, x, y):    
        self._origin = Origin(x, y)    
    
    def move(self, xoffset, yoffset):    
        return Bounds(self.x + xoffset,
                      self.y + yoffset,
                      self.width, self.height)        
    
    def enclosed_by_bounds(self, bounds):
        return (
            (self.x >= bounds.x) and
            (self.x <= bounds.x2) and
            (self.x2 >= bounds.x) and
            (self.x2 <= bounds.x2) and
            (self.y >= bounds.y) and
            (self.y <= bounds.y2) and
            (self.y2 >= bounds.y) and
            (self.y2 <= bounds.y2)
        )
    
    @staticmethod
    def __overlap(bounds, bounds2) :
        return  (
            ((bounds.x >= bounds2.x) and
             (bounds.x <= bounds2.x2)) or
            ((bounds.x2 >= bounds2.x) and
             (bounds.x2 <= bounds2.x2)) or
            ((bounds.y >= bounds2.y) and
             (bounds.y <= bounds2.y2)) or
            ((bounds.y2 >= bounds2.y) and
             (bounds.y2 <= bounds2.y2))
        )
    
    def overlap_bounds(self, bounds):
        return Bounds.__overlap(self, bounds) or Bounds.__overlap(bounds, self)
    
    def __repr__(self) :
        return "{} {}".format(str(self._origin), str(self._size))    
    
    #def next(self):
        #self._counter += 1
        #if self._counter == 1 :
            #return self._origin
        #elif self._counter == 2 :
            #return self._size
        #raise StopIteration  
    
    def next(self):
        self._counter += 1
        if self._counter == 1 :
            return (self.x, self.y)
        elif self._counter == 2 :
            return (self.x2, self.y)
        elif self._counter == 3 :
            return (self.x2, self.y2)
        elif self._counter == 4 :
            return (self.x, self.y2)
        elif self._counter == 5 :
            return (self.x, self.y)
        
        raise StopIteration       