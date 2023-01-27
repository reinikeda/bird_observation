from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///data/birds_observation.db')
Base = declarative_base()

class Bird(Base):
    __tablename__ = 'bird'
    id = Column(Integer, primary_key=True)
    species_lt = Column(String)
    species_en = Column(String)
    species_latin = Column(String)
    status_id = Column(Integer, ForeignKey('status.id'))
    status = relationship('Status', back_populates='bird')
    bird_observation = relationship('BirdObservation', back_populates='bird')

    def __init__(self, species_lt, species_en, species_latin):
        self.species_lt = species_lt
        self.species_en = species_en
        self.species_latin = species_latin

class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    status_name_lt = Column(String)
    status_name_en = Column(String)
    bird = relationship('Bird', back_populates='status')

    def __init__(self, status_name_lt, status_name_en):
        self.status_name_lt = status_name_lt
        self.status_name_en = status_name_en

class Observer(Base):
    __tablename__ = 'observer'
    id = Column(Integer, primary_key=True)
    f_name = Column(String)
    l_name = Column(String)
    birth_date = Column(String)
    gender = Column(String)
    email = Column(String)
    bird_observation = relationship('BirdObservation', back_populates='observer')

    def __init__(self,f_name, l_name, birth_date, gender, email):
        self.f_name = f_name
        self.l_name = l_name
        self.birth_date = birth_date
        self.gender = gender
        self.email = email

class BirdObservation(Base):
    __tablename__ = 'bird_observation'
    id = Column(Integer, primary_key=True)
    observer_id = Column(Integer, ForeignKey('observer.id'))
    observer = relationship('Observer', back_populates='bird_observation')
    bird_id = Column(Integer, ForeignKey('bird.id'))
    bird = relationship('Bird', back_populates='bird_observation')
    number = Column(Integer)
    place_id = Column(Integer, ForeignKey('place.id'))
    place = relationship('Place', back_populates='bird_observation')
    date = Column(String)

    def __init__(self, observer_id, bird_id, number, place_id, date):
        self.observer_id = observer_id
        self.bird_id = bird_id
        self.number = number
        self.place_id = place_id
        self.date = date

class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    place = Column(String)
    bird_observation = relationship('BirdObservation', back_populates='place')

if __name__ == '__main__':
    Base.metadata.create_all(engine)