from datetime import timedelta

from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "111"
app.permanent_session_lifetime = timedelta(days=365)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Init123#@localhost:5432/pizza_shop"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Pizzas(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR)
    properties = db.Column(db.TEXT)
    price = db.Column(db.REAL)
    image = db.Column(db.TEXT)
    type = db.Column(db.VARCHAR)


class Users(db.Model, UserMixin):
    id = db.Column(db.INTEGER, primary_key=True)
    login = db.Column(db.VARCHAR)
    password = db.Column(db.VARCHAR)
    address = db.Column(db.TEXT)
    phone = db.Column(db.VARCHAR)
    role = db.Column(db.VARCHAR)
    orders = db.Column(db.ARRAY(db.INTEGER))


class Ord(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    pizza_id = db.Column(db.INTEGER)
    size = db.Column(db.INTEGER)
    quantity = db.Column(db.INTEGER)
    price = db.Column(db.REAL)


class Receipt(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    orders = db.Column(db.ARRAY(db.INTEGER))
    user_id = db.Column(db.INTEGER)
    total_price = db.Column(db.REAL)