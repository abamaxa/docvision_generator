import random

from page_fragments.drawable_test import DrawableTest
from page_fragments import Formula

formula_parameters = {
    "type" : random.choice(["quadratic", "intergral", "inequalities",
                           "surds", "trig", "factorizations",
                           "angle_ranges"])
}

class FormulaTest(DrawableTest) :
    def _create_drawable(self, parameters = {}) :
        parameters = dict(parameters)
        parameters.update(formula_parameters)
        self.drawable = Formula(parameters)
    
            
    