from app import app
from flask import render_template, request, redirect, session
from db import db
import hotels
import reservations
import users
from datetime import datetime

@app.route("/")
def index():
    all_hotels = hotels.get_all_hotels()
    return render_template("index.html", hotels=all_hotels)

@app.route("/modify_hotels")
def modify_hotels():
    return render_template("modify_hotels.html",
                            hotels = hotels.get_hotels_by_owner_id(users.user_id()))

@app.route("/add_amenity")
def add_amenity():
    return render_template("add_amenity.html",
                            hotels=hotels.get_hotels_by_owner_id(users.user_id()),
                            selected_hotel = None,
                            amenities = None,
                            rooms=([]))

@app.route("/add_hotel_amenities", methods=["POST"])
def add_hotel_amenities():
    hotel_id = request.form["hotel_id"]

    if hotels.add_amenity(request.form.getlist("hotel_amenity"), hotel_id=request.form["hotel_id"]):
        return render_template("/add_amenity.html",
                            hotels = hotels.get_hotels_by_owner_id(users.user_id()),
                            selected_hotel = hotels.get_hotel_information(hotel_id)[1],
                            amenities=hotels.get_amenities(hotel_id),
                            rooms=hotels.get_rooms(hotel_id)
                            )
    else:
        return render_template("error.html", message= 'Ei toimi')

@app.route("/select_hotel", methods=["POST"])
def select_hotel():
    hotel_id = request.form["hotel_id"]
    
    return render_template("/add_amenity.html",
                            hotels = hotels.get_hotels_by_owner_id(users.user_id()),
                            selected_hotel = hotels.get_hotel_information(hotel_id)[1],
                            amenities=hotels.get_amenities(hotel_id),
                            rooms=hotels.get_rooms(hotel_id)
                            )

@app.route("/create_room", methods=["POST"])
def create_room():
    description = request.form["room_description"]
    guests = int(request.form["guests"])
    square_meters = int(request.form["square_meters"])
    number_of_rooms = int(request.form["number_of_rooms"])
    price = float(request.form["price"])
    hotel_id = request.form["hotel_id"]

    if hotels.add_room(hotel_id, description, guests, square_meters, number_of_rooms, price):
        return render_template("/add_amenity.html",
                            hotels = hotels.get_hotels_by_owner_id(users.user_id()),
                            selected_hotel = hotels.get_hotel_information(hotel_id)[1],
                            amenities=hotels.get_amenities(hotel_id),
                            rooms=hotels.get_rooms(hotel_id))
    else:
        return render_template("error.html", message= 'Ei toimi')

@app.route("/book_hotel", methods=["POST"])
def show_available_hotels():
    isinstance(x, datetime.date)
    check_in = request.form["check_in"]
    check_out = request.form["check_out"]
    customers = request.form["customers"]

    if not isinstance(check_in, datetime.date) or not isinstance(check_out, datetime.date):
        return render_template("error.html", message= 'Anna sovellukselle päivämäärät')

    available_hotels = reservations.get_available_hotels(check_in, customers)

    return render_template("book_hotel.html",
                            check_in=check_in,
                            check_out=check_out,
                            customers=customers,
                            available_hotels = available_hotels)

@app.route("/hotel_rooms", methods=["POST"])
def show_available_rooms():
    check_in = str(request.form["check_in"])
    check_out = str(request.form["check_out"])
    guests = request.form["guests"]
    hotel_id = request.form["hotel_id"]
    available_rooms = reservations.get_available_rooms(hotel_id=hotel_id, reservation_date=check_in)
    hotel_name = hotels.get_hotel_information(hotel_id)[1]

    return render_template("hotel_rooms.html",
                            hotel_name = hotel_name[0],
                            available_rooms = available_rooms,
                            check_in = check_in,
                            check_out=check_out,
                            guests=guests,
                            hotel_id=hotel_id)

@app.route("/bookings")
def bookings():
    reserved_rooms = reservations.get_reservations_by_customer_id(users.user_id())
    return render_template("bookings.html",
                            reserved_rooms = reserved_rooms,
                            new_booking = False,
                            number_of_reservations= len(reserved_rooms))

@app.route("/cancel_reservation", methods=["POST"])
def cancel_reservation():
    reservation_id = request.form["reservation_id"]
    check_in = request.form["check_in"]
    check_out = request.form["check_out"]
    room_id = request.form["room_id"]

    try:
        reservations.cancel_reservation(reservation_id)
        reservations.add_available_rooms(room_id, check_in, check_out)
    except:
        return render_template("error.html", message= 'Ei toimi')
        
    reserved_rooms = reservations.get_reservations_by_customer_id(users.user_id())
    return render_template("bookings.html",
                            reserved_rooms = reserved_rooms,
                            new_booking = False,
                            number_of_reservations= len(reserved_rooms))



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

        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Käyttäjätyyppiä ei ole valittu")

        if users.register(username, password1, role) is False:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")


@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/hotel/<int:hotel_id>")
def show_hotel(hotel_id):
    hotel_name = hotels.get_hotel_information(hotel_id)[1]
    amenities = hotels.get_amenities(hotel_id=hotel_id)
    rooms = hotels.get_rooms(hotel_id=hotel_id)
    
    return render_template("hotel.html",
                            hotel_name = hotel_name,
                            rooms = rooms,
                            amenities = amenities)

@app.route("/create_hotel", methods=["POST"])
def create_hotel():
    hotel_name = request.form["hotel_name"]
    hotel_address = request.form["hotel_address"]
    stars = request.form["stars"]

    if hotels.add_hotel(hotel_name, hotel_address, stars, users.user_id()):
        return redirect("/")
    else:
        return render_template("error.html", message= 'Ei toimi')

@app.route("/delete_hotel", methods=["POST"])
def delete_hotel():
    hotel_id = request.form["hotel_id"]

    if hotels.delete_hotel(hotel_id):
        return redirect("/")
    else:
        return render_template("error.html", message= 'Ei toimi')

@app.route("/update_booking_calendar", methods=["POST"])
def update_booking_calendar():
    room_id = request.form["room_id"]
    start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d")
    hotel_id = request.form["hotel_id"]

    if reservations.add_new_dates_to_calendar(start_date, end_date, room_id, hotels.get_room_guest_number(room_id)[0]):
        return render_template("/add_amenity.html",
                            hotels = hotels.get_hotels_by_owner_id(users.user_id()),
                            selected_hotel = hotels.get_hotel_information(hotel_id)[1],
                            amenities=hotels.get_amenities(hotel_id),
                            rooms=hotels.get_rooms(hotel_id))
    else:
        return render_template("error.html", message= 'Ei toimi')

@app.route("/create_booking", methods=["POST"])
def create_booking():
    room_id = request.form["room_id"]
    check_in = str(request.form["check_in"])
    check_out = str(request.form["check_out"])
    guests = int(request.form["guests"])
    hotel_id = request.form["hotel_id"]

    if reservations.add_reservation(room_id, users.user_id(), check_in, check_out, guests, hotel_id):
        return render_template("/bookings.html", reserved_rooms = reservations.get_reservations_by_customer_id(users.user_id()), new_booking = True)
    else:
        return render_template("error.html", message= 'Ei toimi')

                            
    