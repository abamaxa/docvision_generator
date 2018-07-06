from .bounds import Bounds, DimensionObject

class Frame(Bounds) :
    def __init__(self, bounds, label = None) :
        super().__init__(bounds.x, bounds.y, bounds.width, bounds.height)
        if isinstance(bounds, Frame) :
            self._label = bounds.label
        else :
            self._label = label
        
    @property
    def label(self) : return self._label
        
    def as_dict(self) :
        return {"xmin":self.x,"ymin":self.y,
                "xmax":self.x2,"ymax":self.y2,
                "label":self._label,"type": "box"}
    
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
    
    def within_image(self, width, height) :
        return self._x >= 0 and self._y >= 0 and \
               self.normal_width(width) <= 1 and self.normal_height(height) <= 1
        
    def __repr__(self) :
        return "class: {} {} {}".format(self._label, str(self._origin), str(self._size))      
    
class RotatedFrame(DimensionObject) :
    def __init__(self, points, label) :
        self.points = points
        self._label = label
        
    @property
    def label(self) : return self._label 
    
    @property
    def bounds(self) :
        x = self.points[::2]
        y = self.points[1::2]
        return Bounds(x=min(x), y=min(y), x2=max(x), y2=max(y))
        
    def enclosed_by_bounds(self, bounds):
        return self.bounds.enclosed_by_bounds(bounds)
    
    def move(self, offsetx, offsety):   
        offset_points = []
        for i, value in enumerate(self.points) :
            if i % 2 == 0 :
                offset_points.append(value + offsetx)
            else :
                offset_points.append(value + offsety)
        
        return RotatedFrame(tuple(offset_points), self.label)    
    
    def as_dict(self) : 
        bounds = self.bounds
        dic = { 
            "label":self._label, 
            "type": "rotatedbox",
            "xmin": bounds.x,
            "ymin": bounds.y,
            "xmax": bounds.x2,
            "ymax": bounds.y2 
        }
        
        for i, value in enumerate(self.points) :
            if i % 2 == 0 :
                field = "x{}".format(i // 2)
            else :
                field = "y{}".format(i // 2)
                
            dic[field] = value
                
        return dic    
    
    def as_csv(self) :
        return ",".join([str(value) for value in self.points])
    
    def scale(self, xscale, yscale) :
        scaled_points = []
        for i, value in enumerate(self.points) :
            if i % 2 == 0 :
                scaled_points.append(value * xscale)
            else :
                scaled_points.append(value * yscale)
                
        return RotatedFrame(tuple(scaled_points), self.label) 
        
    def __repr__(self) :
        return "{},{}".format(self.as_csv(), self.label)

    def __len__(self) :
        return len(self.points)

    def __getitem__(self, index):
        if index < len(self.points) :
            index *= 2
            return (self.points[index], self.points[index + 1])
        
        raise IndexError
    