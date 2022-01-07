#from bs4 import BeautifulSoup
#import requests
#import csv
#import pandas as pd

#Testing a wiki table
#page = requests.get('https://en.wikipedia.org/wiki/Metropolitan_statistical_area')
#soup = BeautifulSoup(page.text, 'html.parser')
#table = soup.findAll('table',{'class':"wikitable"})
#table_soup = soup.findAll('table')[0].findAll('tr')
#df = pd.read_html(str(table))
#df = pd.DataFrame(df[0])
#df.drop(["Rank"],axis=1)
#df.to_csv('metros.csv')

#Inspired by Will Clifford's RCDB Scraper all rights go to his code
#https://github.com/willcliffy/RCDB-Scraper/blob/d182ff4121b0d81e761e7b96fe038b2c1a1c5782/scraper.py#L121

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import enum

#Roller Coaster Data Base Scraper Class
class RCDB_Parser(enum.Enum):
  
  def parse_page(soup):
    meta = soup.body.section.div.div
    Name = meta.div.h1.string
    
    tmp = meta.div.find_all("a")
    
    if len(tmp) < 4:
      return 0
    
    Park = tmp[-4].string
    City = tmp[-3].string
    State = tmp[-2].string
    Country = tmp[-1].string
    
    OperatingSince = None
    OperatingUntil = None
    
    Status = meta.p.a.string
    
    if Status == "Operating":
      if meta.p.time != None:
        OperatingSince = meta.p.time['datetime']
      elif Status == "Operated":
        tmp = meta.p.find_all('time')
        if len(tmp) == 2:
          OpSince = tmp[0]['datatime']
          OpUntil = tmp[1]['datatime']
      elif Status == "Under Construction":
        pass
      elif Status == "In Business":
        pass


def parse_pages():
    us_url = "https://rcdb.com/location.htm?id=59"
    response = requests.get(us_url)
    soup = bs(response.text, "html.parser")
    states_table = soup.find("body").find("div", class_="stdtbl cen").find("table").find("tbody").find_all("tr")
    for state in states_table:
      table_data = state.find_all("td")
      ref = table_data[0].find("a")
      print(ref)

    
    

def main():
  #print("Heelo")
  parse_pages()


if __name__ == '__main__':
    main()
