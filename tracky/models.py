import datetime

from flask.ext.login import UserMixin

from sqlalchemy import Column, Integer, String, Sequence, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, engine


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, Sequence("activity_id_sequence"), primary_key=True)
    title = Column(String(1024))
    activity = Column(String(1024))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    start_location = Column(String(1024))
    end_location = Column(String(1024))
    notes = Column(Text)
    entry_date = Column(DateTime, default=datetime.datetime.now)


Base.metadata.create_all(engine)


