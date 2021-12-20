from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.car import Car, CarList
from resources.fleet import Fleet, FleetList
from resources.user import UserRegister
from resources.driver import Driver
from resources.assign import AssignDriverToCar
from resources.car_fleet import CarFleet
from resources.car_position import CarPosition
from models.position import PositionModel
from models.fleet import FleetModel
from models.car_fleet import CarFleetLink
from security import authenticate, identity
from db import db
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = environ.get(
    'SQLALCHEMY_TRACK_MODIFICATIONS')
app.secret_key = environ.get('SECRET_KEY')

api = Api(app)
db.init_app(app)


@app.before_first_request
def create_tables():
  db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(CarList, '/cars')
api.add_resource(Car, '/car/<string:plate>')
api.add_resource(UserRegister, '/register')
api.add_resource(Driver, '/driver')
api.add_resource(AssignDriverToCar, '/assign')
api.add_resource(Fleet, '/fleet/<string:name>')
api.add_resource(FleetList, '/fleets')
api.add_resource(CarFleet, '/car_fleet')
api.add_resource(CarPosition, '/car/<string:plate>/position')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)