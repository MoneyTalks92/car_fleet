from models.car_fleet import CarFleetLink
from models.fleet import FleetModel
from models.model_mixin import MixinModel
from flask_restful import Resource, reqparse
from models.car import CarModel


class CarFleet(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('car_id',
                      type=int,
                      required=True,
                      help="This field cannot be blank.")
  parser.add_argument('fleet_id',
                      type=int,
                      required=True,
                      help="This field cannot be blank.")

  def post(self):
    data = CarFleet.parser.parse_args()
    car = CarModel.find_by_attribute(id=data['car_id'])
    if not car:
      return {"message": "this car does not exist"}, 404
    fleet = FleetModel.find_by_attribute(id=data['fleet_id'])
    if not fleet:
      return {"message": "this fleet does not exist"}, 404

    if CarFleetLink.find_by_attribute(car_id=data['car_id'],
                                      fleet_id=data['fleet_id']):
      return {"message": "this car is already in this fleet"}, 200

    link = CarFleetLink(car_id=data['car_id'], fleet_id=data['fleet_id'])
    link.save_to_db()

    return {"message": "Car is assigned to fleet"}, 201