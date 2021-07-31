from db import db
from typing import List


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    gender = db.Column(db.String(100), nullable=False, unique=False)
    age = db.Column(db.Integer, nullable=False, unique=False)
    vehicle_id = db.relationship(
        "VehicleModel", lazy="dynamic", primaryjoin="UserModel.id == VehicleModel.user_id")

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def __repr__(self):
        return 'UserModel(name=%s, gender=%s,age=%s)' % (self.name, self.gender, self.age)

    def json(self):
        return {
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }

    @classmethod
    def find_by_id(cls, _id) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
