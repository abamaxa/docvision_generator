import unittest
from graphics.graph import Graph

class GraphTest(unittest.TestCase) :
    def setUp(self):
        self.graph = Graph(640, 480, 0, "Hello World This Is The Sample Label Text")
        
    def test_bar(self) :
        self.graph.generate_bar_graph()
        self.graph.debug_save("bar.png")
        self.assertTrue(True)
        
    def test_pie(self) :
        self.graph.generate_pie()
        self.graph.debug_save("pie.png")
        self.assertTrue(True)
        
    def test_line(self) :
        self.graph.generate_line_graph()
        self.graph.debug_save("line.png")
        self.assertTrue(True)