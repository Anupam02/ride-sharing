from models import user
from db import db
from typing import List


class VehicleModel(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_type = db.Column(db.String(100), nullable=False, unique=False)
    license_plate_no = db.Column(db.String(100), nullable=False, unique=False)

    def __init__(self, user_id, vehicle_type, license_plate_no):
        self.user_id = user_id
        self.vehicle_type = vehicle_type
        self.license_plate_no = license_plate_no

    def __repr__(self):
        return 'VehicleModel(user_id=%s, vehicle_type=%s, license_plate_no=%s)' % (self.user_id, self.vehicle_type, self.license_plate_no)

    def json(self):
        return {
            'user_id': self.user_id,
            'vehicle_type': self.vehicle_type,
            'license_plate_no': self.license_plate_no}

    @classmethod
    def find_by_id(cls, _id) -> "VehicleModel":
        return cls.query.filter_by(id=_id).first()


    @classmethod
    def find_user_by_id(cls, user_id):
        return db.session.execute('SELECT name from users WHERE id = :user_id', {'user_id': user_id}).first()

    @classmethod
    def find_user_by_name(cls, user_name):
        return db.session.execute('SELECT id from users WHERE name = :user_name', {'user_name': user_name}).first()

    @classmethod
    def find_vehicle_by_type(cls, vehicle_type):
        return db.session.execute('SELECT id from vehicles WHERE vehicle_type = :vehicle_type', {'vehicle_type': vehicle_type}).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
