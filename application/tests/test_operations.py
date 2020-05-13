from application.db_operations import *
from application.rooms import RoomImplementation
from application.amity import Amity
from application.persons import Fellow, Person, Staff
from test import Room, Person
from nose.tools import assert_equal
import os
import mock

from setup_test import test_session, db_session
from test import create_session_db

class TestOperations(object):

    @classmethod
    def setup_class(self):
        create_session_db()
        switch_session(test_session)
        room = Room()
        room.room_name = 'DAUGHTRY'
        room.room_type = 'OFFICE'
        room.capacity = 4
        room.current_occupants = 0
        room.gender = 'BOTH'
        test_session.add(room)
        test_session.commit()

        with mock.patch('__builtin__.raw_input', side_effect=['25904563', 'F']):
            save_person('MARY WAMBUI', 'STAFF')

        room3 = Room()
        room3.room_name = 'LAVENDER'
        room3.room_type = 'LIVINGSPACE'
        room3.capacity = 6
        room3.current_occupants = 0
        room3.gender = 'F'
        test_session.add(room3)
        test_session.commit()

        room4 = Room()
        room4.room_name = 'PHP'
        room4.room_type = 'LIVINGSPACE'
        room4.capacity = 6
        room4.current_occupants = 0
        room4.gender = 'M'
        test_session.add(room4)
        test_session.commit()

        with mock.patch('__builtin__.raw_input', side_effect=['25453567', 'M']):
            save_person('BRIAN KIM', 'FELLOW', 'Y')

        room2 = Room()
        room2.room_name = 'COLDPLAY'
        room2.room_type = 'OFFICE'
        room2.capacity = 4
        room2.current_occupants = 0
        room2.gender = 'BOTH'
        test_session.add(room2)
        test_session.commit()

    @classmethod
    def teardown_class(self):
        if os.path.exists('tests/test_session_amity.db'):
            os.remove('tests/test_session_amity.db')
        if os.path.exists('tests/test_amity.db'):
            os.remove('tests/test_amity.db')
        if os.path.exists('tests/db.txt'):
            os.remove('tests/db.txt')

    def test_get_room_occupants(self):
        assert_equal(get_room_occupants('DAUGHTRY'),
                     2, 'Room has '+str(get_room_occupants('DAUGHTRY'))+' occupants')

    def test_validate_room_name(self):
        '''Assert if room_name exists in the database '''
        assert_equal(validate_room_name('DAUGHTRY'), True, 'Invalid Room Name')
        assert_equal(validate_room_name('No Room Name'),
                     'Invalid Room Name', 'Invalid Room Name')

    def test_room_created(self):
        '''Assert if room was created'''
        roomImp = RoomImplementation()
        assert_equal(roomImp.create_room('DAUGHTRY'),
                     'Room name Unavailable', 'Room name already used')
        with mock.patch('__builtin__.raw_input', side_effect=['A']):
            creation_status = roomImp.create_room('OCULUS')
            assert_equal(creation_status, 'Room Created',
                         'Room name already used')

    def test_room_details(self):
        assert_equal(get_room_details('DAUGHTRY').count(), 1)

    def test_reallocate_person(self):
        '''Tests for room reallocation'''
        person = test_session.query(Person).filter_by(id_number=25904563).one()
        room_name = person.office
        staff = Staff()
        fellow = Fellow()
        assert_equal(staff.reallocate_person(
            25904563, room_name), 'Person is in that Room')
        assert_equal(staff.reallocate_person(
            25904563, 'COLDPLAY'), 'Reallocation Successful')
        assert_equal(fellow.reallocate_person(
            25453567, 'LAVENDER'), 'Invalid Reallocation')
        assert_equal(staff.reallocate_person(43566763, 'OCULUS'), 'Id Missing')

    def test_save_person(self):
        staff = Staff()
        assert_equal(staff.add_person(
            'KOBE BRYANT', 'basketballer', 'Y'), 'Invalid Position')
        assert_equal(staff.add_person('KOBE', 'fellow', 'Y'), 'Invalid Name')

        with mock.patch('__builtin__.raw_input', side_effect=['25900567', 'M']):
            assert_equal(staff.add_person(
                'KEVIN GATES', 'STAFF'), 'Person Saved')

        fellow = Fellow()
        with mock.patch('__builtin__.raw_input', side_effect=['25900000', 'F']):
            assert_equal(fellow.add_person(
                'RUTH BOCHERE', 'fellow', 'Y'), 'Person Saved')

    def test_validate_position(position):
        person = Staff()
        assert_equal(person.validate_position('student'),
                     'Invalid Position', 'Invalid position')
        assert_equal(person.validate_position(
            'staff'), True, 'Invalid position')
        assert_equal(person.validate_position(
            'fellow'), True, 'Invalid position')

    def test_validate_person_id(self):
        fellow = Fellow()
        assert_equal(fellow.validate_person_id_number(
            25453567), True, 'Invalid ID')
        assert_equal(fellow.validate_person_id_number(
            23454388), 'Id Missing', 'Invalid ID')

    def test_print_room(self):
        assert_equal(print_room_details('Invalid Room Name'),
                     'Invalid Room Name / No Room By Name: ' + 'Invalid Room Name', 'Failed to print room information')

    def test_check_db_name(self):
        amity = Amity()
        assert_equal(amity.check_db_name(
            'tests/test_session_amity.db'), True, 'Error occurred')
        assert_equal(amity.check_db_name('No file'),
                     'File Does Not Exist', 'Error occurred')
        import io
        with io.FileIO("tests/db.txt", "w") as file:
            file.write("Hello!")
        assert_equal(amity.check_db_name('tests/db.txt'),
                     'Not SQLite file', 'Error occurred')

    def test_validate_db_tables(self):
        assert_equal(validate_sqlite_db(
            'tests/test_session_amity.db'), True, 'Error occurred')
