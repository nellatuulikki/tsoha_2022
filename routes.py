from app import app
from flask import render_template, request, redirect
from db import db
import hotels

@app.route("/")
def index():
    all_hotels = hotels.get_all_hotels()
    return render_template("index.html", hotels=all_hotels)

@app.route("/add_hotel")
def add_hotel():
    return render_template("add_hotel.html")

@app.route("/hotel/<int:hotel_id>")
def show_hotel(hotel_id):
    #hotel_name = hotels.get_hotel_info(hotel_id=hotel_id)

    return render_template("hotel.html") #hotel_name=hotel_name[0])

@app.route("/database_change", methods=["POST"])
def database_change():
    hotel_name = request.form["hotel_name"]
    hotel_address = request.form["hotel_address"]
    stars = request.form["stars"]

    sql = "INSERT INTO hotels (hotel_name, hotel_address, stars) VALUES (:hotel_name, :hotel_address, :stars)"
    db.session.execute(sql, {"hotel_name":hotel_name, "hotel_address": hotel_address, "stars":stars})
    db.session.commit()

    return render_template("database_change.html",
                            hotel_name=hotel_name,
                            hotel_address=hotel_address,
                            stars=stars)