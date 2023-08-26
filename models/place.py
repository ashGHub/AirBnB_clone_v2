#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base, Column, String, Integer, Float, ForeignKey, relationship
from models.amenity import Amenity, place_amenities

class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = 'places'
    
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    amenity_ids = []

    reviews = relationship('Review', backref='place', cascade='all, delete, delete-orphan')
    place_amenities = relationship('Amenity', secondary=place_amenities, viewonly=False)

    @property
    def reviews(self):
        """ Returns the list of Review instances with place id equals to the current Place.id """
        return [review for review in self.reviews]
    
    @property
    def amenities(self):
        """Getter attribute for amenities"""
        amenities = []
        for amenity_id in self.amenity_ids:
            amenity = Amenity.get(amenity_id)
            amenities.append(amenity)
        return amenities
    
    @amenities.setter
    def amenities(self, amenity):
        """ Setter attribute for amenities """
        if isinstance(amenity, Amenity):
            self.amenity_ids.append(amenity.id)
