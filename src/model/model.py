from sqlalchemy import Column, String, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Availability(Base):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    date = Column(Date)
    hour = Column(Integer)

    __table_args__ = (UniqueConstraint('user_id', 'date', 'hour'),)