import sqlite3
import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import re



class node:
    def __init__(self,data=None):
        self.data = data
        self.next = None

class linked_list:
    def __init__(self):
        self.head = node()
    def push(self,data):
        new_node = node(data)
        cur = self.head
        while cur.next!=None:
            cur = cur.next
        cur.next = new_node
    def display(self):
        el = []
        cur = self.head
        while cur.next!=None:
            cur = cur.next
            el.append(cur.data)
        print(el)
    def length(self):
        total=0
        cur = self.head
        while cur.next!=None:
            total+=1
            cur = cur.next
        return total
    def get(self,index):
        if index > self.length():
            print("Index out of range")
            return None
        else:
            cur_idx = 0
            cur = self.head
            while True:
                cur = cur.next
                if cur_idx==index:
                    return cur.data
                else:
                    cur_idx+=1


def generator_of_df(url,maxpage):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'}

    def getResponse(url,page):
        resp = requests.get(url, params={'page':page}, headers=headers)
        return resp

    months = dict(jan='1', feb='2', mar='3', apr='4',
                  may='5', jun='6', jul='7', aug='8',
                  sep='9', oct='10', nov='11', dec='12')

    page=0
    while page <= maxpage:
        page+=1
        resp = getResponse(url,page)
        soup = BeautifulSoup(resp.content,"html.parser")
        dates=[]
        titles=[]
        for i in soup.find_all('a',class_='u-faux-block-link__overlay js-headline-text'):
            if i.get_text():
              # Extracting the day of the news as tuple
              day = re.findall(r'/(\d{4})/(\w{1,3})/(\d{1,2})/',i.get('href'))[0]
              titles.append(i.get_text('href'))
              listofString = list(day)
              listofString[1] = months[listofString[1]]  # Replace month with number
              TupleofInt = tuple(map(int, listofString))
              datetime_obj = datetime.datetime(*TupleofInt)
              dates.append(datetime_obj.strftime("%Y-%m-%d"))
        df=pd.DataFrame(list(zip(dates,titles)),columns=['Date','Title'])
        yield df

#
def validateLink(s,link):
    name = s.split("-")[1]
    for _ in range(2):
      try:
          temp = f"{link}{s}"
          resp = requests.get(temp, timeout=5)
          if resp.status_code==200:
               print(resp.status_code)
               return temp, name
          s = s.replace("-", "")
      except requests.exceptions.ConnectionError:
          print("Site non reacheable",temp)
          print("Try again")
    return temp, name


def create_table(df, tablename):
    try:
        db = sqlite3.connect('usnews.db')
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS {0} (Date datetime, Title text)""".format(tablename))
        df.to_sql(tablename,db,if_exists="replace",index=False)

        sql_alter = """ALTER TABLE {0} RENAME TO tmp""".format(
            tablename)

        c.execute(sql_alter)

        sql_create = """CREATE TABLE {0} (ID INTEGER PRIMARY KEY, Date datetime,
                               Title text)""".format(
            tablename)

        c.execute(sql_create)

        sql_insert = """INSERT INTO {0} (Date, Title)
         SELECT Date, Title FROM tmp""".format(
            tablename)

        c.execute(sql_insert)

        sql_drop = "DROP TABLE tmp"

        c.execute(sql_drop)

        db.commit()
    except sqlite3.Error as e:
        print(e)


if __name__=='__main__':
    listofstrings = ['donald-trump', 'joe-biden',
                     'mike-pence', 'kamala-harris']

    url = "https://www.theguardian.com/us-news/"

    links, names = [], []
    i = 0
    di = {}
    llist = linked_list()

    while i < len(listofstrings):
        (l, n) = validateLink(listofstrings[i], url)
        links.append(l)
        names.append(n)
        di[n] = None
        llist.push(l)
        i += 1


    for i in range(len(names)):
        iteratorofDf = generator_of_df(llist.get(i),5)
        listofDf = list(iteratorofDf)
        dfconc = pd.concat(listofDf)
        di[names[i]]= dfconc


    for i in range(len(names)):
        create_table(di[names[i]],names[i])
