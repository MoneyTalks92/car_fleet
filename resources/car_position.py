from flask_restful import Resource, reqparse
from models.car import CarModel
from models.position import PositionModel
from sqlalchemy.sql.functions import now


class CarPosition(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('latitude',
                      type=float,
                      required=True,
                      help="This field cannot be blank.")
  parser.add_argument('longitude',
                      type=float,
                      required=True,
                      help="This field cannot be blank.")

  def post(self, plate):
    data = CarPosition.parser.parse_args()
    car = CarModel.find_by_attribute(license_plate=plate)
    if not car:
      return {"message": "this car does not exist"}, 404
    car_position = PositionModel(car_id=car.id,
                                 latitude=data['latitude'],
                                 longitude=data['longitude'])
    car_position.date = now()
    try:
      car_position.save_to_db()
    except Exception:
      return {'message': 'error during database communication...'}, 400
    return {'message': 'Successfully saved!'}, 201
