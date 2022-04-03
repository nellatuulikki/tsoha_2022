from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

import routes