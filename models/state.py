#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.city import City
from models.base_model import BaseModel, Base, Column, String, relationship
import models


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship(
        'City',
        backref='state',
        cascade='all, delete, delete-orphan')

    @property
    def cities(self):
        """ Returns the list of city of the current state """
        cities = models.storage.all(City)
        cities_list = []
        for city in cities.values():
            if city.state_id == self.id:
                cities_list.append(city)
        return cities_list
