from amity import Amity
from db_operations import create_room as c_room
from tabulate import tabulate


class RoomImplementation(Amity):

    def create_room(self, room_name):
        """
                Creates new room
        """
        return c_room(room_name)

    def print_room(self, room_name):
        """
                Prints all information about people in a room
        """
        pass


class Office(RoomImplementation):
    pass


class LivingSpace(RoomImplementation):
    pass
