import json

from .draw import Draw
from .page import Page
from .constructed_page_factory import ConstructedQuestionFactory

class ConstructedPage(Page) :
    pass


def make_question(name, options) :
    factory = ConstructedQuestionFactory()
    
    page = ConstructedPage(name, options)
        
    question = factory.create_question_from_template("simple")
    question.update_page_parameters(page)
    question.calculate_dimensions(draw)
    question.layout(bounds)
    question.render(page.draw)
    
    