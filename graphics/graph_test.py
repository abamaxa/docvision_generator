import os
import unittest
from graphics.graph import Graph

class GraphTest(unittest.TestCase) :
    def setUp(self):
        self.graph = Graph(300, 300, "Hello World This Is The Sample Label Text")
        
    def __debug_save(self, name) :
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
        os.makedirs(os.path.dirname(output_dir), exist_ok = True)
        #self.graph.debug_save(os.path.join(output_dir, name))       
        image = self.graph.get_image()
        image.save(os.path.join(output_dir, name))
        
    def test_bar(self) :
        self.graph.generate_bar()
        self.__debug_save("bar.png")
        self.assertTrue(True)
        
    def test_pie(self) :
        self.graph.generate_pie()
        self.__debug_save("pie.png")
        self.assertTrue(True)
        
    def test_line(self) :
        self.graph.generate_line()
        self.__debug_save("line.png")
        self.assertTrue(True)