from db_operations import validate_sqlite_db, load_db_state, save_state, print_unallocated, print_allocations, load_people


class Amity(object):
    '''Amity class'''

    def print_allocations(self, filename=None):
        '''Prints a list of allocations to the screen'''
        print_allocations(filename)

    def save_state(self, db_name='default_amity.db'):
        """
                Save current state of operations to database
        """
        save_state(db_name)

    def check_db_name(self, db_name):
        '''Check if db file exists and is sqlite db'''
        return validate_sqlite_db(db_name)

    def load_state(self, db_name):
        """
        Loads Amity information from database
        """
        return load_db_state(db_name)

    def print_unallocated(self, output_file=None):
        """
                Prints unallocated people. 
                Outputs to file if filename is provided
        """
        print_unallocated()

    def load_people(self, filename):
        '''Load people from a text file and allocate them rooms'''
        '''Text files should be in data_files folder'''
        load_people(file_name)