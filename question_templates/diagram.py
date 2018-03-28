from .drawable import Drawable

class Diagram(Drawable) :
    GRAPH_XY = 1
    
    def __init__(self, parameters) :
       Drawable.__init__(self, parameters)
       self.line_height = 1
       
    def get_content_size(self) :
        return (FILL_PARENT, self.line_height)
    
    def calculate_dimensions(self, draw, parent_bounds) :
        self.bounds = parent_bounds 
        inner_width = self.inner_bounds.width
        
        super().update_bounds()    
        
    def render(self, draw) :
        super().render(self, draw)
        points = ((self.inner_bounds.x, self.inner_bounds.y),
                  (self.inner_bounds.x2, self.inner_bounds.y2))
        
        draw.draw_line(points, self._foreground_color)
