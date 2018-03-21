from abc import ABC

class Drawable(ABC) :
    def __init__(self, bounds) :
        self._bounds = bounds
        
    def get_bounds(self) :
        return self._bounds
    
    def set_bounds(self, new_bounds) :
        self._bounds = new_bounds
        
    bounds = property(get_bounds, set_bounds)
    
    
        
    