# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, Integer, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class EventLogCopy(Base):
    __tablename__ = 'event_log_copy'

    is_active = Column(Boolean, primary_key=True, nullable=False)
    stamp = Column(DateTime, primary_key=True, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    epoch = Column(Integer, primary_key=True, nullable=False)
    event = Column(Text)
