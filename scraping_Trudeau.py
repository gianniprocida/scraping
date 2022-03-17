import re
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import requests
from random import randint
from time import sleep


# Run the script and enter the in
# For replacing 'month' with number in the url
months = dict(jan='1', feb='2', mar='3', apr='4',may='5',jun='6',jul='7',aug='8',sep='9',oct='10',nov='11',dec='12')

# User-agent. Lets the server identify the application
headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'}

def extract_date(url):
    return re.findall(r'/(\d{4})/(\w{1,3})/(\d{1,2})/', url)



def get_mean_of_page(webpage,npage):
    """ calculate mean of number of articles about Justin Trudeau
       :param webpage,npage where npage is the parameter given in the URL
       :return: d={npage:{mean:period}}
       """
    dates = []
    for i in soup.find_all('a',class_=re.compile("^u-faux")):# match class whose name starts with u-faux
        if i.get_text():
           extracted=extract_date(i.get('href'))[0]
           converted = list(extracted)
           converted[1] = months[converted[1]]  # Replace month withs numbers
           converted = tuple(map(int,converted))
           datetime_obj = datetime.datetime(*converted)
           dates.append(datetime_obj)
    df = pd.DataFrame(dates,columns=['Date'])
    df['count']=df.groupby('Date')['Date'].transform('count')
    df.drop_duplicates(inplace=True)
    d={npage:{'mean':df['count'].mean(),'period':[df.iloc[-1,0].strftime("%d %b %Y")+'-'+df.iloc[0,0].strftime("%d %b %Y")]}}
    return d,df

def plot_mean(data):
    fig, ax = plt.subplots(figsize=(50, 50))
    ax.legend('mean')
    index=0
    # plot generated in a loop
    for i in range(len(data)):
        index += 1
        print(data[i][str(index)])
        print(data[i][str(index)]['period'])
        ax.scatter(data[i][str(index)]['period'],data[i][str(index)]['mean'],color='black', alpha=.6, label='mean')
        fig.autofmt_xdate()
        plt.title('Articles about Justin Trudeau posted ')
    hand, labl = ax.get_legend_handles_labels()
    plt.legend(np.unique(labl))



if __name__=='__main__':
    data,appended_df,=[],[]
    n=input("Number of pages you wish to scrape") # Number of pages to scrape
    for i in np.arange(1,int(n),1):
      page="https://www.theguardian.com/world/justin-trudeau?page="+str(i)
      r = requests.get(page,headers=headers)
      soup = BeautifulSoup(r.content,'html.parser')
      (d,df)=get_mean_of_page(page,str(i))
      appended_df.append(df)

      data.append(d)

      sleep(randint(3, 4))
    plot_mean(data)
    appended_df = pd.concat(appended_df)

