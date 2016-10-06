from db_operations import validate_sqlite_db, load_db_state

class Amity(object):
    '''Amity class'''

    def print_allocations(self, filename=None):
        '''Prints a list of allocations to the screen'''
        pass

    def save_state(self, db_name):
        """
                Save current state of operations to database
        """
        pass

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
        pass