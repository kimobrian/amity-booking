from amity import Amity


class Room(Amity):

    def create_room(self, room_type, room_name):
        """
                Creates new room
        """
        pass

    def print_room(self, room_name):
        """
                Prints all information about people in a room
        """
        pass

    def check_room(self, room_name):
        '''Check if the room(name) exists'''
        pass


class Office(Room):
    pass


class LivingSpace(Room):
    pass
