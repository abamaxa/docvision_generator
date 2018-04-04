from .drawable import Drawable

import graphics
        
class Formula(Drawable) :
    def __init__(self, parameters) :
        super().__init__(parameters)
        self.graphic_type = self.realize_required_parameter("type")
        self.proxy = graphics.Formula()
        
        function_name = "generate_" + self.graphic_type
        function = getattr(self.proxy, function_name)
        function()    
        
    def get_element_size(self) :
        size = self.proxy.image.size
        return self.calculate_size_from_inner_size(graphics.Size(size[0], size[1]))
        
    def render(self, draw) :
        super().render(draw)        
        draw.blit(self.proxy.image, (
            int(self.inner_bounds.x),
            int(self.inner_bounds.y),                         
            int(self.inner_bounds.x2), 
            int(self.inner_bounds.y2)))