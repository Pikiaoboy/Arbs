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

test="C:\\Temp\\Results\\Bet365\\xml.xml"
#Set website base url
base_url = "https://www.bet365.com"
sports_url = base_url+"/sports-betting"
sport="Australian Rules"

#Set output location
base_file = "C:\\Temp\\Results\\Bet365\\"

#load browser driver 
b_driver = webdriver.Chrome()
b_driver.get(base_url)
b_driver.find_element_by_xpath("//*[@title='Sports Betting']").click()
time.sleep(10)

#parse the main page and parse sports list to find sport
b_driver.find_element_by_xpath("//div[@class='wn-Classification ' and contains(text(),'Australian Rules')]").click()
time.sleep(3)

#Select first link to load game lines page
b_driver.find_element_by_xpath("//div[@class='sm-CouponLink_Label ' and contains(text(),'Game Lines')]").click()
time.sleep(6)
#Get all markets links
game_links = b_driver.find_elements_by_xpath("//div[@class='sl-CouponFixtureLinkParticipant_Name ']")
game_links_len=len(game_links)
print(game_links_len)
#TAB
#for i in range(0,game_links_len-1):
game_link = game_links[0]
game_link.click()
time.sleep(5)
#<TODO> Expand match lines
#clicks through page to expand all panes
clicks=b_driver.find_elements_by_xpath("//div[contains(@class,'gl-MarketGroupButton') and not(contains(@class,'gl-MarketGroup_Open'))]")
for i in range(len(clicks)):
    #print(i)
    clicks[len(clicks)-1].click()
    time.sleep(2)
    clicks=b_driver.find_elements_by_xpath("//div[contains(@class,'gl-MarketGroupButton') and not(contains(@class,'gl-MarketGroup_Open'))]") 

# <TODO> Parse match lines
#once all expanded, re-parse page
match_soup = BeautifulSoup(b_driver.page_source, 'lxml')
#get static details - teams, date and time
game_name = match_soup.find("div", class_="cl-BreadcrumbTrail_Breadcrumb cl-BreadcrumbTrail_BreadcrumbCurrent cl-BreadcrumbTrail_BreadcrumbTruncate ").text.strip()
game_date = match_soup.find("div", class_="cm-MarketGroupExtraData_TimeStamp ").text.strip()

game_file = base_file+game_name+".csv"
with open(game_file,'w') as f:
    f.write("Game,Date,Header,Name,Line\n")
    f.close()

#match_soup.find_all("div", class_="title multiple-events") 
lines = match_soup.find_all("div", class_="gl-MarketGroup ") 
#for l in lines:    
l = lines[1]
#line_header=l.find("span",class_="gl-MarketGroupButton_Text").text.strip()
line_headers=l.find_all("div",class_="gl-MarketColumnHeader ")
#line_details = l.find("table", {"class" : re.compile("single-event-table*")})
line_names = l.find_all("div", class_="gl-ParticipantRowName ")
line_lines = l.find_all("span", class_="gl-ParticipantCentered_Name")
line_odds = l.find_all("span",class_="gl-ParticipantCentered_Odds")
print(len(line_headers),len(line_names),len(line_lines),len(line_odds))
for i in range(len(line_headers)-1):
    for x in range(len(line_names)):
        print(game_name+","+game_date+","+line_headers[i+1].text.strip()+","+line_names[x].text.strip()+" "+line_lines[x].text.strip()+","+line_odds[x].text.strip()+"\n")

    # with open(game_file, 'a') as gf:
        # gf.write(game_name+","+game_date+","+line_header+","+line_names[i].text.strip()+","+line_lines[i].text.strip()+"\n")
        
print("complete")


# time.sleep(3)
# b_driver.back()
# time.sleep(3)
# game_links = b_driver.find_elements_by_xpath("//div[@class='sl-CouponFixtureLinkParticipant_Name ']")






# new_soup = BeautifulSoup(b_driver.page_source, 'lxml')
# for i in sports:
#     #print(i.text)
#     if i.text.strip() == "Australian Rules":
#         ahref=i.a.get('href')

# #adjust url and go to sports specific page
# sports_link=base_url+ahref
# b_driver.get(sports_link)
# matches_soup = BeautifulSoup(b_driver.page_source, 'lxml')

# #get list of all matches in sport (TEST to confirm ALL sports listed)
# matches=matches_soup.find_all("span", class_="other-matches")

# #parse through each match
# for match in matches:
#     #match = matches[0]
#     match_href=base_url+match.a.get('href')
#     b_driver.get(match_href)

#     #clicks through page to expand all panes
#     clicks=b_driver.find_elements_by_xpath("//*[@class='drop-down-header clearfix closed  ']")
#     for i in range(len(clicks)):
#         print(i)
#         clicks[len(clicks)-1].click()
#         time.sleep(1)
#         clicks=b_driver.find_elements_by_xpath("//*[@class='drop-down-header clearfix closed  ']")

