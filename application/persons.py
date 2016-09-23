class Person(object):

    def add_person(self, name, position, wants_accommodation='N'):
        """
                Add person to facility and alocates them a room
                if they want accommodation
        """
        pass

    def validate_position(self, position):
        '''Check whether position is STAFF or FELLOW'''
        pass

    def validate_person_id(self, person_id):
        '''Check whether person id is valid(exists)'''
        pass

    def reallocate_person(self, person_id, new_room):
        """
        Reallocates a person to a new room
        """
        pass

    def validate_storage_file(self, storage_file):
        '''Tests if the file name for storing people exists'''
        pass

    def load_people(self):
        """
                Loads the available people records from text file
        """
        pass


class Fellow(Person):
    pass


class Staff(Person):
    pass
