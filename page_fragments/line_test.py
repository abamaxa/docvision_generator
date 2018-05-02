from page_fragments.drawable_test import DrawableTest
from page_fragments import HorizontalLine, VerticalLine

class HorizontalLineTest(DrawableTest) :
    def _create_drawable(self, parameters = {}) :
        self.drawable = HorizontalLine(parameters)
        

class VerticalLineTest(DrawableTest) :
    def _create_drawable(self, parameters = {}) :
        self.drawable = VerticalLine(parameters)
