from models import user
from db import db
from typing import List


class RideModel(db.Model):
    __tablename__ = "rides"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    origin = db.Column(db.String(100), nullable=False, unique=False)
    destination = db.Column(db.String(100), nullable=False, unique=False)
    available_seats = db.Column(db.Integer, nullable=False, unique=False)
    status = db.Column(db.String(100), nullable=False, unique=False)
    license_plate_no = db.Column(db.String(100), nullable=False, unique=False)
    

    def __init__(self, user_id, vehicle_id, origin, destination, available_seats, status,
    license_plate_no):
        self.user_id = user_id
        self.vehicle_id = vehicle_id
        self.origin = origin
        self.destination = destination
        self.available_seats = available_seats
        self.status = status
        self.license_plate_no = license_plate_no



    def json(self):
        return {
            'user_id': self.user_id,
            'vehicle_id': self.vehicle_id,
            'origin': self.origin,
            'destination': self.destination,
            'available_seats': self.available_seats,
            'status': self.status
            }

    @classmethod
    def find_by_id(cls, _id) -> "RideModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def rides_taken_by_user(cls, user_id):
        return db.session.execute(f"SELECT COUNT(*) from rides WHERE user_id = {user_id} AND status = 'ended'").first()

    @classmethod
    def rides_offered_by_user(cls, user_id):
        return db.session.execute(f"SELECT COUNT(*) from rides WHERE user_id = {user_id} AND status = 'offered'").first()
    
    @classmethod
    def fetch_rides_with_requested_seats(cls, seats):
        return db.session.execute(f"SELECT * from rides WHERE available_seats >= {seats} AND status = 'offered'").first()

    @classmethod
    def find_user_by_name(cls, user_name):
        return db.session.execute('SELECT id from users WHERE name = :user_name', {'user_name': user_name}).first()

    @classmethod
    def find_vehicle_by_id(cls, id):
        return db.session.execute('SELECT * from vehicles WHERE id = :id', {'id': id}).first()

    @classmethod
    def find_vehilcle_by_type(cls, vehicle_type):
        return db.session.execute('SELECT id from vehicles WHERE vehicle_type= :vehicle_type', {'vehicle_type': vehicle_type}).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def update_to_db(self) -> None:
        db.session.merge(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
