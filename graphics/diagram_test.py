import unittest
import random

from page_generator.page import Page
from page_generator.page_params import PageParameters
from graphics.draw_test import options
import os

from graphics import Draw, Bounds
from graphics.diagram import Diagram

class DiagramTest(unittest.TestCase) :
    def setUp(self):
        random.seed(42)
        self.params = PageParameters("test", options)
        self.params.generate_random_parameters()        
        self.draw = Draw(self.params)
        self.draw.init_image()
        self.draw.create_draw()
        self.diagram = Diagram(self.draw,Bounds(0,0,640,480) , 2)
        
    def __debug_save(self, name) :
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
        os.makedirs(os.path.dirname(output_dir), exist_ok = True)
        self.draw.save(os.path.join(output_dir, name))    
        
    def test_triangle(self) :
        self.diagram.render_triangle()
        self.__debug_save("triangle.png")
        
    def test_circle(self) :
        self.diagram.render_circle()
        self.__debug_save("circle.png")
        
    def test_quadrilateral(self) :
        self.diagram.render_quadrilateral()
        self.__debug_save("quad.png")
    
    def test_cross(self) :
        self.diagram.render_cross()
        self.__debug_save("cross.png") 
        
    def test_random(self) :
        self.diagram.render_cross()
        self.__debug_save("random_diagram.png")         
   