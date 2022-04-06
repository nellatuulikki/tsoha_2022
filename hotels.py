from db import db

def get_all_hotels():
    sql = "SELECT id, hotel_name FROM hotels"
    
    return db.session.execute(sql).fetchall()

def get_all_amenities_by_hotel_id(hotel_id):
    sql = "SELECT hotel_name FROM hotels WHERE id= :hotel_id"
    
    return db.session.execute(sql, {"hotel_id": hotel_id}).fetchone()

def get_hotel_name(hotel_id):
    sql = "SELECT hotel_name FROM hotels WHERE id= :hotel_id"
    
    return db.session.execute(sql, {"hotel_id": hotel_id}).fetchone()

def get_amenities(hotel_id):
    sql = "SELECT amenity FROM amenities WHERE hotel_id= :hotel_id"
    return db.session.execute(sql, {"hotel_id": hotel_id}).fetchall()

def add_hotel(hotel_name, hotel_address, stars):
    try:
        sql = "INSERT INTO hotels (hotel_name, hotel_address, stars) VALUES (:hotel_name, :hotel_address, :stars)"
        db.session.execute(sql, {"hotel_name":hotel_name, "hotel_address": hotel_address, "stars":stars})
        db.session.commit()

        return True
    except Exception as e:
        print(e)
        return False

def add_amenity(amenities, hotel_id = 1):
    try:
        for amenity in amenities:
            sql = "INSERT INTO amenities (hotel_id, amenity) VALUES (:hotel_id, :amenity)"
            db.session.execute(sql, {"hotel_id":hotel_id, "amenity": amenity})
            db.session.commit()

        return True
    except Exception as e:
        print(e)
        return False