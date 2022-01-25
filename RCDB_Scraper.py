## RCDB WebScraper ##
#Created by: Austin Wright
#Creates a CSV of coasters stats

import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from random import seed
from random import randint

seed(1)

#Parser class: Methods are 
class Parser():

 coaster_data_array = [[]]
 coaster_extant_pages = []

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
    Status_date = None
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

    ##getting the name##
    Name = stat_sections[0].select_one("div:nth-child(1)").div.div.h1.get_text()
  
    ##getting the meta data of the coaster (location)##
    metas = stat_sections[0].select_one("div:nth-child(1)").div.div.find_all("a")
    Park = metas[0].get_text()
    City = metas[1].get_text()
    State = metas[2].get_text()
    Country = metas[3].get_text()
    #time.sleep(randint(1,3))
  
    ##get operational status ##
    Status_type =  stat_sections[0].select_one("div:nth-child(1)").div.p.a.get_text()
    if stat_sections[0].select_one("div:nth-child(1)").div.p.time != None:
     Status_date =  stat_sections[0].select_one("div:nth-child(1)").div.p.time["datetime"]
  
    ##get type##
    Types = stat_sections[0].select_one("div:nth-child(1)").div.ul.find_all("li")
    Material = Types[1].a.get_text()
    Positioning = Types[2].a.get_text()
    #If Thrill type is displayed
    if len(Types) > 3:
     Thrill  = Types[3].a.get_text()

    ##get make and model##
    # soup search meta.ul.strings:
    Types = stat_sections[0].select_one("div:nth-child(1)").div.find("div",class_="scroll")
    if Types != None:
     TypesCheck = Types.get_text().split(":")
     Types = stat_sections[0].select_one("div:nth-child(1)").div.find("div",class_="scroll").find("p").find_all("a")
     for i in range(0, len(Types)):
      if TypesCheck[i].find("Make") != -1:
       Make = Types[i].get_text()
      if TypesCheck[i].find("Model") != -1:
       Model = Types[i].get_text()
    #time.sleep(randint(1,3))

    ##get track stats##
    ## https://github.com/willcliffy/RCDB-Scraper/blob/main/scraper.py##
    ## Lines 85-105 were borrowed from this file for this section since I had trouble parsing this tbody##
    if soup.find('table', {'class' : 'stat-tbl'}) != None:
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
    
    ##Return the data array##
    _ = [Name,Park,City,State,Country,Status_type,Status_date,Material,Positioning,Thrill,Make,Model,Length,Height,Drop,Speed,Inversions,VerticalAngle,Duration,GForce]
    print(_)
    return _


  ####################################################
  #Return an array of extant coaster page links  
  ####################################################
 def get_extant_pages(link):
  response = requests.get(link)                                      #Get Response
  soup = bs(response.text,"html.parser")                      #Create Responser 
  num_pages =  soup.body.section.select_one("div:nth-child(3)").select_one("a:nth-child(5)").get_text()          #Get number of pages of existant coasters
  _ = [None] * (int(num_pages))                       #Array of existing coaster pages
  _[0] = link
  prev_page = link
  for i in range (1,int(num_pages)):
   if i == 36:
       break
   response = requests.get(prev_page)                             #Get Response
   soup = bs(response.text,"html.parser")                      #Create Responser
   _[i] = "https://rcdb.com" + soup.body.section.select_one("div:nth-child(3)").find("a", string=">>").get("href")
   prev_page = _[i]
   print("new page: " + _[i])
   time.sleep(randint(1,5))
  return _


  
  ####################################################
  #Parse through a single page of existant coasters
  ####################################################
 def parse_extant_coasters_page(extant_link):
  response = requests.get(extant_link)
  soup = bs(response.text,"html.parser")                                                                                                                #Create Responser
  coasters_on_page = soup.body.section.find("div", {"class" : "stdtbl rer"}).find("table").find_all("tr") #Find table references of coasters on the next page
  coaster_data_array = [[] for r in range(len(coasters_on_page))]                                                                       #Store data in an array
  #print(coaster_data_array)
  #num_extants = soup.body.find("table").select_one("tr:nth-child(1)").td.a.get_text()                              #Get total number of extisting coasters in the country
  
  ##For first coaster data stats##
  coaster_link = "https://rcdb.com" + coasters_on_page[1].select_one("td:nth-child(2)").a.get("href")    #Next coaster link
  print("Getting the first coaster: " + str(0) + " at " + coaster_link)
  coaster_data_array[0] = Parser.parse_coaster(coaster_link)
  time.sleep(5)

  ##Get the next coaster data stats##                                            
  for i in range(2,len(coasters_on_page)):
    ## If the coaster page contains no image (Clean up logic here in the future)
   if coasters_on_page[i].select_one("td:nth-child(1)").a.get("aria-label") == None:
    coaster_link = "https://rcdb.com" + coasters_on_page[i].select_one("td:nth-child(1)").a.get("href")    #Next coaster link
   else:
    coaster_link = "https://rcdb.com" + coasters_on_page[i].select_one("td:nth-child(2)").a.get("href")    #Next coaster link
   print("Getting the next coaster stats: " + str(i) + " at " + coaster_link + "\n\n")
   coaster_data_array[i] = Parser.parse_coaster(coaster_link)                   #Get the next coaster data stats                                            
   print(coaster_data_array[i])
   time.sleep(20)
   col_names = ['Name','Park','City','State','Country','Status','Status Date','Material','Seating','Thrill','Make','Model','Length','Height','Drop','Speed','Inversions','VerticalAngle','Duration','G-Force']
  _ = pd.DataFrame(coaster_data_array, columns = col_names)
  return _

  ####################################################
  # Parse through  all the pages of existant coasters     
  ####################################################
 def parse_extant_coasters():
  columns = ["Name","Park","City","State","Country","Status","Status Date","Material","Seating","Thrill","Make","Model","Length","Height","Drop","Speed","Inversions","VerticalAngle","Duration","G-Force"]
  link = "https://rcdb.com/r.htm?ot=2&ex&ol=59" #List of existing coasters in the US (page 1)
  response = requests.get(link)                             #Get Response
  soup = bs(response.text,"html.parser")             #Create Responser 
  num_extants = soup.body.find("table").select_one("tr:nth-child(1)").td.a.get_text()    #Get total number of extisting coasters in the country
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
#Main
#####################################################
def main():

 #print(str(int(len("hello"))))
 #Parser.parse_coaster("https://rcdb.com/1530.htm")
 Parser.parse_extant_coasters()     #Parse Coaster List


 ######
# Tester
######
def test_oddoties(extant_link):
 response = requests.get(extant_link)
 soup = bs(response.text,"html.parser")     #Create Responser
 coasters_on_page = soup.body.section.find("div", {"class" : "stdtbl rer"}).find("table").find_all("tr") #Find table references of coasters on the next page
 print(str(len(coasters_on_page)) + " coasters on page " + extant_link)
 #num_extants = soup.body.find("table").select_one("tr:nth-child(1)").td.a.get_text()    #Get total number of extisting coasters in the country
 coaster_data_array = [[] for r in range((len(coasters_on_page) - 1))]                                       #Store data in an array
 

 ##For first coaster data stats##
 coaster_link = "https://rcdb.com" + coasters_on_page[1].select_one("td:nth-child(2)").a.get("href")    #Next coaster link
 print("Getting the first coaster: " + str(0) + " at " + coaster_link)
 coaster_data_array[0] = Parser.parse_coaster(coaster_link)
 #time.sleep(2)

 ##Get the next coaster data stats##                                            
 for i in range(2,len(coasters_on_page)):
  if coasters_on_page[i].select_one("td:nth-child(1)").a.get("aria-label") == None:
   print("No picture!!!")
   coaster_link = "https://rcdb.com" + coasters_on_page[i].select_one("td:nth-child(1)").a.get("href")    #Next coaster link
  else:
   coaster_link = "https://rcdb.com" + coasters_on_page[i].select_one("td:nth-child(2)").a.get("href")    #Next coaster link
  print("Getting the next coaster: " + str(i) + " at " + coaster_link)
  coaster_data_array[i - 1] = Parser.parse_coaster(coaster_link)                   #Get the next coaster data stats                                            
  print(coaster_data_array[i - 1])
  col_names = ['Name','Park','City','State','Country','Status','Status Date','Material','Seating','Thrill','Make','Model','Length','Height','Drop','Speed','Inversions','VerticalAngle','Duration','G-Force']
  _ = pd.DataFrame(coaster_data_array,columns = col_names)
 return _
    

#####################################################
#Return an array of links to extant coasters from a state
#####################################################
#def get_state_coasters_list(extant_link):
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
#def get_state_extant_coasters_link(state_link):
  #link = "https://rcdb.com/location.htm?id=13833" #State page with the number of extant coasters, defunct, etc
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
    
if __name__ == '__main__':
    main()
