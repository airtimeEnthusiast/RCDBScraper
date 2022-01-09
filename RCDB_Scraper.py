## RCDB WebScraper ##
#Created by: Austin Wright
#Creates a CSV of coasters stats

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from random import seed
from random import randint

seed(1)

#####################################################
#Return an array of links to extant coasters from a state
#####################################################
#def parse_extant_coasters(extant_link):
  #link = "https://rcdb.com/r.htm?ot=2&ex&ol=13833" #state of nevada existant coasters
 # response = requests.get(extant_link)      #Create response
  #soup = bs(response.text, "html.parser") #Parse response
  #extants = soup.find("body").find("tbody").find_all("tr")  #Find table of extant coasters
  #refs = [None] * len(extants)                      #Create array of links to extant coasters
  #for i in range (len(extants)):
    #name = extants[i].select_one('td:nth-child(2)').find("a").get_text()
   # ref = "https://rcdb.com" + extants[i].select_one('td:nth-child(2)').find("a").get("href")
    #refs[i] = ref                                             #Populate the references array with the next reference
    #print("Parse " + name + " at "  + ref)


#####################################################
#Return a link to the extant coasters of a state page
#Must include a link to a state page
#####################################################
#def parse_state_extant_coasters_link(state_link):
  #link = "https://rcdb.com/location.htm?id=13833" #State page with the number of extant coasters, defunct
  #name = "Nevada"
  #response = requests.get(state_link)           #Create response
  #soup = bs(response.text, "html.parser")    #Parse the response
  #extant_ref = soup.find("body").find("table").find_all("tr") #Find tr's within the table body
  #extant_ref = extant_ref[0].find("td").find("a").get("href") #Extract first table reference to get the url href
  #extant_ref =  "https://rcdb.com" + extant_ref  #Format url
  #return extant_ref



####################################################
#Return an array of links to State pages
####################################################
#def parse_state_pages():
 # us_url = "https://rcdb.com/location.htm?id=59" #List of Coasters in the US
  #response = requests.get(us_url)                           #Create the response 
  #soup = bs(response.text, "html.parser")             #Parse the response
  #states_table = soup.find("body").find("div", class_="stdtbl cen").find("table").find("tbody").find_all("tr")  #Find the table of States
  #refs = [None]* len(states_table)                          #Create array of refs
  #for i in range (len(states_table)):                     #Parse each State
    #time.sleep(randint(0,10))
    #table_data = states_table[i].find_all("td")    #State table data sections
    #td = table_data[0].find("a")                              #State name and link section
    #ref = "https://rcdb.com" + td.get('href')        #URL to State page
    #name = td.get_text()                                           #State name
    #refs[i] = ref                                                       #Populate reference array with new url reference
    #print("Parsing the state of " + name +  " at " + ref)
  #return refs


#Parser class
class Parser():

 coaster_data_array = [[]]
 columns = ["Name","Park","City","State","Country","Status","Material","Seating","Thrill","Make","Model","Length","Height","Drop","Speed","Inversions","VerticalAngle","Duration","G-Force"]
 
#####################################################
#Return a data array of coaster stats
#Must include a link to a coaster
#####################################################
 def parse_coaster(coaster_link):
  ##The stats of the data array##
    Name = None
    Park = None
    City = None
    State = None
    Country = None
    Status_type = None
    #Status_date = None
    Material = None
    Positioning = None
    Thrill = None
    Make = None
    Model = None
    Length = None
    Height = None
    Drop = None
    Speed = None
    Inversions = None
    VerticalAngle = None
    Duration = None
    GForce = None

    ##Building the response##
    response = requests.get(coaster_link)
    soup = bs(response.text, "html.parser")
    stat_sections = soup.find("body").find_all("section")
    time.sleep(randint(1,10))

    ##getting the name##
    Name = stat_sections[0].select_one("div:nth-child(1)").div.div.h1.get_text()
  
    ##getting the meta data of the coaster (location)##
    metas = stat_sections[0].select_one("div:nth-child(1)").div.div.find_all("a")
    Park = metas[0].get_text()
    City = metas[1].get_text()
    State = metas[2].get_text()
    Country = metas[3].get_text()
    time.sleep(randint(1,10))
  
    ##get operational status ##
    Status_type =  stat_sections[0].select_one("div:nth-child(1)").div.p.a.get_text()
    #Status_date =  stat_sections[0].select_one("div:nth-child(1)").div.p.time["datetime"]
  
    ##get type##
    Types = stat_sections[0].select_one("div:nth-child(1)").div.ul.find_all("li")
    Material = Types[1].a.get_text()
    Positioning = Types[2].a.get_text()
    Thrill  = Types[3].a.get_text()
    time.sleep(randint(1,10))

    ##get make and model##
    Types = stat_sections[0].select_one("div:nth-child(1)").div.find("div",class_="scroll").find("p").find_all("a")
    Make = Types[0].get_text()
    Model = Types[2].get_text()
    time.sleep(randint(1,10))

    ##get track stats##
    ## https://github.com/willcliffy/RCDB-Scraper/blob/main/scraper.py##
    ## Lines 85-105 were borrowed from this file for this section since I had trouble parsing this tbody##
    specs = list(soup.find('table', {'class' : 'stat-tbl'}).strings)
    for i in range (len(specs)):
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
      else:
          continue
      i += 1
      time.sleep(randint(1,10))
    ##Return the data array##
    data = [Name,Park,City,State,Country,Status_type,Material,Positioning,Thrill,Make,Model,Length,Height,Drop,Speed,Inversions,VerticalAngle,Duration,GForce]
    #print(data)
    return data
  

  ####################################################
  #Parse through a single page of existant coasters
  ####################################################
  #def parse_extant_coasters_link():
    #country_link = "https://rcdb.com/location.htm?id=59" #List of Coasters in the US test
    ##Get Existant Link##
    #response = requests.get(country_link)       #Get Response
    #soup = bs(response.text,"html.parser")     #Create Responser 
    #num_extants = soup.body.find("table").select_one("tr:nth-child(1)").td.a.get_text()                                         #Get total number of extisting coasters in the country
    #extants_link = "https://rcdb.com" +  soup.body.find("table").select_one("tr:nth-child(1)").td.a.get("href") #Get link to all the existanting coasters
    ##Get Existant Coasters##
    #extant_link = "https://rcdb.com/r.htm?ot=2&ex&ol=59"
    #response = requests.get(extant_link)
    #soup = bs(response.text,"html.parser")     #Create Responser
    #coasters_on_page = soup.body.section.find("div", {"class" : "stdtbl rer"}).find("table").find_all("tr") #Find table references of coasters on the next page
    #for i in range(1,len(coasters_on_page):
      #coaster_link = "https://rcdb.com" + coasters_on_page[1].select_one("td:nth-child(2)").a.get("href")
  ####################################################
  #Return a link to the next single page of existant coasters
  ####################################################
 def get_extant_coasters_link(prev_page):
  response = requests.get(prev_page)                             #Get Response
  soup = bs(response.text,"html.parser")                      #Create Responser 
  next_page = "https://rcdb.com" + soup.body.section.select_one("div:nth-child(3)").select_one("a:nth-child(6)").get("href")
  if next_page != None:
    return next_page
  else:
    return None

  ####################################################
  #Return an array of extant coaster page links  
  ####################################################
 def get_extant_pages(link):
  response = requests.get(link)                                      #Get Response
  soup = bs(response.text,"html.parser")                      #Create Responser 
  num_pages =  soup.body.section.select_one("div:nth-child(3)").select_one("a:nth-child(5)").get_text()          #Get number of pages of existant coasters
  extant_pages = [None] * int(num_pages)                       #Array of existing coaster pages
  for i in range (1,int(num_pages)):
    if i == 1:
     extant_pages[i] = Parser.get_extant_coasters_link(link)
    else:
      extant_pages[i] = Parser.get_extant_coasters_link(extant_pages[i-1])
    print(extant_pages[i])
    time.sleep(randint(1,5))
  return extant_pages
    
  ####################################################
  #Parse through a single page of existant coasters
  ####################################################
 def parse_extant_coasters_page(extant_link):
  response = requests.get(extant_link)
  soup = bs(response.text,"html.parser")     #Create Responser
  coasters_on_page = soup.body.section.find("div", {"class" : "stdtbl rer"}).find("table").find_all("tr") #Find table references of coasters on the next page
  #num_extants = soup.body.find("table").select_one("tr:nth-child(1)").td.a.get_text()                               #Get total number of extisting coasters in the country
  coaster_data_array = [[0 for c in range(19)] for r in range(len(coasters_on_page))]                                       #Store data in an array
  for i in range(1,len(coasters_on_page)):
    coaster_link = "https://rcdb.com" + coasters_on_page[i].select_one("td:nth-child(2)").a.get("href")    #Next coaster link
    coaster_data_array[i] = Parser.parse_coaster(coaster_link)                                                                           #Get the next coaster data stats
    print("Running Getting the next coaster: " + i + " of " + len(coasters_on_page))                                            
    print(coaster_data_array[i])        
    time.sleep(randint(1,10))
    if(i == 3):
      break
 df = pd.DataFrame(coaster_data_array, columns)
 df.to_csv("US_Coaster_Stats_2021")
    

  ####################################################
  # Parse through  all the pages of existant coasters     
  ####################################################
 def parse_extant_coasters():
  link = "https://rcdb.com/r.htm?ot=2&ex&ol=59" #List of existing coasters in the US (page 1)
  #response = requests.get(link)                             #Get Response
  #soup = bs(response.text,"html.parser")             #Create Responser 
  #num_extants = soup.body.find("table").select_one("tr:nth-child(1)").td.a.get_text()    #Get total number of extisting coasters in the country
  #pages = Parser.get_extant_pages(link)
  #for i in range(len(pages)):
  Parser.parse_extant_coasters_page(link)

                 
#####################################################
#Main
#####################################################
def main():
  #print("Heelo")
  Parser.parse_extant_coasters()
  #parse_coaster()
  #parse_extant_coasters_tester()
  #parse_state_page_tester()
  #parse_coaster_tester()
  #parse_extant_coasters_link()
  #link = "https://rcdb.com/103.htm" #The Desperado In Primn
  #columns = ["Name","Park","City","State","Country","Status","Material","Seating","Thrill","Make","Model","Length","Height","Drop","Speed","Inversions","VerticalAngle","Duration","G-Force"]
  #data = [[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
  #desperado_data = parse_coaster("https://rcdb.com/103.htm")
  #df = pd.DataFrame(desperado_data
  #us_state_refs = parse_state_pages()
  #For Each State
  #for i in range(len(us_state_refs)):
    #For each coaster in the next State
    #extant_link = parse_state_extant_coasters_link(us_state_refs[i])
    
    
if __name__ == '__main__':
    main()
