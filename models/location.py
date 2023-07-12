#!/usr/bin/python3
""" holds class Location"""
import models
from models.base_model import BaseModel, Base
from models.street import Street
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Location(BaseModel, Base):
    """Representation of location """
    if models.storage_t == "db":
        __tablename__ = 'locations'
        name = Column(String(128), nullable=False)
        streets = relationship("Street",
                              backref="location",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def streets(self):
            """getter for list of street instances related to the location"""
            street_list = []
            all_streets = models.storage.all(Street)
            for street in all_streets.values():
                if street.location_id == self.id:
                    street_list.append(street)
            return street_list
