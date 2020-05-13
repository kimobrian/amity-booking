from db_operations import save_person, validate_position, validate_person_id, reallocate_person, save_state, switch_session
import os
from db_models import create_session_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Person(object):

    def __init__(self):
        if not os.path.exists('session_amity.db'):
            create_session_db()
            engine = create_engine('sqlite:///session_amity.db')
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)
            session = DBSession()
            switch_session(session)

    def add_person(self, name, position, wants_accommodation='N'):
        """
                Add person to facility and alocates them a room
                if they want accommodation
        """
        return save_person(name, position, wants_accommodation)

    def validate_position(self, position):
        '''Check whether position is STAFF or FELLOW'''
        return validate_position(position)

    def validate_person_id_number(self, person_id):
        '''Check whether person id is valid(exists)'''
        return validate_person_id(person_id)

    def reallocate_person(self, person_id, new_room):
        """
        Reallocates a person to a new room
        """
        return reallocate_person(person_id, new_room)


class Fellow(Person):
    pass


class Staff(Person):
    pass
