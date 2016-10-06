from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from test import Base

engine = create_engine('sqlite:///tests/test_amity.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()