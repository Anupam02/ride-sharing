from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db

from resources.user import User, UserFetch, user_ns
from resources.vehicle import Vehicle, VehicleFetch, vehicle_ns
from resources.ride import Ride, SelectRides, EndRides, TotalRides, ride_ns


from marshmallow import ValidationError

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Ride Sharing Management Service')
app.register_blueprint(bluePrint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(user_ns)
api.add_namespace(vehicle_ns)
api.add_namespace(ride_ns)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True,host='0.0.0.0')
