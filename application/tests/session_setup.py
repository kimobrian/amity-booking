from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from test import Base

test_engine = create_engine('sqlite:///tests/test_session_amity.db')
Base.metadata.bind = test_engine
test_DBSession = sessionmaker(bind=test_engine)
test_session = test_DBSession()

engine = create_engine('sqlite:///tests/test_amity.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session_b = DBSession()
