import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask import abort, request, session
from db import db

def register(name, password, role):
    hash_value = generate_password_hash(password)
    sql = """INSERT INTO users (username, password, role)
                VALUES (:name, :password, :role)"""
    db.session.execute(sql, {"name":name, "password":hash_value, "role":role})
    db.session.commit()

    return login(name, password)

def login(username, password):
    sql = "SELECT password, id, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = username
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()

    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]

def user_id():
    return session.get("user_id", 0)

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
