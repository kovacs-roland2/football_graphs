from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

df = pd.DataFrame (columns = ['Name','Seasion','Club','Position','Nationality'])

#basic driver settings
GECKODRIVER_PATH = ''

options = Options()
#options.headless = True
#firefox profile
fp= ""
driver = webdriver.Firefox(executable_path = GECKODRIVER_PATH, options = options, firefox_profile=fp)
wait = WebDriverWait(driver,10)
driver.set_window_size(1920, 1080)
driver.maximize_window()
actionchain = ActionChains(driver)

driver.get("https://www.premierleague.com/players")

#collecting the season attribute
wait.until(expected_conditions.element_to_be_clickable((By.XPATH,"//div[@data-dropdown-current='compSeasons']")))
time.sleep(1)
driver.find_element_by_xpath("//div[@data-dropdown-current='compSeasons']").click()
time.sleep(3)
seasons = driver.find_elements_by_xpath("//ul[@data-dropdown-list='compSeasons']/li")
number_of_seasons = len(seasons)

#loop through seasons
for s in range(number_of_seasons):
    current_season = seasons[s]
    player_season = current_season.get_attribute("data-option-name")
    driver.execute_script("arguments[0].click();", current_season)

    #scraping the data
    for i in range(20):
        num = i+1
        #club selection
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH,"//div[@data-dropdown-current='clubs']")))
        time.sleep(1)
        driver.find_element_by_xpath("//div[@data-dropdown-current='clubs']").click()
        time.sleep(3)
        clubs = driver.find_elements_by_xpath("//ul[@data-dropdown-list='clubs']/li")
        current_club = clubs[num]
        player_team = current_club.text
        print(player_season, player_team)
        driver.execute_script("arguments[0].click();", current_club)

        #player information from table
        time.sleep(3)
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH,"//tbody[@class='dataContainer indexSection']")))
        table = driver.find_element_by_xpath("//tbody[@class='dataContainer indexSection']")
        number_of_rows = table.find_elements_by_xpath("//tr")
        number_of_rows = len(number_of_rows)
        
        for row in range(number_of_rows-1):
            time.sleep(1)
            player_name = table.find_element_by_xpath("//tr[" + str(row + 1) + "]/td[1]").text
            player_position = table.find_element_by_xpath("//tr[" + str(row + 1) + "]/td[2]").text
            player_nationality = table.find_element_by_xpath("//tr[" + str(row + 1) + "]/td[3]").text
            #print(player_name, player_season, player_team, player_position, player_nationality)
            df_to_add = pd.DataFrame([[player_name, player_season, player_team, player_position, player_nationality]], columns = ['Name','Seasion','Club','Position','Nationality'])
            df = df.append(df_to_add, ignore_index=True)
        
        time.sleep(3)

    #save df to excel file
    df.to_excel("") 

    time.sleep(3)


