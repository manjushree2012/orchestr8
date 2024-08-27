from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models.flow import Flow

import json

class Repository:
    def __init__(self, config_file = 'database\config.config.json'):
        # Load the JSON config file
        with open('database/config.json', 'r') as file:
            config = json.load(file)
        
        self.DATABASE_URL = config['engine']

        # Create an engine
        self.engine = create_engine(self.DATABASE_URL, echo=True)

        # Create a declarative base class
        self.Base = declarative_base()

        # Create the table in the database
        self.Base.metadata.create_all(self.engine)

        # Create a session
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def create_flow(self, name, entry_point):
        new_flow = Flow(name=name, entry_point=entry_point)
        self.session.add(new_flow)
        self.session.commit()
        return new_flow

    def close_session(self):
        self.session.close()
