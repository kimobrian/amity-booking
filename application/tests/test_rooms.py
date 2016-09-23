from nose.tools import assert_equal
from application.rooms import Room


class TestRooms(object):
    '''Test Rooms class'''

    def test_create_room(self):
        room = Room()
        assert_equal(room.create_room('room type', 'room name'),
                     True, 'Failed to create room')

    def test_print_room(self):
        room = Room()
        assert_equal(room.print_room('room name'), True,
                     'Failed to print room information')

    def test_check_room(self):
        room = Room()
        assert_equal(room.check_room('room name'),
                     'Invalid Room Name', 'Room name does not exist')
