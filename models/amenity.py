#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, Column, String, ForeignKey, Table


class Amenity(BaseModel, Base):
    """ Amentiy class """

    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)


place_amenities = Table('place_amenities', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)
