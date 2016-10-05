from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from tabulate import tabulate
from sqlalchemy_utils.types.choice import ChoiceType

Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'
    person_id = Column(Integer, primary_key=True)
    id_number = Column(Integer, nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    position = Column(String(20), nullable=False)
    office = Column(String(50), nullable=False)
    livingspace = Column(String(50), default='N')
    gender = Column(String(20), nullable=False)

    def __repr__(self):
        table = [[self.person_id, self.id_number, self.name,self.position, self.office, self.livingspace]]
        return tabulate(table, headers=["Id", "Id Number", "Name", "Position", "Office", "Livingspace"], tablefmt='grid')


class Room(Base):
    __tablename__ = 'rooms'
    room_id = Column(Integer, primary_key=True)
    room_name = Column(String(50), nullable=False, unique=True)
    room_type = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    current_occupants = Column(Integer, default=0)
    gender = Column(String(20), default='BOTH')

    def __repr__(self):
        table = [[self.room_id, self.room_name, self.room_type,
                  self.capacity, self.current_occupants]]
        return tabulate(table, headers=["Room Id", "Room Name", "Room Type", "Capacity", "Current Occupants"], tablefmt='grid')


engine = create_engine("sqlite:///amity.db")

Base.metadata.create_all(engine)
