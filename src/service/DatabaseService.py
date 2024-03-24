from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

engine = create_engine('sqlite:///padel.sqlite')
conn = engine.connect()
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_user(username: str, password: str):
    user = session.query(User).filter_by(username=username).first()
    if user:
        print(f"User {username} already used!")
        return False
    
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    print(f"New user {username} add to database")

    return True