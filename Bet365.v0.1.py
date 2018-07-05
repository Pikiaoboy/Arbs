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

def format_1col(my_code):
    for t1 in test_1_col:
        text = l.find(text=re.compile('^'+t1+'$'))
        if text:
            return text
    return my_code.text
def format_2col(my_code):
    for t2 in test_2_col:
        text = l.find(text=re.compile('^'+t2+'$'))
        if text:
            return text
    return my_code.text
def format_3col(my_code):
    for t3 in test_3_col:
        text = l.find(text=re.compile('^'+t3+'$'))
        if text:
            return text
    return my_code.text
def format_4col(my_code):
    text_list = []
    for t4 in test_4_col:
        if my_code.find(text=re.compile(t4)):
            #line_header=l.find("span",class_="gl-MarketGroupButton_Text").text.strip()
            line_headers=my_code.find_all("div",class_="gl-MarketColumnHeader ")
            #line_details = l.find("table", {"class" : re.compile("single-event-table*")})
            line_names = my_code.find_all("div", class_="gl-ParticipantRowName ")
            line_lines = my_code.find_all("span", class_="gl-ParticipantCentered_Name")
            line_odds = my_code.find_all("span",class_="gl-ParticipantCentered_Odds")
            #print(len(line_headers),len(line_names),len(line_lines),len(line_odds))
            for i in range(len(line_headers)-1):
                for x in range(len(line_names)):
                    text_list.append(game_name+","+game_date+","+line_headers[i+1].text.strip()+","+line_names[x].text.strip()+" "+line_lines[x].text.strip()+","+line_odds[x].text.strip())
            #print(text_list)
            return text_list 
    return

def test_format(code_data):
    code_test = format_1col(code_data)
    if(code_test is None):
        code_test = format_2col(code_data)
        if(code_test is None):
            code_test = format_3col(code_data)
            if(code_test is None):
                code_test = format_4col(code_data)
                if(code_test is None):
                    return("data not found")
    return code_test 




test="C:\\Temp\\Results\\Bet365\\xml.xml"
test_1_col =["Alternative Handicaps"]
test_3_col =["Winning Margin","1st Quarter Lines","1st Half","Disposal Specials","Team Total Points","Team Total Goals","Team Goals (Bands)","Team Early Goal","1st Quarter Winning Margin","1st Quarter Winning Margin 5-Way","1st Quarter Team Total Points","Team - 1st Quarter Total Scoring"]
test_2_col =["Alternative Match Total"]
test_4_col =["Game Lines","Goal Scorers","1st Quarter Race to (Points)","Game Lines","1st Half Race to (Points)"]
len(test_1_col+test_2_col+test_3_col+test_4_col)
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

#Checks Market Group Name against list to work out what format the table is in
for l in lines:
    print(test_format(l))

print("Done")    
#for l in lines:
#     
l = lines[0]
#line_header=l.find("span",class_="gl-MarketGroupButton_Text").text.strip()
line_headers=l.find_all("div",class_="gl-MarketColumnHeader ")
#line_details = l.find("table", {"class" : re.compile("single-event-table*")})
line_names = l.find_all("div", class_="gl-ParticipantRowName ")
line_lines = l.find_all("span", class_="gl-ParticipantCentered_Name")
line_odds = l.find_all("span",class_="gl-ParticipantCentered_Odds")
print(len(line_headers),len(line_names),len(line_lines),len(line_odds))
for i in range(len(line_headers)-1):
    for x in range(len(line_names)):
        print(game_name+","+game_date+","+line_headers[i+1].text.strip()+","+line_names[x].text.strip()+" "+line_lines[x].text.strip()+","+line_odds[x].text.strip())

    # with open(game_file, 'a') as gf:
        # gf.write(game_name+","+game_date+","+line_header+","+line_names[i].text.strip()+","+line_lines[i].text.strip()+"\n")
        
print("complete")


# time.sleep(3)
# b_driver.back()
# time.sleep(3)
# game_links = b_driver.find_elements_by_xpath("//div[@class='sl-CouponFixtureLinkParticipant_Name ']")


#make list of 3-column and 2-column odds?
#split odd-getting into functions
#make list at top of script to only search existing 
for t in lines:
    t.get_text(',').split(',')
