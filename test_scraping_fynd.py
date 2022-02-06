import unittest
from scraping_fynd import website
"""Test for scraping_fynd.py."""


url = "https://www.booking.com/hotel/de/kempinskibristolberlin.en-gb.html?aid=1649686;label=kempinskibristolberlin-BxmtH89CeFt5COrk%2AP71ywS323958243077%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atiaud-617622003811%3Akwd-395949224771%3Alp9043675%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YdwTcLIbWZlfefYGj3m2lIc;sid=716df04b0ec19f628bf5155e8ffa1fa5;all_sr_blocks=6066428_340785799_2_2_0;checkin=2022-02-10;checkout=2022-02-11;dest_id=-1746443;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=6066428_340785799_2_2_0;hpos=1;matching_block_id=6066428_340785799_2_2_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=6066428_340785799_2_2_0__13356;srepoch=1643632855;srpvid=b32a592a2c420297;type=total;ucfs=1&#tab-main"



class Testwebsite(unittest.TestCase):
    def setUp(self):
        self.booking = website(url)
    def test_get_hotel_name(self):
        solution = ['Hotel Bristol Berlin']
        self.assertEqual(self.booking.get_hotelname(), solution)

    def test_get_stars(self):
        solution = '5'
        self.assertEqual(self.booking.get_stars(),solution)

    def test_get_address(self):
        solution = ['Kurfürstendamm 27, Charlottenburg-Wilmersdorf, 10719 Berlin, Germany']
        self.assertEqual(self.booking.get_address(),solution)

    def test_get_description(self):
        solution= [
    "You're eligible for a Genius discount at Hotel Bristol Berlin! To save at this property, all you have to do is sign in.Hotel Bristol Berlin is a vibrant, legendary hotel located directly on the famous Kurfürstendamm boulevard, opening its doors in 1952. The hotel offers complimentary WiFi throughout the premises and there is a nearby underground parking garage.The hotel's rooms and suites are spread across several main floors plus an 11-storey tower. All rooms are a stylistic mix of classic and modern with tiltable and soundproof windows. The hotel is now 100% non-smoking.The wellness area in Roman-Greek style has a heated 20 yards pool, sauna, infrared cabin and steam room with a cold water plunge pool.Enjoy the best seasonal martinis at the Bristol Bar, or cosy up at the Bristol Café. And you will still have legendary Crêpes Suzettes flambéed at your table at the well-loved Bristol Grill, which serves traditional German-French cuisine with the occasional modern twist.Nearby attractions include the Kaiser Wilhelm Memorial Church, Savigny Square, Theater des Westens, the BIKINI Berlin concept mall and The Story of Berlin interactive museum. Attractions for families includes the nearby zoo and aquarium, and the Tiergarten, Berlin's largest park, is just a 10-minute walk from the Hotel Bristol Berlin. "
  ]
     #   solution = ["You're eligible for a Genius discount at Hotel Bristol Berlin! To save at this property, all you have to do is sign in.Hotel Bristol Berlin is a vibrant, legendary hotel located directly on the famous Kurfürstendamm boulevard, opening its doors in 1952. The hotel offers complimentary WiFi throughout the premises and there is a nearby underground parking garage.The hotel's rooms and suites are spread across several main floors plus an 11-storey tower. All rooms are a stylistic mix of classic and modern with tiltable and soundproof windows. The hotel is now 100% non-smoking.The wellness area in Roman-Greek style has a heated 20 yards pool, sauna, infrared cabin and steam room with a cold water plunge pool.Enjoy the best seasonal martinis at the Bristol Bar, or cosy up at the Bristol Café. And you will still have legendary Crêpes Suzettes flambéed at your table at the well-loved Bristol Grill, which serves traditional German-French cuisine with the occasional modern twist.Nearby attractions include the Kaiser Wilhelm Memorial Church, Savigny Square, Theater des Westens, the BIKINI Berlin concept mall and The Story of Berlin interactive museum. Attractions for families includes the nearby zoo and aquarium, and the Tiergarten, Berlin's largest park, is just a 10-minute walk from the Hotel Bristol Berlin. "]
        self.assertEqual(self.booking.get_description(),solution)

    def test_get_score_reviews(self):
        solution = ['8.1', 'Very good ', '3,392 reviews']
        self.assertEqual(self.booking.get_score_reviews(),solution)
        
    def test_get_roooms(self):
        solution = ['Balcony Suite', 'Berlin Suite', 'Economy Room', 'Executive Room',\
             'Executive Suite', 'Junior Suite', 'Kudamm Suite', 'Premium Room', 'Premium Suite',\
                  'Presidential Suite']
        self.assertEqual(self.booking.get_rooms(),solution)

    def get_room_details(self):
        solution = ['1 large double bed', 'Bedroom 1: 1 large double bed', 'Living room: 1 sofa bed',\
             '2 single beds', '1 large double bed', '1 large double bed', '1 extra-large double bed',\
                  '1 extra-large double bed', '1 extra-large double bed', '2 single beds',\
                       '1 extra-large double bed', '1 extra-large double bed']
        self.assertEqual(self.booking.get_room_details(),)
if __name__ =='__main__':
    unittest.main()





