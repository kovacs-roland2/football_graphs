from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

df = pd.DataFrame (columns = ['Manager','Club','Nationality'])

#basic driver settings
GECKODRIVER_PATH = ''

options = Options()
#options.headless = True
#firefox profile path
fp= ""
driver = webdriver.Firefox(executable_path = GECKODRIVER_PATH, options = options, firefox_profile=fp)
wait = WebDriverWait(driver,10)
driver.set_window_size(1920, 1080)
driver.maximize_window()
actionchain = ActionChains(driver)

driver.get("https://www.premierleague.com/managers")

#collecting the season attribute
wait.until(expected_conditions.element_to_be_clickable((By.XPATH,"//div[@data-dropdown-current='compSeasons']")))
time.sleep(1)
driver.find_element_by_xpath("//div[@data-dropdown-current='compSeasons']").click()
time.sleep(3)
seasons = driver.find_elements_by_xpath("//ul[@data-dropdown-list='compSeasons']/li")
seasons = seasons[1:]
number_of_seasons = len(seasons)

#loop through seasons
for s in range(number_of_seasons):
    current_season = seasons[s]
    manager_season = current_season.get_attribute("data-option-name")
    driver.execute_script("arguments[0].click();", current_season)

    #scraping the data
    for i in range(20):
        num = i+1
        #club selection
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH,"//div[@data-dropdown-current='teams']")))
        time.sleep(1)
        driver.find_element_by_xpath("//div[@data-dropdown-current='teams']").click()
        time.sleep(3)
        clubs = driver.find_elements_by_xpath("//ul[@data-dropdown-list='teams']/li")
        current_club = clubs[num]
        manager_team = current_club.text
        print(manager_season, manager_team)
        driver.execute_script("arguments[0].click();", current_club)

        #player information from table
        time.sleep(3)
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH,"//tbody[@class='dataContainer']")))
        table = driver.find_element_by_xpath("//tbody[@class='dataContainer']")
        number_of_rows = table.find_elements_by_xpath("//tr")
        number_of_rows = len(number_of_rows)
        
        for row in range(number_of_rows-1):
            time.sleep(1)
            try:
                manager_name = table.find_element_by_xpath("//tr[" + str(row + 1) + "]/td[1]").text
                manager_club = table.find_element_by_xpath("//tr[" + str(row + 1) + "]/td[2]").text
                manager_nationality = table.find_element_by_xpath("//tr[" + str(row + 1) + "]/td[3]").text
                #print(player_name, player_season, player_team, player_position, player_nationality)
                df_to_add = pd.DataFrame([[manager_name, manager_season, manager_team, manager_nationality]], columns = ['Manager','Seasion','Club','Nationality'])
                df = df.append(df_to_add, ignore_index=True)
            except:
                pass
        
        time.sleep(3)

    #save df into excel file
    df.to_excel("") 

    time.sleep(3)


