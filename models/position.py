from db import db, BaseModel
from models.model_mixin import MixinModel
import requests, json
from urllib.parse import urlparse


class PositionModel(BaseModel, MixinModel):
  __tablename__ = 'positions'

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime)
  latitude = db.Column(db.Float(precision=5))
  longitude = db.Column(db.Float(precision=5))
  address = db.Column(db.String(300))
  # one to many with bidirectional relationship
  # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
  car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
  car = db.relationship('CarModel', back_populates='positions')

  def __init__(self, car_id, latitude, longitude):
    self.car_id = car_id
    self.latitude = latitude
    self.longitude = longitude

  def json(self):
    position_json = {
        'latitude': self.latitude,
        'longitude': self.longitude,
        'date': self.date.isoformat(),
        'address': self.address
    }
    return position_json

  def resolve_address(latitude, longitude):
    try:
      url = requests.get(
          urlparse(
              f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
          ).geturl())
      data = json.loads(url.text)
      return data['display_name']
    except:
      return ""