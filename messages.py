
import os
from db import db
from flask import abort, request, session

def send(hotel_name, hotel_address, stars):
    try:
        sql = "INSERT INTO hotels (hotel_name, hotel_address, stars) VALUES (:hotel_name, :hotel_address, :stars)"
        db.session.execute(sql, {"hotel_name":hotel_name, "hotel_address": hotel_address, "stars":stars})
        db.session.commit()

        return True
    except Exception as e:
        print(e)
        return False