from .drawable import Drawable
from graphics import Size

class BaseLine(Drawable) :
    def __init__(self, parameters) :
        Drawable.__init__(self, parameters)
        self.line_size = 1
        
    def render(self, draw) :
        super().render(draw)
        points = ((self.inner_bounds.x, self.inner_bounds.y),
                  (self.inner_bounds.x2, self.inner_bounds.y2))
        
        draw.draw_line(points, self.line_size, self._foreground_color)    

class HorizontalLine(BaseLine) :       
    def get_element_size(self) :
        outer_size = self.calculate_size_from_inner_size(
            Size(Drawable.FILL_PARENT, self.line_size))
        return Size(Drawable.FILL_PARENT, outer_size.height)
    
        
class VerticalLine(BaseLine) :
    def get_element_size(self) :
        outer_size = self.calculate_size_from_inner_size(
            Size(self.line_size, Drawable.FILL_PARENT))        
        return Size(outer_size.width, Drawable.FILL_PARENT)
    
   