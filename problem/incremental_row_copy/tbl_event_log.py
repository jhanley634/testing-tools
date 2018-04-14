# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class EventLog(Base):
    __tablename__ = 'event_log'

    stamp = Column(DateTime, primary_key=True, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    event = Column(Text)
