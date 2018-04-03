from .drawable import Drawable

import graphics

class RectangularContent(Drawable) :
    def get_content_size(self) :
        bounds = self.inner_bounds
        aspect = self.realize_parameter("aspect_ratio", 0.6)
        size = graphics.Size(bounds.width, int(bounds.width * aspect)) 
        return self.calculate_size_from_inner_size(size)
    
    def layout(self, bounds) :
        self._bounds = graphics.Bounds(bounds.x, bounds.y, bounds.width, bounds.height)     
        size = self.get_content_size()
        self._bounds = graphics.Bounds(bounds.x, bounds.y, size.width, size.height)      