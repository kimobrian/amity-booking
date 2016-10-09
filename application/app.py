"""
    Commands:
        create_room <room_name>...
        add_person <first_name> <last_name> <FELLOW|STAFF|fellow|staff> [--accomm=N]
        reallocate_person <person_id> <new_room_name>
        load_people <filename>
        print_allocations [--o=filename]
        print_unallocated [--o=filename]
        print_room <room_name>
        save_state [--db=sqlite_db]
        load_state <sqlite_db>
        quit

    Options:
        -h, --help  Show this screen and exit
        --o filename  Specify filename
        --db    Name of SQLite DB
        --accomm  If person needs accommodation [default='N']
"""


from docopt import docopt, DocoptExit
import cmd
import os
from amity import Amity
from persons import Person, Staff, Fellow
from rooms import RoomImplementation
from termcolor import cprint, colored
from pyfiglet import figlet_format


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match
            # We print a message to the user and the usage block
            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


def intro():
    os.system("clear")
    cprint(figlet_format('\tAMITY', font='digital'),
               'green', attrs=['bold', 'blink'])
    print colored(__doc__)

def safe_mode():
    '''Ensure user does not accidentally lose data on exit or keyboard interrupt '''
    '''Save state to deafult DB and destroy application session'''
    amity = Amity()
    if os.path.exists('session_amity.db'):
        print colored('Saving Your Application State','yellow')
        amity.save_state()
        os.remove('session_amity.db')

class RoomAllocation(cmd.Cmd):
    prompt = 'rooms@amity>>>'

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_name>..."""
        room = RoomImplementation()
        rooms = arg['<room_name>']
        for r in rooms:
            print('Room Name: ' + r.upper())
            status = room.create_room(r)
            print(status)

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <position> [--accomm=N]"""
        person = Person()
        name = arg['<first_name>'] + ' ' + arg['<last_name>']
        position = arg['<position>']
        accommodation = arg['--accomm']
        if accommodation is None:
            save_status = person.add_person(name, position)
            if save_status == 'No Spaced Offices':
                print colored('Please Create rooms before allocating people', 'red')
                return
            else:
                print colored(save_status, 'green')
        elif accommodation is not None:
            save_status = person.add_person(name, position, accommodation)
            if save_status == 'No Spaced Offices':
                print colored('Please Create rooms before allocating people', 'red')
                return
            else:
                print colored(save_status, 'green')

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person  <person_id> <new_room_name>"""
        person = Person()
        status = person.reallocate_person(
            arg['<person_id>'], arg['<new_room_name>'])
        print(status)

    @docopt_cmd
    def do_load_people(self, arg):
        '''Usage: load_people <filename>'''
        amity = Amity()
        amity.load_people(arg['<filename>'])

    @docopt_cmd
    def do_print_allocations(self, arg):
        '''Usage: print_allocations [--o=filename]'''
        amity = Amity()
        file = arg['--o']
        if file is not None:
            amity.print_allocations(file)
        else:
            amity.print_allocations()

    @docopt_cmd
    def do_print_unallocated(self, arg):
        '''Usage: print_unallocated [--o=filename]'''
        amity = Amity()
        file = arg['--o']
        if file is not None:
            amity.print_unallocated(file)
        else:
            amity.print_unallocated()

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        room = RoomImplementation()
        room.print_room(arg['<room_name>'])

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlitedb]"""
        amity = Amity()
        db_name = arg['--db']
        if db_name is not None:
            if os.path.exists(db_name):
                print colored('You are about to override '+db_name+' DB which may have data:', 'red')
                reply = raw_input(
                    'Do you want to Continue. Y for yes | N for no: ')
                while reply.upper() not in ['Y', 'N']:
                    print('Invalid Reply!!')
                    reply = raw_input('Please Enter Y for yes | N for no: ')
                if reply.upper() == 'Y':
                    print colored('Overriding database ...','yellow')
                    amity.save_state(db_name)
                else:
                    print('Please provide an alternative DB name for the command')
                    return
            else:
                print colored('Saving database state ...', 'yellow')
                amity.save_state(db_name)
        
        else:   
            if os.path.exists('default_amity.db'):
                print(
                    'You are about to override the default DB (default_amity.db) which may have data:')
                reply = raw_input(
                    'Do you want to Continue. Y for yes | N for no: ')
                while reply.upper() not in ['Y', 'N']:
                    print('Invalid Reply!!')
                    reply = raw_input('Please Enter Y for yes | N for no: ')
                if reply.upper() == 'Y':
                    print('Overriding default storage database..')
                    amity.save_state()
                else:
                    print('Please provide an alternative DB name for the command')
                    return
            else:
                amity.save_state()

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>"""
        print('Loading Saved DB. May take a while ...')
        amity = Amity()
        amity.load_state(arg['<sqlite_database>'])

    @docopt_cmd
    def do_quit(self, arg):
        """Usage: quit"""
        safe_mode()
        os.system('clear')
        print colored('Application Exiting','red')
        exit()


if __name__ == "__main__":
    try:
        intro()
        RoomAllocation().cmdloop()
        if os.path.exists('session_amity.db'):
            os.remove('session_amity.db')
    except KeyboardInterrupt:
        safe_mode() #Save state on KeyboardInterrupt Error
        os.system("clear")
        print colored('Application Exiting','red')
