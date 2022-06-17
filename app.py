import sqlite3
import pandas as pd
from flask import Flask, render_template, request, url_for, flash, redirect



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

def get_db_conn():
    dict_cur = sqlite3.connect('HotelData.db')
    dict_cur.row_factory = sqlite3.Row
    return dict_cur


@app.route('/')
def home():
    dict_cur = get_db_conn()
    listhotelNames = dict_cur.execute("SELECT * FROM Reviews").fetchall()

    return render_template('home.html',listhotelNames=listhotelNames)

@app.route('/add/',methods=('GET','POST'))
def add():
    if request.method=='POST':
        HotelName = request.form['HotelName']
        Staff = request.form['Staff']
        Cleanliness = request.form['Cleanliness']
        Comfort = request.form['Comfort']
        ValueForMoney = request.form['ValueForMoney']
        Location = request.form['Location']
        FreeWifi = request.form['FreeWifi']
        print(HotelName, Staff,FreeWifi)
        if not HotelName:
            flash('HotelName is required')
        else:
            dict_cur = get_db_conn()
            dict_cur.execute("""INSERT INTO Reviews (
            HotelName, Staff, Cleanliness, Comfort, ValueForMoney, Location,
            FreeWifi) VALUES (?,?,?,?,?,?,?)""",(HotelName, Staff, Cleanliness,
                                                 Comfort, ValueForMoney, Location, FreeWifi))
            dict_cur.commit()
            dict_cur.close()
            return redirect((url_for('home')))


    return render_template('add.html')


# @app.route("/user/<int:id>")
# def retrieve(id):
#     if id==1:
#         dict_cur = get_db_conn()
#         dict_cur.execute(""" CREATE TABLE Avg as
#          SELECT((Staff + Facilities + Cleanliness + Comfort + ValueForMoney +
#           Location + FreeWif) / 7) AS Average
#         FROM
#         Reviews;""")
#         dict_cur.execute("""SELECT MAX(Average) FROM Avg""")
#
#
#     return render_template("other.html",data=data)
#
#



if __name__=='__main__':
    app.run(debug=True)