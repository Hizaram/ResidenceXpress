#!/usr/bin/python
""" holds class Street"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Street(BaseModel, Base):
    """Representation of street """
    if models.storage_t == "db":
        __tablename__ = 'streets'
        location_id = Column(String(60), ForeignKey('locations.id'), nullable=False)
        name = Column(String(128), nullable=False)
        lodges = relationship("Lodge",
                              backref="streets",
                              cascade="all, delete, delete-orphan")
    else:
        location_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
