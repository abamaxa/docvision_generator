from .bounds import Bounds

class Frame(Bounds) :
    def __init__(self, bounds, label = None) :
        super().__init__(bounds.x,bounds.y,bounds.width,bounds.height)
        if isinstance(bounds, Frame) :
            self._label = bounds.label
        else :
            self._label = label
        
    @property
    def label(self) : return self._label
        
    def as_dict(self) :
        return {"xmin":self.x,"ymin":self.y,"xmax":self.x2,"ymax":self.y2,"label":self._label}
    
    def set_from_dict(self, values) :
        self._label = values.get("label", self._label)
        self._x = values.get("xmin", self._x)
        self._y = values.get("ymin", self._y)
        
        if not values.get("xmax") is None :
            self._width = values.get("xmax") - self.x
            
        if not values.get("ymax") is None :
            self._height = values.get("ymax") - self.y  
            
    def move_to(self, x, y):   
        return Frame(super().move_to(x, y), self.label)
    
    def move(self, offsetx, offsety):   
        return Frame(super().move(offsetx, offsety), self.label)    
    
    def scale(self, xscale, yscale):   
        return Frame(super().scale(xscale, yscale), self.label)    
            
    def normal_center_x(self, width) :
        return (self.x / width) + self.normal_width(width)
            
    def normal_center_y(self, height) :
        return (self.y / height) + self.normal_height(height) 

    def normal_width(self, width) :
        return (self.width / width) 
    
    def normal_height(self, height) :
        return (self.height / height)
        
    def __repr__(self) :
        return "class: {} {} {}".format(self._label, str(self._origin), str(self._size))      