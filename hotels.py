from db import db

def add_hotel(hotel_name, hotel_address, stars):
    sql = "INSERT INTO hotels (hotel_name, hotel_address, stars) VALUES (:hotel_name, :hotel_address, :stars)"
    db.session.execute(sql, {"hotel_name":hotel_name, "hotel_address": hotel_address, "stars":stars})
    db.session.commit()

def get_all_hotels():
    sql = "SELECT id, hotel_name FROM hotels"
    
    return db.session.execute(sql).fetchall()

def get_hotel_info(hotel_id):
    sql = "SELECT hotel_name FROM hotels WHERE id= :hotel_id"
    
    return db.session.execute(sql, {"hotel_id": hotel_id}).fetchone()
