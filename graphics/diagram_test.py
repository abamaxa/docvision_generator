import unittest
import random

from question_generator.page import Page
from question_generator.question_params import QuestionParams
from graphics.draw_test import options
from graphics import Draw
from graphics.diagram import Diagram

class DiagramTest(unittest.TestCase) :
    def setUp(self):
        random.seed(42)
        self.params = QuestionParams("test", options)
        self.params.generate_random_parameters()        
        self.draw = Draw(self.params)
        self.draw.init_image()
        self.draw.create_draw()
        self.diagram = Diagram(self.draw, 640, 480, 2)
        
    def test_triangle(self) :
        self.diagram.draw_triangle()
        self.draw.save("triangle.png")
        
    def test_circle(self) :
        self.diagram.draw_circle()
        self.draw.save("circle.png")
        
    def test_quadrilateral(self) :
        self.diagram.draw_quadrilateral()
        self.draw.save("quad.png")
    
    def test_cross(self) :
        self.diagram.draw_cross()
        self.draw.save("cross.png") 
   