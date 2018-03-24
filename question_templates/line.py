from .drawable import Drawable

class Line(Drawable) :
    def __init__(self, parameters) :
       Drawable.__init__(self, parameters)
        
    def render(self, draw) :
        super().render(self, draw)
        draw.line(self.origin, self.size)