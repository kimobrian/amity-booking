from amity import Amity
from db_operations import create_room as c_room, print_room_details


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
        print(print_room_details(room_name))


class Office(RoomImplementation):
    pass


class LivingSpace(RoomImplementation):
    pass
