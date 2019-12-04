from __future__ import absolute_import

from . import db, BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.constants import ORDER_WAITING_CONFIRMATION, STATUS_USER_ACTIVE


class UserModel(BaseModel):
    __tablename__ = "user"
    public_id = db.Column(db.BigInteger)
    email = db.Column(db.String(), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(), unique=True, nullable=False, index=True)
    name = db.Column(db.String(), nullable=False)
    status = db.Column(db.Integer, default=STATUS_USER_ACTIVE)
    role = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(), nullable=False)
    image_uri = db.Column(db.String())
    number_plate = db.Column(db.String())
    device_id = db.Column(db.String())
    ride_category = db.Column(db.Integer)
    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)
    current_status = db.Column(db.Integer)
