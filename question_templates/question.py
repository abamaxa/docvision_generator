from .drawable import Drawable
from .container import Container
from .parameter_parser import ParameterParser
from .numerator import Numerator

class Question(Container) :
    DEFAULTS = {
        "padding_top" : 0
    }
    
    def __init__(self, parameters) :
        params = dict(Question.DEFAULTS)
        params.update(parameters)
        Drawable.__init__(self, params)
        Container.__init__(self, params.get("question"))
        self._type = parameters.get("name")
        self._numerator = None
        self.__create_numerator()
                        
    @property
    def type(self) :
        return self._type
        
    def update_page_parameters(self, page) :
        Drawable.update_page_parameters(self, page)
        self.__update_inter_question_gap(page.parameters.inter_question_gap)
        super().update_page_parameters(page)
        
        Drawable.set_numerator(self, self._numerator)
        self.set_numerator(self._numerator)
        
    def __update_inter_question_gap(self, gap) :
        if self._margin_top + self._padding_top < gap :
            self._padding_top = gap - self._margin_top
            
        if self._margin_bottom + self._padding_bottom < gap :
            self._padding_bottom = gap - self._margin_bottom 
            
    def __create_numerator(self) :
        numerator_parameters = self.parameters.get("numerator")
        if not numerator_parameters :
            return
        
        parser = ParameterParser(numerator_parameters)
        #if not parser.realize_parameter("probability", True) :
        #    return
        
        self._numerator = Numerator(numerator_parameters)
            
