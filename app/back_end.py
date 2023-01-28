from create_db import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data/birds_observation.db')
session = sessionmaker(bind=engine)()

def add_new_row(observer_id, bird_id, number, place_id, date):
    new_observation = BirdObservation(observer_id, bird_id, number, place_id, date)
    session.add(new_observation)
    session.commit()

def delete_observation(id):
    observation = session.query(BirdObservation).get(id)
    session.delete(observation)
    session.commit()