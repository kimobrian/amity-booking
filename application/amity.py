class Amity(object):
    '''Amity class'''

    def print_allocations(self, filename=None):
        pass

    def save_state(self, db_name):
        """
                Save current state of operations to database
        """
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

    def __str__(self):
        print("Welcome to Amity Facility")
