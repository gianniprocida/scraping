import requests
from bs4 import  BeautifulSoup
import json
import re

"""Scraping data from the URL below"""
"""Just run the script in interactive window or python terminal"""

url = "https://www.booking.com/hotel/de/kempinskibristolberlin.en-gb.html?aid=1649686;label=kempinskibristolberlin-BxmtH89CeFt5COrk%2AP71ywS323958243077%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atiaud-617622003811%3Akwd-395949224771%3Alp9043675%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YdwTcLIbWZlfefYGj3m2lIc;sid=716df04b0ec19f628bf5155e8ffa1fa5;all_sr_blocks=6066428_340785799_2_2_0;checkin=2022-02-10;checkout=2022-02-11;dest_id=-1746443;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=6066428_340785799_2_2_0;hpos=1;matching_block_id=6066428_340785799_2_2_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=6066428_340785799_2_2_0__13356;srepoch=1643632855;srpvid=b32a592a2c420297;type=total;ucfs=1&#tab-main"

class website():
    def __init__(self,URL):
        self.URL = URL
        self.r = requests.get(self.URL)
        self.webpage = BeautifulSoup(self.r.content,"html.parser")


    def get_hotelname(self):
        if self.webpage.find('h2'):
           headers = [name.get_text() for name in self.webpage.find_all('h2', id=re.compile('^hp_hotel'))]
           hotel_name = [headers[0].splitlines()[2]]
           return hotel_name

    def get_stars(self):
        if self.webpage.find('span'):
          stars = 0
          for span in self.webpage.find_all('span',class_="_3ae5d40db _617879812 _6ab38b430"):
             if span.find('svg'):
               stars +=1
          return str(stars)

    def get_address(self):
        if self.webpage.find('span'):
           address = [address.get_text() for address in self.webpage.find_all('span', class_=re.compile("^hp_address"))]
           address = [item.strip() for item in address]
           return address


    def get_description(self):
        if self.webpage.find('div'):
           description = [d.get_text() for d in self.webpage.find_all('div', id="property_description_content")]
           description = [i.replace("\n","") for i in description]
           return description


    def get_score_reviews(self):
        if self.webpage('div'):
            for item in self.webpage.find_all('div', class_="_9c5f726ff bd528f9ea6"):
                if item.get_text():
                    score = [item.get_text()]
                    reviews = [div.get_text().replace("\xa0","") for div in item.find_next()]
                    score_reviews = score + reviews
                    return score_reviews
    def get_rooms(self):
        if self.webpage.find('table'):
            table = self.webpage.find('table')
            rooms = [str(room.get_text().strip()) for room in table.find_all('a')]
            return rooms

    def get_room_details(self):
        if self.webpage.find('table'):
           table = self.webpage.find('table')
           rooms = self.get_rooms()
           total_inf = [j.get_text(" ", strip=True).replace("\xa0"," ") for j in table.find_all(['a','li'])]
           room_details = []
           for r in total_inf:
               if r not in rooms:
                   room_details.append(r)
           return room_details



if __name__=='__main__':
      booking = website(url)
      d={'Name':booking.get_hotelname(),'Stars':booking.get_stars(),'Address':booking.get_address(),\
    'Score&Reviews':booking.get_score_reviews(),'Description':booking.get_description(),\
   'Room type':booking.get_rooms(),'Det':booking.get_room_details()}

      def save_data(title,data):
        with open(title, 'w', encoding='utf-8') as f:
         json.dump(data, f, ensure_ascii=False, indent=2)

      save_data('hotel_briston.json', d)






