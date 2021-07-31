from flask import request
from flask_restplus import Resource, fields, Namespace
from models import vehicle

from models.user import UserModel
from schemas.user import UserSchema

from models.vehicle import VehicleModel
from schemas.vehicle import VehicleSchema

from models.ride import RideModel

USER_NOT_FOUND = "Ride not found."


ride_ns = Namespace('rides', description='Ridess')


rides_api_model = ride_ns.model('RidesApiModel', {
    'user_name': fields.String(description='User Name',
                                    required=True,
                                    example='Rohan'),
    'origin': fields.String(description='origin',
                            required=True,
                            example='Hyderabad'), 
    'available_seats': fields.Integer(description='available seats',
                            required=True,
                            example=2),                                                         
    'vehicle_type': fields.String(description='Vehicle Name',
                                 required=True,
                                 example='Baleno'),
    'license_plate_no': fields.String(description='License Plate No',
                                 required=True,
                                 example='KA-01-12345'),
    'destination': fields.String(description='destination',
                            required=True,
                            example='Bangalore')
})

ride_success = ride_ns.model('RideCreated', {
    'user_name': fields.String(description='User Name',
                                    required=True,
                                    example='Rohan'),
    'origin': fields.String(description='origin',
                            required=True,
                            example='Hyderabad'), 
    'available_seats': fields.Integer(description='available seats',
                            required=True,
                            example=2),                                                         
    'vehicle_type': fields.String(description='Vehicle Name',
                                 required=True,
                                 example='Baleno'),
    'license_plate_no': fields.String(description='License Plate No',
                                 required=True,
                                 example='KA-01-12345'),
    'destination': fields.String(description='destination',
                            required=True,
                            example='Bangalore')
})


select_rides_api_model = ride_ns.model('SelectRidesApiModel', {
    'user_name': fields.String(description='user name',
                                    required=True,
                                    example='Nandini'),
    'origin': fields.String(description='origin',
                            required=True,
                            example='Bangalore'), 
    'seats_requested': fields.Integer(description='requested seats',
                            required=True,
                            example=1),                                                         
    'preference': fields.String(description='Preference',
                                 required=True,
                                 example='most vacant'),
    'destination': fields.String(description='destination',
                            required=True,
                            example='Mysore')
})


@ride_ns.route('', methods=["POST"])
class Ride(Resource):

    @ride_ns.response(201, 'Created Ride', model=ride_success)
    @ride_ns.response(400, 'Bad Request')
    @ride_ns.expect(rides_api_model)
    def post(self):

        try:
            payload = ride_ns.payload
            print(payload, flush=True)
            user_name = payload['user_name']
            print(user_name, flush=True)
            vehicle_type = payload['vehicle_type']
            print(vehicle_type, flush=True)

            vehicle_row_set = RideModel.find_vehilcle_by_type(vehicle_type)
            print(vehicle_row_set.id, flush=True)
            user_row_set = RideModel.find_user_by_name(user_name)
            print(user_row_set.id, flush=True)
            if vehicle_row_set and user_row_set:
                vehicle_id = vehicle_row_set.id
                user_id = user_row_set.id

                ride_data = RideModel(user_id=user_id,
                                    vehicle_id=vehicle_id,
                                    origin=payload['origin'],
                                    destination=payload['destination'],
                                    available_seats=payload['available_seats'],
                                    status='offered',
                                    license_plate_no=payload['license_plate_no'])
                ride_data.save_to_db()
                return {'status': 'success', 'response': ride_data.json()}, 201
            
            else:
                return {'status': 'failure', 'message': f'User or Vehicle Not Found'}, 404

           

        except BaseException as e:
            print(e, flush=True)
            return {'status': 'failure', 'message': 'Ride Creation Failed'}, 400


@ride_ns.route('/select_rides', methods=["POST"])
class SelectRides(Resource):

    @ride_ns.response(200, 'Selected Ride JSON', model=ride_success)
    @ride_ns.response(400, 'Bad Request')
    @ride_ns.expect(select_rides_api_model)
    def post(self):

        try:
            payload = ride_ns.payload
    
            requested_seats = payload['seats_requested']
            rides_row_set = RideModel.fetch_rides_with_requested_seats(requested_seats)
            if rides_row_set:
                rides_id = rides_row_set.id
                new_status = 'booked'

                ride_data = RideModel(
                                    user_id=rides_row_set.user_id,
                                    vehicle_id=rides_row_set.vehicle_id,
                                    origin=rides_row_set.origin,
                                    destination=rides_row_set.destination,
                                    available_seats=rides_row_set.available_seats - requested_seats,
                                    status=new_status,
                                    license_plate_no=rides_row_set.license_plate_no)
                rides_json = ride_data.json()
                rides_json['id'] = rides_id
                ride_data.update_to_db()
                return {'status': 'success', 'response': rides_json}, 200
            
            else:
                return {'status': 'failure', 'message': f'Requested Seat Not found in any Rides'}, 202

           

        except BaseException as e:
            print(e, flush=True)
            return {'status': 'failure', 'message': 'Ride Creation Failed'}, 400




@ride_ns.route('/end_rides/<string:ride_id>', methods=["POST"])
class EndRides(Resource):

    @ride_ns.response(200, 'Ride Ended')
    @ride_ns.response(400, 'Bad Request')
    def post(self, ride_id):

        try:
            ride_data = RideModel.find_by_id(id)
            if ride_data:
                ride_json = ride_data.json()
                new_status = 'ended'
                ride_data = RideModel(
                                    user_id=ride_data.user_id,
                                    vehicle_id=ride_data.vehicle_id,
                                    origin=ride_data.origin,
                                    destination=ride_data.destination,
                                    available_seats=ride_data.available_seats,
                                    status=new_status,
                                    license_plate_no=ride_data.license_plate_no)
                ride_data.update_to_db()
                ride_json = ride_data.json()

                return {'status': 'success', 'response': ride_json}, 200
               
            else:
                return {'status': 'failure', 'message': 'Ride ID  Not found'},  404

           

        except BaseException as e:
            print(e, flush=True)
            return {'status': 'failure', 'message': 'Ride End Failed'}, 400



@ride_ns.route('/total_rides/<string:user_name>', methods=["GET"])
class TotalRides(Resource):

    @ride_ns.response(200, 'Total Rides')
    @ride_ns.response(400, 'Bad Request')
    def get(self, user_name):

        try:
            user_row_set = RideModel.find_user_by_name(user_name)
            user_id = user_row_set.id
            rides_taken_resp = RideModel.rides_taken_by_user(user_id)
            print(rides_taken_resp.count, flush=True)

            rides_offered_resp = RideModel.rides_offered_by_user(user_id)

          
            return {'status': 'success', 'response': 'dummy' }, 200


        except BaseException as e:
            print(e, flush=True)
            return {'status': 'failure', 'message': 'Ride End Failed'}, 400