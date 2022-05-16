import requests
from bs4 import  BeautifulSoup
import json
import re
import pandas as pd
from textblob import TextBlob
from collections import deque




headers = {"User-agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"}

class hotelWebsite():
    def __init__(self,URL):
        self.URL = URL
        self.r = requests.get(self.URL,headers)
        self.webpage = BeautifulSoup(self.r.content,"html.parser")

    def get_hotelname(self):
        if self.webpage.find('h2'):
           q=deque([self.webpage.find_all('h2',id='hp_hotel_name')[0].get_text().splitlines()[2]])
           return q.pop()

    def get_stars(self):
        return str(len(self.webpage.find_all('span', {'class' : 'b6dc9a9e69 adc357e4f1 fe621d6382'})))

    def get_address(self):
        if self.webpage.find('span'):
           q = deque([self.webpage.find_all('span', class_=re.compile("^hp_address"))[0].get_text().strip()])
           return q.pop()

    def get_description(self):
        if self.webpage.find('div'):
           q = deque([self.webpage.find_all('div',id="property_description_content")[0].get_text().replace("\n","")])
           return q.pop()

    def get_reviews(self):
        scores = [ i.get_text() for i in self.webpage.find_all('span',class_='c-score-bar__score')]
        scores = [float(i) for i in scores]
        categories = [ j.get_text().replace("\xa0"," ") for j in self.webpage.find_all('span',class_='c-score-bar__title')]
        reviews = dict(zip(categories,scores))
        return reviews

    def get_table(self):
        if self.webpage.find('table'):
            table = self.webpage.find('table')
            span_with_kids = table.find_all('span',class_="with_kids")
            rooms_type = [str(room.get_text().strip()) for room in table.find_all('a')]
            occupancy_adults, occupancy_children = [], []
            for i in span_with_kids:
                if i.find_all('span',class_="occupancy_adults") or i.find_all('span', class_="occupancy_child"):
                    occupancy_adults.append(len(i.find_all('span',class_="occupancy_adults")[0].find_all('i')))
                    occupancy_children.append(len(i.find_all('span',class_="occupancy_children")[0].find_all('i')))
            df = pd.DataFrame(list(zip(rooms_type, occupancy_adults,occupancy_children)),\
            columns=['room', 'adults','child'])

            return df

    def get_what_they_loved(self):
        polarity = [TextBlob(i.get_text().replace("\n"," ")).sentiment.polarity\
                             for i in self.webpage.find_all('span',class_='c-review__body')]

        subjectivity = [TextBlob(i.get_text().replace("\n", " ")).sentiment.subjectivity\
                                 for i in self.webpage.find_all('span',class_='c-review__body')]

        divs = self.webpage.find_all('div',class_='bui-avatar-block__text')

        name,country=[], []
        for i in divs:
            name.append(i.get_text().split("\n")[1])
            country.append(i.get_text().split("\n")[3])
            if len(name) == 10 and len(country) ==10:
                break

        df = pd.DataFrame(list(zip(name, country, subjectivity, polarity)), \
                          columns=['Name', 'country','subjectivity','polarity'])

        return df

    def get_hotelsurroundings(self):
        i=0

        # Grab the locations
        location, distance=[],[]
        ul_list=self.webpage.find_all('ul',class_="bui-list bui-list--divided bui-list--text")
        while ul_list[i].find('div',class_='bui-list__description'):
            div = ul_list[i].find_all('div',class_='bui-list__description')
            i += 1
            for item in div:
                location.append(item.get_text().replace("\n"," "))

        # Grab distances
        i=0
        while ul_list[i].find('div',class_='bui-list__item-action hp_location_block__section_list_distance'):
            div = ul_list[i].find_all('div',class_='bui-list__item-action hp_location_block__section_list_distance')
            i += 1
            for item in div:
                distance.append(item.get_text().replace("\n"," ").replace("miles"," ").split()[0])
        # miles to km
        cf=1.60934
        distance=[float(i)*cf for i in distance]


        df = pd.DataFrame(list(zip(location,distance)), columns=['Surroundings','Distance'])

        return df




if __name__=='__main__':
    url = "https://www.booking.com/hotel/de/kempinskibristolberlin.en-gb.html?aid=1649686;label=kempinskibristolberlin-BxmtH89CeFt5COrk%2AP71ywS323958243077%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atiaud-617622003811%3Akwd-395949224771%3Alp9043675%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YdwTcLIbWZlfefYGj3m2lIc;sid=716df04b0ec19f628bf5155e8ffa1fa5;all_sr_blocks=6066428_340785799_2_2_0;checkin=2022-02-10;checkout=2022-02-11;dest_id=-1746443;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=6066428_340785799_2_2_0;hpos=1;matching_block_id=6066428_340785799_2_2_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=6066428_340785799_2_2_0__13356;srepoch=1643632855;srpvid=b32a592a2c420297;type=total;ucfs=1&#tab-main"
    hotel_bristolberlin = hotelWebsite(url)
    d={'Name':hotel_bristolberlin.get_hotelname(),'Address':hotel_bristolberlin.get_address(),
       'Stars':hotel_bristolberlin.get_stars(),
       'Surroundings':hotel_bristolberlin.get_hotelsurroundings(),
               'Stars':hotel_bristolberlin.get_stars(),'Address':hotel_bristolberlin.get_address(),\
            'Description':hotel_bristolberlin.get_description(),\
          'Det':hotel_bristolberlin.get_table(),
         'Reviews':hotel_bristolberlin.get_reviews(), 'WhatTheyLoved':hotel_bristolberlin.get_what_they_loved()}

