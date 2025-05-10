import unittest

from main import extract_title 

class TestExtractTitle(unittest.TestCase):

    def test_basic_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_h1_with_whitespace(self):
        self.assertEqual(extract_title("   #   Welcome   "), "Welcome")

    def test_h1_not_first_line(self):
        self.assertEqual(extract_title("Some text\n# Title"), "Title")

    def test_no_h1(self):
        with self.assertRaises(Exception) as context:
            extract_title("## Subtitle\nSome content")
        self.assertEqual(str(context.exception), "No H1 header found")

    def test_multiple_h1(self):
        self.assertEqual(extract_title("# First\n# Second"), "First")

    def test_empty_input(self):
        with self.assertRaises(Exception) as context:
            extract_title("")
        self.assertEqual(str(context.exception), "No H1 header found")

if __name__ == "__main__":
    unittest.main()