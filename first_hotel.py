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
#city=input("Insert the city")
search_bar.send_keys('Berlin')

search_bar.send_keys(Keys.ENTER)

try:
    div = WebDriverWait(wd, 20).until(
        EC.presence_of_element_located(
            (By.ID, "ajaxsrwrap"))
    )
    window_before = wd.window_handles[0]

    #XPath query elements with multiple attributes : xpath("//a[@class='fb01724e5b][@href]") or xpath("//a[@class='fb01724e5b' and @href])
    try:
        link=WebDriverWait(wd, 950).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[@class='fb01724e5b' and @href]"))
        )
        time.sleep(50)
        link.click()

       # window_after = wd.window_handles[1]
    #    wd.switch_to.window(window_after)
    #    aa=wd.title
    except TimeoutError as e:
      print(a)

   # wd.switch_to.window(window_after)
   # a=wd.title

   # first_hotel=links[0]
   # first_hotel.click()
   # aa = [l.get_attribute('href') for l in div.find_elements_by_xpath("//a[@class='fb01724e5b' and @href]")]

   # first_hotel=div.find_elements_by_xpath("//a[@class='fb01724e5b' and @href]")[0].click()

    # links_berlin,elements_berlin =[],[]
    # for elem in elems:
    #     if elem.get_property('target')=='_blank' and 'hotel' in elem.get_attribute('href'):
    #        links_berlin.append(elem.get_attribute('href'))
    #        elements_berlin.append(elem)
    # first_hotel=elements_berlin[1]
    #Store the window handle

    #time.sleep(10)
    # elems = WebDriverWait(wd, 4).until(
    #      EC.presence_of_element_located(
    #          (By.XPATH,"//a[@href and @class=fb01724e5b]"))
    #  )
  #  first_hotel.click()
    # Store the window handle of the newly opened window
    # time.sleep(10)
    # window_after = wd.window_handles[1]
    #
    #

    # element = WebDriverWait(wd, 10).until(
    #              EC.visibility_of_element_located(
    #                  (By.ID, "hp_hotel_name"))
    #          )

except TimeoutError as e:
    print(e)
    wd.quit()


