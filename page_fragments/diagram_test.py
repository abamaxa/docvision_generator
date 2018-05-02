import random

from graphics import Bounds
from page_generator import ParameterError
from page_fragments.drawable_test import DrawableTest, BOUNDS_HEIGHT, \
     BOUNDS_WIDTH, create_test_page
from page_fragments import Diagram

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
            
    def test_padding_margins_no_aspect(self) :
        params = {
            "class" : "Diagram",
            "type" : "triangle",
            "number_level" : 1,
            "margin" : "10%",    
            "padding" : "20%",
            "aspect_ratio" :1
        }
        
        self._create_drawable(params)
        page = create_test_page()
        bounds = Bounds(20,10,BOUNDS_WIDTH,BOUNDS_HEIGHT)
        
        self.drawable.update_page_parameters(page)
        self.drawable.layout(bounds)
        
        test_bounds = self.drawable.bounds
        
        self.assertEqual(test_bounds.x, bounds.x)
        self.assertEqual(test_bounds.y, bounds.y)
        self.assertEqual(test_bounds.width, bounds.width)
        self.assertEqual(test_bounds.height, bounds.width)    
        
        test_bounds = self.drawable.inner_bounds
        
        self.assertEqual(test_bounds.x, int(bounds.x + (bounds.width * 0.3)))
        self.assertEqual(test_bounds.y, int(bounds.y + (bounds.width * 0.3)))
        self.assertEqual(test_bounds.width, int(bounds.width * 0.4))
        self.assertEqual(test_bounds.height, int(bounds.width * 0.4))      
        
    def test_padding_margins_with_aspect(self) :
        params = {
            "class" : "Diagram",
            "type" : "triangle",
            "number_level" : 1,
            "margin" : "10%",    
            "padding" : "20%",
            "aspect_ratio" : 0.5
        }
        
        self._create_drawable(params)
        page = create_test_page()
        bounds = Bounds(20,10,BOUNDS_WIDTH,BOUNDS_HEIGHT)
        
        self.drawable.update_page_parameters(page)
        self.drawable.layout(bounds)
        
        test_bounds = self.drawable.bounds
        
        self.assertEqual(test_bounds.x, bounds.x)
        self.assertEqual(test_bounds.y, bounds.y)
        self.assertEqual(test_bounds.width, bounds.width)
        self.assertEqual(test_bounds.height, 80)    
        
        test_bounds = self.drawable.inner_bounds
        
        self.assertEqual(test_bounds.x, int(bounds.x + (bounds.width * 0.3)))
        self.assertEqual(test_bounds.y, int(bounds.y + (bounds.width * 0.3)))
        self.assertEqual(test_bounds.width, int(bounds.width * 0.4))
        self.assertEqual(test_bounds.height, int((bounds.width // 2) * 0.4))            
