from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dto.Availability import AvailabilityDTO

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
    start = Column(Integer)
    end = Column(Integer)

    __table_args__ = (UniqueConstraint('user_id', 'date', 'start', 'end'),)


engine = create_engine('sqlite:///padel.sqlite')
conn = engine.connect()
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_user(username: str, password: str):
    user = get_user(username)
    if user:
        print(f"User {username} already used!")
        return None
    
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    print(f"New user {username} add to database")

    return new_user

def get_user(username: str):
    user = session.query(User).filter_by(username=username).first()
    return user 

def add_availability(user_id: int, availability: AvailabilityDTO):
    new_availability = Availability(
        user_id = user_id,
        date = availability.date,
        start = availability.start_hour,
        end = availability.end_hour, 
    )
    
    try:
        session.add(new_availability)
        session.commit()
        print(f"New availability add for user {user_id}: {new_availability}")
    except IntegrityError:
        session.rollback()
        print(f"Availability {availability} already exists for user {user_id}")