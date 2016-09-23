from application.persons import Person
from nose.tools import assert_equal


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
