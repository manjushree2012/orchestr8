from sqlalchemy import Column, Integer, String, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Create a declarative base class
Base = declarative_base()

class FlowRuns(Base):
    __tablename__ = 'flow_runs'
    
    id = Column(Integer, Sequence('flow_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    flow_id = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False, default="QUEUED")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)