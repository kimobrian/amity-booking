class Amity(object):
	"""Amity facility"""

	def print_allocations(self, output_file):
    	"""
    	Prints all room allocations.
		Outputs to file if filename is specified
    	"""
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

    def print_unallocated(self, output_file):
    	"""
		Prints unallocated people. 
		Outputs to file if filenam eis provided
    	"""
        pass

    def __str__(self):
        print("Welcome to Amity Facility")
