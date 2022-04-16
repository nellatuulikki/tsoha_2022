from db import db

def get_available_hotels(reservation_date, guests):
    sql = "SELECT distinct hotel_id, hotel_name FROM calendar a left join rooms b on (a.room_id = b.id) left join hotels c on (b.hotel_id = c.id) where reservation_date = :reservation_date and available_rooms > 0 and guests >= :guests"
    
    return db.session.execute(sql, {"reservation_date": reservation_date, "guests": guests}).fetchall()

def get_available_rooms(reservation_date, hotel_id):
    sql = "SELECT a.id, room_description, guests, square_meters, hotel_id FROM calendar a left join rooms b on (a.room_id = b.id) where reservation_date = :reservation_date and hotel_id = :hotel_id"

    return db.session.execute(sql, {"reservation_date": reservation_date, "hotel_id":hotel_id}).fetchall()

def add_reservation(room_id, customer_id, check_in, check_out, guests):
    try:
        sql = "INSERT INTO reservations (room_id, customer_id, check_in, check_out, guests) VALUES (:room_id, :customer_id, :check_in, :check_out, :guests)"
        db.session.execute(sql, {"room_id":room_id, "customer_id": customer_id, "check_in":check_in, "check_out":check_out, "guests":guests})
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def get_reservations_by_customer_id(customer_id):
    sql = "SELECT reservation_id, room_id, check_in, check_out, guests FROM reservations WHERE customer_id = :customer_id"
    return db.session.execute(sql, {"customer_id":customer_id}).fetchall()


def update_available_rooms(room_id, check_in):
    try:
        sql = "UPDATE calendar SET available_rooms = available_rooms - 1 where room_id = :room_id and reservation_date = reservation_date"
        db.session.execute(sql, {"room_id":room_id, "reservation_date":check_in})
        db.session.commit()
        return True

    except Exception as e:
        print(e)
        return False
