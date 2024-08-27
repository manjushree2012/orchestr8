from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from models.flow import Flow
from models.flow_runs import FlowRuns

# Load the JSON config file
with open('database/config.json', 'r') as file:
    config = json.load(file)

# Define the database URL
DATABASE_URL = config['engine']

# Create an engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a declarative base class
Base = declarative_base()

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert a sample flow record
new_flow = Flow(name='Sample Flow', entry_point='main.py')
session.add(new_flow)
session.commit()

# Query the database
for instance in session.query(Flow).order_by(Flow.id):
    print(f"ID: {instance.id}, Name: {instance.name}, Entry Point: {instance.entry_point}, Created At: {instance.created_at}, Updated At: {instance.updated_at}")

# Close the session
session.close()
