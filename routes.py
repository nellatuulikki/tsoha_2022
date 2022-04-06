from email import message
from app import app
from flask import render_template, request, redirect
from db import db
import messages 
import hotels

@app.route("/")
def index():
    all_hotels = hotels.get_all_hotels()
    return render_template("index.html", hotels=all_hotels)

@app.route("/add_hotel")
def add_hotel():
    return render_template("add_hotel.html")

@app.route("/add_amenity")
def add_amenity():
    return render_template("add_amenity.html")

@app.route("/hotel/<int:hotel_id>")
def show_hotel(hotel_id):
    hotel_name = hotels.get_hotel_name(hotel_id=hotel_id)
    amenities = hotels.get_amenities(hotel_id=hotel_id)
    print(amenities)

    return render_template("hotel.html", hotel_name = hotel_name[0], amenities = amenities)

@app.route("/send", methods=["POST"])
def send():
    hotel_name = request.form["hotel_name"]
    hotel_address = request.form["hotel_address"]
    stars = request.form["stars"]

    if hotels.add_hotel(hotel_name, hotel_address, stars):
        return redirect("/")
    else:
        return render_template("database_change.html", message= 'Ei toimi')

@app.route("/send_1", methods=["POST"])
def send_hotel_amenities():
    hotel_amenities = request.form.getlist("hotel_amenity")

    if hotels.add_amenity(hotel_amenities):
        return redirect("/add_amenity")
    else:
        return render_template("database_change.html", message= 'Ei toimi')

@app.route("/send_2", methods=["POST"])
def send_room_amenities():
    room_amenities = request.form.getlist("room_amenity")

    if hotels.add_amenity(room_amenities):
        return redirect("/add_amenity")
    else:
        return render_template("database_change.html", message= 'Ei toimi')