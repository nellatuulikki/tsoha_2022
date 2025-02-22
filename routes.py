from datetime import datetime
from flask import render_template, request, redirect
from app import app
import hotels
import reservations
import users

@app.route("/")
def index():
    all_hotels = hotels.get_all_hotels()
    return render_template("index.html", hotels=all_hotels)

@app.route("/modify_hotels")
def modify_hotels():
    return render_template("modify_hotels.html",
                           hotels=hotels.get_hotels_by_owner_id(users.user_id()),
                           count_hotels = hotels.count_hotels_by_owner_id(users.user_id()))

@app.route("/add_amenity")
def add_amenity():
    return render_template("add_amenity.html",
                           hotels=hotels.get_hotels_by_owner_id(users.user_id()),
                           selected_hotel=None,
                           amenities=None,
                           rooms=([]),
                           count_rooms=None)

@app.route("/add_hotel_amenities", methods=["POST"])
def add_hotel_amenities():
    users.check_csrf()
    hotel_id = request.form["hotel_id"]

    hotels.add_amenity(request.form.getlist("hotel_amenity"), hotel_id=request.form["hotel_id"])
    return render_template("/add_amenity.html",
                           hotels=hotels.get_hotels_by_owner_id(users.user_id()),
                           selected_hotel=hotels.get_hotel_information(hotel_id),
                           amenities=hotels.get_amenities(hotel_id),
                           rooms=hotels.get_rooms(hotel_id),
                           count_rooms=hotels.count_rooms_by_hotel_id(hotel_id))


@app.route("/select_hotel", methods=["POST"])
def select_hotel():
    users.check_csrf()
    hotel_id = request.form["hotel_id"]

    return render_template("/add_amenity.html",
                           hotels=hotels.get_hotels_by_owner_id(users.user_id()),
                           selected_hotel=hotels.get_hotel_information(hotel_id),
                           amenities=hotels.get_amenities(hotel_id),
                           rooms=hotels.get_rooms(hotel_id),
                           count_rooms=hotels.count_rooms_by_hotel_id(hotel_id))

@app.route("/create_room", methods=["POST"])
def create_room():
    users.check_csrf()
    description = request.form["room_description"]
    guests = request.form["guests"]
    square_meters = request.form["square_meters"]
    number_of_rooms = request.form["number_of_rooms"]
    price = request.form["price"]
    hotel_id = request.form["hotel_id"]

    if description in hotels.get_all_room_names_by_hotel_id(hotel_id):
        return render_template("error.html", message='Huoneen kuvaus on jo olemassa')
    if not guests.isdigit():
        return render_template("error.html", message='Anna asiakkaiden määrä kokonaislukuna')
    if not square_meters.isdigit():
        return render_template("error.html", message='Anna pinta-ala kokonaislukuna')
    if not number_of_rooms.isdigit():
        return render_template("error.html", message='Anna huoneiden lukumäärä kokonaislukuna')
    if not price.isdigit():
        return render_template("error.html", message='Anna hinta kokonaislukuna')

    hotels.add_room(hotel_id,
                    description,
                    int(guests), int(square_meters),
                    int(number_of_rooms),
                    float(price))

    return render_template("/add_amenity.html",
                           hotels=hotels.get_hotels_by_owner_id(users.user_id()),
                           selected_hotel=hotels.get_hotel_information(hotel_id),
                           amenities=hotels.get_amenities(hotel_id),
                           rooms=hotels.get_rooms(hotel_id),
                           count_rooms=hotels.count_rooms_by_hotel_id(hotel_id))

@app.route("/book_hotel", methods=["POST"])
def show_available_hotels():
    users.check_csrf()
    check_in = request.form["check_in"]
    check_out = request.form["check_out"]
    customers = request.form["customers"]

    if check_in == "" or check_out == "":
        return render_template("error.html", message="Anna tulo- ja lähtöpäivämäärät")
    if datetime.strptime(check_in, "%Y-%m-%d") < datetime.today():
        return render_template("error.html", message="Päivää ei ole enää mahdollista varata")
    if datetime.strptime(check_in, "%Y-%m-%d") > datetime.strptime(check_out, "%Y-%m-%d"):
        return render_template("error.html", message="Tulopäivä ei voi olla lähtöpäivän jälkeen")
    if customers == "" or not customers.isdigit():
        return render_template("error.html", message="Anna asiakkaiden lukumäärä kokonaislukuna")
    if int(customers) > 10 or int(customers) < 1:
        return render_template("error.html", message="Asiakkaita voi olla väliltä 1-10")

    available_hotels = reservations.get_available_hotels(datetime.strptime(check_in, "%Y-%m-%d"), customers)

    return render_template("book_hotel.html",
                           check_in=check_in,
                           check_out=check_out,
                           customers=int(customers),
                           available_hotels=available_hotels)

@app.route("/hotel_rooms", methods=["POST"])
def show_available_rooms():
    users.check_csrf()
    check_in = str(request.form["check_in"])
    check_out = str(request.form["check_out"])
    guests = request.form["guests"]
    hotel_id = request.form["hotel_id"]
    available_rooms = reservations.get_available_rooms(hotel_id=hotel_id, reservation_date=check_in)
    hotel_name = hotels.get_hotel_information(hotel_id)[1]

    return render_template("hotel_rooms.html",
                           hotel_name=hotel_name,
                           available_rooms=available_rooms,
                           check_in=check_in,
                           check_out=check_out,
                           guests=guests,
                           hotel_id=hotel_id)

@app.route("/bookings")
def bookings():
    reserved_rooms = reservations.get_reservations_by_customer_id(users.user_id())
    return render_template("bookings.html",
                           reserved_rooms=reserved_rooms,
                           new_booking=False,
                           number_of_reservations=len(reserved_rooms))

@app.route("/cancel_reservation", methods=["POST"])
def cancel_reservation():
    users.check_csrf()
    reservation_id = request.form["reservation_id"]
    check_in = request.form["check_in"]
    check_out = request.form["check_out"]
    room_id = request.form["room_id"]

    reservations.cancel_reservation(reservation_id)
    reservations.add_available_rooms(room_id, check_in, check_out)

    reserved_rooms = reservations.get_reservations_by_customer_id(users.user_id())
    return render_template("bookings.html",
                           reserved_rooms=reserved_rooms,
                           new_booking=False,
                           number_of_reservations=len(reserved_rooms))



@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        users.check_csrf()
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
        users.check_csrf()
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
                           hotel_name=hotel_name,
                           rooms=rooms,
                           amenities=amenities)

@app.route("/create_hotel", methods=["POST"])
def create_hotel():
    users.check_csrf()
    hotel_name = request.form["hotel_name"]
    hotel_address = request.form["hotel_address"]
    stars = request.form["stars"]

    if hotel_name == "":
        return render_template("error.html", message="Anna hotellille nimi")
    if hotel_name in hotels.get_all_hotel_names():
        return render_template("error.html", message="Hotellin nimi on jo käytössä")
    if hotel_address == "":
        return render_template("error.html", message="Anna hotellille osoite")
    if not stars.isdigit():
        return render_template("error.html", message="Anna tähdet kokonaislukuna 1-5 väliltä")
    if int(stars) > 5 or int(stars) < 1:
        return render_template("error.html", message="Anna tähdet kokonaislukuna 1-5 väliltä")

    hotels.add_hotel(hotel_name, hotel_address, int(stars), users.user_id())

    return render_template("modify_hotels.html",
                           hotels=hotels.get_hotels_by_owner_id(users.user_id()),
                           count_hotels=hotels.count_hotels_by_owner_id(users.user_id()))

@app.route("/delete_hotel", methods=["POST"])
def delete_hotel():
    users.check_csrf()
    hotel_id = request.form["hotel_id"]

    hotels.delete_hotel(hotel_id)
    return render_template("modify_hotels.html",
                           hotels=hotels.get_hotels_by_owner_id(users.user_id()),
                           count_hotels=hotels.count_hotels_by_owner_id(users.user_id()))

@app.route("/update_booking_calendar", methods=["POST"])
def update_booking_calendar():
    users.check_csrf()
    room_id = request.form["room_id"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    hotel_id = request.form["hotel_id"]

    if start_date == "" or end_date == "":
        return render_template("error.html",
                               message='Anna aloitus ja lopetuspäivämäärä')

    start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d")

    if start_date > end_date:
        return render_template("error.html",
                               message='Aloituspäivä ei voi olla lopetuspäivän jälkeen')

    reservations.add_new_dates_to_calendar(start_date=start_date,
                                           end_date=end_date,
                                           room_id=room_id,
                                           available_rooms=hotels.get_room_guest_number(room_id)[0])

    return render_template("/add_amenity.html",
                           hotels=hotels.get_hotels_by_owner_id(users.user_id()),
                           selected_hotel=hotels.get_hotel_information(hotel_id),
                           amenities=hotels.get_amenities(hotel_id),
                           rooms=hotels.get_rooms(hotel_id),
                           count_rooms=hotels.count_rooms_by_hotel_id(hotel_id))

@app.route("/create_booking", methods=["POST"])
def create_booking():
    users.check_csrf()
    room_id = request.form["room_id"]
    check_in = datetime.strptime(request.form["check_in"], "%Y-%m-%d")
    check_out = datetime.strptime(request.form["check_out"], "%Y-%m-%d")
    guests = int(request.form["guests"])
    hotel_id = request.form["hotel_id"]

    reservations.add_reservation(room_id,
                                 users.user_id(), check_in,
                                 check_out, guests, hotel_id)

    return render_template("/bookings.html",
                           reserved_rooms=reservations.get_reservations_by_customer_id(users.user_id()),
                           new_booking=True)
