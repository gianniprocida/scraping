import time
from flask import Blueprint, render_template, request, redirect
from flask import jsonify
from bot import grab_links
from scraping import hotelWebsite

views=Blueprint('views',__name__)

@views.route("/home")
def home():
     a='title'
     return render_template('index.html')


@views.route("/hotel/<hotelname>",methods=['GET','POST'])
def show(hotelname):

    return render_template('base.html',title="Jinja Demo Site",)

#return render_template('index.html',content1=h1, content2=h2,content3=h3)




