import json

from graphics import Draw, Bounds
from .page import Page
from .constructed_page_factory import ConstructedQuestionFactory

class ConstructedPage(Page) :
    pass


def make_question(name, options) :
    factory = ConstructedQuestionFactory()
    page = ConstructedPage(name, options)
    bounds = Bounds(0, 0, 400, 1000)
        
    question = factory.create_question_from_template("simple")
    question.update_page_parameters(page)
    question.calculate_dimensions(page.draw, bounds)
    question.layout(bounds)
    question.render(page.draw)
    
    page.draw.save("test.png")
    
    