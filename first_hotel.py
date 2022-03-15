import time
from selenium import webdriver
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys



# Find the first hotel popping up the research

# TO DO : web scraping the page of the first hotel popping up in the research

wd=webdriver.Chrome('/usr/bin/chromedriver')

url="https://www.booking.com/index.html?aid=376363;label=booking-name-L*Xf2U1sq4*GEkIwcLOALQS267777916054:pl:ta:p1:p22,563,000:ac:ap:neg:fi:tiaud-1183547561427:kwd-65526620:lp9043675:li:dec:dm:ppccp=UmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1XFzPnqOODws;ws=&gclid=Cj0KCQjwz7uRBhDRARIsAFqjulkeeGiMTlJ3WPwKB6U6QJxBtBYefQPt9AaQakNLY8PeTGRCAa1sIbQaAiF0EALw_wcB"


# Loading the page
wd.get(url)


search_bar=wd.find_element_by_id('ss')
time.sleep(4)
city=input("Insert the city")
search_bar.send_keys(city)

search_bar.send_keys(Keys.ENTER)

try:
    div = WebDriverWait(wd, 4).until(
        EC.presence_of_element_located(
            (By.ID, "ajaxsrwrap"))
    )

    elems = div.find_elements_by_xpath("//a[@href]")
    links_berlin,elements_berlin =[],[]
    for elem in elems:
        if elem.get_property('target')=='_blank' and 'hotel' in elem.get_attribute('href'):
           links_berlin.append(elem.get_attribute('href'))
           elements_berlin.append(elem)
    elements_berlin[1].click()

    #element = WebDriverWait(wd, 10).until(
    #       EC.visibility_of_element_located(
    #            (By.CLASS_NAME, "bodyconstraint"))
    # )


except TimeoutError as e:
    print(e)
    wd.quit()


