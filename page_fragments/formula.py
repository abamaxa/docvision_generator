from .drawable import Drawable

import graphics
        
class Formula(Drawable) :
    def __init__(self, parameters) :
        super().__init__(parameters)
        self._graphic_type = None
        self._proxy = None
        self._text_size = 0
        
    @property
    def graphic_type(self) :
        return self._graphic_type
    
    def update_page_parameters(self, page) :
        super().update_page_parameters(page)
        self._text_size = page.parameters.font_size 
        self.generate_formulas()
        
    def get_element_size(self) :
        size = self._proxy.image.size
        return self.calculate_size_from_inner_size(graphics.Size(size[0], size[1]))
    
    def generate_formulas(self) :
        self._proxy = graphics.Formula(self._text_size)
        
        if self.primary_element :
            self._graphic_type = self.primary_element.graphic_type
        else :
            self._graphic_type = self.realize_required_parameter("type")
           
        function_name = "generate_" + self.graphic_type
        function = getattr(self._proxy, function_name)
        function()            
        
    def render(self, draw) :
        super().render(draw)        
        draw.blit_text(self._proxy.image, (
            int(self.inner_bounds.x),
            int(self.inner_bounds.y),                         
            int(self.inner_bounds.x2), 
            int(self.inner_bounds.y2)))