import sqlite3
import time
from bot import grab_links
from scraping_base import hotelWebsite
import pandas as pd


hotelLinks = grab_links()

obs = [hotelWebsite(i) for i in hotelLinks]

listName = [i.get_hotelname() for i in obs]

listAddress = [i.get_address() for i in obs]

listHotelReview = [i.get_reviews() for i in obs]

listwhattheyLoved = [i.get_whattheylovedTable() for i in obs]


listHotelSurroundings = []
for i in obs:
    try:
        listHotelSurroundings.append(i.get_hotelsurroundingsTable())
        frame_su = pd.concat(listHotelSurroundings,axis=0,ignore_index=True)
    except Exception:
        continue


# Cleaning data
def cleanDataframe(df,HotelName):
    df.columns = df.columns.str.replace(' ', '')
    df.rename(columns={df.columns[4]: "ValueForMoney"},inplace=True)
    df.rename(columns={df.columns[5]: "Location"},inplace=True)
    df.rename(columns={df.columns[6]: "FreeWifi"},inplace=True)
    df.insert(0, 'HotelName', HotelName)


def createTable(df,tablename):

    try:
        db = sqlite3.connect('HotelData.db')
        c = db.cursor()

        if tablename=='Reviews':

            c.execute("""CREATE TABLE IF NOT EXISTS Reviews (
              HotelName text,
              Staff float,
              Facilities float,
              Cleanliness float,
              Comfort float,
              ValueForMoney float,
              Location float,
              FreeWifi float)""")
            df.to_sql('Reviews', db, if_exists="replace",index=False)
            db.commit()
            db.close()

        if 'Reviews' not in tablename:

          db = sqlite3.connect('HotelData.db')
          c = db.cursor()
          c.execute("""CREATE TABLE IF NOT EXISTS {0} (
                      Name text,
                      country text,
                      subjectivity float,
                      polarity float
                      )""".format(tablename))
          df.to_sql(tablename,db,if_exists="replace", index=False)

          db.commit()
          db.close()
    except sqlite3.Error as e:
        print(e)
    return db


def AppendData(df,HotelName):
    try:
        db = sqlite3.connect('HotelData.db')
        c = db.cursor()
        df.to_sql('Reviews', db, if_exists="append",index=False)
    except sqlite3.Error as e:
        print(e)
    return db


if __name__=='__main__':
   strippedName= [i.replace(" ","").replace(",","") for i in listName]
   i,j=0,0
   while i<=len(listwhattheyLoved) and j <= len(strippedName):
       try:
           createTable(listwhattheyLoved[i],strippedName[j])
           i+=1
           j+=1
       except Exception as e:
           print(e)

   i,j=0,0
   while i<=len(listHotelReview) and j <= len(listName):
       try:
           cleanDataframe(listHotelReview[i],strippedName[j])
           i+=1
           j+=1
       except Exception as e:
           i+=1
           j+=1
           print(e)
           continue

   createTable(listHotelReview.pop(), strippedName.pop())
   while len(listHotelReview)>0:
         AppendData(listHotelReview.pop(), strippedName.pop())






# listReview[0].columns = listReview[1].columns.str.replace(' ', '')
# listReview[0].rename(columns={listReview[0].columns[4]:"ValueForMoney"},inplace=True)
# listReview[0].rename(columns={listReview[0].columns[5]: "Location"},inplace=True)
# listReview[0].rename(columns={listReview[0].columns[6]: "FreeWifi"},inplace=True)
# listReview[0].insert(0,'HotelName',listName[0])
# listReview[0].to_sql('Reviews',db, if_exists="replace",index=False)
#
#
# listReview[1].columns = listReview[1].columns.str.replace(' ', '')
# listReview[1].rename(columns={listReview[1].columns[4]:"ValueForMoney"},inplace=True)
# listReview[1].rename(columns={listReview[1].columns[5]: "Location"},inplace=True)
# listReview[1].rename(columns={listReview[1].columns[6]: "FreeWifi"},inplace=True)
# listReview[1].insert(0,'HotelName',listName[1])
# listReview[1].to_sql('Reviews',db, if_exists="append",index=False)
#
# listReview[2].columns = listReview[2].columns.str.replace(' ', '')
# listReview[2].rename(columns={listReview[2].columns[4]:"ValueForMoney"},inplace=True)
# listReview[2].rename(columns={listReview[2].columns[5]: "Location"},inplace=True)
# listReview[2].rename(columns={listReview[2].columns[6]: "FreeWifi"},inplace=True)
# listReview[2].insert(0,'HotelName',listName[2])
# listReview[2].to_sql('Reviews',db, if_exists="append",index=False)