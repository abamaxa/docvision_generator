from .drawable import Drawable

import graphics

class Graph(Drawable) :
    def __init__(self, parameters) :
       Drawable.__init__(self, parameters)
       self.graphic_type = self.realize_parameter("type")
       self.proxy = None
    
    def update_page_parameters(self, page) :
        self.labels = page.get_words(10)
        
    def create_proxy(self) :
        bounds = self.inner_bounds
        self.proxy = Graph(bounds.width, bounds.height, self.labels)
        
        function_name = "generate_" + self.graphic_type
        function = getattr(self.proxy, function_name)
        function()        
        
    def render(self, draw) :
        super().render(self, draw)
        self.create_proxy()
        
        draw.blit(self.proxy.get_image(), self.inner_bounds.origin)
        
class Diagram(Drawable) :
    def __init__(self, parameters) :
        super().__init__(parameters)
        self.graphic_type = self.realize_parameter("type")
        self.weight = self.realize_parameter("weight", 1)
                
    def render(self, draw) :
        super().render(self, draw)
        bounds = self.inner_bounds
        
        diagram = Diagram(draw, bounds, self.weight)
        
        function_name = "render_" + self.graphic_type
        render_function = getattr(self.proxy, function_name)
        render_function()  
        
class Formula(Drawable) :
    def __init__(self, parameters) :
        super().__init__(parameters)
        self.graphic_type = self.realize_parameter("type")
        self.proxy = Formula()
        
        function_name = "generate_" + self.graphic_type
        function = getattr(self.proxy, function_name)
        function()    
        
    def get_content_size(self) :
        size = self.proxy.image.size
        return graphics.Size(size[0], size[1])
        
    def render(self, draw) :
        super().render(self, draw)        
        draw.blit(self.proxy.image, self.inner_bounds.origin)