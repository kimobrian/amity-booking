from amity import Amity
from db_operations import create_room as c_room, print_room_details, switch_session, switch_session
import os
from db_models import create_session_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from termcolor import colored

class RoomImplementation(Amity):

    def __init__(self):
        if not os.path.exists('session_amity.db'):
            create_session_db()
            engine = create_engine('sqlite:///session_amity.db')
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)
            session = DBSession()
            switch_session(session)

    def create_room(self, room_name):
        """
                Creates new room
        """
        return c_room(room_name)

    def print_room(self, room_name):
        """
                Prints all information about people in a room
        """
        print(colored(print_room_details(room_name), 'green'))


class Office(RoomImplementation):
    pass


class LivingSpace(RoomImplementation):
    pass
