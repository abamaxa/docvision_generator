import random

from page_fragments.drawable_test import DrawableTest
from page_fragments import Graph

graph_parameters = {
    "type" : random.choice(["bar", "line", "pie"])
}

class GraphTest(DrawableTest) :
    def _create_drawable(self, parameters = {}) :
        parameters = dict(parameters)
        parameters.update(graph_parameters)        
        self.drawable = Graph(parameters)
        
            

        