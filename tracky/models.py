import datetime

from flask.ext.login import UserMixin

from sqlalchemy import Column, Integer, String, Sequence, Text, DateTime, ForeignKey

from sqlalchemy.orm import relationship

from database import Base, engine


class Activity(Base):
    __tablename__ = 'activities'

    activity_id = Column(Integer, Sequence("activity_id_sequence"), primary_key=True)
    title = Column(String(1024))
    activity = Column(String(1024))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(String(1024))
    start_location = Column(String(1024))
    end_location = Column(String(1024))
    notes = Column(Text)
    calories = Column(Integer)
    entry_date = Column(DateTime, default=datetime.datetime.now)


class Meal(Base):
    __tablename__ = 'meal'

    meal_id = Column(Integer, Sequence('meal_id_sequence'), primary_key=True)
    meal = Column(String(1024))
    contents = Column(String(1024))
    calories = Column(Integer)
    entry_date = Column(DateTime, default=datetime.datetime.now)

Base.metadata.create_all(engine)


