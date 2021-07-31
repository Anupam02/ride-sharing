from flask import request
from flask_restplus import Resource, fields, Namespace
from models import vehicle

from models.vehicle import VehicleModel
from schemas.vehicle import VehicleSchema
# from models.tag import TagModel
# from schemas.tag import TagSchema

# from models.assignment_tag_mapping import AssignmentTagMappingModel
# from schemas.tag import TagSchema
# from schemas.assignment import AssignmentSchema


VEHICLE_NOT_FOUND = "Vehicle not found."

vehicle_ns = Namespace('vehicles', description='Vehicle related operations')

vehicle_schema = VehicleSchema(many=True)


vehicle_api_model = vehicle_ns.model('VehicleApiModel', {
    'user_name': fields.String(description='Name of the User',
                                    required=True,
                                    example='Rohan'),
    'vehicle_type': fields.String(description='Vehicle Type',
                                    required=True,
                                    example='Baleno'),
    'license_plate_no': fields.String(description='vehicles license plate no',
                                    required=True,
                                    example='KA-01-12345')
})

vehicle_success = vehicle_ns.model('VehicleCreated', {
    'id': fields.String(description='Id of the Vehicle',
                                    required=True,
                                    example='1'),
    'user_id': fields.Integer(description='User ID',
                                    required=True,
                                    example=1),
    'vehicle_type': fields.String(description='Vehicle Type',
                                    required=True,
                                    example='Baleno'),
    'license_plate_no': fields.String(description='vehicles license plate no',
                                    required=True,
                                    example='KA-01-12345')
})



@vehicle_ns.route('', methods=["POST"])
class Vehicle(Resource):

    @vehicle_ns.response(201, 'Created Vehicle', model=vehicle_success)
    @vehicle_ns.response(404, 'User Name not Found')
    @vehicle_ns.response(400, 'Bad Request')
    @vehicle_ns.expect(vehicle_api_model)
    def post(self):

        try:
            vehicle_json = request.get_json()
            user_name = vehicle_json["user_name"]
            print(user_name)
            row_set = VehicleModel.find_user_by_name(user_name)
            user_id = row_set.id
            if row_set:
                del vehicle_json['user_name']
                vehicle_json['user_id'] = user_id
                print(f"vehicle json = {vehicle_json}")
                vehicle_data = VehicleModel(user_id, vehicle_json['vehicle_type'], vehicle_json['license_plate_no'])
                vehicle_data.save_to_db()
                print('after saving')
                # vehicle_data = vehicle_schema.load(vehicle_json)
                # print(vehicle_data)
                # vehicle_data.save_to_db()

                return {'status': 'success', 'response': vehicle_data.json()}, 201
            else:
                return {'status': 'failure', 'response': f'{user_name} not found'}, 404


        except BaseException as e:
            print(e, flush=True)
            return {'status': 'failure', 'message': 'Vehicle Creation Failed'}, 400



@vehicle_ns.route('/<string:id>', methods=['GET'])
class VehicleFetch(Resource):
    @vehicle_ns.response(200, 'Vehicle Json', model=vehicle_success)
    @vehicle_ns.response(404, 'Vehilce Not Found')
    @vehicle_ns.response(400, 'Bad Request')
    def get(self, id):
        try:

            vehicle_data = VehicleModel.find_by_id(id)
            if vehicle_data:

                return {'status': 'success', 'response': vehicle_schema.dump(vehicle_data.json())}, 200
            else:
                return {'status': 'failure', 'message': f'{id} not found'}, 404

        except BaseException as e:
            print(e, flush=True)
            return {'status': 'failure', 'message': 'Vehicle Fetch Failed'}, 400
