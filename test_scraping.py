import unittest
import requests
from scraping import hotelWebsite
import pandas as pd

"""Test for scraping using the URL below"""


class TesthotelWebsite(unittest.TestCase):
    URL = "https://www.booking.com/hotel/de/kempinskibristolberlin.en-gb.html?aid=1649686;label=kempinskibristolberlin-BxmtH89CeFt5COrk%2AP71ywS323958243077%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atiaud-617622003811%3Akwd-395949224771%3Alp9043675%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YdwTcLIbWZlfefYGj3m2lIc;sid=716df04b0ec19f628bf5155e8ffa1fa5;all_sr_blocks=6066428_340785799_2_2_0;checkin=2022-02-10;checkout=2022-02-11;dest_id=-1746443;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=6066428_340785799_2_2_0;hpos=1;matching_block_id=6066428_340785799_2_2_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=6066428_340785799_2_2_0__13356;srepoch=1643632855;srpvid=b32a592a2c420297;type=total;ucfs=1&#tab-main"
    def setUp(self):
        self.soup = hotelWebsite(self.URL)
    def test_get_hotelname(self):
        self.assertEqual(self.soup.get_hotelname(),'Hotel Bristol Berlin')
    def test_get_stars(self):
        self.assertEqual(self.soup.get_stars(),5)
    def test_get_address(self):
        self.assertEqual(self.soup.get_address(),'Kurfürstendamm 27, Charlottenburg-Wilmersdorf, 10719 Berlin, Germany')
    def tes_get_description(self):
        self.assertIsInstance(self.soup.get_description(), str)
    def test_get_reviews(self):
        self.assertIsInstance(self.soup.get_reviews(),pd.DataFrame)
    def test_get_roomsTable(self):
        self.assertIsInstance(self.soup.get_roomsTable(), pd.DataFrame)
    def test_getwhattheylovedTable(self):
        self.assertIsInstance(self.soup.get_whattheylovedTable(), pd.DataFrame)
    def test_gethotelsurroundingsTable(self):
        self.assertIsInstance(self.soup.get_hotelsurroundingsTable(), pd.DataFrame)
if __name__=='__main__':
    unittest.main()





