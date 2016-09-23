from nose.tools import assert_equal
from application.amity import Amity


class TestAmity(object):
    '''
    Tests for amity class
    '''

    def test_print_allocations(self):
        amity = Amity()
        assert_equal(amity.print_allocations(), True,
                     'Function did not return True')

    def test_save_state(self):
        amity = Amity()
        assert_equal(amity.save_state('db_name'),
                     True, 'Saving state to DB failed')

    def test_load_state(self):
        amity = Amity()
        assert_equal(amity.load_state('db_name'), True,
                     'Loading state from DB failed')

    def test_print_unallocated(self):
        amity = Amity()
        assert_equal(amity.print_unallocated('file_name'), True,
                     'Failed to print unallocated people to file')

    def test_check_db(self):
        amity = Amity()
        assert_equal(amity.check_db_name('db name'), True, 'Invalid DB name')
