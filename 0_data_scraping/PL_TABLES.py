from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

df = pd.DataFrame (columns = ['Season','Position','Club', 'Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points'])

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

driver.get("https://www.premierleague.com/tables")

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
    season_name = current_season.get_attribute("data-option-name")
    driver.execute_script("arguments[0].click();", current_season)

    #scraping the data
    time.sleep(3)
    try:
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH,"//tbody[@class='tableBodyContainer']")))
        table = driver.find_element_by_xpath("//tbody[@class='tableBodyContainer']")
        rows = table.find_elements_by_xpath("//tr[@data-compseason]")
    except:
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH,"//tbody[@class='tableBodyContainer isPL']")))
        table = driver.find_element_by_xpath("//tbody[@class='tableBodyContainer isPL']")
        rows = table.find_elements_by_xpath("//tr[@data-compseason='363']")
    
    number_of_rows = len(rows)
    
    curr = 1
    for row in range(number_of_rows): 
        time.sleep(1)
        try:
            position = table.find_element_by_xpath("//tr[" + str(curr) + "]/td[2]").text
            club = table.find_element_by_xpath("//tr[" + str(curr) + "]/td[3]").text
            played = table.find_element_by_xpath("//tr[" + str(curr) + "]/td[4]").text
            won = table.find_element_by_xpath("//tr[" + str(curr) + "]/td[5]").text
            drawn = table.find_element_by_xpath("//tr[" + str(curr) + "]/td[6]").text
            lost = table.find_element_by_xpath("//tr[" + str(curr) + "]/td[7]").text
            gf = table.find_element_by_xpath("//tr[" + str(curr) + "]/td[8]").text
            ga = table.find_element_by_xpath("//tr[" + str(curr) + "]/td[9]").text
            gd = table.find_element_by_xpath("//tr[" + str(curr) + "]/td[10]").text
            points = table.find_element_by_xpath("//tr[" + str(curr) + "]/td[11]").text
            #print(player_name, player_season, player_team, player_position, player_nationality)
            df_to_add = pd.DataFrame([[season_name, position, club, played, won, drawn, lost, gf, ga, gd, points]], columns = ['Season','Position','Club','Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points'])
            df = df.append(df_to_add, ignore_index=True)
        except:
            pass
        
        curr += 2
        
        time.sleep(3)

    #save df to excel file
    df.to_excel("") 
    print(season_name)
    time.sleep(3)


