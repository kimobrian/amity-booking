class Amity(object):
    '''Amity class'''

    def print_allocations(self, filename=None):
        pass

    def save_state(self, db_name):
        """
                Save current state of operations to database
        """
        pass

    def check_db_name(self, db_name):
        '''Check if db file exists'''
        pass
        
    def load_state(self, db_name):
        """
        Loads Amity infromation from database
        """
        pass

    def print_unallocated(self, output_file=None):
        """
                Prints unallocated people. 
                Outputs to file if filenam eis provided
        """
        pass
