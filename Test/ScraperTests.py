import unittest
import sys
import os

# Run unit tests from terminal:
#' python3 - m unittest discover - s Test - p "*.py" '

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from RCDB_Scraper import Parser

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_get_state_pages(self):
        print("Get the links to the state pages")
        USA_Link = "https://rcdb.com/location.htm?id=59"
        references = Parser.get_state_page_links(USA_Link)
        self.assertEqual(len(references),53)


if __name__ == '__main__':
    unittest.main()
