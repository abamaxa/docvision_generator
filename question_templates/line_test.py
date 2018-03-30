import unittest
import random
from unittest.mock import patch, call, MagicMock

from graphics import Bounds, Draw
from question_templates.drawable_test import DrawableTest
from question_templates import *

class HorizontalLineTest(DrawableTest) :
    def _create_drawable(self, parameters = {}) :
        self.drawable = HorizontalLine(parameters)
