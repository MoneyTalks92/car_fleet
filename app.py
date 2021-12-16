from flask import Flask
from flask_restful import Api
from resources.car import Car, CarList
from db import db
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db.init_app(app)


@app.before_first_request
def create_tables():
  db.create_all()


api.add_resource(CarList, '/cars')
api.add_resource(Car, '/car/<string:plate>')