import unittest
import random
from unittest.mock import patch, call, MagicMock

from graphics import Bounds, Draw
from question_templates.drawable_test import DrawableTest, create_test_page
from question_templates import *

graph_parameters = {
    "type" : random.choice(["bar", "line", "pie"])
}

class GraphTest(DrawableTest) :
    def _create_drawable(self, parameters = {}) :
        parameters = dict(parameters)
        parameters.update(graph_parameters)        
        self.drawable = Graph(parameters)
        
            

        