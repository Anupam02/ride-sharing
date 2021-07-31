from flask import request
from flask_restplus import Resource, fields, Namespace
from models import vehicle

from models.user import UserModel
from schemas.user import UserSchema

from models.vehicle import VehicleModel
from schemas.vehicle import VehicleSchema


USER_NOT_FOUND = "User not found."


user_ns = Namespace('user', description='Users')


user_schema = UserSchema()
vehicle_schema = VehicleSchema()


user_api_model = user_ns.model('UserApiModel', {
    'name': fields.String(description='Name of the User',
                                    required=True,
                                    example='Rohan'),
    'gender': fields.String(description='gender',
                                    required=True,
                                    example='M'),
    'age': fields.Integer(description='Age',
                                    required=True,
                                    example=36)
})

user_success = user_ns.model('UserCreated', {
    'id': fields.String(description='Id of the User',
                                    required=True,
                                    example=1),
    'name': fields.String(description='Name of the User',
                                    required=True,
                                    example='Rohan'),
    'gender': fields.String(description='gender',
                                    required=True,
                                    example='M'),
    'age': fields.Integer(description='Age',
                                    required=True,
                                    example=36)
})


@user_ns.route('', methods=["POST"])
class User(Resource):

    @user_ns.response(201, 'Created User', model=user_success)
    @user_ns.response(400, 'Bad Request')
    @user_ns.expect(user_api_model)
    def post(self):

        try:
            user_json = request.get_json()

            user_data = user_schema.load(user_json)
            user_data.save_to_db()

            return {'status': 'success', 'response': user_schema.dump(user_data)}, 201

        except BaseException as e:
            print(e, flush=True)
            return {'status': 'failure', 'message': 'User Creation Failed'}, 400


@user_ns.route('/<string:id>', methods=['GET'])
class UserFetch(Resource):
    @user_ns.response(200, 'User Json', model=user_success)
    @user_ns.response(404, 'User Not Found')
    @user_ns.response(400, 'Bad Request')
    def get(self, id):
        try:

            user_data = UserModel.find_by_id(id)
            if user_data:

                return {'status': 'success', 'response': user_schema.dump(user_data.json())}, 200
            else:
                return {'status': 'failure', 'message': f'{id} not found'}, 404

        except BaseException as e:
            print(e, flush=True)
            return {'status': 'failure', 'message': 'User Fetch Failed'}, 400
            
# class Vehilce(Resource):

#     def get(self, user_id):
#         user_name = VehicleModel.find_user_by_id(user_id)
#         if user_name:
#             return {'status': 'success', 'response': assignment_schema.dump(assignment_data)}, 201
#         return {'message': ASSIGNMENT_NOT_FOUND}, 404
