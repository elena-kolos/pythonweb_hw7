from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///academy.db")
Session = sessionmaker(bind=engine)
session = Session()



