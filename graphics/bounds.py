class Object(object) :
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False    

class Size(Object) :
    def __init__(self, width = None, height = None) :
        self._width = width
        self._height = height
        
    @property
    def width(self) :
        return self._width
    
    @property
    def height(self) :
        return self._height
    
    @property
    def as_tuple(self) :
        return (self.width, self.height)
    
    def __repr__(self) :
        return "Width: {} Height: {}".format(self.width, self.height)
    
class Origin(Object) :
    def __init__(self, x = None, y = None) :
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
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False    
   
class Bounds(Object) :
    def __init__(self, x = None, y = None, width = None, height = None) :
        self._origin = Origin(x, y)
        self._size = Size(width, height)
        
    @property
    def size(self) :
        return self._size
    
    @property
    def origin(self) :
        return self._origin    
    
    @property
    def width(self) :
        return self._size.width
    
    @property
    def height(self) :
        return self._size.height   
    
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
    
    def move(self, xoffset, yoffset):
        #xoffset = offset[0]
        #yoffset = offset[1]
    
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
    
    
    