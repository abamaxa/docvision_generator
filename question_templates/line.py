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
    def get_content_size(self) :
        return Size(Drawable.FILL_PARENT, self.line_size)
    
        
class VerticalLine(BaseLine) :
    def get_content_size(self) :
        return Size(self.line_size, FILL_PARENT)
    
   