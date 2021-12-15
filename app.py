from flask import Flask
from flask_restful import Api

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_fleet.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)