from app import app
from flask import render_template, request, redirect
from db import db
import hotels
import reservations
import users
from datetime import datetime

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

@app.route("/book_hotel", methods=["POST"])
def show_available_hotels():
    check_in = request.form["check_in"]
    check_out = request.form["check_out"]
    customers = request.form["customers"]

    available_hotels = reservations.get_available_hotels(check_in, customers)

    return render_template("book_hotel.html", check_in=check_in, check_out=check_out, customers=customers, available_hotels = available_hotels)

@app.route("/hotel_rooms", methods=["POST"])
def show_available_rooms():
    check_in = str(request.form["check_in"])
    check_out = str(request.form["check_out"])
    guests = request.form["guests"]
    hotel_id = request.form["hotel_id"]

    available_rooms = reservations.get_available_rooms(hotel_id=hotel_id, reservation_date=check_in)
    hotel_name = hotels.get_hotel_name(hotel_id=hotel_id)

    return render_template("hotel_rooms.html", hotel_name = hotel_name[0], available_rooms = available_rooms, check_in = check_in, check_out=check_out, guests=guests)

@app.route("/bookings")
def bookings():
    reserved_rooms = reservations.get_reservations_by_customer_id(1)
    return render_template("bookings.html", reserved_rooms = reserved_rooms, new_booking = False)


@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 15:
            return render_template("error.html", message="Tunnuksen tulee sisältää 1-15 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää, yritä uudelleen")
        if password1 == "":
            return render_template("error.html", message="Salasanakentät eivät voi olla tyhjiä")

        customer_type = request.form["role"]
        if customer_type not in ("1", "2"):
            return render_template("error.html", message="Käyttäjätyyppiä ei ole valittu")

        if users.register(username, password1, customer_type) is False:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")

@app.route("/hotel/<int:hotel_id>")
def show_hotel(hotel_id):
    hotel_name = hotels.get_hotel_name(hotel_id=hotel_id)
    amenities = hotels.get_amenities(hotel_id=hotel_id)
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

@app.route("/send_3", methods=["POST"])
def send_rooms():
    description = request.form["room_description"]
    guests = int(request.form["guests"])
    square_meters = int(request.form["square_meters"])
    number_of_rooms = int(request.form["number_of_rooms"])
    price = float(request.form["price"])

    if hotels.add_room(1, description, guests, square_meters, number_of_rooms, price):
        return redirect("/add_amenity")
    else:
        return render_template("database_change.html", message= 'Ei toimi')

@app.route("/update_booking_calendar", methods=["POST"])
def update_booking_calendar():
    room_id = request.form["room_id"]
    start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d")

    if reservations.add_new_dates_to_calendar(start_date, end_date, room_id, hotels.get_room_guest_number(room_id)[0]):
        return redirect("/")
    else:
        return render_template("database_change.html", message= 'Ei toimi')

@app.route("/create_booking", methods=["POST"])
def create_booking():
    room_id = request.form["room_id"]
    check_in = str(request.form["check_in"])
    check_out = str(request.form["check_out"])
    guests = int(request.form["guests"])


    if reservations.add_reservation(room_id, 1, check_in, check_out, guests):
        reservations.update_available_rooms(room_id, check_in)
        return render_template("/bookings.html", reserved_rooms = reservations.get_reservations_by_customer_id(1), new_booking = True)
    else:
        return render_template("database_change.html", message= 'Ei toimi')