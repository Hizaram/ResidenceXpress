#!/usr/bin/python
""" holds class Lodge"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

if models.storage_t == 'db':
    lodge_amenity = Table('lodge_amenity', Base.metadata,
                          Column('lodge_id', String(60),
                                 ForeignKey('lodges.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))


class Lodge(BaseModel, Base):
    """Representation of Lodge """
    if models.storage_t == 'db':
        __tablename__ = 'lodges'
        street_id = Column(String(60), ForeignKey('streets.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        price = Column(Integer, nullable=False, default=0)
        reviews = relationship("Review",
                               backref="lodge",
                               cascade="all, delete, delete-orphan")
        amenities = relationship("Amenity",
                                 secondary=lodge_amenity,
                                 viewonly=False)
    else:
        street_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        price = 0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    if models.storage_t != 'db':
        @property
        def reviews(self):
            """getter attribute returns the list of Review instances"""
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.lodge_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """getter attribute returns the list of Amenity instances"""
            from models.amenity import Amenity
            amenity_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.lodge_id == self.id:
                    amenity_list.append(amenity)
            return amenity_list
