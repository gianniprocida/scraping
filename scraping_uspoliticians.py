import re
import tarfile
import time
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import requests
import matplotlib.dates as mdates
from random import randint
from time import sleep
import psycopg2
from sqlalchemy import create_engine


# For replacing 'month' with number in the url
months = dict(jan='1', feb='2', mar='3', apr='4',may='5',jun='6',jul='7',aug='8',sep='9',oct='10',nov='11',dec='12')

# User-agent. Lets the server identify the application
headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'}

class us_pool:
    def __init__(self,root, name):
        self.root=root
        self.name = name
        self.website=f"{self.root}{self.name}"
        self.r=requests.get(self.website)
    def generator_of_df(self,maxnpage):
        page=0
        while page < maxnpage:
            page+=1
            r = requests.get(self.website,params={'page':page})
            soup = BeautifulSoup(r.content,"html.parser")
            dates=[]
            titles=[]
            for i in soup.find_all('a', class_=re.compile("^u-faux")):  # match class whose name starts with u-faux
              if i.get_text():
                extracted = re.findall(r'/(\d{4})/(\w{1,3})/(\d{1,2})/',i.get('href'))[0]
                titles.append(i.get_text('href'))
                converted = list(extracted)
                converted[1] = months[converted[1]]  # Replace month with number
                converted = tuple(map(int, converted))
                datetime_obj = datetime.datetime(*converted)
                dates.append(datetime_obj)
            df = pd.DataFrame(dates, columns=['Date'])
            df_title=pd.DataFrame(list(zip(dates,titles)),columns=['Date','Title'])
            # Adding 'count'  for each date
            df['count'] = df.groupby('Date')['Date'].transform('count')
            df.drop_duplicates(inplace=True)
            df.reset_index(drop=True, inplace=True)
            yield df


def plot_data(g,name):
    fig, ax = plt.subplots(figsize=(50, 50))
    ax.legend('total')
    page=0
    while True:
        try:
            page += 1
            df = next(g)
            print("Plotting number of articles per day from page {0}".format(str(page)))
            ax=df.plot(kind='scatter',x='Date',y='count',color='red')
            ax.locator_params(integer=True)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

            plt.gcf().autofmt_xdate()

            plt.title('Number of articles about {0} from {1}'.format(name,str(page)))

        except StopIteration:
          print("Done")
          break



if __name__=='__main__':
    trump=us_pool("https://www.theguardian.com/us-news/","donaldtrump")

    g=trump.generator_of_df(8)

    all_df=list(g)
    df_trump=pd.concat(all_df)

    # Adding 'count' for each date
    df_trump['count'] = df_trump.groupby('Date')['count'].transform('sum')

    df_trump.rename(columns={'count': 'count_tr'},inplace=True)

    df_trump.drop_duplicates(inplace=True)



    biden = us_pool("https://www.theguardian.com/us-news/",
                    "joebiden")

    g=biden.generator_of_df(8)

    all_df=list(g)
    df_biden = pd.concat(all_df)

    df_biden['count'] = df_biden.groupby('Date')[
        'count'].transform('sum')

    df_biden.rename(columns={'count': 'count_bi'},
                    inplace=True)

    df_biden.drop_duplicates(inplace=True)


    time.sleep(2)

    print("SQL...")


    pgconn=psycopg2.connect(host="localhost",user="gianni",password="gianni90",database='numberofcount')

    pgcursor=pgconn.cursor()

#  connection string : driver://username:password@server/database
    engine=create_engine('postgresql+psycopg2://gianni:gianni90@localhost/numberofcount')
#
    df_trump.to_sql('trump',engine, if_exists='replace', index=False)
#
    df_biden.to_sql('biden',engine, if_exists='replace', index=False)

    sql_join=' CREATE TABLE final as SELECT biden."Date", biden.count_bi, trump.count_tr FROM biden INNER JOIN trump on biden."Date"=trump."Date" '

    pgcursor.execute(sql_join)

    final=pd.read_sql_query("SELECT * FROM final",pgconn)
    pgconn.commit()
    pgconn.close()

    final['DATE']=final['Date'].apply(lambda x:x.strftime('%Y-%m-%d'))

    fig, ax = plt.subplots()

    ax.scatter(final.DATE, final.count_bi,label='biden')

    ax.scatter(final.DATE, final.count_tr,label='trump')

    #Rotate and align the tick labels so they look better
    fig.autofmt_xdate()

    ax.set_xlabel('Date')
    ax.set_ylabel('N. of article ')
    ax.legend()
    # Use a more precise date string for the x axis locations in the toolbar.
    ax.set_title('https://www.theguardian.com')


