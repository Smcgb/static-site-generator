import unittest

from generate_webpage import *


class TestGenerateWebpage(unittest.TestCase):

    def test_extract_title(self):
        self.assertEqual(extract_title('# Heading'), "Heading")
        self.assertEqual(extract_title('#   Heading  '), "Heading")
        self.assertEqual(extract_title('# # Heading'), "# Heading")
        self.assertEqual(extract_title('Opener Text that is NOT a heading \n# Heading'), "Heading")
        self.assertEqual(extract_title('## minor heading \n# Heading'), "Heading")
        self.assertEqual(extract_title('# First\n# Second'), "First")
        
        with self.assertRaises(ValueError):
            extract_title('Opener Text that is NOT a heading')
        with self.assertRaises(ValueError):
            extract_title('Opener Text that is NOT a heading\n ## minor header')
        with self.assertRaises(ValueError):
            extract_title('#Heading')
        with self.assertRaises(ValueError):
            extract_title('')

if __name__ == "__main__":
    unittest.main()