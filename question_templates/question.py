from . import *

class Question(Container) :
    def __init__(self, parameters) :
        Drawable.__init__(self, parameters)
        Container.__init__(self, parameters.get("question"))
        self._type = parameters.get("name")
        self.width = 0
      
    @property
    def type(self) :
        return self._type
    
    def update_page_parameters(self, page) :
        self.width = page.parameters.get_column_width()
        super().update_page_parameters(page)
        
    def layout(self, bounds) :
        pass    
        
    def layout(self, bounds) :
        for child in self._children :
            pass
              
    def get_height(self) :
        pass
