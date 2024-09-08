from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models.flow import Flow, FlowRuns, TaskRuns, Base

import json

from coolname import generate_slug
class Repository:
    def __init__(self, config_file = 'database\config.config.json'):
        # Load the JSON config file
        with open('database/config.json', 'r') as file:
            config = json.load(file)
        
        self.DATABASE_URL = config['engine']

        # Create an engine
        self.engine = create_engine(self.DATABASE_URL, echo=True)

        # Create the table in the database
        Base.metadata.create_all(self.engine)

        # Create a session
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def __del__(self):
        self.close_session()
    
    def create_flow(self, name, entry_point):
        # Check if a flow with the same name already exists
        existing_flow = self.session.query(Flow).filter_by(name = name).first()
        
        if not existing_flow:
            new_flow = Flow(name=name, entry_point=entry_point)
            self.session.add(new_flow)
            self.session.commit()
            return new_flow
        return existing_flow

    def create_flow_run(self, flow_id):
        flow_run = FlowRuns(name=generate_slug(2), flow_id=flow_id)
        self.session.add(flow_run)
        self.session.commit()
        return self.session.query(FlowRuns).get(flow_run.id)

    def get_all_flows(self):
        return self.session.query(Flow).all()

    def create_task_run(self, flow_run_id):
        task_run = TaskRuns(name = generate_slug(2), flow_run_id = flow_run_id)
        self.session.add(task_run)
        self.session.commit()
        return task_run

    def close_session(self):
        self.session.close()
