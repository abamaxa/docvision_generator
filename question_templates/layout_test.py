import unittest
import random
from unittest.mock import patch, call, MagicMock

from graphics import Bounds, Draw
from question_templates.drawable_test import create_test_page, page_parameters
from question_templates.drawable import Drawable
from question_templates.layout import VerticalLayout, GridLayout

class LayoutTest(unittest.TestCase) :
    def setUp(self) :
        random.seed(42)
        self.page = create_test_page()
        self.bounds = Bounds(5,10,100,500)
        self.children = [Drawable({}), Drawable({}), Drawable({})]
        for child in self.children :
            child.update_page_parameters(self.page)   
            child.calculate_dimensions(MagicMock(), self.bounds.size)
         
    def test_vertical_layout(self) :
        layout = VerticalLayout(self.bounds, self.children)  
        layout.layout()
        
        size = layout.get_content_size()
        
    def test_grid_layout(self) :
        layout = GridLayout(self.bounds, self.children,3)  
        layout.layout()
        
        size = layout.get_content_size()    