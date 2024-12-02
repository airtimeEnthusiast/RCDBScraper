import unittest
import sys
import os

# Run unit tests from terminal:
#' python3 - m unittest discover - s Test - p "*.py" '

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from RCDB_Scraper import Parser

class MyTestCase(unittest.TestCase):
    #def test_something(self):
        #Parser.print_visited_parks_and_rides(Parser.visited_parks_and_rides)
        #self.assertEqual(True, True)  # add assertion here

    #def test_get_state_pages(self):
        #print("Get the links to the state pages")
        #usa_link = "https://rcdb.com/location.htm?id=59"
        #states_link = Parser.get_state_page_links(usa_link, Parser.visited_parks_and_rides)

    #def test_get_state_extant_park_page(self):
        #ca_state_link = "https://rcdb.com/location.htm?id=1499"
        #park_pages = Parser.get_state_extant_parks_links(ca_state_link)

    # Test the function to get a state's second park page
    #def test_get_additional_park_page_links(self):
        #state_park_page_one_link = "https://rcdb.com/r.htm?ot=3&ex&ol=1499"
        #print(Parser.get_additional_park_page_links(state_park_page_one_link))

    #def test_get_park_coaster_page_links(self):
        #mult_table = "https://rcdb.com/4571.htm" # with multiple ride table
        #one_table = "https://rcdb.com/4627.htm" # with one ride table
        #Parser.get_park_coaster_page_links(mult_table,Parser.visited_parks_and_rides)


    def test_print_missing_values(self):
        Parser.test_missing_values("Visited_Coasterlist.csv", Parser.visited_parks_and_rides)


    #def test_get_coaster(self):
    #    coaster_link = "https://rcdb.com/16985.htm"
    #    Parser.parse_coaster(coaster_link)

    #def test_get_park(self):
    #    park_link = "https://rcdb.com/4543.htm"
    #    Parser.parse_park_page(park_link)

    #def test_parse_visited_parks(self):
        #Parser.parse_visited_parks()


if __name__ == '__main__':
    unittest.main()
