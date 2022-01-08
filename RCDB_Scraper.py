## RCDB WebScraper ##
#Created by: Austin Wright
#Creates a CSV of coasters stats

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import enum

#parse the coasters found on each state page
def parse_state_page(link,name):
  print("Parse " + name + " at "  + link)
  response = requests.get(link)
  soup = bs(response.text,"html.parser")
  extant_ref = soup.find("body").find("table", id_="counts")
  time.sleep(5)
  print(extant_ref)
  time.sleep(5)


#test the parse_state_page
def parse_state_page_tester():
  link = "https://rcdb.com/location.htm?id=13833"
  name = "Nevada"
  response = requests.get(link)
  soup = bs(response.text, "html.parser")
  extant_ref = soup.find("body").find("table").find_all("tr")
  time.sleep(5)
  extant_ref = extant_ref[0].find("td").find("a").get("href")
  extant_ref =  "https://rcdb.com" + extant_ref
  time.sleep(5)
  
#test the parser of state extant coasters using state nevada
def parse_extant_coasters_tester():
  link = "https://rcdb.com/r.htm?ot=2&ex&ol=13833" #state of nevada existant coasters
  response = requests.get(link)
  soup = bs(response.text, "html.parser")
  extants = soup.find("body").find("tbody").find_all("tr")
  time.sleep(5)
  for extant in extants:
    name = extant.select_one('td:nth-child(2)').find("a").get_text()
    time.sleep(5)
    ref = "https://rcdb.com" + extant.select_one('td:nth-child(2)').find("a").get("href")
    print("Parse " + name + " at "  + ref)
    time.sleep(5)
    


#test the parse coaster stats page
def parse_coaster_tester():
  link = "https://rcdb.com/103.htm" #The Desperado In Primn
  response = requests.get(link)
  soup = bs(response.text, "html.parser")
  stat_sections = soup.find("body").find_all("section")

  #getting the name
  Name = stat_sections[0].select_one("div:nth-child(1)").div.div.h1.get_text()

  #getting the meta data of the coaster (location)
  metas = stat_sections[0].select_one("div:nth-child(1)").div.div.find_all("a")
  Park = metas[0].get_text()
  City = metas[1].get_text()
  State = metas[2].get_text()
  Country = metas[3].get_text()
  

#parse the pages found on the US List of coasters on RCDB 
def parse_parent_pages():
    us_url = "https://rcdb.com/location.htm?id=59"#List of Coasters in the US
    response = requests.get(us_url)                           #Create the response 
    soup = bs(response.text, "html.parser")              #Parse the response
    states_table = soup.find("body").find("div", class_="stdtbl cen").find("table").find("tbody").find_all("tr")  #Find the table of states
    time.sleep(5)
    for state in states_table:                #Parse each state
      table_data = state.find_all("td") #State table data sections
      time.sleep(5)
      td = table_data[0].find("a")          #State name and link section
      ref = "https://rcdb.com" + td.get('href') #Link reference
      time.sleep(5)
      name = td.get_text()                        #State name
      print("Parsing the state of " + ref)
      parse_state_page(ref,name)
      time.sleep(10)

def main():
  #print("Heelo")
  #parse_extant_coasters_tester()
  #parse_state_page_tester()
  parse_coaster_tester()


if __name__ == '__main__':
    main()
