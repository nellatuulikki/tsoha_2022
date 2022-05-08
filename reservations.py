from db import db
from datetime import datetime, timedelta

def get_available_hotels(reservation_date, guests):
    sql = """SELECT distinct hotel_id,hotel_name 
            FROM calendar a 
            left join rooms b on (a.room_id = b.id) 
            left join hotels c on (b.hotel_id = c.id) 
            where reservation_date = :reservation_date and available_rooms > 0 and guests >= :guests"""
    
    return db.session.execute(sql, {"reservation_date": reservation_date, "guests": guests}).fetchall()

def get_available_rooms(reservation_date, hotel_id):
    sql = """SELECT b.id, room_description, guests, square_meters, hotel_id 
            FROM calendar a
            left join rooms b on (a.room_id = b.id) 
            where reservation_date = :reservation_date and hotel_id = :hotel_id"""

    return db.session.execute(sql, {"reservation_date": reservation_date, "hotel_id":hotel_id}).fetchall()

def add_reservation(room_id, customer_id, check_in, check_out, guests, hotel_id):
    try:
        sql = """INSERT INTO reservations (room_id, customer_id, check_in, check_out, guests, hotel_id)
                VALUES (:room_id, :customer_id, :check_in, :check_out, :guests, :hotel_id)"""

        db.session.execute(sql, {"room_id":room_id, "customer_id": customer_id, "check_in":check_in, "check_out":check_out, "guests":guests, "hotel_id":hotel_id})
        db.session.commit()
        substract_available_rooms(room_id, check_in, check_out)
        
        return True

    except Exception as e:
        print(e)
        
        return False

def get_reservations_by_customer_id(customer_id):
    sql = """SELECT reservation_id, room_id, check_in, check_out, guests 
            FROM reservations WHERE customer_id = :customer_id"""

    return db.session.execute(sql, {"customer_id":customer_id}).fetchall()

def get_all_the_dates_by_hotel_room(room_id):
    sql = "SELECT reservation_date from calendar where room_id = room_id"
    return [datetime.strptime(str(date[0]), "%Y-%m-%d") for date in db.session.execute(sql, {"customer_id":room_id}).fetchall()]

def add_new_dates_to_calendar(start_date, end_date, room_id, available_rooms):
    reservation_date = start_date
    
    reservation_dates_for_room = get_all_the_dates_by_hotel_room(room_id)

    while reservation_date <= end_date:
        if not reservation_date in reservation_dates_for_room:
            sql = """INSERT INTO calendar (reservation_date, room_id, available_rooms) 
                    VALUES (:reservation_date, :room_id, :available_rooms)"""

            db.session.execute(sql, {"reservation_date":reservation_date, "room_id":room_id, "available_rooms":available_rooms})
            db.session.commit()
        reservation_date = reservation_date + timedelta(days=1)

def substract_available_rooms(room_id, check_in, check_out):
    try:
        sql = """UPDATE calendar 
                SET available_rooms = available_rooms - 1
                where room_id = :room_id 
                and reservation_date >= :check_in
                and reservation_date < :check_out"""
        db.session.execute(sql, {"room_id":room_id, "check_in":check_in, "check_out":check_out})
        db.session.commit()
        return True

    except Exception as e:
        print(e)
        return False

def add_available_rooms(room_id, check_in, check_out):
    try:
        sql = """UPDATE calendar 
                SET available_rooms = available_rooms + 1 
                where room_id = :room_id 
                and reservation_date >= :check_in
                and reservation_date < :check_out"""
        db.session.execute(sql, {"room_id":room_id, "check_in":check_in, "check_out":check_out})
        db.session.commit()
        return True

    except Exception as e:
        print(e)
        return False

def cancel_reservation(reservation_id):
    try:
        print(reservation_id)
        sql = """DELETE FROM reservations where reservation_id = :reservation_id"""
        db.session.execute(sql, {"reservation_id" :reservation_id})
        db.session.commit()
        return True

    except Exception as e:
        print(e)
        return False

