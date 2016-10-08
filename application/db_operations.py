from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import Base, Person, Room
from sqlalchemy.orm.exc import NoResultFound
import random
import os
import sys
from os.path import isfile, getsize
from tabulate import tabulate
from db_models import create_db, create_session_db

# Room's model operations

engine = create_engine('sqlite:///session_amity.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def check_session_db():
    if not os.path.exists('session_amity.db'):
        print('Application Session Database Missing')
        return False


def switch_session(sess):
    global session
    session = sess


def get_room_occupants(room_name):
    '''Returns current number of occupants in a room'''
    try:
        occupants = session.query(Room).filter_by(room_name=room_name).one()
        return occupants.current_occupants
    except NoResultFound:
        return 0


def print_room_details(room_name):
    ''' Print people in a room print_room <room_name> command '''
    try:
        room_details = session.query(Room).filter_by(
            room_name=room_name.upper()).one()
        if room_details.room_type == 'OFFICE':
            people_info = session.query(
                Person).filter_by(office=room_name.upper()).all()
        else:
            people_info = session.query(
                Person).filter_by(livingspace=room_name.upper()).all()

        if people_info:
            data = []
            for person in people_info:
                fields = [person.person_id, person.name,
                          person.position, person.office, person.livingspace]
                data.append(fields)
            return tabulate(data, headers=['Id', 'Name', 'Position', 'Office', 'Living Space'], tablefmt='grid')
        else:
            return 'Room is Empty'

    except NoResultFound:
        return 'Invalid Room Name'


def print_room_allocations(filename=None):
    ''' print all allocations for the amity facility'''


def check_room_name(room_name):
    '''Check if room name already exist'''
    try:
        room = room_name.upper()
        status = session.query(Room).filter_by(room_name=room).one()
        return True
    except NoResultFound:
        return False  # Room name does not exist


def is_room_full(room_name):
    '''Check if the room is full'''
    try:
        room = session.query(Room).filter_by(room_name=room_name.upper()).one()
        capacity = room.capacity
        current_occupants = room.current_occupants
        if capacity == current_occupants:
            return 'Room Full'
        else:
            return capacity - current_occupants
    except NoResultFound:
        return 'Error Checking Capacity'


def validate_position(position):
    if position.upper() not in ['STAFF', 'FELLOW']:
        return 'Invalid Position'
    else:
        return True


def validate_room_name(room_name):
    try:
        session.query(Room).filter_by(room_name=room_name.upper()).one()
        return True
    except NoResultFound:
        return 'Invalid Room Name'


def create_room(room_name):
    room_exists = check_room_name(room_name)
    if room_exists is True:
        return 'Room name Unavailable'
    else:
        room_type = raw_input(
            'Enter room type, A for Office , B for Livingspace: ')
        while room_type.upper() not in ['A', 'B']:
            print('Invalid room type: Enter either A or B')
            room_type = raw_input(
                'Enter room type, A for Office , B for Livingspace: ')

        room = Room()
        room.room_name = room_name.upper()
        room.current_occupants = 0
        if room_type.upper() == 'A':
            room.room_type = 'OFFICE'
            room.capacity = 6
        elif room_type.upper() == 'B':
            room.room_type = 'LIVINGSPACE'
            room.capacity = 4
            gender = raw_input('Room Gender: Enter M for Male, F for female: ')
            while gender.upper() not in ['F', 'M']:
                gender = raw_input(
                    'Room Gender: Enter M fro Male, F for female: ')
            room.gender = gender.upper()
        try:
            session.add(room)
            session.commit()
            return 'Room Created'
        except Exception:
            session.rollback()
            return 'Error Occurred'


def validate_person_id(p_id_num):
    try:
        session.query(Person).filter_by(id_number=p_id_num).one()
        return True
    except NoResultFound:
        return 'Id Missing'


def validate_name(name):
    username = name.strip().split()
    if len(username) != 2:
        return 'Invalid Name'
    else:
        return name


def get_spaced_offices():
    '''Return all offices with space '''
    offices = session.query(Room).filter_by(room_type='OFFICE').filter(
        Room.current_occupants < Room.capacity)
    if offices.count() == 0:
        return False
    else:
        return offices


def get_room_details(room_name):
    try:
        room = session.query(Room).filter_by(room_name=room_name.upper())
        return room
    except NoResultFound:
        return 'No Room'


def get_spaced_living_spaces(gender):
    '''Return all  living spaces with space'''
    living_spaces = session.query(Room).filter_by(room_type='LIVINGSPACE').filter_by(gender=gender).filter(
        Room.current_occupants < Room.capacity)
    if living_spaces.count() == 0:
        return False
    else:
        return living_spaces


def get_all_spaces():
    '''Returns a listy of all rooms with spaces'''
    offices = get_spaced_offices()
    l_spaces = get_spaced_living_spaces()
    if offices is False and l_spaces is not False:
        return l_spaces
    elif offices is not False and l_spaces is False:
        return offices
    elif offices is not False and l_spaces is not False:
        return offices.union(l_spaces)
    else:
        return False


# Person's model operations

def save_person(name, position, wants_accommodation='N'):
    ''' Adds a person to the system either a fellow or a staff '''
    pos = validate_position(position)
    if pos == 'Invalid Position':
        return pos
    name_status = validate_name(name)
    if name_status == 'Invalid Name':
        print 'Invalid Name: Name should be first and last names separated by a space'
        return 'Invalid Name'
    id_number = raw_input('Enter an 8 digit ID Number: ')
    while not id_number.isdigit() or len(id_number) != 8:
        id_number = raw_input('Invalid ID. Enter an 8 digit ID Number: ')

    person = Person()
    person.name = name.upper()
    person.position = position.upper()
    person.id_number = id_number
    gender = raw_input('Enter Gender: M for Male and F for Female: ')
    while gender.upper() not in ['M', 'F']:
        gender = raw_input('Enter Gender: M for Male and F for Female: ')
    person.gender = gender.upper()
    if position.upper() == 'STAFF':
        offices = get_spaced_offices()
        if offices is False:
            return 'No Spaced Offices'
        else:
            length = offices.count()
            random_record = random.randint(0, length - 1)
            office = offices[random_record]
            person.office = office.room_name
            session.add(person)
            room_update = session.query(Room).filter_by(room_name=office.room_name).update(
                {'current_occupants': office.current_occupants + 1})
            session.commit()
            return 'Person Saved'
    elif position.upper() == 'FELLOW':
        offices = get_spaced_offices()
        if offices is False:
            person.office = 'N'
            return 'No Spaced Offices'
        else:
            length = offices.count()
            random_record = random.randint(
                0, length - 1)  # Index of random office
            office = offices[random_record]
            person.office = office.room_name
            room_update = session.query(Room).filter_by(room_name=office.room_name).update(
                {'current_occupants': office.current_occupants + 1})
            if wants_accommodation.upper() == 'Y':
                livingspaces = get_spaced_living_spaces(gender.upper())
                if livingspaces is False:
                    person.livingspace = 'N'
                else:
                    space_numbers = livingspaces.count()
                    random_space = random.randint(
                        0, space_numbers - 1)  # Index of random space
                    l_space = livingspaces[random_space]
                    person.livingspace = l_space.room_name
                    room_update = session.query(Room).filter_by(room_name=l_space.room_name).update(
                        {'current_occupants': l_space.current_occupants + 1})

            try:
                session.add(person)
                session.commit()
                return 'Person Saved'
            except Exception:
                return 'Error Saving Person'


def reallocate_person(id_number, new_room):
    id_status = validate_person_id(id_number)
    if id_status == 'Id Missing':
        return id_status
    else:
        room_status = validate_room_name(new_room)
        if room_status == 'Invalid Room Name':
            return room_status
        else:
            room_capacity_status = is_room_full(new_room)
            if room_capacity_status == 'Room Full':
                return room_capacity_status
            else:
                room = session.query(Room).filter_by(
                    room_name=new_room.upper()).one()
                room_type = room.room_type
                new_room_gender = room.gender
                if is_room_full(new_room) == 'Room Full':
                    return 'Room Full'
                else:
                    person_details = session.query(
                        Person).filter_by(id_number=id_number).one()
                    if person_details.office == new_room.upper() or person_details.livingspace == new_room.upper():
                        return 'Person is in that Room'
                    if room_type == 'OFFICE':
                        current_room = session.query(Room).filter_by(
                            room_name=person_details.office).one()
                    elif room_type == 'LIVINGSPACE':
                        if person_details.gender != new_room_gender:
                            print(
                                'You can\'t rallocate to a living space of opposite gender')
                            return 'Invalid Reallocation'
                        current_room = session.query(Room).filter_by(
                            room_name=person_details.livingspace).one()
                    session.query(Room).filter_by(room_name=current_room.room_name).update(
                        {'current_occupants': current_room.current_occupants - 1})
                    session.query(Room).filter_by(room_name=new_room.upper()).update(
                        {'current_occupants': current_room.current_occupants + 1})
                    if room_type == 'OFFICE':
                        session.query(Person).filter_by(
                            id_number=id_number).update({'office': new_room})
                    elif room_type == 'LIVINGSPACE':
                        session.query(Person).filter_by(
                            id_number=id_number).update({'livingspace': new_room.upper()})
                    session.commit()
                    return 'Reallocation Successful'


def validate_sqlite_db(db_name):
    ''' Validate if its indeed an SQlite3 db '''
    ''' SQLite3 db headers are 100 bytes '''
    if not isfile(db_name):
        return 'File Does Not Exist'
    if getsize(db_name) < 100:
        return 'Not SQLite file'
    with open(db_name, 'rb') as fd:
        header = fd.read(100)
    return header[:16] == 'SQLite format 3\x00'


def validate_db_tables(db_name):
    ''' Check if db format is correct. '''
    ''' DB should contain both persons and rooms tables '''
    test_engine = create_engine('sqlite:///' + db_name)
    if not test_engine.dialect.has_table(test_engine, 'persons'):
        persons_status = False
    else:
        persons_status = True

    if not engine.dialect.has_table(engine, 'rooms'):
        rooms_status = False
    else:
        rooms_status = True

    return True if persons_status and rooms_status else False


def load_db_state(db_name):
    ''' Load data from another database file '''
    if os.path.exists('session_amity.db'):
        os.remove('session_amity.db')
    create_session_db()
    db_status = validate_sqlite_db(db_name)
    if db_status is False:
        return 'Invalid DB'
    table_status = validate_db_tables(db_name)
    if table_status is False:
        return 'Invalid DB Format'

    global session
    engine = create_engine('sqlite:///' + db_name)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    people = session.query(Person).all()
    rooms = session.query(Room).all()

    people_count = len(people)
    room_count = len(rooms)

    engine = create_engine('sqlite:///session_amity.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    if people_count > 0:
        for person in people:
            person_obj = Person()
            person_obj.id_number = person.id_number
            person_obj.name = person.name
            person_obj.position = person.position
            person_obj.office = person.office
            person_obj.livingspace = person.livingspace
            person_obj.gender = person.gender
            session.add(person_obj)
            session.commit()
    else:
        print('No People to Load')

    if room_count > 0:
        for room in rooms:
            room_obj = Room()
            room_obj.room_name = room.room_name
            room_obj.room_type = room.room_type
            room_obj.capacity = room.capacity
            room_obj.current_occupants = room.current_occupants
            room_obj.gender = room.gender
            session.add(room_obj)
            session.commit()
    else:
        print('No Rooms to Load')

    if os.path.exists(db_name):
        os.remove(db_name)
    print('Data Loaded Successfully')

    return True


def save_state(db_name='default_amity.db'):
    import os
    if os.path.exists(db_name):
        os.remove(db_name)
    create_db(db_name)
    if not os.path.exists('session_amity.db'):
        print('No Session Database for Application State')
        return 'No Session'
    global session
    engine = create_engine('sqlite:///session_amity.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    people = session.query(Person).all()
    rooms = session.query(Room).all()

    people_count = len(people)
    room_count = len(rooms)

    engine = create_engine('sqlite:///' + db_name)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    if people_count > 0:
        for person in people:
            person_obj = Person()
            person_obj.id_number = person.id_number
            person_obj.name = person.name
            person_obj.position = person.position
            person_obj.office = person.office
            person_obj.livingspace = person.livingspace
            person_obj.gender = person.gender
            session.add(person_obj)
            session.commit()

    if room_count > 0:
        for room in rooms:
            room_obj = Room()
            room_obj.room_name = room.room_name
            room_obj.room_type = room.room_type
            room_obj.capacity = room.capacity
            room_obj.current_occupants = room.current_occupants
            room_obj.gender = room.gender
            session.add(room_obj)
            session.commit()
    import os
    if os.path.exists('session_amity.db'):
        os.remove('session_amity.db')

    print('Application State Saved Successfully')

    return True


def print_unallocated(file_name=None):
    people = session.query(Person).all()
    if people:
        data = []
        for person in people:
            if person.position == 'FELLOW':
                if person.office == 'N' or person.livingspace == 'N':
                    fields = [person.person_id, person.id_number, person.name,
                              person.position, person.office, person.livingspace]
                    data.append(fields)
        print tabulate(data, headers=['Id', 'ID Number', 'Name', 'Position', 'Office', 'Living Space'], tablefmt='grid')
    if file_name != None:
        pass


def print_allocations(file_name=None):
    people = session.query(Person).all()
    rooms = session.query(Room).all()
    if len(rooms) > 0:
        for room in rooms:
            room_name = room.room_name
            room_type = room.room_type
            print(room_name)
            print('-' * 100)
            if file_name != None:
                with open('data_files/' + file_name + '.txt', 'a') as output:
                    if rooms.index(room) != 0:
                        output.write('\n')
                    output.write(room_name)
                    output.write('\n')
                    output.write('-' * 100)
                    output.write('\n')
            if room_type == 'OFFICE':
                people_in_room = session.query(
                    Person).filter_by(office=room_name).all()
                if len(people_in_room) > 0:
                    for person in people_in_room:
                        sys.stdout.write(person.name + ', ')
                        if file_name != None:
                            with open('data_files/' + file_name + '.txt', 'a') as output:
                                output.write(person.name + ', ')
                else:
                    print('Room Empty')
            elif room_type == 'LIVINGSPACE':
                people_in_room = session.query(Person).filter_by(
                    livingspace=room_name).all()
                if len(people_in_room) > 0:
                    for person in people_in_room:
                        sys.stdout.write(person.name + ', ')
                        if file_name != None:
                            with open('data_files/' + file_name + '.txt', 'a') as output:
                                output.write(person.name + ', ')
            print('\n')


def load_people(file_name):
    '''Load people from a text file and allocate them to rooms'''
    full_path = 'data_files' + file_name + '.txt'
    if file_name:
        if os.path.isfile(full_path) and os.path.getsize(full_path) > 0:
            with open('data_files/' + file_name + '.txt') as input_file:
                content = input_file.readlines()
            for line in content:
                line_values = line.split()
                name = line_values[0] + ' ' + line_values[1]
                position = line_values[2]
                try:
                    wants_accommodation = line_values[3]
                except:
                    wants_accommodation = 'N'
                    pass
                print("[ " + name + "  " + position + " ]")
                print(save_person(name, position, wants_accommodation))
        else:
            print('File is empty or does not Exist')
            return False
