import time
from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import redirect
from bot import grab_links
from scraping import hotelWebsite

views=Blueprint('views',__name__)

@views.route("/home")
def home():
     return render_template('index.html', content='gianni')



@views.route("/hotel/<hotelname>")
def show(hotelname):
    q = grab_links()
    time.sleep(10)
    hotel1=hotelWebsite(q.pop())
    h1 = {'Name': hotel1.get_hotelname(),
          'Stars': hotel1.get_stars(),
          'Address': hotel1.get_address(),
          'table': hotel1.get_description(),
          'reviews': hotel1.get_reviews()}

    hotel2=hotelWebsite(q.pop())

    h2 = {'Name': hotel2.get_hotelname(),
          'Stars': hotel2.get_stars(),
          'Address': hotel2.get_address(),
          'table': hotel2.get_description(),
          'reviews': hotel2.get_reviews()}

    hotel3=hotelWebsite(q.pop())

    h3={'Name': hotel3.get_hotelname(),
         'Stars': hotel3.get_stars(),
         'Address': hotel3.get_address(),
         'table':hotel3.get_description(),
        'reviews':hotel3.get_reviews()}


    return render_template('index.html',content1=h1, content2=h2,content3=h3)



