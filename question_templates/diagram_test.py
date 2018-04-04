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
        with self.assertRaises(ParameterError) :
            self.drawable = Diagram({})   
            
    def test_layout(self) :
        for diagram_type in diagram_parameters["type"] :
            self._create_drawable({"type" : diagram_type, "aspect_ratio" : 1.0 })
            bounds = Bounds(20,10,200,100)
            self.drawable.layout(bounds)
            
            test_bounds = self.drawable.bounds
            self.assertEqual(test_bounds.x, bounds.x)
            self.assertEqual(test_bounds.y, bounds.y)
            self.assertEqual(test_bounds.width, bounds.width)
            self.assertEqual(test_bounds.height, bounds.width)
            
    def test_aspect_ratio(self) :
        for diagram_type in diagram_parameters["type"] :
            self._create_drawable({"type" : diagram_type, "aspect_ratio" : 0.5 })
            bounds = Bounds(20,10,200,100)
            self.drawable.layout(bounds)
            
            test_bounds = self.drawable.bounds
            self.assertEqual(test_bounds.x, bounds.x)
            self.assertEqual(test_bounds.y, bounds.y)
            self.assertEqual(test_bounds.width, bounds.width)
            self.assertEqual(test_bounds.height, bounds.width // 2)    
            
            
    
