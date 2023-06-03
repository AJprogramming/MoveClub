from selenium import webdriver
from movieclubs.scraped_movies.config import connect, driver_path
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

web = "https://www.entoin.com/entertainment/pg-13-movies"
path = driver_path
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(path, options=options)
driver.get(web)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

pagination = wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, '//div[@class="sptable"]')))

movies = wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, '//div[@class="sptable"]/table/tbody/tr')))

title = []
release_year = []

for movie in movies:
    try:
        first_cell = movie.find_element_by_xpath('.//td[1]')
        if "Title" in first_cell.text:
            title_cell = movie.find_element_by_xpath('.//td[2]')
            title.append(title_cell.text)
        elif "Release Year" in first_cell.text:
            release_cell = movie.find_element_by_xpath('.//td[2]')
            release_year.append(release_cell.text)
    except:
        continue

driver.quit()

if len(title) > len(release_year):
    print("title list is longer")
elif len(title) < len(release_year):
    print("release_year list is longer")
else:
    print("lists are equal size")

# cnx = connect

# cursor = cnx.cursor()

# insert_query = """INSERT INTO movietitles (title, releaseyear) VALUES (%s, %s)"""

# for i in range(len(title)):
#     col1 = title[i]
#     col2 = release_year[i]
#     cursor.execute(insert_query, (col1, col2))

# cnx.commit()
# cursor.close()
# cnx.close()
