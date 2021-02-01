from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique = True)
    name = db.Column(db.String(128))


class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text())
    price = db.Column(db.Float())
    at = db.Column(db.Boolean)
    free = db.Column(db.Boolean)
    img_url1 = db.Column(db.String(128))
    img_url2 = db.Column(db.String(128))
    img_url3 = db.Column(db.String(128))
    img_url4 = db.Column(db.String(128))
    created = db.Column(db.DateTime, default=datetime.now)


class RentTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auto = db.Column(db.Integer)
    start_rent = db.Column(db.DateTime)
    end_rent = db.Column(db.DateTime)
    cost = db.Column(db.Float())
