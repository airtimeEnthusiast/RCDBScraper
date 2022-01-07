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
  time.sleep(10)
  extant_ref = soup.find("body").find("table", id_="counts")
  print(extant_ref)


#test the parse_state_page
def parse_state_page_tester():
  link = "https://rcdb.com/location.htm?id=13833"
  name = "Nevada"
  response = requests.get(link)
  soup = bs(response.text, "html.parser")


#parse the pages found on the US List of coasters on RCDB 
def parse_pages():
    us_url = "https://rcdb.com/location.htm?id=59" #List of Coasters in the US
    response = requests.get(us_url)                           #Create the response 
    soup = bs(response.text, "html.parser")             #Parse the response
    states_table = soup.find("body").find("div", class_="stdtbl cen").find("table").find("tbody").find_all("tr")  #Find the table of states
    for state in states_table:                #Parse each state
      table_data = state.find_all("td") #State table data sections
      td = table_data[0].find("a")          #State name and link section
      ref = "https://rcdb.com" + td.get('href') #Link reference
      name = td.get_text()                        #State name
      parse_state_page(ref,name)
      print("next state...")
      time.sleep(10)
    

def main():
  #print("Heelo")
  parse_pages()


if __name__ == '__main__':
    main()
