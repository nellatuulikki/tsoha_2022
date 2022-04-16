import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash,  generate_password_hash

def register(name, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, password, role)
                 VALUES (:name, :password, :role)"""
        db.session.execute(sql, {"name":name, "password":hash_value, "role":role})
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True

def user_id():
    return session.get("user_id", 0)

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)