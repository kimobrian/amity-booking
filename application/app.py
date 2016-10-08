from db_operations import *
import os
from db_models import create_db, create_session_db
from db_models import Room, Person

if not os.path.exists('session_amity.db'):
    create_session_db()
    engine = create_engine('sqlite:///session_amity.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    global session
    session = DBSession()
else:
    engine = create_engine('sqlite:///session_amity.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

create_room('NARNIA')
create_room('PHP')
create_room('JAVA')

save_person('BRIAN KIM', 'STAFF')
save_state('kimbrian.db')
load_db_state('kimbrian.db')
save_state('dbfinal.db')
load_db_state('dbfinal.db')
