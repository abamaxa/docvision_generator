import unittest

from graphics.formula import Formula

class FormulaTest(unittest.TestCase) :
    def test_quadratic(self) :
        formula = Formula()
        formula.quadratic()
        
        image = formula.image
        image.save("formula.png")