from .drawable import Drawable

import graphics

class Diagram(Drawable) :
    def __init__(self, parameters) :
        super().__init__(parameters)
        self.graphic_type = self.realize_required_parameter("type")
        self.weight = self.realize_parameter("weight", 1)
        
    def get_content_size(self) :
        bounds = self.inner_bounds
        return graphics.Size(bounds.width, int(bounds.width * 0.6))    
                
    def render(self, draw) :
        super().render(draw)
        bounds = self.inner_bounds
        
        diagram = graphics.Diagram(draw, bounds, self.weight)
        
        function_name = "render_" + self.graphic_type
        render_function = getattr(diagram, function_name)
        render_function()  
