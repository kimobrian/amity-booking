class Person(object):
    def __init__(self, name, position):
        """
                Initialize new person
        """
        pass

    def add_person(self, name, position, wants_accommodation='N'):
        """
                Add person to facility and alocates them a room
                if they want accommodation
        """
        pass

    def reallocate_person(self, person_id, new_room):
        """
        Reallocates a person to a new room
        """
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
