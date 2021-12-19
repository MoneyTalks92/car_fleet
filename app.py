from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.car import Car, CarList
from resources.user import UserRegister
from resources.driver import Driver
from resources.assign import AssignDriverToCar
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

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)