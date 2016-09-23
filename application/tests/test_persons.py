from application.persons import Person
from nose.tools import assert_equal, assert_in


class TestPersons(object):
    '''Tests for Persons class'''

    def test_add_person(self):
        person = Person()
        assert_equal(person.add_person('name', 'position', 'N'),
                     True, 'Addition of a person was unsuccesful')

    def test_reallocate_person(self):
        person = Person()
        assert_equal(person.reallocate_person('id', 'new_room'),
                     True, 'Failed to reallocate person to new room')

    def test_load_people(self):
        person = Person()
        assert_equal(person.load_people(), True,
                     'Failed to load people from file')

    def test_validate_position(position):
        person = Person()
        assert_in(person.validate_position('student'), [
                  'STAFF', 'FELLOW', 'staff', 'fellow'], 'Invalid position')

    def test_validate_person_id(self):
        person = Person()
        assert_equal(person.validate_person_id('id'), True, 'Invalid ID')

    def test_validate_storage_file(self):
        person = Person()
        assert_equal(person.validate_storage_file(
            'file name'), True, 'Invalid storage file name')
