import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title_basic(self):
        line = "# header"
        self.assertEqual(extract_title(line), "header")
    def test_extract_title_no_h1(self):
        with self.assertRaises(Exception):
            extract_title("no header ")
    def test_extract_title_h2_not_h1(self):
        with self.assertRaises(Exception):
            extract_title("## h2 header ")

    