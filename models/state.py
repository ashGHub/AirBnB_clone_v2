#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import BaseModel, Base, Column, String, relationship

class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='all, delete, delete-orphan')

    @property
    def cities(self):
        """ Returns the list of City instances with state_id equals to the current State.id """
        return [city for city in self.cities]
