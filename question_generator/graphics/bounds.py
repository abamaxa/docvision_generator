
class Bounds(object) :
    def __init(self, x = None, y = None, width = None, height = None) :
        self._offset = (x, y)
        self._size = (width, height)
        
    @property
    def size(self) :
        return self._size
    
    @property
    def offset(self) :
        return self._offset    
    
    @property
    def width(self) :
        return self._size[0]
    
    @property
    def height(self) :
        return self._size[1]    
    
    @property
    def x(self) :
        return self._offset[0]
    
    @property
    def y(self) :
        return self._offset[1]       
    
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
    
    def offset(self, offset):
        xoffset = offset[0]
        yoffset = offset[1]
    
        return Bounds(self.x - xoffset,
                      self.y - yoffset,
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
    
    def overlap_bounds(self, bounds):
        return (
            ((self.x >= bounds.x) and
             (self.x <= bounds.x2)) or
            ((self.x2 >= bounds.x) and
             (self.x2 <= bounds.x2)) or
            ((self.y >= bounds.y) and
             (self.y <= bounds.y2)) or
            ((self.y2 >= bounds.y) and
             (self.y2 <= bounds.y2))
        )
    
    
    