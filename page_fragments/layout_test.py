import unittest
import random
from unittest.mock import patch, call, MagicMock

from graphics import Bounds, Draw
from page_fragments.drawable_test import create_test_page, page_parameters
from page_fragments.drawable import Drawable
from page_fragments.layout import VerticalLayout, GridLayout

class LayoutTest(unittest.TestCase) :
    def setUp(self) :
        random.seed(42)
        self.page = create_test_page()
        self.bounds = Bounds(5,10,100,50)
        self.children = [Drawable({}), Drawable({}), Drawable({})]
        for child in self.children :
            child.update_page_parameters(self.page)   
            child.calculate_dimensions(MagicMock(), self.bounds.size)
         
    def test_vertical_layout(self) :
        layout = VerticalLayout(self.bounds, self.children)  
        layout.layout()
        
        size = layout.get_element_size()
        
        expected_y = self.bounds.y
        for child in self.children :
            self.assertEqual(child.bounds.width, self.bounds.width)
            self.assertEqual(child.bounds.height, self.bounds.height)
            self.assertEqual(child.bounds.y, expected_y)
            self.assertEqual(child.bounds.x, self.bounds.x)
            expected_y += self.bounds.height        
        
    def test_grid_layout(self) :
        layout = GridLayout(self.bounds, self.children,3)  
        layout.layout()
        
        size = layout.get_element_size()    
        
        expected_width = self.bounds.width // len(self.children)
        expected_x = self.bounds.x
        for child in self.children :
            self.assertEqual(child.bounds.width, expected_width)
            self.assertEqual(child.bounds.height, expected_width)
            self.assertEqual(child.bounds.y, self.bounds.y)
            self.assertEqual(child.bounds.x, expected_x)
            expected_x += expected_width
            