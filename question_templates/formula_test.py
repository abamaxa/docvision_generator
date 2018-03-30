import unittest
import random
from unittest.mock import patch, call, MagicMock

from graphics import Bounds, Draw
from question_templates.drawable_test import DrawableTest
from question_templates import *

formula_parameters = {
    "type" : random.choice(["quadratic", "intergral", "inequalities",
                           "surds", "trig", "factorizations",
                           "angle_ranges"])
}

class FormulaTest(DrawableTest) :
    def _create_drawable(self, parameters = {}) :
        parameters = dict(parameters)
        parameters.update(formula_parameters)
        self.drawable = Formula(parameters)
        
    def test_no_type(self) :
        with self.assertRaises(ValueError) :
            self.drawable = Formula({})