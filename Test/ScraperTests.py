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

    #def test_get_state_pages(self):
        #print("Get the links to the state pages")
        #usa_link = "https://rcdb.com/location.htm?id=59"
        #states_link = Parser.get_state_page_links(usa_link)
        # Use '53' when !include_visited and '11' when include_visited
        #self.assertEquals(len(states_link),11)

    def test_get_state_extant_park_page(self):
        ca_state_link = "https://rcdb.com/location.htm?id=1499"
        first_park_page = Parser.get_state_extant_parks_link(ca_state_link)
        second_park_page = Parser.get_second_extant_park_page(first_park_page)
        park_pages = Parser.get_park_page_links(first_park_page, Parser.visited_parks_and_rides)

if __name__ == '__main__':
    unittest.main()
