import json
from flask import Flask, redirect, url_for, render_template
from scraping_fynd import website

app=Flask(__name__)

# with open("hotel_briston.json") as f:
#      data=json.load(f)


@app.route("/")
def home():
    url = "https://www.booking.com/hotel/de/kempinskibristolberlin.en-gb.html?aid=1649686;label=kempinskibristolberlin-BxmtH89CeFt5COrk%2AP71ywS323958243077%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atiaud-617622003811%3Akwd-395949224771%3Alp9043675%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YdwTcLIbWZlfefYGj3m2lIc;sid=716df04b0ec19f628bf5155e8ffa1fa5;all_sr_blocks=6066428_340785799_2_2_0;checkin=2022-02-10;checkout=2022-02-11;dest_id=-1746443;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=6066428_340785799_2_2_0;hpos=1;matching_block_id=6066428_340785799_2_2_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=6066428_340785799_2_2_0__13356;srepoch=1643632855;srpvid=b32a592a2c420297;type=total;ucfs=1&#tab-main"
    booking = website(url)
    data = {'Name': booking.get_hotelname(),
         'Stars': booking.get_stars(),
         'Address': booking.get_address(), \
         'Score&Reviews': booking.get_score_reviews(),
         'Description': booking.get_description(), \
         'Room type': booking.get_rooms(),
         'Det': booking.get_room_details()}

    return render_template("index.html",content=data)

if __name__=='__main__':
    app.run(debug=True)
