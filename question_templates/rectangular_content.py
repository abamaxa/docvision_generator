from .drawable import Drawable

import graphics

class RectangularContent(Drawable) :
    def __init__(self, parameters) :
        super().__init__(parameters)
        self.aspect = self.realize_parameter("aspect_ratio", 0.6)
        
    def get_element_size(self) :
        inner_width = self.bounds.width - self._total_margin_left_right
        size = graphics.Size(inner_width, int(inner_width * self.aspect)) 
        return self.calculate_size_from_inner_size(size)
    
    def layout(self, bounds) :
        self._bounds = graphics.Bounds(bounds.x, bounds.y, bounds.width, bounds.height)     
        size = self.get_element_size()
        self._bounds = graphics.Bounds(bounds.x, bounds.y, size.width, size.height)      