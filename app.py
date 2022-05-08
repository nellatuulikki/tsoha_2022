from flask import Flask
from os import getenv

APP = Flask(__name__)
APP.secret_key = getenv("SECRET_KEY")

