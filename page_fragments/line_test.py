import unittest
import random
from unittest.mock import patch, call, MagicMock

from graphics import Bounds, Draw
from page_fragments.drawable_test import DrawableTest
from page_fragments import *

class HorizontalLineTest(DrawableTest) :
    def _create_drawable(self, parameters = {}) :
        self.drawable = HorizontalLine(parameters)
        

class VerticalLineTest(DrawableTest) :
    def _create_drawable(self, parameters = {}) :
        self.drawable = VerticalLine(parameters)