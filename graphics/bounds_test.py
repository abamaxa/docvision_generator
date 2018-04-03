import unittest
from graphics.bounds import Size, Origin, Bounds

class BoundsTest(unittest.TestCase) :
    def setUp(self):
        self.bounds = [Bounds(0, 0, 20, 10), Bounds(-5, -5, 20, 10)]
        
    def test_size(self):
        size = Size(1,2)
        self.assertEqual(size.width, 1)
        self.assertEqual(size.height, 2)
        self.assertEqual(str(size), "Width: 1 Height: 2")

    def test_origin(self):
        origin = Origin(3,4)
        self.assertEqual(origin.x, 3)
        self.assertEqual(origin.y, 4)    
        self.assertEqual(str(origin), "x: 3 y: 4")
    
    def test_bounds_size(self):
        for bounds in self.bounds :
            self.assertEqual(bounds.width, 20)
            self.assertEqual(bounds.height, 10)
            self.assertEqual(bounds.size, Size(20, 10))
            self.assertNotEqual(bounds.size, Size(0, 0))
            
    def test_bounds_x2y2(self):
        bounds = Bounds(5,5,15,5)
        self.assertEqual(bounds.x2, 20)
        self.assertEqual(bounds.y2, 10)   
            
    def test_bounds_str(self):
        self.assertEqual(str(self.bounds[0]), "x: 0 y: 0 Width: 20 Height: 10")
        self.assertEqual(str(self.bounds[1]), "x: -5 y: -5 Width: 20 Height: 10")
    
    def test_bounds_origin(self):
        self.assertEqual(self.bounds[0].x, 0)
        self.assertEqual(self.bounds[0].y, 0)
        self.assertEqual(self.bounds[0].origin, Origin(0,0))
        self.assertNotEqual(self.bounds[0].origin, Origin(1,1))
        
        self.assertEqual(self.bounds[1].x, -5)
        self.assertEqual(self.bounds[1].y, -5)    
        self.assertEqual(self.bounds[1].origin, Origin(-5,-5))
        self.assertNotEqual(self.bounds[1].origin, Origin(1,1))
        
    def test_bounds_inflate(self) :
        result1 = Bounds(-1, -2, 22, 14)
        self.assertEqual(self.bounds[0].inflate(1,2), result1)
        result2 = Bounds(-8, -9, 26, 18)
        self.assertEqual(self.bounds[1].inflate(3,4), result2)        
    
    def test_bounds_scale(self) :
        result1 = Bounds(0, 0, 40, 40)
        self.assertEqual(self.bounds[0].scale(2,4), result1)
        result2 = Bounds(-20, -10, 80, 20)
        self.assertEqual(self.bounds[1].scale(4,2), result2)      
    
    def test_bounds_move(self) :
        result1 = Bounds(1, 2, 20, 10)
        self.assertEqual(self.bounds[0].move(1,2), result1)
        result2 = Bounds(-10, -15, 20, 10)
        self.assertEqual(self.bounds[1].move(-5,-10), result2)      
    
    def test_bounds_enclosed_by_bounds(self):
        test_in = Bounds(1,1,2,2)
        test_enclosed = Bounds(-100,-100,200,200)
        test_out = Bounds(1,2,200,200)
    
        for bounds in self.bounds :
            self.assertTrue(bounds.enclosed_by_bounds(test_enclosed))
            self.assertFalse(bounds.enclosed_by_bounds(test_in))
            self.assertFalse(bounds.enclosed_by_bounds(test_out))
            
    def test_bounds_overlap_bounds(self):
        test_in = Bounds(1,1,2,2)
        test_enclosed = Bounds(-100,-100,200,200)
        test_out = Bounds(1,2,200,200)
        test_far = Bounds(-100,-100, 10,10)
    
        for bounds in self.bounds :
            self.assertTrue(bounds.overlap_bounds(test_enclosed))
            self.assertTrue(bounds.overlap_bounds(test_in))
            self.assertTrue(bounds.overlap_bounds(test_out))        
            self.assertFalse(bounds.overlap_bounds(test_far)) 
            
    def test_iterator(self) :
        test_size = Size(1,2)
        a,b = test_size
        self.assertEqual(a,1)
        self.assertEqual(b,2)
        
        test_origin = Size(3,4)
        a,b = test_origin
        self.assertEqual(a,3)
        self.assertEqual(b,4)
        
        test_bounds = Bounds(1,2,3,4)
        a,b,c,d,e = test_bounds
        self.assertEqual(a,(1,2))
        self.assertEqual(b,(4,2))  
        self.assertEqual(c,(4,6))
        self.assertEqual(d,(1,6))
        self.assertEqual(e,(1,2))
        
    def test_merge(self) :
        bounds = Bounds(0, 0, 20, 10)
        bounds2 = bounds.merge(bounds)
        
        self.assertEqual(bounds, bounds2)
        
        bounds2 = bounds.merge(Bounds(-1,-2, x2=21, y2=11))
        self.assertEqual(bounds2.x, -1)
        self.assertEqual(bounds2.y, -2)
        self.assertEqual(bounds2.x2, 21)
        self.assertEqual(bounds2.y2, 11)        
   

if __name__ == '__main__':
    unittest.main()
    