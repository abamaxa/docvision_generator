from .drawable import Drawable
from .container import Container
from .parameter_parser import ParameterParser
from .numerator import Numerator

class Question(Container) :
    DEFAULTS = {
        "padding_top" : 0,
        "number_level" : 0 
    }
    
    def __init__(self, parameters) :
        params = dict(Question.DEFAULTS)
        params.update(parameters.get("question"))
        super().__init__(params)
        self._type = parameters.get("name")
        self._numerator = None
                                
    @property
    def type(self) :
        return self._type
        
    def update_page_parameters(self, page) :
        Drawable.update_page_parameters(self, page)
        super().update_page_parameters(page)
        self.__update_inter_question_gap(page.parameters.inter_question_gap)
                
    def set_numerator(self, numerator) :
        self._numerator = numerator
        if numerator :
            Drawable.set_numerator(self, numerator)
            Container.set_numerator(self, numerator)
        
    def __update_inter_question_gap(self, gap) :
        half_gap = gap // 2
        if self._margin_top + self._padding_top < half_gap :
            self._padding_top = half_gap - self._margin_top
            
        if self._margin_bottom + self._padding_bottom < half_gap :
            self._padding_bottom = half_gap - self._margin_bottom 
            
        if self._margin_left + self._padding_left < half_gap :
            self._padding_left = half_gap - self._margin_left
            
        if self._margin_right + self._padding_right < half_gap :
            self._padding_right = half_gap - self._margin_right        
            