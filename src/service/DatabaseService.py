from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from model.model import Base, Availability, User

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
    
    new_user = User(username=username, password=password) # todo add password hashing
    session.add(new_user)
    session.commit()
    print(f"New user {username} add to database")

    return new_user

def get_user(username: str):
    user = session.query(User).filter_by(username=username).first()
    return user 

def add_availability(user_id: int, date, slot):
    new_availability = Availability(
        user_id = user_id,
        date = date,
        hour = slot
    )
    
    try:
        session.add(new_availability)
        session.commit()
        print(f"New availability add for user {user_id}: {new_availability}")
    except IntegrityError:
        session.rollback()
        print(f"Availability {date}, {slot} already exists for user {user_id}")
    
def get_slots():
    slots = session.query(
        Availability.date,
        Availability.hour,
        func.count(Availability.user_id).label('count')
    ).group_by(
        Availability.date,
        Availability.hour
    ).having(
        func.count(Availability.user_id) >= 4
    ).all()

    return slots

def get_user_by_slot(date, hour):
    users = session.query(User).join(
        Availability, User.id == Availability.user_id
    ).filter(
        Availability.date == date,
        Availability.hour == hour
    ).all()

    return users