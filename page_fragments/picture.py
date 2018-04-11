from .drawable import Drawable
from .rectangular_content import RectangularContent

import graphics

class Picture(RectangularContent) :
    def __init__(self, parameters) :
       super().__init__(parameters)
       self.image = None
               
    def render(self, draw) :
        super().render(draw)
        x, y = self.inner_bounds.origin
        width, height = self.inner_bounds.size
                
        x += (width - image.width) // 2
        y += (height - image.height) // 2
        
        draw.blit(self.image, (int(x), int(y)))