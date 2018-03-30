from graphics import Bounds, Size, Origin
from .drawable import Drawable

class Layout :
    def __init__(self, bounds) :
        self.bounds = bounds
        self.width =  bounds.width # Drawable.FILL_PARENT
        self.height = bounds.height # Drawable.FILL_PARENT

    def get_max_child_size(self) :
        return Size(self.width, self.height)
  
class VerticalLayout(Layout) :
    def __init__(self, bounds) :
        super().__init__(bounds)
        self.width = bounds.width
        self.height = bounds.width * 0.5
        
    def layout(self, children) :
        bounds = self.bounds
        for child in children :
            child.layout(bounds)   
            bounds = child.bounds.move(0, child.bounds.height)   
    

class GridLayout(Layout) :
    def __init__(self, bounds, cols) :
        super().__init__(bounds)
        self.width = bounds.width // cols
        self.height = self.width
        self.cols = cols
        
    def layout(self, children) :
        x = self.bounds.x
        y = self.bounds.y
        col = 0
        max_height = 0
        
        for child in children :
            child_bounds = Bounds(x, y, self.width, self.height)
            child.layout(child_bounds)   
            max_height = max(max_height, child.bounds.height)
            col += 1
            
            if col % self.cols == 0 :
                x = self.bounds.x
                y += max_height
                max_height = 0
            else :
                x += self.width
                            
