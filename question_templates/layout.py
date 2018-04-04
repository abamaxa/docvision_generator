from graphics import Bounds, Size, Origin
from .drawable import Drawable

class Layout :
    def __init__(self, bounds, children) :
        self.bounds = bounds
        self.children = children
        self.width =  bounds.width # Drawable.FILL_PARENT
        self.height = bounds.height # Drawable.FILL_PARENT

    def get_max_child_size(self) :
        return Size(self.width, self.height)
    
    def get_element_size(self) :   
        self.layout()
        bounds = self.children[0].bounds
        for i in range(1, len(self.children)) :
            bounds = bounds.merge(self.children[i].bounds)
 
        return bounds.size
  
class VerticalLayout(Layout) :
    def __init__(self, bounds, children) :
        super().__init__(bounds, children)
        self.width = bounds.width
        self.height = int(bounds.width * 0.5)
            
    def layout(self) :
        bounds = self.bounds
        for child in self.children :
            child.layout(bounds)   
            bounds = child.bounds.move(0, child.bounds.height)   
    
class GridLayout(Layout) :
    def __init__(self, bounds, children, cols) :
        super().__init__(bounds, children)
        self.cell_width = bounds.width // cols
        self.cell_height = self.cell_width
        self.cols = cols
        
    def layout(self) :
        x = self.bounds.x
        y = self.bounds.y
        col = 0
        max_height = 0
        self.height = 0
        
        for child in self.children :
            child_bounds = Bounds(x, y, self.cell_width, self.cell_height)
            child.layout(child_bounds)   
            max_height = max(max_height, child.bounds.height)
            col += 1
            
            if col % self.cols == 0 :
                x = self.bounds.x
                y += max_height
                self.height += max_height
                max_height = 0
            else :
                x += self.cell_width

                
        
                            
