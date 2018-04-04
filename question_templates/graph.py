import logging

from .drawable import Drawable
from .rectangular_content import RectangularContent

import graphics

class Graph(RectangularContent) :
    def __init__(self, parameters) :
       super().__init__(parameters)
       self.graphic_type = self.realize_required_parameter("type")
       self.proxy = None
    
    def update_page_parameters(self, page) :
        self.labels = page.get_words(10)
        super().update_page_parameters(page)     
        
    def create_proxy(self) :
        bounds = self.inner_bounds
        self.proxy = graphics.Graph(bounds.width, bounds.height, self.labels)
        
        function_name = "generate_" + self.graphic_type
        function = getattr(self.proxy, function_name)
        function()        
        
    def render(self, draw) :
        super().render(draw)
        self.create_proxy()
        x, y = self.inner_bounds.origin
        width, height = self.inner_bounds.size
        logging.debug("Render Graphic of type %s (%d,%d) (%d,%d)", 
                      self.graphic_type, x, y, width, height)
        
        image = self.proxy.get_image()
        image = image.resize(tuple(self.bounds.size))
        #x += (width - image.width) // 2
        #y += (height - image.height) // 2
        #draw.blit(image, (int(x), int(y)))
                
        draw.blit(image, (
            int(self.inner_bounds.x),
            int(self.inner_bounds.y),                         
            int(self.inner_bounds.x2), 
            int(self.inner_bounds.y2)))        
        
