## RCDB WebScraper ##
# Created by: Austin Wright
# Creates a CSV of coasters stats

import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from random import seed
from random import randint
import logging
import re

seed(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Parser class: Methods are
class Parser():
    coaster_data_array = [[]]
    coaster_extant_pages = []

    #####################################################
    # Return a data array of coaster stats
    # Must include a link to a coaster
    #####################################################
    def parse_coaster(coaster_link):

        ## Initialize the stats ##
        Name = Park = City = State = Country = None
        Status_type = Status_date = Material = Positioning = Thrill = None
        Make = Model = Length = Height = Drop = Speed = Inversions = None
        VerticalAngle = Duration = GForce = None

        # Fetch the page
        try:
            response = requests.get(coaster_link)
            response.raise_for_status()
            soup = bs(response.text, "html.parser")

            try:
                # Parse the name
                stat_sections = soup.find("body").find_all("section")
                Name = stat_sections[0].select_one("div:nth-child(1)").div.div.h1.get_text(strip=True)
            except Exception as e:
                logging.error(f"Error parsing Name: {e}")

            try:
                # Parse location metadata
                metas = stat_sections[0].select_one("div:nth-child(1)").div.div.find_all("a")
                if metas:
                    Park = metas[0].get_text(strip=True)
                    City = metas[1].get_text(strip=True)
                    State = metas[2].get_text(strip=True)
                    Country = metas[3].get_text(strip=True)
            except Exception as e:
                logging.error(f"Error parsing location metadata: {e}")

            try:
                # Parse operational status
                status = stat_sections[0].select_one("div:nth-child(1)").div.p
                if status:
                    Status_type = status.a.get_text(strip=True)
                    if status.time:
                        Status_date = status.time.get("datetime", None)
            except Exception as e:
                logging.error(f"Error parsing operational status: {e}")

            try:
                # Parse type (Material, Positioning, Thrill)
                Types = stat_sections[0].select_one("div:nth-child(1)").div.ul.find_all("li")
                if Types:
                    Material = Types[1].a.get_text(strip=True) if len(Types) > 1 else None
                    Positioning = Types[2].a.get_text(strip=True) if len(Types) > 2 else None
                    Thrill = Types[3].a.get_text(strip=True) if len(Types) > 3 else None
            except Exception as e:
                logging.error(f"Error parsing type: {e}")

            try:
                # Parse Make and Model
                Types = stat_sections[0].select_one("div:nth-child(1)").div.find("div", class_="scroll")
                if Types:
                    TypesCheck = Types.get_text().split(":")
                    for i, t in enumerate(Types.find_all("a")):
                        if "Make" in TypesCheck[i]:
                            Make = t.get_text(strip=True)
                        if "Model" in TypesCheck[i]:
                            Model = t.get_text(strip=True)
            except Exception as e:
                logging.error(f"Error parsing Make and Model: {e}")

            try:
                # Parse track stats
                stats_table = soup.find('table', {'class': 'stat-tbl'})
                if stats_table:
                    specs = list(stats_table.strings)
                    for i in range(len(specs)):
                        if specs[i] == 'Length':
                            Length = specs[i + 1]
                        elif specs[i] == 'Height':
                            Height = specs[i + 1]
                        elif specs[i] == 'Drop':
                            Drop = specs[i + 1]
                        elif specs[i] == 'Speed':
                            Speed = specs[i + 1]
                        elif specs[i] == 'Inversions':
                            Inversions = specs[i + 1]
                        elif specs[i] == 'Vertical Angle':
                            VerticalAngle = specs[i + 1]
                        elif specs[i] == 'Duration':
                            Duration = specs[i + 1]
                        elif specs[i] == 'G-Force':
                            GForce = specs[i + 1]
            except Exception as e:
                logging.error(f"Error parsing track stats: {e}")

        except requests.exceptions.RequestException as e:
            logging.critical(f"Request error: {e}")
            return None

        except Exception as e:
            logging.critical(f"Unexpected error: {e}")
            return None

        # Return the data array
        data = [
            Name, Park, City, State, Country, Status_type, Status_date,
            Material, Positioning, Thrill, Make, Model, Length, Height,
            Drop, Speed, Inversions, VerticalAngle, Duration, GForce
        ]
        logging.info("Parsed data successfully")
        #print(data)

        return data

    def parse_coaster_coordinates(coaster_link):
        try:
            # Fetch the webpage
            response = requests.get(coaster_link)
            response.raise_for_status()
            page_content = response.text

            # Parse the HTML content
            soup = bs(page_content, 'html.parser')

            # Find the maps pop-up link
            maps_link_tag = soup.find('a', string='Maps')
            if maps_link_tag:
                maps_popup_url = maps_link_tag.get('href')

                # Extract coordinates from the URL
                match = re.search(r'lat=([-\d.]+)&lng=([-\d.]+)', maps_popup_url)
                if match:
                    latitude = match.group(1)
                    longitude = match.group(2)
                    return latitude, longitude

            return None  # Coordinates not found
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    ####################################################
    # Return an array of extant coaster page links
    ####################################################
    def get_extant_pages(link):
        response = requests.get(link)  # Get Response
        soup = bs(response.text, "html.parser")  # Create Responser
        num_pages = soup.body.section.select_one("div:nth-child(3)").select_one(
            "a:nth-child(5)").get_text()  # Get number of pages of existant coasters
        _ = [None] * (int(num_pages))  # Array of existing coaster pages
        _[0] = link
        prev_page = link
        for i in range(1, int(num_pages)):
            if i == 36:
                break
            response = requests.get(prev_page)  # Get Response
            soup = bs(response.text, "html.parser")  # Create Responser
            _[i] = "https://rcdb.com" + soup.body.section.select_one("div:nth-child(3)").find("a", string=">>").get(
                "href")
            prev_page = _[i]
            print("new page: " + _[i])
            time.sleep(randint(1, 5))
        return _

    ####################################################
    # Parse through a single page of existant coasters
    ####################################################
    def parse_extant_coasters_page(extant_link):
        response = requests.get(extant_link)
        soup = bs(response.text, "html.parser")  # Create Responser
        coasters_on_page = soup.body.section.find("div", {"class": "stdtbl rer"}).find("table").find_all(
            "tr")  # Find table references of coasters on the next page
        coaster_data_array = [[] for r in range(len(coasters_on_page))]  # Store data in an array
        # print(coaster_data_array)
        # num_extants = soup.body.find("table").select_one("tr:nth-child(1)").td.a.get_text()                              #Get total number of extisting coasters in the country

        ##For first coaster data stats##
        coaster_link = "https://rcdb.com" + coasters_on_page[1].select_one("td:nth-child(2)").a.get(
            "href")  # Next coaster link
        print("Getting the first coaster: " + str(0) + " at " + coaster_link)
        coaster_data_array[0] = Parser.parse_coaster(coaster_link)
        time.sleep(5)

        ##Get the next coaster data stats##
        for i in range(2, len(coasters_on_page)):
            ## If the coaster page contains no image (Clean up logic here in the future)
            if coasters_on_page[i].select_one("td:nth-child(1)").a.get("aria-label") == None:
                coaster_link = "https://rcdb.com" + coasters_on_page[i].select_one("td:nth-child(1)").a.get(
                    "href")  # Next coaster link
            else:
                coaster_link = "https://rcdb.com" + coasters_on_page[i].select_one("td:nth-child(2)").a.get(
                    "href")  # Next coaster link
            print("Getting the next coaster stats: " + str(i) + " at " + coaster_link + "\n\n")
            coaster_data_array[i] = Parser.parse_coaster(
                coaster_link)  # Get the next coaster data stats
            print(coaster_data_array[i])
            time.sleep(20)
            col_names = ['Name', 'Park', 'City', 'State', 'Country', 'Status', 'Status Date', 'Material', 'Seating',
                         'Thrill', 'Make', 'Model', 'Length', 'Height', 'Drop', 'Speed', 'Inversions', 'VerticalAngle',
                         'Duration', 'G-Force']
        _ = pd.DataFrame(coaster_data_array, columns=col_names)
        return _

    ####################################################
    # Parse through all the pages of existant coasters
    ####################################################
    def parse_extant_coasters():
        columns = ["Name", "Park", "City", "State", "Country", "Status", "Status Date", "Material", "Seating", "Thrill",
                   "Make", "Model", "Length", "Height", "Drop", "Speed", "Inversions", "VerticalAngle", "Duration",
                   "G-Force"]
        link = "https://rcdb.com/r.htm?ot=2&ex&ol=59"  # List of existing coasters in the US (page 1)
        response = requests.get(link)  # Get Response
        soup = bs(response.text, "html.parser")  # Create Responser
        num_extants = soup.body.find("table").select_one(
            "tr:nth-child(1)").td.a.get_text()  # Get total number of extisting coasters in the country
        pages = Parser.get_extant_pages(link)
        frames = [None] * len(pages)
        print("frames length: " + str(len(frames)))
        for i in range(len(pages)):
            frames[i] = Parser.parse_extant_coasters_page(pages[i])
            time.sleep(2)
        data_frame = pd.concat(frames)
        data_frame.set_axis(columns, axis=1)
        data_frame.to_csv("US_Coaster_Stats_2021.csv")

    #####################################################
    # Return an array of links to extant coasters from a state
    #####################################################
    def get_state_coasters_list(extant_link):
        response = requests.get(extant_link)  # Create response
        soup = bs(response.text, "html.parser")  # Parse response
        extants = soup.find("body").find("tbody").find_all("tr")  # Find table of extant coasters
        refs = [None] * len(extants)  # Create array of links to extant coasters
        for i in range(len(extants)):
            name = extants[i].select_one('td:nth-child(2)').find("a").get_text()
            ref = "https://rcdb.com" + extants[i].select_one('td:nth-child(2)').find("a").get("href")
            refs[i] = ref  # Populate the references array with the next reference
            print("Found " + name + " at " + ref)

    #####################################################
    # Return a link to the extant coasters of a state page
    # Must include a link to a state page
    #####################################################
    def get_state_extant_coasters_link(state_link):
        response = requests.get(state_link)  # Create response
        soup = bs(response.text, "html.parser")  # Parse the response
        name = soup.find("body").find("h1").get_text()
        time.sleep(randint(1, 2))
        extant_ref = soup.find("table").find_all("tr")  # Find tr's within the table body
        extant_ref = extant_ref[0].find("td").find("a").get("href")  # Extract first table reference to get the url href
        extant_ref = "https://rcdb.com" + extant_ref  # Format url
        print(name, "'s extant coasters are located at: ", extant_ref)
        return extant_ref

    ####################################################
    # Return a dictionary of links to State pages
    ####################################################
    def get_state_page_links(us_url):
        #us_url = "https://rcdb.com/location.htm?id=59"  # List of Coasters in the US
        response = requests.get(us_url)  # Create the response
        soup = bs(response.text, "html.parser")  # Parse the response
        states_table = soup.find("body").find("div", class_="stdtbl cen").find("table").find("tbody").find_all(
            "tr")  # Find the table of States
        #refs = [None] * len(states_table)  # Create array of refs
        refs = []
        for i in range(len(states_table)):  # Parse each State
            time.sleep(randint(0, 4))
            table_data = states_table[i].find_all("td")  # State table data sections
            td = table_data[0].find("a")  # State name and link section
            ref = "https://rcdb.com" + td.get('href')  # URL to State page
            name = td.get_text()  # State name
            refs.append({"name": name, "url": ref})  # Populate reference array with new url reference
            #print("The state of " + name + " is at " + ref)
        return refs


    def get_state_park_page_links():
#####################################################
# Main
#####################################################
def main():
    print(str(int(len("hello"))))
    # Parser.parse_coaster("https://rcdb.com/21371.htm")
    # Parser.parse_extant_coasters()     #Parse Coaster List
    #get_state_coasters_list("https://rcdb.com/r.htm?ot=2&df&ol=13833") # Get the list of existing coasters links State of Nevada
    #get_state_extant_coasters_link("https://rcdb.com/location.htm?id=13833") # Find the link to an existing coasters page in Nevada
    # get_state_extant_parks_link() # Get

if __name__ == '__main__':
    main()
