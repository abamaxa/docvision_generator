import unittest
import random
from unittest.mock import patch, call, MagicMock

from page_fragments.drawable_test import DrawableTest
from page_fragments.container import Container

class ContainerTest(DrawableTest) :
    def _create_drawable(self, parameters = {}) :
        self.drawable = Container(parameters) 
        
    def test_single(self) :
        json = {
            "elements" : [{
                "class" : "Text",
                "sentences" : 1,
            }]
        }
        
        self._create_drawable()
        self.drawable.create_children(json)
        
        self.assertEqual(len(self.drawable._children), 1)
        
    def test_repeat(self) :
        json = {
            "elements" : [{
                "class" : "Text",
                "sentences" : 1,
                "repeat" : 3
            }]
        }        

        self._create_drawable()
        self.drawable.create_children(json)
        self.assertEqual(len(self.drawable._children), 4)       
        
    def test_create_probability(self) :
        json = {
            "elements" : [{
                "class" : "Text",
                "sentences" : 1,
                "probability" : 0.0
            }]
        }        

        self._create_drawable()
        self.drawable.create_children(json)
        self.assertEqual(len(self.drawable._children), 0)          
