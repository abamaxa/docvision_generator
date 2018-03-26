import unittest

from question_generator.dictionary_generator import TextGen

class TextGenTest(unittest.TestCase) :
    def setUp(self) :
        self.generator = TextGen.get_generator()
        
    def test_get_sentence(self) :
        _, length, sentence = self.generator.generate_sentence()
        self.assertTrue(sentence.endswith("."))
        words = sentence.split(' ')
        self.assertGreaterEqual(len(words), 3)

        
if __name__ == '__main__':
    unittest.main()
        