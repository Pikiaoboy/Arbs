import csv
from selenium import webdriver
from bs4 import BeautifulSoup,Comment
import time 
import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

test="C:\\Temp\\Results\\Crownbet\\xml.xml"
#Set website base url
base_url = "https://crownbet.com.au"
sports_url = base_url+"/sports-betting"
sport="Australian Rules"

#Set output location
base_file = "C:\\Temp\\Results\\Crownbet\\"

#load browser driver 
cb_driver = webdriver.Chrome()
cb_driver.get(sports_url)

#parse the main page and parse sports list to find sport
new_soup = BeautifulSoup(cb_driver.page_source, 'lxml')
sports=new_soup.find_all("li",class_="sport-button")
for i in sports:
    #print(i.text)
    if i.text.strip() == "Australian Rules":
        ahref=i.a.get('href')

#adjust url and go to sports specific page
sports_link=base_url+ahref
cb_driver.get(sports_link)
matches_soup = BeautifulSoup(cb_driver.page_source, 'lxml')

#get list of all matches in sport (TEST to confirm ALL sports listed)
matches=matches_soup.find_all("span", class_="other-matches")

#parse through each match
for match in matches:
    #match = matches[0]
    match_href=base_url+match.a.get('href')
    cb_driver.get(match_href)

    #clicks through page to expand all panes
    clicks=cb_driver.find_elements_by_xpath("//*[@class='drop-down-header clearfix closed  ']")
    for i in range(len(clicks)):
        print(i)
        clicks[len(clicks)-1].click()
        time.sleep(1)
        clicks=cb_driver.find_elements_by_xpath("//*[@class='drop-down-header clearfix closed  ']")

    #once all expanded, re-parse page
    match_soup = BeautifulSoup(cb_driver.page_source, 'lxml')
    #get static details - teams, date and time
    game_name = match_soup.find("span", class_="item match-name").text.strip()
    game_date = match_soup.find("span", class_="item tv").text.strip()

    game_file = base_file+game_name+".csv"
    with open(game_file,'w') as f:
        f.write("Game,Date,Header,Name,Line\n")
        f.close()

    #match_soup.find_all("div", class_="title multiple-events") 
    lines = match_soup.find_all("div", class_="middle-section match-list") 
    for l in lines:    
        #l = lines[0]
        line_header=l.find("div",class_="title multiple-events").text.strip()
        line_details = l.find("table", {"class" : re.compile("single-event-table*")})
        line_names = line_details.find_all("span", class_="outcome-anchor-text")
        line_lines = line_details.find_all("span", class_="single-bet-amount")
        for i in range(len(line_names)):
            with open(game_file, 'a') as gf:
                gf.write(game_name+","+game_date+","+line_header+","+line_names[i].text.strip()+","+line_lines[i].text.strip()+"\n")
print("complete")