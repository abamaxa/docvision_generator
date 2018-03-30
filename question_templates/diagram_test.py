import unittest
import random
from unittest.mock import patch, call, MagicMock

from graphics import Bounds, Draw
from question_templates.drawable_test import DrawableTest
from question_templates import *

diagram_parameters = {
    "type" : random.choice(["triangle", "circle", "quadrilateral", "cross"])
}

class DiagramTest(DrawableTest) :
    def _create_drawable(self, parameters = {}) :
        parameters = dict(parameters)
        parameters.update(diagram_parameters)           
        self.drawable = Diagram(parameters)
        
    def test_no_type(self) :
        with self.assertRaises(ValueError) :
            self.drawable = Diagram({})   
            
    
