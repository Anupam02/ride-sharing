from ma import ma
from models.vehicle import VehicleModel
from models.user import UserModel


class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VehicleModel
        load_instance = True
        load_only = ("user",)
        include_fk= True
