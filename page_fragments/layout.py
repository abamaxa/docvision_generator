from abc import abstractmethod

from graphics import Bounds, Size

class Layout :
    def __init__(self, bounds, children, cols = 1) :
        self.children = children
        self._cols = cols
        self.update_bounds(bounds)
        self.height = 0
                
    def update_bounds(self, bounds) :
        self.bounds = bounds
        self.width =  bounds.width # Drawable.FILL_PARENT
        self.height = bounds.height # Drawable.FILL_PARENT    
        
    @property
    def columns(self) : return self._cols

    def get_max_child_size(self) :
        return Size(self.width, self.height)
    
    def get_element_size(self) :   
        self.layout()
        bounds = self.children[0].bounds
        for i in range(1, len(self.children)) :
            bounds = bounds.merge(self.children[i].bounds)
 
        return bounds.size
    
    @abstractmethod
    def layout(self) :
        pass
  
class VerticalLayout(Layout) :               
    def update_bounds(self, bounds) :
        super().update_bounds(bounds)
        self.height = int(bounds.width * 0.5)   
            
    def layout(self) :
        bounds = self.bounds
        for child in self.children :
            new_bounds = Bounds(bounds.x, bounds.y, bounds.width, child.bounds.height)
            child.layout(new_bounds)   
            bounds = child.bounds.move(0, child.bounds.height)   
    
class GridLayout(Layout) :
    def __init__(self, bounds, children, cols) :
        super().__init__(bounds, children, cols)

    def update_bounds(self, bounds) :
        super().update_bounds(bounds)
        self.cell_width = bounds.width // self.columns
        self.cell_height = self.cell_width    
        
    def layout(self) :
        x = self.bounds.x
        y = self.bounds.y
        col = 0
        max_height = 0
        self.height = 0
        
        for child in self.children :
            height = min(child.bounds.height, self.cell_height)
            child_bounds = Bounds(x, y, self.cell_width, height)
            child.layout(child_bounds)   
            max_height = max(max_height, child.bounds.height)
            col += 1
            
            if col % self._cols == 0 :
                x = self.bounds.x
                y += max_height
                self.height += max_height
                max_height = 0
            else :
                x += self.cell_width

                
        
                            
